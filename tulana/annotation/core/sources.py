"""Source verification — showing an annotator the printed page behind a pair.

The annotation workspace is text. But some questions cannot be answered from
text alone: *did the parser really read a 5 there, or was it an S?*, *is that
fraction upside down?*, *does the table in the book have four columns or five?*
For those, the annotator needs to see the page.

This module is a **bridge, not a second cropping system**. Tulana already knows
how to cut a region out of a PDF — :func:`pairs._render_crop` does it, taking a
box in *fractions of the page*, which is exactly how every segment already
stores its position (``setu_segment.fx0..fy1``). So source verification is the
existing crop machinery pointed at a segment's own box, and nothing here
re-implements any of it.

Three things it adds:

* **Locating the PDF** for a book, through ``blocks._find_pdf``, which already
  understands the corpus's folder conventions.
* **A cache**, because an annotator checking the same page twice should not pay
  for it twice, and because an autosave firing mid-crop must not queue up
  renders.
* **Honest failure.** The PDFs in this corpus are Git LFS objects and are
  frequently not fetched; PyMuPDF is an optional dependency. Both cases are
  reported as a plain sentence the interface can show, rather than an exception
  that reaches an annotator as a red traceback.
"""
from __future__ import annotations

import hashlib
import logging
import math
import os
import sqlite3
import threading
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import config

from .store import NotFound, Repository

log = logging.getLogger("annotation.sources")

#: Resolution for a verification crop. Lower than the 300 dpi Tulana uses for
#: exported clippings: this one is read on screen for a few seconds, and a
#: 300 dpi cut of a full page is several megabytes through a Gradio event.
VIEW_DPI = int(getattr(config, "SOURCE_VIEW_DPI", 150) or 150)

#: How much of the surrounding page to include. A crop cut exactly to the
#: parser's box is hard to place on the page; a little context makes it obvious
#: which paragraph you are looking at.
CONTEXT = 0.02

#: A little breathing room around any cut, as a fraction of the page — the
#: same margin Tulana's own crops have always had.
CROP_PAD = 0.006

#: How far the shape of the drawn page may differ from the image the parser
#: measured its boxes on (as a relative difference of width/height) before
#: the two are said not to line up. Real pages agree to a fraction of a
#: percent; a different page, or a cropped scan, is off by several.
FIT_TOLERANCE = 0.015

_lock = threading.Lock()


@dataclass
class SourceView:
    """The result of asking to see a segment's page. Never raises at the caller."""
    ok: bool
    path: Path | None = None
    message: str = ""
    page: int = 0
    book: str = ""
    relpath: str = ""
    #: Which of the PDF page's boxes was drawn ("crop" or "media"), and how far
    #: its shape is from the image the parser measured on (None: not known).
    area: str = "crop"
    fit_error: float | None = None

    @property
    def fits(self) -> bool:
        """The boxes can be trusted to sit on the printed text."""
        return self.fit_error is None or self.fit_error <= FIT_TOLERANCE

    def as_dict(self) -> dict:
        return {"ok": self.ok, "path": str(self.path) if self.path else "",
                "message": self.message, "page": self.page, "book": self.book,
                "relpath": self.relpath, "area": self.area,
                "fit_error": self.fit_error, "fits": self.fits}


def cache_dir() -> Path:
    d = Path(config.STATE_DIR) / "source_views"
    d.mkdir(parents=True, exist_ok=True)
    return d


def available() -> tuple[bool, str]:
    """Can source verification work on this machine at all?

    Answered once, plainly, so the interface can hide or explain the feature
    instead of offering a button that always fails.
    """
    try:
        import pdflib
    except Exception as exc:                     # pragma: no cover - import shape
        return False, f"The PDF library could not be loaded ({exc})."
    if not pdflib.available():
        return False, ("PyMuPDF is not installed, so the original pages cannot "
                       "be shown. Install it with:  pip install PyMuPDF")
    return True, ""


