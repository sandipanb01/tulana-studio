"""Layout annotation and cross-language layout comparison.

This module is **additive**. It creates its own tables with
`CREATE TABLE IF NOT EXISTS`, never alters or deletes anything that already
exists, and never writes to `documents`, `projects`, `clips`, `pairs`,
`labels`, `pair_labels`, `exports` or `audit`. An existing database gains new
tables and loses nothing; if every table here were dropped, the studio would
work exactly as it did before.

What it records, and why each piece matters:

**Exact bounding boxes.** Stored in PDF points with a top-left origin — the
page's own units — so a region is independent of any rendering resolution.
Rasterise at any DPI and multiply by `dpi / 72`.

**Font and size.** Taken from the PDF's own text layer per span: family, size,
weight and style. Two editions of the same textbook can carry identical words
in a completely different typographic treatment, and that difference is
invisible in plain text.

**Spacing.** Line height, first-line indent and the gap to the previous block,
in points. This is what makes a "paragraph" look like a paragraph.

**Layout similarity across languages.** The point of the whole exercise: does
the Marathi edition of a page preserve the structure of the English one? Four
separate measures, kept separate because they disagree in informative ways —
a page can preserve reading order perfectly while the geometry drifts badly.
"""
from __future__ import annotations

import json
import math
import re
import time
from pathlib import Path

import config
from pdflib import fitz

# ── schema ─────────────────────────────────────────────────────────────────
# Every statement is CREATE ... IF NOT EXISTS. Nothing here alters or removes
# an existing table, so it is safe against a database holding real annotation.
SCHEMA = """
CREATE TABLE IF NOT EXISTS layout_region_types (
  id INTEGER PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  color TEXT DEFAULT '#1f4e79',
  shortcut TEXT DEFAULT '',
  ord INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS layout_pages (
  id INTEGER PRIMARY KEY,
  doc_id INTEGER NOT NULL,
  page INTEGER NOT NULL,
  width REAL, height REAL,
  status TEXT DEFAULT 'in_progress',
  annotator TEXT DEFAULT '',
  note TEXT DEFAULT '',
  created_at REAL, updated_at REAL,
  UNIQUE(doc_id, page)
);
CREATE INDEX IF NOT EXISTS ix_layout_page_doc ON layout_pages(doc_id, page);

CREATE TABLE IF NOT EXISTS layout_regions (
  id INTEGER PRIMARY KEY,
  layout_page_id INTEGER NOT NULL,
  type_code TEXT NOT NULL,
  seq INTEGER DEFAULT 0,
  x0 REAL, y0 REAL, x1 REAL, y1 REAL,
  text TEXT DEFAULT '',
  typography TEXT DEFAULT '{}',
  spacing TEXT DEFAULT '{}',
  note TEXT DEFAULT '',
  annotator TEXT DEFAULT '',
  created_at REAL
);
CREATE INDEX IF NOT EXISTS ix_layout_region_page ON layout_regions(layout_page_id, seq);

-- one row per (source page, target page) comparison, so a score can be
-- recomputed and compared over time rather than being a transient number
CREATE TABLE IF NOT EXISTS layout_comparisons (
  id INTEGER PRIMARY KEY,
  src_page_id INTEGER NOT NULL,
  tgt_page_id INTEGER NOT NULL,
  metrics TEXT DEFAULT '{}',
  metrics_version TEXT DEFAULT '1.0.0',
  created_by TEXT DEFAULT '',
  created_at REAL,
  UNIQUE(src_page_id, tgt_page_id)
);
"""

METRICS_VERSION = "1.0.0"

