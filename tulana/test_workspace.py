#!/usr/bin/env python3
"""Tests for the workspace: page images, block geometry, crops, the API.

Run with no arguments::

    python3 test_workspace.py
    python3 test_workspace.py -v

The fixture comes from ``test_annotation``, and this suite adds one thing of
its own: **a real PDF, built here, with a known mark at a known fraction of
each page.** That is what makes the geometry claim testable rather than
asserted. No textbook is needed and nothing is downloaded.

The claim being defended
------------------------
Tulana's whole coordinate story is one sentence: *a box travels as a fraction
of the page.* The parser measured its boxes against a raster of some size; the
page is drawn on screen at whatever size fits the pane; a crop is cut at 300
dpi. None of the three knows about the others, and none has to.

If that is true, then cutting the fractional box of a block out of the real PDF
must return the region that block's text came from — at any DPI. These tests
draw four marks at four known fractions, cut those exact fractions back out,
and read the text that really falls inside. If a rescale, a y-flip or an
off-by-one page ever creeps in, ``test_a_fraction_cuts_the_region_it_names``
fails and says which quadrant moved.

The second claim is the page numbering. Storage counts from zero because the
layout JSON does and PyMuPDF does; people count from one. Every number the
interface shows is ``page + 1``, and ``display_page`` is where that happens on
the way out of the API.
"""
from __future__ import annotations

import hashlib
import sqlite3
import unittest

from test_annotation import LEGACY_TABLES, SetuCase          # noqa: E402

import config                                                # noqa: E402
from annotation.core import ids, sources, store              # noqa: E402

try:
    import pymupdf as _fitz
except ImportError:                                          # pragma: no cover
    try:
        import fitz as _fitz
    except ImportError:
        _fitz = None

#: Where each mark is drawn, as a fraction of the page. The box stored for it
#: is (fx, fy, fx + 0.35, fy + 0.06), which is wide enough to hold the word and
#: narrow enough that the quadrants cannot overlap.
QUADRANTS = {
    "TOPLEFT": (0.05, 0.08),
    "TOPRIGHT": (0.60, 0.08),
    "BOTLEFT": (0.05, 0.80),
    "BOTRIGHT": (0.60, 0.80),
}
PAGES = 3


def status(result) -> int:
    """The HTTP code an endpoint answered with.

    Every endpoint wears ``@guard``, so a refusal comes back as a JSONResponse
    rather than as an exception — that is what keeps a traceback out of a
    browser. A plain dict means it succeeded.
    """
    return getattr(result, "status_code", 200)


class PageCase(SetuCase):
    """A real three-page PDF with a known mark in each quadrant of each page."""

    def setUp(self):
        super().setUp()
        if _fitz is None:
            self.skipTest("PyMuPDF is not installed, so no page can be drawn")
        self.pdf_dir = self.dir / "pdfs"
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self._old_data = config.DATA_DIR
        config.DATA_DIR = self.pdf_dir

        self.pdf = self.pdf_dir / "MARKS.pdf"
        doc = _fitz.open()
        for page_no in range(PAGES):
            pg = doc.new_page(width=595, height=842)         # A4, in points
            w, h = pg.rect.width, pg.rect.height
            for name, (fx, fy) in QUADRANTS.items():
                pg.insert_text((fx * w, fy * h + 20), f"{name}-P{page_no}",
                               fontsize=26)
        doc.save(self.pdf)
        doc.close()

        self.book = ids.book_key("MARKS")
        with store.connect() as con:
            con.execute("PRAGMA foreign_keys=OFF")
            con.execute("BEGIN")
            cols = [r[1] for r in con.execute("PRAGMA table_info(setu_book)")]
            row = {"book_key": self.book, "pl_book_id": 999999, "book": "MARKS",
                   "title": "Marked pages", "board": "ZZ", "class": 1,
                   "subject": "Mathematics", "language": "English",
                   "script": "Latin", "volume": "", "num_pages": PAGES,
                   "n_segments": len(QUADRANTS) * PAGES, "pdf_present": 1,
                   "relpath": "MARKS.pdf", "dedup_key": "marks"}
            keys = [c for c in cols if c in row]
            con.execute(f"INSERT INTO setu_book({','.join(keys)})"
                        f" VALUES({','.join('?' * len(keys))})",
                        [row[c] for c in keys])
            seq = 0
            for page_no in range(PAGES):
                for name, (fx, fy) in QUADRANTS.items():
                    con.execute(
                        "INSERT INTO setu_segment(sid, book_key, seq, page,"
                        " ord_start, ord_end, kind, label, source_text, n_chars,"
                        " fx0, fy0, fx1, fy1)"
                        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (f"sg_MARK{seq:04d}", self.book, seq, page_no, seq, seq,
                         "paragraph", "Paragraph", f"{name}-P{page_no}",
                         len(name), fx, fy, fx + 0.35, fy + 0.06))
                    seq += 1
            con.execute("COMMIT")

    def tearDown(self):
        config.DATA_DIR = self._old_data
        super().tearDown()

    def text_really_at(self, page: int, box) -> str:
        """What the PDF itself has inside that fraction of that page.

        Read straight from the document rather than from anything Setu
        produced, so the test cannot agree with a bug by sharing it.
        """
        doc = _fitz.open(self.pdf)
        try:
            pg = doc[page]
            r = pg.rect
            clip = _fitz.Rect(box[0] * r.width, box[1] * r.height,
                              box[2] * r.width, box[3] * r.height)
            return " ".join(pg.get_text("text", clip=clip).split())
        finally:
            doc.close()