def for_segment(con, sid: str, *, side_label: str = "", dpi: int | None = None,
                context: float | None = None) -> SourceView:
    """Render the region of the printed page that a segment came from.

    Returns a :class:`SourceView` whose ``message`` explains any failure in
    words an annotator can act on. This never raises for a missing PDF, a
    missing library or a page out of range, because all three are ordinary
    states of this corpus rather than faults.
    """
    ok, why = available()
    if not ok:
        return SourceView(False, message=why)

    repo = Repository(con)
    seg = repo.one(
        "SELECT s.sid, s.page, s.fx0, s.fy0, s.fx1, s.fy1, s.book_key,"
        "       b.relpath, b.book, b.title, b.pdf_present"
        "  FROM setu_segment s JOIN setu_book b ON b.book_key = s.book_key"
        " WHERE s.sid = ?", (sid,))
    if not seg:
        raise NotFound(f"no such segment: {sid}")

    label = seg["title"] or seg["book"]
    pdf = _find_pdf(seg["relpath"])
    if pdf is None:
        return SourceView(
            False, page=seg["page"], book=label, relpath=seg["relpath"],
            message=(f"The original PDF for “{label}” is not on this machine, so "
                     f"the page cannot be shown. The text is unaffected. "
                     f"If the PDFs are stored with Git LFS, run:  git lfs pull"))

    if _is_lfs_pointer(pdf):
        return SourceView(
            False, page=seg["page"], book=label, relpath=seg["relpath"],
            message=(f"The PDF for “{label}” has not been downloaded — the file "
                     f"here is a Git LFS pointer, not the book. The text is "
                     f"unaffected. To fetch the PDFs, run:  git lfs pull"))

    box = (_f(seg["fx0"]), _f(seg["fy0"]), _f(seg["fx1"]), _f(seg["fy1"]))
    if box[2] <= box[0] or box[3] <= box[1]:
        # A block the parser recorded with no usable box. Show the whole page
        # rather than nothing — the annotator can still find the passage.
        box = (0.0, 0.0, 1.0, 1.0)

    pad = CONTEXT if context is None else max(0.0, min(0.2, float(context)))
    box = (max(0.0, box[0] - pad), max(0.0, box[1] - pad),
           min(1.0, box[2] + pad), min(1.0, box[3] + pad))
    res = int(dpi or VIEW_DPI)
    res = max(60, min(300, res))

    area, err = fit(pdf, int(seg["page"]), raster_size(con, seg["book_key"], seg["page"]))
    out = _cached_path(seg["relpath"], seg["page"], box, res, area)
    if out.exists():
        return SourceView(True, out, page=seg["page"], book=label,
                          relpath=seg["relpath"], area=area, fit_error=err)

    try:
        png, _w, _h = _render(pdf, int(seg["page"]), box, res, area)
    except Exception as exc:
        # The reason goes to the log with its path and its library error; the
        # annotator gets a sentence. A traceback on screen tells them nothing
        # they can act on and leaks where the file lives on the server.
        log.info("source view failed for %s (%s p%s): %s", sid, pdf, seg["page"], exc)
        return SourceView(
            False, page=seg["page"], book=label, relpath=seg["relpath"],
            message=(f"Page {seg['page'] + 1} of “{label}” could not be shown. "
                     f"The text is unaffected — carry on annotating, and tell "
                     f"whoever runs the server if it keeps happening."))

    # Written to a temporary name and moved into place, so a second annotator
    # asking for the same page never reads a half-written file.
    tmp = out.with_name(out.name + f".{threading.get_ident()}.part")
    try:
        tmp.write_bytes(png)
        tmp.replace(out)
    except OSError as exc:                       # pragma: no cover - disk full
        tmp.unlink(missing_ok=True)
        log.warning("could not cache source view: %s", exc)
        return SourceView(False, page=seg["page"], book=label,
                          message=f"The page could not be saved for display ({exc}).")
    return SourceView(True, out, page=seg["page"], book=label,
                      relpath=seg["relpath"], area=area, fit_error=err)


# ── which part of the PDF page the parser saw ──────────────────────────────
#
# Every box travels as a fraction of the image the parser measured it on, and
# that image was a render of the PDF page. Which render matters. PyMuPDF and
# every PDF viewer draw the page's CropBox; pdftoppm and pdf2image, the usual
# OCR front ends, draw the MediaBox unless told otherwise. On most pages the
# two are the same rectangle. Where a publisher left printer's marks outside
# a smaller CropBox, they are not — and fractions of one drawn over the other
# put every box in the wrong place, the boxes "empty" over white margin.
#
# So the page is drawn the way the parser saw it: of the two boxes, the one
# whose shape (with the page's rotation applied) matches the parser's image.
# The PDF says nothing else about it, and the shapes differ whenever the boxes
# do, so this decides it. How well the chosen box fits is kept, so a page
# whose scan matches neither is reported rather than drawn wrongly in silence.