# DocLayNet / PubLayNet vocabulary, so a corpus annotated here can be trained
# on or merged with the public layout datasets instead of being private.
DEFAULT_TYPES = [
    ("title", "Title", "#1f4e79", "1"),
    ("chapter-title", "Chapter title", "#c2571f", "2"),
    ("section-title", "Section title", "#c98a1b", "3"),
    ("paragraph", "Paragraph", "#c2404a", "4"),
    ("list", "List", "#6a8f2f", "5"),
    ("table", "Table", "#a8552f", "6"),
    ("figure", "Figure", "#7a4fc0", "7"),
    ("caption", "Caption", "#8a7bb8", "8"),
    ("equation", "Equation", "#2e7bb8", "9"),
    ("footnote", "Footnote", "#7d879c", ""),
    ("header", "Page header", "#9aa5b8", ""),
    ("footer", "Page footer", "#9aa5b8", ""),
    ("page-number", "Page number", "#b0b8c6", ""),
    ("sidebar", "Sidebar / callout", "#c2503f", ""),
    ("other", "Other", "#68738c", ""),
]


def ensure_schema(con):
    """Create the layout tables if they are absent. Never touches anything else."""
    con.executescript(SCHEMA)
    if not con.execute("SELECT COUNT(*) FROM layout_region_types").fetchone()[0]:
        for i, (code, name, color, key) in enumerate(DEFAULT_TYPES):
            con.execute("""INSERT OR IGNORE INTO layout_region_types
                           (code, name, color, shortcut, ord) VALUES(?,?,?,?,?)""",
                        (code, name, color, key, i))
    con.commit()


def region_types(con) -> list:
    ensure_schema(con)
    return [dict(r) for r in con.execute(
        """SELECT t.*, (SELECT COUNT(*) FROM layout_regions r
                        WHERE r.type_code = t.code) AS uses
           FROM layout_region_types t ORDER BY ord, id""")]


# ── typography and spacing, read from the PDF's own text layer ─────────────
def describe_region(page, rect) -> dict:
    """Font, size, weight and spacing for everything inside a rectangle.

    Read from the PDF rather than guessed from the image. Where the page is a
    scan or uses an unmapped font encoding there is no text layer, and the
    result says so instead of inventing values — an empty `fonts` list means
    "not recoverable here", not "no formatting".
    """
    out = {"fonts": [], "sizes": [], "dominant_font": None, "dominant_size": None,
           "bold": False, "italic": False, "n_spans": 0, "n_lines": 0,
           "text_layer": True}
    try:
        raw = page.get_text("dict", clip=rect)
    except Exception:
        out["text_layer"] = False
        return out

    sizes, fonts, lines = [], {}, []
    for block in raw.get("blocks", []):
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            lines.append(line)
            for sp in spans:
                out["n_spans"] += 1
                size = round(float(sp.get("size", 0)), 2)
                name = str(sp.get("font", ""))
                if size:
                    sizes.append(size)
                if name:
                    fonts[name] = fonts.get(name, 0) + len(sp.get("text", "")) or 1
                low = name.lower()
                flags = int(sp.get("flags", 0))
                # PyMuPDF span flags: bit 4 = bold, bit 1 = italic. The name is
                # checked too because many Indic fonts do not set the flags.
                if flags & 2 ** 4 or "bold" in low or "-bd" in low:
                    out["bold"] = True
                if flags & 2 ** 1 or "italic" in low or "oblique" in low:
                    out["italic"] = True

    out["n_lines"] = len(lines)
    out["sizes"] = sorted({s for s in sizes})
    out["fonts"] = sorted(fonts, key=fonts.get, reverse=True)
    if fonts:
        out["dominant_font"] = out["fonts"][0]
    if sizes:
        out["dominant_size"] = round(sum(sizes) / len(sizes), 2)
    if out["n_spans"] == 0:
        out["text_layer"] = False
    return out


