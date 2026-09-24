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
import threading
from dataclasses import dataclass
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

    def as_dict(self) -> dict:
        return {"ok": self.ok, "path": str(self.path) if self.path else "",
                "message": self.message, "page": self.page, "book": self.book,
                "relpath": self.relpath}


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

    out = _cached_path(seg["relpath"], seg["page"], box, res)
    if out.exists():
        return SourceView(True, out, page=seg["page"], book=label,
                          relpath=seg["relpath"])

    try:
        png, _w, _h = _render(pdf, int(seg["page"]), box, res)
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
                      relpath=seg["relpath"])


def _render(pdf: Path, page: int, box: tuple, dpi: int):
    """Delegate to Tulana's own crop renderer.

    Imported here rather than at module load so that the annotation core can be
    imported — and tested — on a machine with no PyMuPDF at all.
    """
    import pairs
    return pairs._render_crop(pdf, page, box, dpi=dpi)


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
    """Locate a book's PDF using the corpus conventions Tulana already knows."""
    try:
        import blocks
        return blocks._find_pdf(Path(config.DATA_DIR), relpath)
    except Exception as exc:                     # pragma: no cover - import shape
        log.info("could not look for %s: %s", relpath, exc)
        return None


def _cached_path(relpath: str, page: int, box: tuple, dpi: int) -> Path:
    """A content-addressed name.

    The file name is a digest of everything that determines the image, so two
    requests for the same region share a file and a request for a different
    region cannot collide with it. It also means no part of a caller-supplied
    string ever becomes a path component — the book's path is hashed, not
    embedded.
    """
    key = "|".join([str(relpath), str(page), str(dpi),
                    *(f"{v:.5f}" for v in box)])
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
    out = _cached_path(book["relpath"], n, (0.0, 0.0, 1.0, 1.0), res)
    if out.exists():
        return SourceView(True, out, page=n, book=label, relpath=book["relpath"])

    try:
        png, _w, _h = _render(pdf, n, (0.0, 0.0, 1.0, 1.0), res)
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
    return SourceView(True, out, page=n, book=label, relpath=book["relpath"])


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
    out = _cached_path(book["relpath"], n, (x0, y0, x1, y1), res)
    if out.exists():
        return SourceView(True, out, page=n, book=label, relpath=book["relpath"])
    try:
        png, _w, _h = _render(pdf, n, (x0, y0, x1, y1), res)
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
    return SourceView(True, out, page=n, book=label, relpath=book["relpath"])