def raster_size(con, book_key: str, page: Any) -> tuple[float, float] | None:
    """The size, in pixels, of the image the parser measured this page on."""
    try:
        n = int(page)
    except (TypeError, ValueError):
        return None
    for sql, args in (
            ("SELECT width, height FROM setu_page_meta WHERE book_key = ? AND page = ?",
             (book_key, n)),
            ("SELECT p.width, p.height FROM setu_book b JOIN pl_pages p"
             "    ON p.book_id = b.pl_book_id AND p.page = ? WHERE b.book_key = ?",
             (n, book_key))):
        try:
            row = con.execute(sql, args).fetchone()
        except sqlite3.Error:                    # pl_pages is the studio's; it may be absent
            continue
        if row:
            try:
                w, h = float(row[0] or 0), float(row[1] or 0)
            except (TypeError, ValueError):
                continue
            if 1 < w < 1e6 and 1 < h < 1e6:
                return w, h
    return None


def page_area(pg, raster: tuple[float, float] | None) -> tuple[str, float | None]:
    """Which part of a PDF page the parser drew — ("crop" | "media" | "img:…", error).

    ``pg`` is a PyMuPDF page. The parser's image was either a render of the
    page — of its CropBox (PyMuPDF, viewers) or its MediaBox (pdftoppm,
    pdf2image) — or, for a scanned book, the scan itself taken out of the PDF.
    A scan placed on the page with margins round it is a third rectangle, and
    the decisive sign of it is an image on the page whose size in pixels is
    exactly the parser's image size: then the boxes are fractions of where
    that image sits ("img:x0,y0,x1,y1", page coordinates). Otherwise the box
    whose shape (rotation applied) matches the parser's image is taken.

    ``error`` is the relative difference between the chosen rectangle's shape
    and the parser's image (|log of the aspect ratios|): 0.003 is a rounding
    difference, 0.05 a different picture. None when the parser's image size is
    not known, and then the CropBox, as before.
    """
    if not raster:
        return "crop", None
    want = raster[0] / raster[1]

    def err(w: float, h: float) -> float:
        return abs(math.log((w / h) / want)) if w > 0 and h > 0 else 9.0

    crop = err(pg.rect.width, pg.rect.height)            # rotation already applied
    mb = pg.mediabox
    turned = pg.rotation % 180 == 90
    media = err(mb.height, mb.width) if turned else err(mb.width, mb.height)
    scan = _scan_rect(pg, raster)
    if scan is not None:
        same = lambda a, b: max(abs(a.x0 - b.x0), abs(a.y0 - b.y0),
                                abs(a.x1 - b.x1), abs(a.y1 - b.y1)) < 0.5
        if not same(scan, pg.rect):
            return (f"img:{scan.x0:.2f},{scan.y0:.2f},{scan.x1:.2f},{scan.y1:.2f}",
                    round(err(scan.width, scan.height), 5))
    if media + 0.002 < crop:
        return "media", round(media, 5)
    return "crop", round(crop, 5)


def _scan_rect(pg, raster: tuple[float, float]):
    """Where the page's scan sits, when the parser's image is that scan: an
    image drawn upright, covering most of the page, whose size in pixels is
    the parser's image size exactly. Else None."""
    if pg.rotation % 360:
        return None
    try:
        infos = pg.get_image_info()
    except Exception:                            # a damaged image list: not a scan we can place
        return None
    want = (round(raster[0]), round(raster[1]))
    whole = max(pg.rect.width * pg.rect.height, 1.0)
    from pdflib import fitz
    for info in infos:
        if (info.get("width"), info.get("height")) != want:
            continue
        a, b, c, d, _e, _f = (tuple(info.get("transform") or ()) + (0,) * 6)[:6]
        if not (a > 0 and d > 0 and abs(b) < 1e-6 and abs(c) < 1e-6):
            continue                             # turned or flipped: drawn some other way
        r = fitz.Rect(info.get("bbox") or (0, 0, 0, 0)) & pg.rect
        if r.width * r.height >= 0.5 * whole:
            return r
    return None