def measure_spacing(page, rect, previous_rect=None) -> dict:
    """Line height, indent and the gap above, in PDF points."""
    out = {"line_height": None, "first_line_indent": None, "gap_above": None,
           "left_margin": None, "right_margin": None, "line_gaps": []}
    try:
        raw = page.get_text("dict", clip=rect)
    except Exception:
        return out
    tops, lefts = [], []
    for block in raw.get("blocks", []):
        for line in block.get("lines", []):
            if not line.get("spans"):
                continue
            bx = line.get("bbox") or [0, 0, 0, 0]
            tops.append(round(bx[1], 2))
            lefts.append(round(bx[0], 2))
    tops.sort()
    gaps = [round(tops[i + 1] - tops[i], 2) for i in range(len(tops) - 1)]
    out["line_gaps"] = gaps
    if gaps:
        out["line_height"] = round(sum(gaps) / len(gaps), 2)
    if len(lefts) >= 2:
        body = min(lefts[1:])
        out["first_line_indent"] = round(lefts[0] - body, 2)
        out["left_margin"] = round(body - rect.x0, 2)
    elif lefts:
        out["left_margin"] = round(lefts[0] - rect.x0, 2)
    out["right_margin"] = round(page.rect.x1 - rect.x1, 2)
    if previous_rect is not None:
        out["gap_above"] = round(rect.y0 - previous_rect.y1, 2)
    return out


# ── layout comparison across languages ─────────────────────────────────────
def _norm(r, w, h):
    """A box as fractions of the page, so two differently sized pages compare."""
    return (r["x0"] / w, r["y0"] / h, r["x1"] / w, r["y1"] / h)


def _iou(a, b) -> float:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    ix0, iy0 = max(ax0, bx0), max(ay0, by0)
    ix1, iy1 = min(ax1, bx1), min(ay1, by1)
    if ix1 <= ix0 or iy1 <= iy0:
        return 0.0
    inter = (ix1 - ix0) * (iy1 - iy0)
    ua = (ax1 - ax0) * (ay1 - ay0) + (bx1 - bx0) * (by1 - by0) - inter
    return inter / ua if ua > 0 else 0.0


def _sequence_similarity(a: list, b: list) -> float:
    """Normalised edit distance over two lists of region types."""
    n, m = len(a), len(b)
    if n == 0 and m == 0:
        return 1.0
    if n == 0 or m == 0:
        return 0.0
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cur[j] = prev[j - 1] if a[i - 1] == b[j - 1] else \
                1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur
    return max(0.0, 1.0 - prev[m] / max(n, m))


