#!/usr/bin/env python3
"""Do the boxes land on the printed text? Every aligned page against its PDF.

    python3 check_mapping.py                       every pair, every 4th page
    python3 check_mapping.py --every 1             every page (about ten minutes)
    python3 check_mapping.py --pair MH10_1_en-mr   one pair (repeat for more)
    python3 check_mapping.py --report mapping.md   also write the report to a file
    python3 check_mapping.py --pdfs /path/to/board_pdfs

Setu draws the parser's boxes over a page it renders from the PDF, and cuts
"as printed" pictures of a passage out of it. Both are right only if four
things hold, and each is measured here against the PDF itself — never against
the data being checked:

1. **The right file.** Each book finds its own PDF. NCERT's English and Hindi
   chapters share file names (eng/10/1001.pdf, hin/10/1001.pdf); a lookup by
   name alone would put the Hindi boxes on the English page.
2. **The right page, the right part of it.** The page exists, and the part of
   it Setu draws — CropBox, MediaBox, or the scan where it sits on the page,
   rotation applied (sources.page_area) — has the shape of the image the
   parser measured on.
3. **The printed words.** Where the PDF has a text layer, the share of its
   words whose centre falls inside one of the parser's text boxes. Legacy-font
   Indic text layers are unreadable, but their words still have positions, so
   this works in every script.
4. **The ink.** The page is rendered and binarised. For every text box, how
   much printed ink it holds; and, the decisive test, which shift and scale of
   all the boxes together (within ±4% of the page) puts the most ink inside
   them. On a correctly mapped page that is no shift at all.

A page passes when its shape fits, its boxes hold ink (or words) and no shift
does clearly better. The exit code is the number of books with a page that
does not pass, so this can gate a deployment.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402

import config  # noqa: E402
from annotation.core import aligned, sources  # noqa: E402

#: How far the boxes are tried away from where the data puts them, as a
#: fraction of the page, and how many steps across that.
SHIFT = 0.04
STEPS = 17
SCALES = (0.97, 0.985, 1.0, 1.015, 1.03)
#: Rendering resolution for the ink test: enough to see a line of text.
INK_DPI = 50
#: A box "holds ink" when at least this share of it is dark.
INK_MIN = 0.02
#: A candidate a step or two away "does clearly better" when it holds this
#: much more ink above chance than the boxes where they are; one 1% or more
#: away, this much. Correctly mapped synthetic pages stay under 0.2%.
GAIN_NEAR = 0.10
GAIN_FAR = 0.012


# ── pieces that need no PDF ────────────────────────────────────────────────

def text_boxes(page: dict) -> list[list[float]]:
    """The parser's boxes on a page that hold text, as fractions of the page.

    The OCR blocks merged into a passage (``members``) are used where the file
    has them: they are the boxes the parser measured, and finer than their
    union."""
    w, h = float(page.get("width") or 0), float(page.get("height") or 0)
    out = []
    if w <= 1 or h <= 1:
        return out
    for b in page.get("blocks") or []:
        if not str(b.get("text") or "").strip():
            continue
        boxes = [m.get("bbox_xyxy") for m in (b.get("members") or [])] or [b.get("bbox_xyxy")]
        for box in boxes:
            try:
                x0, y0, x1, y1 = (float(v) for v in box)
            except (TypeError, ValueError):
                continue
            if x1 > x0 and y1 > y0:
                out.append([x0 / w, y0 / h, x1 / w, y1 / h])
    return out


def otsu(gray: np.ndarray) -> int:
    """The threshold that best splits a page into paper and ink."""
    hist = np.bincount(gray.ravel(), minlength=256).astype(float)
    total = hist.sum()
    if total == 0:
        return 128
    cum = np.cumsum(hist)
    mean = np.cumsum(hist * np.arange(256))
    best, thr = -1.0, 128
    for t in range(1, 255):
        w0, w1 = cum[t], total - cum[t]
        if w0 == 0 or w1 == 0:
            continue
        m0, m1 = mean[t] / w0, (mean[-1] - mean[t]) / w1
        between = w0 * w1 * (m0 - m1) ** 2
        if between > best:
            best, thr = between, t
    return thr


def ink_scores(ink: np.ndarray, boxes: list[list[float]]) -> dict:
    """How much ink the boxes hold where they are, and which shift/scale of all
    of them together holds the most.

    ``ink`` is a boolean page image; ``boxes`` are fractions of it. The search
    scores each candidate by the ink inside the boxes *above what the page's
    average ink would put there by chance* (a matched filter): growing the
    boxes over white paper scores less, not more, so neither bigger nor
    smaller boxes are favoured, and the best candidate is where the boxes and
    the print coincide. On a correctly mapped page that is no shift at all."""
    H, W = ink.shape
    integral = np.zeros((H + 1, W + 1), dtype=np.int64)
    integral[1:, 1:] = np.cumsum(np.cumsum(ink, axis=0), axis=1)
    mean = float(ink.mean())
    b = np.asarray(boxes, dtype=float)
    cx = (b[:, 0] + b[:, 2]) / 2
    cy = (b[:, 1] + b[:, 3]) / 2
    hw = (b[:, 2] - b[:, 0]) / 2
    hh = (b[:, 3] - b[:, 1]) / 2
    half = STEPS // 2
    shifts = np.arange(-half, half + 1) * (SHIFT / half)     # 0 is exactly 0
    S, DX, DY = np.meshgrid(np.asarray(SCALES), shifts, shifts, indexing="ij")
    S, DX, DY = S.ravel()[:, None], DX.ravel()[:, None], DY.ravel()[:, None]
    # Scaled about the page centre, then shifted: the two ways a render can be off.
    X0 = (0.5 + (cx - hw - 0.5) * S + DX) * W
    X1 = (0.5 + (cx + hw - 0.5) * S + DX) * W
    Y0 = (0.5 + (cy - hh - 0.5) * S + DY) * H
    Y1 = (0.5 + (cy + hh - 0.5) * S + DY) * H
    x0 = np.clip(np.floor(X0), 0, W).astype(int)
    x1 = np.clip(np.ceil(X1), 0, W).astype(int)
    y0 = np.clip(np.floor(Y0), 0, H).astype(int)
    y1 = np.clip(np.ceil(Y1), 0, H).astype(int)
    inside = (integral[y1, x1] - integral[y0, x1] - integral[y1, x0] + integral[y0, x0])
    area = np.maximum((x1 - x0) * (y1 - y0), 0)
    score = (inside - mean * area).sum(axis=1)                # per candidate
    here = int(np.argmin(np.abs(S.ravel() - 1.0) + np.abs(DX.ravel()) + np.abs(DY.ravel())))
    best = int(np.argmax(score))
    if score[best] - score[here] <= 1e-9 * max(abs(score[best]), 1.0):
        best = here                              # a tie is no evidence of a shift
    per_box = inside[here] / np.maximum(area[here], 1)
    return {"held": float(np.mean(per_box >= INK_MIN)) if len(per_box) else 0.0,
            "density": float(inside[here].sum() / max(area[here].sum(), 1)),
            "page_ink": round(mean, 4),
            "score": float(score[here]), "best_score": float(score[best]),
            "best": {"scale": float(S.ravel()[best]), "dx": round(float(DX.ravel()[best]), 4),
                     "dy": round(float(DY.ravel()[best]), 4)}}


def word_coverage(words: list[list[float]], boxes: list[list[float]], pad: float = 0.004) -> float | None:
    """Share of the PDF's words (fractions of the page) whose centre is in a box."""
    if len(words) < 5 or not boxes:
        return None
    b = np.asarray(boxes, dtype=float)
    w = np.asarray(words, dtype=float)
    cx, cy = ((w[:, 0] + w[:, 2]) / 2)[:, None], ((w[:, 1] + w[:, 3]) / 2)[:, None]
    hit = ((cx >= b[:, 0] - pad) & (cx <= b[:, 2] + pad) &
           (cy >= b[:, 1] - pad) & (cy <= b[:, 3] + pad)).any(axis=1)
    return float(hit.mean())