def area_rect(pg, area: str):
    """The rectangle of a PyMuPDF page that ``area`` names, in the page's own
    (rotated, CropBox-relative) coordinates — what a clip is given in. For
    "media", the page is widened to its MediaBox in memory; the file is never
    saved."""
    if area == "media":
        if pg.mediabox != pg.cropbox:
            pg.set_cropbox(pg.mediabox)
        return pg.rect
    if area.startswith("img:"):
        from pdflib import fitz
        try:
            x0, y0, x1, y1 = (float(v) for v in area[4:].split(","))
            r = fitz.Rect(x0, y0, x1, y1) & pg.rect
            if r.width > 1 and r.height > 1:
                return r
        except ValueError:
            pass
    return pg.rect


@lru_cache(maxsize=4096)
def _fit_cached(path: str, stamp: int, page: int, raster: tuple | None) -> tuple:
    from pdflib import fitz
    with fitz.open(path) as doc:
        if page < 0 or page >= doc.page_count:
            return "crop", None
        return page_area(doc[page], raster)


def fit(pdf: Path, page: int, raster: tuple[float, float] | None) -> tuple[str, float | None]:
    """page_area() for a page of a file, remembered until the file changes."""
    try:
        stamp = os.stat(pdf).st_mtime_ns
        return _fit_cached(str(pdf), stamp, int(page), tuple(raster) if raster else None)
    except Exception as exc:                     # an unreadable PDF: drawn as before
        log.info("could not measure %s p%s: %s", pdf, page, exc)
        return "crop", None


def _render(pdf: Path, page: int, box: tuple, dpi: int, area: str = "crop"):
    """Cut one region of a PDF page, as PNG bytes. Returns (png, width, height).

    ``box`` is (x0, y0, x1, y1) as fractions of the page — of the rectangle
    named by ``area`` (see page_area), with the page's rotation applied — so it is
    independent of the parser's raster and of the DPI asked for here. Imported
    lazily so that the annotation core can be imported, and tested, on a
    machine with no PyMuPDF at all.
    """
    from pdflib import fitz
    with fitz.open(pdf) as doc:
        if page < 0 or page >= doc.page_count:
            raise ValueError(f"page {page} is outside this PDF (0..{doc.page_count - 1})")
        pg = doc[page]
        r = area_rect(pg, area)
        x0 = r.x0 + max(0.0, box[0] - CROP_PAD) * r.width
        y0 = r.y0 + max(0.0, box[1] - CROP_PAD) * r.height
        x1 = r.x0 + min(1.0, box[2] + CROP_PAD) * r.width
        y1 = r.y0 + min(1.0, box[3] + CROP_PAD) * r.height
        if x1 - x0 < 1 or y1 - y0 < 1:
            raise ValueError("the selected region is too small to crop")
        pix = pg.get_pixmap(clip=fitz.Rect(x0, y0, x1, y1), dpi=dpi)
        return pix.tobytes("png"), pix.width, pix.height


def _is_lfs_pointer(path: Path) -> bool:
    """Is this a Git LFS pointer standing in for a PDF that was never fetched?

    The commonest reason a page cannot be shown on a fresh checkout, and one
    with a specific fix, so it is worth telling apart from a genuinely broken
    file. A pointer is a ~132-byte text file that every directory listing and
    file count reports as a PDF.
    """
    try:
        with open(path, "rb") as fh:
            return fh.read(5) != b"%PDF-"
    except OSError:                              # pragma: no cover - race
        return False


def _find_pdf(relpath: str) -> Path | None:
    """Locate a book's PDF: at its own relative path, or else by its name.

    A corpus gets reorganised; the file name is the stable part, so it is
    searched for. But names repeat — NCERT's English and Hindi chapters are
    both called ``1001.pdf``, in ``eng/10/`` and ``hin/10/`` — so of several
    files with the name, the one whose folders match the most of the relpath's
    is taken, and a tie is no answer: no page at all is better than the page
    of the other language, under boxes that belong to this one.
    """
    try:
        data = Path(config.DATA_DIR).resolve()
        parts = [x for x in str(relpath or "").replace("\\", "/").split("/") if x not in ("", ".")]
        if not parts or ".." in parts:
            return None
        direct = data.joinpath(*parts)
        if direct.is_file() and direct.resolve().is_relative_to(data):
            return direct
        want = [x.lower() for x in parts]
        found = []
        for cand in data.rglob(parts[-1]):
            try:
                if not cand.is_file() or not cand.resolve().is_relative_to(data):
                    continue
                have = [x.lower() for x in cand.relative_to(data).parts]
            except (OSError, ValueError):
                continue
            same = 0
            for a, b in zip(reversed(have), reversed(want)):
                if a != b:
                    break
                same += 1
            found.append((same, cand))
        if not found:
            return None
        found.sort(key=lambda t: -t[0])
        if len(found) > 1 and found[0][0] == found[1][0]:
            log.info("%d files named %s fit %s equally; showing none", len(found),
                     parts[-1], relpath)
            return None
        return found[0][1]
    except Exception as exc:                     # pragma: no cover - filesystem shape
        log.info("could not look for %s: %s", relpath, exc)
        return None


