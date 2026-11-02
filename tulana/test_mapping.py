#!/usr/bin/env python3
"""Do the boxes land on the printed page? Tests with PDFs built here.

    python3 test_mapping.py
    python3 test_mapping.py -v

The aligned set's boxes are fractions of the image the parser measured on.
Setu renders the PDF page and draws the boxes over it, and cuts "as printed"
pictures out of it. These tests build PDFs whose text is at known places —
plain, with a CropBox inside the MediaBox, rotated, both — write the boxes the
way the parser would have measured them, and check three things:

* sources.page_area picks the part of the page the parser saw — CropBox,
  MediaBox, or a scan placed inside the page with margins — so a box cut back
  out of the PDF holds the words it was drawn around;
* sources._find_pdf never answers with another book's file — NCERT's English
  and Hindi chapters share names (eng/10/1001.pdf, hin/10/1001.pdf);
* check_mapping, the audit for real PDFs, passes a correct page and catches a
  shifted one, a page of the wrong shape, and boxes over blank paper.
"""
from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import config
from annotation.core import sources

try:
    import pymupdf as fitz
except ImportError:                                          # pragma: no cover
    try:
        import fitz                                          # type: ignore
    except ImportError:
        fitz = None

WORDS = [f"Line{i} the angles of a triangle add up to 180 degrees" for i in range(16)]


def make_pdf(path: Path, crop=None, rotate=0, size=(595, 842)) -> None:
    doc = fitz.open()
    pg = doc.new_page(width=size[0], height=size[1])
    y = 90
    for i, t in enumerate(WORDS):
        pg.insert_text((60 if i % 3 else 95, y), t, fontsize=11)
        y += 38 if i % 4 else 54
    pg.draw_rect(fitz.Rect(4, 4, size[0] - 4, size[1] - 4), color=(.8, .8, .8))
    if crop:
        pg.set_cropbox(fitz.Rect(*crop))
    if rotate:
        pg.set_rotation(rotate)
    doc.save(path)
    doc.close()


def parser_page(pdf: Path, area="crop", shift=(0.0, 0.0), dpi=200, stretch=(1.0, 1.0)) -> dict:
    """One page as the parser would have written it: line boxes in pixels of
    its own render of the page — of the CropBox, or (``area="media"``) of the
    whole MediaBox, as pdftoppm draws it."""
    with fitz.open(pdf) as doc:
        pg = doc[0]
        if area == "media":
            pg.set_cropbox(pg.mediabox)
        r = pg.rect
        W = round(r.width * dpi / 72 * stretch[0])
        H = round(r.height * dpi / 72 * stretch[1])
        blocks, k = [], 0
        for b in pg.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                q = fitz.Rect(line["bbox"]) * pg.rotation_matrix
                box = [(q.x0 / r.width + shift[0]) * W, (q.y0 / r.height + shift[1]) * H,
                       (q.x1 / r.width + shift[0]) * W, (q.y1 / r.height + shift[1]) * H]
                text = "".join(s["text"] for s in line["spans"])
                blocks.append({"order": k, "text": text, "bbox_xyxy": box,
                               "members": [{"order": k, "bbox_xyxy": box}]})
                k += 1
    return {"page": 0, "width": W, "height": H, "blocks": blocks}


def make_scan_pdf(path: Path, place=(40, 50, 555, 800), px=(1300, 1900)) -> dict:
    """A scanned book's page: a picture of the page (dark bars where the text
    is), placed on an A4 page with margins round it — and the parser's page as
    it would read that picture: boxes in the picture's own pixels."""
    import numpy as np
    W, H = px
    img = np.full((H, W), 255, np.uint8)
    blocks = []
    for i in range(14):
        y, x1 = 150 + i * 120, 1150 - (i % 3) * 150
        img[y:y + 40, 120:x1] = 20
        box = [120.0, float(y), float(x1), float(y + 40)]
        blocks.append({"order": i, "text": f"Line{i} printed", "bbox_xyxy": box,
                       "members": [{"order": i, "bbox_xyxy": box}]})
    doc = fitz.open()
    pg = doc.new_page(width=595.28, height=841.89)
    pg.insert_image(fitz.Rect(*place), pixmap=fitz.Pixmap(fitz.csGRAY, W, H, img.tobytes(), False))
    doc.save(path)
    doc.close()
    return {"page": 0, "width": W, "height": H, "blocks": blocks}