def verdict(fit_error: float | None, ink: dict | None, coverage: float | None) -> str:
    """ok | shape | offset | blank, for one page.

    "offset" when the boxes, where they are, hold no more ink than blank paper
    would; or when another candidate holds clearly more — 10% more from a step
    away, 1.2% more from 1% of the page (or 1.5% of scale) away or further."""
    if fit_error is not None and fit_error > sources.FIT_TOLERANCE:
        return "shape"
    if ink is None:
        return "blank"
    if ink["score"] <= 0 and (coverage is None or coverage < 0.5):
        return "offset"
    best = ink["best"]
    moved = best != {"scale": 1.0, "dx": 0.0, "dy": 0.0}
    far = abs(best["dx"]) >= 0.01 or abs(best["dy"]) >= 0.01 or abs(best["scale"] - 1) >= 0.015
    gain = (ink["best_score"] - ink["score"]) / max(abs(ink["best_score"]), 1e-9)
    if moved and (gain >= GAIN_NEAR or (far and gain >= GAIN_FAR)):
        return "offset"
    return "ok"


# ── one page of one PDF ────────────────────────────────────────────────────

def check_page(doc, page: dict) -> dict:
    """Measure one parser page against its PDF page (PyMuPDF document)."""
    from pdflib import fitz
    n = int(page["page"])
    out = {"page": n}
    if n >= doc.page_count:
        out["verdict"] = "missing"
        return out
    pg = doc[n]
    raster = (float(page["width"]), float(page["height"]))
    area, err = sources.page_area(pg, raster)
    out.update(area=area.split(":")[0], fit_error=err)
    r = sources.area_rect(pg, area)
    boxes = text_boxes(page)
    out["boxes"] = len(boxes)
    if not boxes:
        out["verdict"] = "blank"
        return out
    words = []
    for x0, y0, x1, y1, *_ in pg.get_text("words"):
        q = fitz.Rect(x0, y0, x1, y1) * pg.rotation_matrix
        if q.width > 0 and q.height > 0:
            words.append([(q.x0 - r.x0) / r.width, (q.y0 - r.y0) / r.height,
                          (q.x1 - r.x0) / r.width, (q.y1 - r.y0) / r.height])
    out["words"] = len(words)
    out["coverage"] = word_coverage(words, boxes)
    pix = pg.get_pixmap(dpi=INK_DPI, colorspace=fitz.csGRAY, clip=r)
    gray = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width]
    ink = gray < min(otsu(gray), 200)
    if ink.mean() < 0.002:                       # a blank render: nothing to measure
        out["ink"] = None
    else:
        out["ink"] = ink_scores(ink, boxes)
    out["verdict"] = verdict(err, out["ink"], out["coverage"])
    return out