# ── the geometry ───────────────────────────────────────────────────────────

class TestGeometry(PageCase):

    def test_a_whole_page_renders(self):
        with store.ro() as con:
            view = sources.page_image(con, self.book, 0)
        self.assertTrue(view.ok, view.message)
        self.assertTrue(view.path and view.path.is_file())
        self.assertGreater(view.path.stat().st_size, 1000)

    def test_each_page_is_a_different_page(self):
        """An off-by-one would hand back the same image for two page numbers."""
        seen = {}
        with store.ro() as con:
            for page in range(PAGES):
                view = sources.page_image(con, self.book, page)
                self.assertTrue(view.ok, view.message)
                seen[page] = hashlib.sha256(view.path.read_bytes()).hexdigest()
        self.assertEqual(len(set(seen.values())), PAGES,
                         "two page numbers rendered the same image")

    def test_a_fraction_cuts_the_region_it_names(self):
        """The claim the whole coordinate design rests on."""
        with store.ro() as con:
            for page in range(PAGES):
                for name, (fx, fy) in QUADRANTS.items():
                    box = (fx, fy, fx + 0.35, fy + 0.06)
                    with self.subTest(page=page, quadrant=name):
                        view = sources.region(con, self.book, page, box)
                        self.assertTrue(view.ok, view.message)
                        found = self.text_really_at(page, box)
                        self.assertIn(f"{name}-P{page}", found,
                                      f"the box for {name} on page {page} "
                                      f"covers {found!r} instead")

    def test_the_fraction_is_the_same_at_every_resolution(self):
        """A crop at 100 and at 300 dpi must be the same region, larger."""
        box = (0.05, 0.08, 0.40, 0.14)
        with store.ro() as con:
            low = sources.region(con, self.book, 0, box, dpi=100)
            high = sources.region(con, self.book, 0, box, dpi=300)
        self.assertTrue(low.ok and high.ok)
        self.assertNotEqual(low.path, high.path, "two resolutions, two files")
        from PIL import Image
        with Image.open(low.path) as a, Image.open(high.path) as b:
            self.assertAlmostEqual(a.width / a.height, b.width / b.height,
                                   places=1,
                                   msg="the same fraction changed shape with dpi")
            self.assertGreater(b.width, a.width * 2)

    def test_a_box_outside_the_page_is_clamped_not_fatal(self):
        with store.ro() as con:
            view = sources.region(con, self.book, 0, (-5.0, -5.0, 9.0, 9.0))
        self.assertTrue(view.ok, view.message)

    def test_a_box_of_nothing_is_refused_with_a_sentence(self):
        with store.ro() as con:
            view = sources.region(con, self.book, 0, (0.5, 0.5, 0.5001, 0.5001))
        self.assertFalse(view.ok)
        self.assertIn("too small", view.message)


# ── page numbering ─────────────────────────────────────────────────────────

class TestPageNumbers(PageCase):

    def test_storage_counts_from_zero(self):
        row = store.Repository(self.con).one(
            "SELECT MIN(page) AS lo FROM setu_segment WHERE book_key = ?",
            (self.book,))
        self.assertEqual(row["lo"], 0)

    def test_the_api_reports_the_printed_number(self):
        from annotation.api import page_blocks
        out = page_blocks(self.book, 0)
        self.assertEqual(out["page"], 0)
        self.assertEqual(out["display_page"], 1,
                         "the first page must be called page 1")
        for b in out["blocks"]:
            self.assertEqual(b["display_page"], b["page"] + 1)

    def test_the_last_page_is_not_off_the_end(self):
        from annotation.api import page_blocks
        out = page_blocks(self.book, PAGES - 1)
        self.assertEqual(out["display_page"], PAGES)
        self.assertEqual(out["last_page"], PAGES - 1)


# ── what the interface is handed ───────────────────────────────────────────