def _cached_path(relpath: str, page: int, box: tuple, dpi: int, area: str = "crop") -> Path:
    """A content-addressed name.

    The file name is a digest of everything that determines the image, so two
    requests for the same region share a file and a request for a different
    region cannot collide with it. It also means no part of a caller-supplied
    string ever becomes a path component — the book's path is hashed, not
    embedded.
    """
    key = "|".join([str(relpath), str(page), str(dpi),
                    *(f"{v:.5f}" for v in box)] + ([area] if area != "crop" else []))
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
    return cache_dir() / f"pg_{digest}.png"


def _f(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def prune_cache(keep_bytes: int = 256 * 1024 * 1024) -> dict:
    """Drop the least recently used page images once the cache gets large.

    Source views are regenerable, so deleting one costs a re-render and nothing
    else. Called from the launcher at start-up rather than on a timer: a cache
    sweep competing with an annotator's autosave is a bad trade.
    """
    d = cache_dir()
    files = sorted((p for p in d.glob("pg_*.png") if p.is_file()),
                   key=lambda p: p.stat().st_atime)
    total = sum(p.stat().st_size for p in files)
    removed = 0
    freed = 0
    with _lock:
        for p in files:
            if total - freed <= keep_bytes:
                break
            try:
                size = p.stat().st_size
                p.unlink()
                freed += size
                removed += 1
            except OSError:                      # pragma: no cover - race
                continue
    return {"files": len(files), "removed": removed, "freed_bytes": freed,
            "remaining_bytes": total - freed}


# ── whole pages, for the block overlay ─────────────────────────────────────
#
# `for_segment` above answers "show me where this piece of text came from" and
# deliberately clamps its context to a fifth of a page: it is a verification
# crop, not a page. The block overlay needs the opposite — the entire page,
# once, at a resolution that is comfortable to read on screen, with every
# block drawn on top of it.
#
# The two share everything below the box: the same PDF lookup that tolerates a
# reorganised corpus, the same Git LFS pointer check, the same content-keyed
# cache written through a temporary name so a second annotator never reads a
# half-written file.

#: On-screen resolution for a whole page. Tulana's own viewer uses 110; this
#: is a little higher because Setu's panes are narrower than the studio's.
PAGE_DPI = int(getattr(config, "SOURCE_PAGE_DPI", 130) or 130)


def page_image(con, book_key: str, page: Any, *, dpi: int | None = None) -> SourceView:
    """Render one whole page of one book.

    Never raises. A missing PDF, a Git LFS pointer, a page past the end of the
    file and a machine with no PyMuPDF are all ordinary states of this corpus,
    and each comes back as a sentence an annotator can act on.

    ``page`` is the **stored** page number, counting from zero, which is what
    ``setu_segment.page`` holds and what PyMuPDF indexes by. The interface is
    responsible for showing it as ``page + 1``.
    """
    ok, why = available()
    if not ok:
        return SourceView(False, message=why)

    try:
        n = int(page)
    except (TypeError, ValueError):
        return SourceView(False, message="That is not a page number.")
    if n < 0:
        return SourceView(False, message="That is not a page number.")

    book = Repository(con).one(
        "SELECT book_key, relpath, book, title, num_pages FROM setu_book"
        "  WHERE book_key = ?", (book_key,))
    if not book:
        return SourceView(False, message="No such textbook.")

    label = book["title"] or book["book"] or book_key
    pdf = _find_pdf(book["relpath"])
    if pdf is None:
        return SourceView(
            False, page=n, book=label, relpath=book["relpath"],
            message=(f"The scanned pages of “{label}” are not on this machine. "
                     f"The text is unaffected. If the PDFs are stored with Git "
                     f"LFS, run:  git lfs pull"))
    if _is_lfs_pointer(pdf):
        return SourceView(
            False, page=n, book=label, relpath=book["relpath"],
            message=(f"“{label}” has not been downloaded — the file here is a "
                     f"Git LFS pointer, not the book. The text is unaffected. "
                     f"To fetch the scans, run:  git lfs pull"))

    res = max(60, min(300, int(dpi or PAGE_DPI)))
    area, err = fit(pdf, n, raster_size(con, book_key, n))
    out = _cached_path(book["relpath"], n, (0.0, 0.0, 1.0, 1.0), res, area)
    if out.exists():
        return SourceView(True, out, page=n, book=label, relpath=book["relpath"],
                          area=area, fit_error=err)

    try:
        png, _w, _h = _render(pdf, n, (0.0, 0.0, 1.0, 1.0), res, area)
    except Exception as exc:
        log.info("page image failed for %s p%s (%s): %s", book_key, n, pdf, exc)
        return SourceView(
            False, page=n, book=label, relpath=book["relpath"],
            message=(f"Page {n + 1} of “{label}” could not be drawn. The text "
                     f"is unaffected — carry on."))

    tmp = out.with_name(out.name + f".{threading.get_ident()}.part")
    try:
        tmp.write_bytes(png)
        tmp.replace(out)
    except OSError as exc:                       # pragma: no cover - disk full
        tmp.unlink(missing_ok=True)
        log.warning("could not cache a page image: %s", exc)
        return SourceView(False, page=n, book=label,
                          message=f"The page could not be saved for display ({exc}).")
    return SourceView(True, out, page=n, book=label, relpath=book["relpath"],
                      area=area, fit_error=err)


def region(con, book_key: str, page: Any, box: Any, *,
           dpi: int | None = None) -> SourceView:
    """Cut one rectangle out of one page — the crop tool's whole job.

    ``box`` is ``(x0, y0, x1, y1)`` as **fractions of the page**, which is the
    form every box travels in throughout Tulana: it survives any DPI and any
    rescale, so what the annotator dragged on a 130 dpi image is cut correctly
    from a 300 dpi render without either knowing about the other.
    """
    ok, why = available()
    if not ok:
        return SourceView(False, message=why)
    try:
        n = int(page)
        x0, y0, x1, y1 = (max(0.0, min(1.0, float(v))) for v in list(box)[:4])
    except (TypeError, ValueError, IndexError):
        return SourceView(False, message="That is not a rectangle on a page.")
    if x1 - x0 < 0.004 or y1 - y0 < 0.004:
        return SourceView(False, message="That rectangle is too small to cut.")

    book = Repository(con).one(
        "SELECT relpath, book, title FROM setu_book WHERE book_key = ?", (book_key,))
    if not book:
        return SourceView(False, message="No such textbook.")
    label = book["title"] or book["book"] or book_key
    pdf = _find_pdf(book["relpath"])
    if pdf is None or _is_lfs_pointer(pdf):
        return SourceView(False, page=n, book=label,
                          message=(f"The scanned pages of “{label}” are not on "
                                   f"this machine, so nothing can be cut from "
                                   f"them. Run:  git lfs pull"))

    res = max(72, min(400, int(dpi or 300)))
    area, err = fit(pdf, n, raster_size(con, book_key, n))
    out = _cached_path(book["relpath"], n, (x0, y0, x1, y1), res, area)
    if out.exists():
        return SourceView(True, out, page=n, book=label, relpath=book["relpath"],
                          area=area, fit_error=err)
    try:
        png, _w, _h = _render(pdf, n, (x0, y0, x1, y1), res, area)
    except Exception as exc:
        log.info("crop failed for %s p%s %s: %s", book_key, n, (x0, y0, x1, y1), exc)
        return SourceView(False, page=n, book=label,
                          message="That region could not be cut from the page.")
    tmp = out.with_name(out.name + f".{threading.get_ident()}.part")
    try:
        tmp.write_bytes(png)
        tmp.replace(out)
    except OSError as exc:                       # pragma: no cover
        tmp.unlink(missing_ok=True)
        return SourceView(False, page=n, book=label,
                          message=f"The crop could not be saved ({exc}).")
    return SourceView(True, out, page=n, book=label, relpath=book["relpath"],
                      area=area, fit_error=err)