# ── the dataset ────────────────────────────────────────────────────────────

def same_name_files(relpath: str) -> list[str]:
    data = Path(config.DATA_DIR)
    try:
        return sorted(p.relative_to(data).as_posix() for p in data.rglob(Path(relpath).name)
                      if p.is_file())
    except OSError:
        return []


def check_side(pair_id: str, which: str, side: dict, every: int) -> dict:
    from pdflib import fitz
    rel = side["relpath"]
    res = {"pair": pair_id, "side": which, "language": side["language"], "relpath": rel,
           "pages": [], "problems": []}
    pdf = sources._find_pdf(rel)
    if pdf is None:
        res["problems"].append("no PDF found for this book")
        return res
    if sources._is_lfs_pointer(pdf):
        res["problems"].append("the PDF is a Git LFS pointer — run git lfs pull")
        return res
    data = Path(config.DATA_DIR).resolve()
    try:
        found = pdf.resolve().relative_to(data).as_posix()
    except ValueError:
        found = pdf.as_posix()
    res["pdf"] = found
    if not found.replace("\\", "/").endswith(rel):
        others = same_name_files(rel)
        res["problems"].append(f"found by name, not by path ({len(others)} file(s) of that name)")
    with fitz.open(pdf) as doc:
        res["pdf_pages"] = doc.page_count
        pages = sorted(side["pages"], key=lambda p: p["page"])
        last = max((p["page"] for p in pages), default=-1)
        if last >= doc.page_count:
            res["problems"].append(f"the data has page {last + 1}, the PDF {doc.page_count}")
        for i, p in enumerate(pages):
            if every > 1 and i % every and not any(
                    b.get("align_state") in aligned.NOT_ALIGNED for b in p.get("blocks") or []):
                continue                         # a sample — but every page with work is checked
            res["pages"].append(check_page(doc, p))
    return res


def summarise(side: dict) -> dict:
    pages = side["pages"]
    by = {}
    for p in pages:
        by[p["verdict"]] = by.get(p["verdict"], 0) + 1
    errs = [p["fit_error"] for p in pages if p.get("fit_error") is not None]
    cov = [p["coverage"] for p in pages if p.get("coverage") is not None]
    held = [p["ink"]["held"] for p in pages if p.get("ink")]
    media = sum(1 for p in pages if p.get("area") == "media")
    scans = sum(1 for p in pages if p.get("area") == "img")
    bad = by.get("shape", 0) + by.get("offset", 0) + by.get("missing", 0)
    return {"checked": len(pages), "ok": by.get("ok", 0), "blank": by.get("blank", 0),
            "shape": by.get("shape", 0), "offset": by.get("offset", 0),
            "missing": by.get("missing", 0), "media_box": media, "scan_placed": scans,
            "fit_error_median": round(statistics.median(errs), 4) if errs else None,
            "fit_error_max": round(max(errs), 4) if errs else None,
            "word_coverage_median": round(statistics.median(cov), 3) if cov else None,
            "ink_held_median": round(statistics.median(held), 3) if held else None,
            "verdict": "CHECK" if (bad or side["problems"]) else "OK"}