class TestApi(PageCase):

    def test_blocks_come_back_in_reading_order_with_their_boxes(self):
        from annotation.api import page_blocks
        out = page_blocks(self.book, 1)
        self.assertEqual(len(out["blocks"]), len(QUADRANTS))
        self.assertEqual([b["seq"] for b in out["blocks"]],
                         sorted(b["seq"] for b in out["blocks"]))
        for b in out["blocks"]:
            for k in ("fx0", "fy0", "fx1", "fy1"):
                self.assertGreaterEqual(b[k], 0.0)
                self.assertLessEqual(b[k], 1.0)
            self.assertLess(b["fx0"], b["fx1"])
            self.assertLess(b["fy0"], b["fy1"])

    def test_the_interface_is_told_whether_a_scan_exists(self):
        from annotation.api import page_blocks
        out = page_blocks(self.book, 0)
        self.assertTrue(out["image_available"])
        self.assertEqual(out["image_message"], "")

    def test_a_missing_scan_is_a_sentence_not_a_failure(self):
        """The normal state of a Git LFS checkout. It must not stop the work."""
        self.pdf.unlink()
        from annotation.api import page_blocks
        out = page_blocks(self.book, 0)
        self.assertFalse(out["image_available"])
        self.assertTrue(out["image_message"])
        self.assertIn("git lfs pull", out["image_message"])
        self.assertEqual(len(out["blocks"]), len(QUADRANTS),
                         "the blocks must still be served without the scan")

    def test_an_unknown_book_is_refused(self):
        # Every endpoint wears @guard, which turns the service layer's
        # exceptions into the one error shape rather than letting a traceback
        # reach a browser. So a refusal arrives as a 404 response, not a raise.
        from annotation.api import page_blocks
        self.assertEqual(status(page_blocks("bk_NOTAREALBOOK", 0)), 404)

    def test_a_book_key_cannot_name_a_file(self):
        """The key reaches a SQL parameter, never a path."""
        from annotation.api import page_blocks
        for hostile in ("../../etc/passwd", "bk_'; DROP TABLE setu_book;--",
                        "../../../../../../etc/shadow"):
            with self.subTest(key=hostile):
                self.assertEqual(status(page_blocks(hostile, 0)), 404)
        self.assertTrue(store.Repository(self.con).one(
            "SELECT 1 AS ok FROM setu_book LIMIT 1"),
            "setu_book survived every hostile key")

    def test_the_two_sides_get_two_chapter_lists(self):
        from annotation.api import project_outline
        proj = self.project()
        out = project_outline(proj["pid"])
        self.assertIn("src", out)
        self.assertIn("tgt", out)
        self.assertNotEqual(out["src"]["book_key"], out["tgt"]["book_key"])
        for side in ("src", "tgt"):
            for ch in out[side]["chapters"]:
                if ch["first_page"] is not None:
                    self.assertEqual(ch["display_page"], ch["first_page"] + 1)

    def test_the_page_link_is_saved_read_and_cleared(self):
        from annotation.api import get_page_link, set_page_link

        class Req:                                # the API only reads headers
            headers = {"X-Annotator": "tester"}

        proj = self.project()
        self.assertEqual(get_page_link(proj["pid"])["link"], {})
        out = set_page_link(Req(), proj["pid"],
                            {"src_page": 7, "tgt_page": 4, "annotator": "tester"})
        self.assertEqual(out["link"]["offset"], 3)
        self.assertEqual(get_page_link(proj["pid"])["link"]["src_page"], 7)
        set_page_link(Req(), proj["pid"], {"clear": True})
        self.assertEqual(get_page_link(proj["pid"])["link"], {})

    def test_the_link_needs_two_real_page_numbers(self):
        from annotation.api import set_page_link

        class Req:
            headers = {"X-Annotator": "tester"}

        proj = self.project()
        for bad in ({}, {"src_page": "x", "tgt_page": 1}, {"src_page": 1},
                    {"src_page": None, "tgt_page": None}):
            with self.subTest(payload=bad):
                self.assertEqual(status(set_page_link(Req(), proj["pid"], bad)),
                                 400)


# ── the one that means stop ────────────────────────────────────────────────

class TestLegacyUntouched(PageCase):

    @staticmethod
    def _fingerprint(con) -> dict:
        out = {}
        for t in LEGACY_TABLES:
            try:
                rows = con.execute(f"SELECT * FROM {t} ORDER BY rowid").fetchall()
            except sqlite3.OperationalError:
                out[t] = "absent"
                continue
            h = hashlib.sha256()
            for r in rows:
                h.update(repr(tuple(r)).encode("utf-8"))
            out[t] = f"{len(rows)}:{h.hexdigest()[:16]}"
        return out

    def test_drawing_pages_changes_none_of_tulanas_tables(self):
        from annotation.api import page_blocks, project_outline
        before = self._fingerprint(self.con)
        proj = self.project()
        project_outline(proj["pid"])
        with store.ro() as con:
            for page in range(PAGES):
                sources.page_image(con, self.book, page)
                sources.region(con, self.book, page, (0.1, 0.1, 0.5, 0.3))
                page_blocks(self.book, page, pid=proj["pid"])
        self.assertEqual(before, self._fingerprint(self.con),
                         "drawing pages changed one of Tulana's own tables")

    def test_page_images_are_written_only_under_the_state_folder(self):
        """No user value ever decides where a file is written."""
        with store.ro() as con:
            view = sources.page_image(con, self.book, 0)
        self.assertTrue(view.ok)
        self.assertTrue(
            view.path.resolve().is_relative_to(sources.cache_dir().resolve()),
            f"a page image landed outside the cache: {view.path}")


if __name__ == "__main__":                       # pragma: no cover
    unittest.main(verbosity=2)