def compare_layouts(src: dict, tgt: dict, src_page=None, tgt_page=None) -> dict:
    """How far does the target page preserve the source page's layout?

    Four measures, deliberately separate because they disagree in ways that
    matter. A translated page can keep the reading order perfectly while the
    geometry drifts badly — longer words push a table onto the next page — and
    a single blended score would hide exactly that.

    Every figure is reported with the counts it came from. A similarity over
    two regions means much less than the same number over twenty.
    """
    sw, sh = src["width"] or 1, src["height"] or 1
    tw, th = tgt["width"] or 1, tgt["height"] or 1
    sr = sorted(src["regions"], key=lambda r: r.get("seq", 0))
    tr = sorted(tgt["regions"], key=lambda r: r.get("seq", 0))

    src_types = [r["type_code"] for r in sr]
    tgt_types = [r["type_code"] for r in tr]

    # 1 — structural preservation: same kinds of blocks, in the same order
    structural = _sequence_similarity(src_types, tgt_types)

    # 2 — 2D layout similarity: greedy IoU match on page-normalised boxes,
    #     restricted to regions of the same type so a paragraph is never
    #     matched to a figure merely because they overlap
    pairs, used = [], set()
    for i, a in enumerate(sr):
        na = _norm(a, sw, sh)
        best, best_j = 0.0, None
        for j, b in enumerate(tr):
            if j in used or b["type_code"] != a["type_code"]:
                continue
            score = _iou(na, _norm(b, tw, th))
            if score > best:
                best, best_j = score, j
        if best_j is not None and best > 0:
            used.add(best_j)
            pairs.append({"src_seq": a.get("seq"), "tgt_seq": tr[best_j].get("seq"),
                          "type": a["type_code"], "iou": round(best, 4)})
    denom = max(len(sr), len(tr))
    layout_2d = round(sum(p["iou"] for p in pairs) / denom, 4) if denom else 0.0

    # 3 — bounding-box preservation over the matched pairs only: of the blocks
    #     that clearly correspond, how closely do they sit?
    bbox_pres = round(sum(p["iou"] for p in pairs) / len(pairs), 4) if pairs else None

    # 4 — typography preservation: do corresponding blocks use a comparable
    #     size hierarchy? Font *names* differ by necessity across scripts, so
    #     comparing them directly would always score zero and say nothing.
    #     Relative size within the page is the comparable quantity.
    def size_profile(regions):
        sizes = [(r.get("typography") or {}).get("dominant_size") for r in regions]
        sizes = [s for s in sizes if s]
        if not sizes:
            return None
        top = max(sizes)
        return [round(s / top, 3) for s in sizes]

    sp, tp = size_profile(sr), size_profile(tr)
    if sp and tp:
        k = min(len(sp), len(tp))
        typo = round(1.0 - sum(abs(sp[i] - tp[i]) for i in range(k)) / k, 4)
        typo = max(0.0, typo)
    else:
        typo = None

    # 5 — spacing preservation: line height relative to the page
    def spacing_profile(regions, h):
        vals = [(r.get("spacing") or {}).get("line_height") for r in regions]
        vals = [v / h for v in vals if v]
        return round(sum(vals) / len(vals), 5) if vals else None

    ss, ts = spacing_profile(sr, sh), spacing_profile(tr, th)
    spacing = None
    if ss and ts:
        spacing = round(1.0 - min(1.0, abs(ss - ts) / max(ss, ts)), 4)

    # 6 — visual similarity of the rendered pages, when both are available.
    #     A coarse ink-density grid: it answers "is the page shaped the same",
    #     which is what a reader notices, and it is stable across DPI.
    visual = None
    if src_page is not None and tgt_page is not None:
        try:
            visual = _visual_similarity(src_page, tgt_page)
        except Exception:
            visual = None

    return {
        "metrics_version": METRICS_VERSION,
        "structural_preservation": round(structural, 4),
        "layout_2d_similarity": layout_2d,
        "bbox_preservation": bbox_pres,
        "typography_preservation": typo,
        "spacing_preservation": spacing,
        "visual_similarity": visual,
        "n_src_regions": len(sr), "n_tgt_regions": len(tr),
        "n_matched": len(pairs),
        "src_types": src_types, "tgt_types": tgt_types,
        "matches": pairs,
        "notes": _comparison_notes(sr, tr, structural, layout_2d),
    }


def _visual_similarity(src_page, tgt_page, grid: int = 16) -> float:
    """Compare two rendered pages as a coarse ink-density grid.

    Deliberately coarse. Comparing pixels would report that Devanagari and
    Latin look nothing alike, which is true and useless. What is being asked is
    whether the *page* is shaped the same — where the dense areas fall.
    """
    def density(page):
        pix = page.get_pixmap(dpi=36, colorspace=fitz.csGRAY)
        w, h, samples = pix.width, pix.height, pix.samples
        cells = []
        for gy in range(grid):
            for gx in range(grid):
                x0, x1 = gx * w // grid, max(gx * w // grid + 1, (gx + 1) * w // grid)
                y0, y1 = gy * h // grid, max(gy * h // grid + 1, (gy + 1) * h // grid)
                total = n = 0
                for y in range(y0, y1):
                    row = y * w
                    for x in range(x0, x1):
                        total += 255 - samples[row + x]
                        n += 1
                cells.append(total / n / 255 if n else 0.0)
        return cells

    a, b = density(src_page), density(tgt_page)
    # cosine similarity: insensitive to one page simply being darker
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return round(dot / (na * nb), 4) if na and nb else None