@unittest.skipIf(fitz is None, "PyMuPDF is not installed")
class TestScannedPages(unittest.TestCase):
    """A scan placed inside the page with margins: the parser's boxes are
    fractions of the scan, not of the page — drawn on the page they would sit
    beside the print."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="setu-scan-"))
        self.pdf = self.dir / "scan.pdf"
        self.page = make_scan_pdf(self.pdf)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_the_scan_is_found_where_it_sits(self):
        with fitz.open(self.pdf) as doc:
            area, err = sources.page_area(doc[0], (self.page["width"], self.page["height"]))
            r = sources.area_rect(doc[0], area)
        self.assertTrue(area.startswith("img:"), area)
        self.assertLess(err, sources.FIT_TOLERANCE)
        self.assertAlmostEqual(r.y1, 800, delta=1)

    def test_a_cut_holds_the_print_it_names(self):
        """Every box, cut out of the PDF, is dark where the parser saw print."""
        import numpy as np
        with fitz.open(self.pdf) as doc:
            area, _ = sources.page_area(doc[0], (self.page["width"], self.page["height"]))
        for b in self.page["blocks"]:
            x0, y0, x1, y1 = b["bbox_xyxy"]
            box = (x0 / self.page["width"], y0 / self.page["height"],
                   x1 / self.page["width"], y1 / self.page["height"])
            png, w, h = sources._render(self.pdf, 0, box, 100, area)
            pix = fitz.Pixmap(png)
            gray = np.frombuffer(pix.samples, np.uint8)[::pix.n]
            self.assertGreater(float((gray < 128).mean()), 0.5, b["order"])

    def test_the_whole_page_image_is_the_scan(self):
        with fitz.open(self.pdf) as doc:
            area, _ = sources.page_area(doc[0], (self.page["width"], self.page["height"]))
        _png, w, h = sources._render(self.pdf, 0, (0, 0, 1, 1), 72, area)
        self.assertAlmostEqual(w / h, self.page["width"] / self.page["height"], delta=0.01)

    def test_a_scan_that_fills_the_page_is_just_the_page(self):
        pdf = self.dir / "full.pdf"
        page = make_scan_pdf(pdf, place=(0, 0, 595.28, 841.89), px=(1654, 2339))
        with fitz.open(pdf) as doc:
            self.assertEqual(sources.page_area(doc[0], (page["width"], page["height"]))[0], "crop")

    def test_the_audit_passes_it_and_would_have_failed_it(self):
        import check_mapping
        with fitz.open(self.pdf) as doc:
            self.assertEqual(check_mapping.check_page(doc, self.page)["verdict"], "ok")
        # the same boxes taken as fractions of the whole page: what Setu drew before
        with mock.patch.object(sources, "_scan_rect", lambda pg, raster: None), \
                fitz.open(self.pdf) as doc:
            self.assertIn(check_mapping.check_page(doc, self.page)["verdict"], ("offset", "shape"))


@unittest.skipIf(fitz is None, "PyMuPDF is not installed")
class TestPageArea(unittest.TestCase):
    """The part of the PDF page drawn is the part the parser measured on."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="setu-map-"))

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def cut_and_read(self, pdf: Path, page: dict, area: str) -> float:
        """Share of the parser's boxes whose own line is read back from the
        region of the PDF that sources._render cuts for them."""
        hits = 0
        with fitz.open(pdf) as doc:
            pg = doc[0]
            if area == "media":
                pg.set_cropbox(pg.mediabox)
            r = pg.rect
            for b in page["blocks"]:
                x0, y0, x1, y1 = b["bbox_xyxy"]
                box = fitz.Rect(x0 / page["width"] * r.width, y0 / page["height"] * r.height,
                                x1 / page["width"] * r.width, y1 / page["height"] * r.height)
                # back to unrotated page space, where get_textbox reads
                box = box * ~pg.rotation_matrix
                got = pg.get_textbox(box.normalize())
                hits += b["text"].split()[0] in got
        return hits / max(len(page["blocks"]), 1)

    def check(self, name: str, crop=None, rotate=0, area="crop"):
        pdf = self.dir / f"{name}.pdf"
        make_pdf(pdf, crop=crop, rotate=rotate)
        page = parser_page(pdf, area=area)
        with fitz.open(pdf) as doc:
            chosen, err = sources.page_area(doc[0], (page["width"], page["height"]))
        self.assertEqual(chosen, area, name)
        self.assertLess(err, sources.FIT_TOLERANCE, name)
        self.assertGreater(self.cut_and_read(pdf, page, chosen), 0.95, name)
        # and the page image Setu renders has the parser's shape
        png, w, h = sources._render(pdf, 0, (0, 0, 1, 1), 72, chosen)
        self.assertAlmostEqual(w / h, page["width"] / page["height"], delta=0.02)

    def test_a_plain_page(self):
        self.check("plain")

    def test_a_cropped_page_the_parser_saw_cropped(self):
        self.check("crop_crop", crop=(40, 50, 555, 800))

    def test_a_cropped_page_the_parser_saw_whole(self):
        """pdftoppm draws the MediaBox: drawing the CropBox under those boxes
        is what leaves them over white paper."""
        self.check("crop_media", crop=(40, 50, 555, 800), area="media")

    def test_rotated_pages(self):
        for rot in (90, 180, 270):
            with self.subTest(rot=rot):
                self.check(f"rot{rot}", rotate=rot)

    def test_rotated_and_cropped_seen_whole(self):
        self.check("both", crop=(40, 50, 555, 800), rotate=270, area="media")

    def test_an_unknown_raster_draws_the_cropbox_as_before(self):
        pdf = self.dir / "x.pdf"
        make_pdf(pdf, crop=(40, 50, 555, 800))
        with fitz.open(pdf) as doc:
            self.assertEqual(sources.page_area(doc[0], None), ("crop", None))

    def test_a_page_of_another_shape_is_reported(self):
        pdf = self.dir / "tall.pdf"
        make_pdf(pdf)
        page = parser_page(pdf, stretch=(1.0, 1.06))
        with fitz.open(pdf) as doc:
            _, err = sources.page_area(doc[0], (page["width"], page["height"]))
        self.assertGreater(err, sources.FIT_TOLERANCE)