def report_md(results: list[dict], seconds: float) -> str:
    lines = ["# Scan mapping check", "",
             f"{len(results)} book sides, {sum(len(r['pages']) for r in results)} pages, "
             f"{seconds:.0f} s. A page is OK when the drawn part of the PDF page has the "
             "shape of the parser's image, its boxes hold printed ink (or the PDF's words), "
             "and no shift or scale of the boxes does clearly better.", "",
             "| pair | side | verdict | pages | ok | shape | offset | missing | MediaBox "
             "| scan inside page | fit error (median / max) | words in boxes | boxes with ink "
             "| notes |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        s = r["summary"]
        fe = (f"{s['fit_error_median']} / {s['fit_error_max']}"
              if s["fit_error_median"] is not None else "—")
        lines.append(
            f"| {r['pair']} | {r['side']} ({r['language']}) | **{s['verdict']}** | {s['checked']} "
            f"| {s['ok']} | {s['shape']} | {s['offset']} | {s['missing']} | {s['media_box']} "
            f"| {s['scan_placed']} "
            f"| {fe} | {s['word_coverage_median'] if s['word_coverage_median'] is not None else '—'} "
            f"| {s['ink_held_median'] if s['ink_held_median'] is not None else '—'} "
            f"| {'; '.join(r['problems'])} |")
    bad_pages = [(r["pair"], r["side"], p) for r in results for p in r["pages"]
                 if p["verdict"] in ("shape", "offset", "missing")]
    if bad_pages:
        lines += ["", "## Pages that did not pass", "",
                  "| pair | side | page | verdict | fit error | best shift (scale, dx, dy) "
                  "| words in boxes |", "|---|---|---|---|---|---|---|"]
        for pair, side, p in bad_pages[:300]:
            best = (p.get("ink") or {}).get("best") or {}
            lines.append(f"| {pair} | {side} | {p['page'] + 1} | {p['verdict']} "
                         f"| {p.get('fit_error')} | {best.get('scale')}, {best.get('dx')}, "
                         f"{best.get('dy')} | {p.get('coverage')} |")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dataset", default=None,
                    help="the aligned data folder (default: data/aligned_v2 in the repository)")
    ap.add_argument("--pdfs", default=None, help="the folder holding the PDFs (board_pdfs)")
    ap.add_argument("--pair", action="append", default=[], help="only these pairs")
    ap.add_argument("--every", type=int, default=4,
                    help="check every Nth page (pages with unaligned text always)")
    ap.add_argument("--report", default="", help="write the report to this file")
    ap.add_argument("--json", default="", help="write every measurement to this file")
    args = ap.parse_args(argv)

    try:
        import pdflib
        if not pdflib.available():
            print("PyMuPDF is not installed:  pip install PyMuPDF")
            return 1
    except Exception as exc:                     # pragma: no cover
        print(f"PyMuPDF could not be loaded: {exc}")
        return 1
    if args.pdfs:
        config.DATA_DIR = Path(args.pdfs).resolve()
    root = aligned.find_dataset(args.dataset)
    if not root:
        print("No aligned data found: expected data/aligned_v2 in the repository (or use --dataset).")
        return 1
    started = time.time()
    results = []
    for pair_dir in aligned._pair_dirs(root):
        if args.pair and pair_dir.name not in args.pair:
            continue
        try:
            pair = aligned.read_pair(pair_dir)
        except Exception as exc:
            print(f"{aligned.shown_name(pair_dir.name)}: not readable ({type(exc).__name__})")
            continue
        for which in ("src", "tgt"):
            r = check_side(pair["pair_id"], which, pair[which], max(1, args.every))
            r["summary"] = summarise(r)
            results.append(r)
            s = r["summary"]
            print(f"{s['verdict']:5} {pair['pair_id']:22} {which} {r['language']:10} "
                  f"pages {s['checked']:4}  ok {s['ok']:4}  shape {s['shape']}  "
                  f"offset {s['offset']}  missing {s['missing']}  "
                  f"words-in-boxes {s['word_coverage_median']}  ink {s['ink_held_median']}"
                  + (f"  [{'; '.join(r['problems'])}]" if r["problems"] else ""), flush=True)
    seconds = time.time() - started
    text = report_md(results, seconds)
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
        print(f"report written to {args.report}")
    if args.json:
        Path(args.json).write_text(json.dumps(results, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
    flagged = sum(1 for r in results if r["summary"]["verdict"] != "OK")
    print(f"\n{len(results) - flagged} of {len(results)} book sides OK, {flagged} to check "
          f"({seconds:.0f} s)")
    return flagged


if __name__ == "__main__":
    sys.exit(main())