def _comparison_notes(sr, tr, structural, layout_2d) -> list:
    """Say what a number means when it is easy to misread."""
    notes = []
    if len(sr) < 3 or len(tr) < 3:
        notes.append("Few regions annotated; these figures are unstable and should "
                     "not be quoted.")
    if len(sr) != len(tr):
        notes.append(f"The pages have different block counts ({len(sr)} and "
                     f"{len(tr)}) — often a real difference, since translated text "
                     f"reflows, not necessarily an annotation error.")
    if structural > 0.85 and layout_2d < 0.5:
        notes.append("Reading order is preserved but the geometry is not: the same "
                     "blocks in the same order, sitting in different places.")
    if not any((r.get("typography") or {}).get("text_layer") for r in sr + tr):
        notes.append("Neither page has a usable text layer, so typography and "
                     "spacing could not be measured.")
    return notes


# ── persistence ────────────────────────────────────────────────────────────
def get_page(con, doc_id: int, page: int, doc_path: Path) -> dict:
    ensure_schema(con)
    with fitz.open(doc_path) as doc:
        if page < 1 or page > doc.page_count:
            raise ValueError(f"Page out of range (1..{doc.page_count})")
        rect = doc[page - 1].rect
        pages = doc.page_count
    lp = con.execute("SELECT * FROM layout_pages WHERE doc_id=? AND page=?",
                     (doc_id, page)).fetchone()
    regions = []
    if lp:
        for r in con.execute("""SELECT * FROM layout_regions WHERE layout_page_id=?
                                ORDER BY seq, id""", (lp["id"],)):
            d = dict(r)
            d["typography"] = json.loads(d["typography"] or "{}")
            d["spacing"] = json.loads(d["spacing"] or "{}")
            regions.append(d)
    return {"doc_id": doc_id, "page": page, "pages": pages,
            "width": round(rect.width, 2), "height": round(rect.height, 2),
            "layout_page": dict(lp) if lp else None, "regions": regions}