@unittest.skipIf(fitz is None, "PyMuPDF is not installed")
class TestFindingThePdf(unittest.TestCase):
    """A book's own PDF, or none — never another language's."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="setu-find-"))
        self._old = config.DATA_DIR
        config.DATA_DIR = self.dir
        for rel in ("dataset/input/eng/10/1001.pdf", "dataset/input/hin/10/1001.pdf",
                    "Boardwise/CLASS-10/MH_EN_10_1.pdf"):
            f = self.dir / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(b"%PDF-1.4\n%placeholder\n")

    def tearDown(self):
        config.DATA_DIR = self._old
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_by_its_own_path(self):
        got = sources._find_pdf("dataset/input/hin/10/1001.pdf")
        self.assertEqual(got.relative_to(self.dir).as_posix(), "dataset/input/hin/10/1001.pdf")

    def test_moved_folders_still_find_the_right_language(self):
        """The corpus re-rooted: the relpath's prefix no longer exists, but its
        language folder decides between the two files of that name."""
        got = sources._find_pdf("old/root/dataset/input/eng/10/1001.pdf")
        self.assertEqual(got.relative_to(self.dir).as_posix(), "dataset/input/eng/10/1001.pdf")

    def test_a_name_that_fits_two_files_equally_finds_none(self):
        self.assertIsNone(sources._find_pdf("elsewhere/1001.pdf"))

    def test_a_unique_name_is_found_anywhere(self):
        got = sources._find_pdf("CLASS-10/MH_EN_10_1.pdf")
        self.assertEqual(got.name, "MH_EN_10_1.pdf")

    def test_paths_that_leave_the_folder_find_nothing(self):
        for rel in ("../outside.pdf", "dataset/../../x.pdf", "", None):
            with self.subTest(rel=rel):
                self.assertIsNone(sources._find_pdf(rel))


@unittest.skipIf(fitz is None, "PyMuPDF is not installed")
class TestTheAudit(unittest.TestCase):
    """check_mapping's verdicts on pages whose truth is known."""

    @classmethod
    def setUpClass(cls):
        import check_mapping
        cls.cm = check_mapping
        cls.dir = Path(tempfile.mkdtemp(prefix="setu-audit-"))
        cls.plain = cls.dir / "plain.pdf"
        make_pdf(cls.plain)
        cls.cropped = cls.dir / "cropped.pdf"
        make_pdf(cls.cropped, crop=(40, 50, 555, 800))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dir, ignore_errors=True)

    def verdict(self, pdf, **kw):
        page = parser_page(pdf, **kw)
        with fitz.open(pdf) as doc:
            return self.cm.check_page(doc, page)["verdict"]

    def test_correct_pages_pass(self):
        self.assertEqual(self.verdict(self.plain), "ok")
        self.assertEqual(self.verdict(self.plain, dpi=150), "ok")
        self.assertEqual(self.verdict(self.cropped), "ok")
        self.assertEqual(self.verdict(self.cropped, area="media"), "ok")

    def test_shifted_boxes_are_caught(self):
        for shift in ((0, 0.01), (0, -0.02), (0.03, 0), (-0.03, 0)):
            with self.subTest(shift=shift):
                self.assertEqual(self.verdict(self.plain, shift=shift), "offset")

    def test_a_page_of_another_shape_is_caught(self):
        self.assertEqual(self.verdict(self.plain, stretch=(1.0, 1.05)), "shape")


if __name__ == "__main__":
    unittest.main()