def save_page(con, doc_id: int, page: int, doc_path: Path, regions: list,
              status: str = "in_progress", annotator: str = "",
              note: str = "") -> dict:
    """Replace the regions on one page, capturing typography and spacing.

    Whole-page replace: an annotator works on a page as a unit, and reading
    order is a property of the set rather than of any single box.
    """
    ensure_schema(con)
    known = {r["code"] for r in con.execute("SELECT code FROM layout_region_types")}
    unknown = sorted({r.get("type_code") for r in regions} - known)
    if unknown:
        raise ValueError(f"Unknown region type(s): {', '.join(unknown)}")

    with fitz.open(doc_path) as doc:
        if page < 1 or page > doc.page_count:
            raise ValueError(f"Page out of range (1..{doc.page_count})")
        pg = doc[page - 1]
        rect = pg.rect
        lp = con.execute("SELECT id FROM layout_pages WHERE doc_id=? AND page=?",
                         (doc_id, page)).fetchone()
        if lp:
            lp_id = lp["id"]
            con.execute("""UPDATE layout_pages SET width=?, height=?, status=?,
                           annotator=?, note=?, updated_at=? WHERE id=?""",
                        (rect.width, rect.height, status, annotator, note,
                         time.time(), lp_id))
        else:
            lp_id = con.execute("""INSERT INTO layout_pages(doc_id, page, width,
                                   height, status, annotator, note, created_at,
                                   updated_at) VALUES(?,?,?,?,?,?,?,?,?)""",
                                (doc_id, page, rect.width, rect.height, status,
                                 annotator, note, time.time(), time.time())).lastrowid
        con.execute("DELETE FROM layout_regions WHERE layout_page_id=?", (lp_id,))

        saved, prev = 0, None
        for i, r in enumerate(regions):
            x0, x1 = sorted((float(r["x0"]), float(r["x1"])))
            y0, y1 = sorted((float(r["y0"]), float(r["y1"])))
            x0 = max(0.0, min(rect.width, x0)); x1 = max(0.0, min(rect.width, x1))
            y0 = max(0.0, min(rect.height, y0)); y1 = max(0.0, min(rect.height, y1))
            if x1 - x0 < 2 or y1 - y0 < 2:
                continue
            box = fitz.Rect(x0, y0, x1, y1)
            try:
                text = (pg.get_textbox(box) or "").strip()
            except Exception:
                text = ""
            typo = describe_region(pg, box)
            space = measure_spacing(pg, box, prev)
            con.execute("""INSERT INTO layout_regions(layout_page_id, type_code, seq,
                           x0, y0, x1, y1, text, typography, spacing, note,
                           annotator, created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (lp_id, r["type_code"], r.get("seq", i), x0, y0, x1, y1,
                         text, json.dumps(typo, ensure_ascii=False),
                         json.dumps(space, ensure_ascii=False),
                         r.get("note", ""), annotator, time.time()))
            prev = box
            saved += 1
    return {"layout_page_id": lp_id, "page": page, "regions": saved,
            "status": status}


def compare_pages(con, src_doc: int, src_page: int, src_path: Path,
                  tgt_doc: int, tgt_page: int, tgt_path: Path,
                  actor: str = "") -> dict:
    """Compare two annotated pages and store the result."""
    ensure_schema(con)
    s = get_page(con, src_doc, src_page, src_path)
    t = get_page(con, tgt_doc, tgt_page, tgt_path)
    if not s["regions"] or not t["regions"]:
        raise ValueError("Both pages need layout regions before they can be "
                         "compared — annotate each side first")
    with fitz.open(src_path) as sd, fitz.open(tgt_path) as td:
        metrics = compare_layouts(s, t, sd[src_page - 1], td[tgt_page - 1])
    sp = con.execute("SELECT id FROM layout_pages WHERE doc_id=? AND page=?",
                     (src_doc, src_page)).fetchone()
    tp = con.execute("SELECT id FROM layout_pages WHERE doc_id=? AND page=?",
                     (tgt_doc, tgt_page)).fetchone()
    if sp and tp:
        con.execute("""INSERT INTO layout_comparisons(src_page_id, tgt_page_id,
                       metrics, metrics_version, created_by, created_at)
                       VALUES(?,?,?,?,?,?)
                       ON CONFLICT(src_page_id, tgt_page_id) DO UPDATE SET
                         metrics=excluded.metrics,
                         metrics_version=excluded.metrics_version,
                         created_by=excluded.created_by,
                         created_at=excluded.created_at""",
                    (sp["id"], tp["id"], json.dumps(metrics, ensure_ascii=False),
                     METRICS_VERSION, actor, time.time()))
    return metrics


def progress(con, doc_id: int = None) -> dict:
    ensure_schema(con)
    where, args = ("WHERE lp.doc_id=?", (doc_id,)) if doc_id else ("", ())
    pages = con.execute(
        f"SELECT COUNT(*) n, SUM(status='done') done FROM layout_pages lp {where}",
        args).fetchone()
    by_type = [dict(r) for r in con.execute("""
        SELECT t.code, t.name, t.color, COUNT(r.id) n
        FROM layout_region_types t
        LEFT JOIN layout_regions r ON r.type_code = t.code
        GROUP BY t.id ORDER BY t.ord""")]
    docs = [dict(r) for r in con.execute("""
        SELECT d.id, d.title, d.language, d.pages,
               COUNT(lp.id) annotated, SUM(lp.status='done') done,
               (SELECT COUNT(*) FROM layout_regions lr
                JOIN layout_pages lp2 ON lp2.id = lr.layout_page_id
                WHERE lp2.doc_id = d.id) regions
        FROM documents d JOIN layout_pages lp ON lp.doc_id = d.id
        GROUP BY d.id ORDER BY annotated DESC""")]
    comps = con.execute("SELECT COUNT(*) FROM layout_comparisons").fetchone()[0]
    return {"pages_annotated": pages["n"] or 0, "pages_done": pages["done"] or 0,
            "comparisons": comps, "by_type": by_type, "by_document": docs}
