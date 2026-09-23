#!/usr/bin/env python3
"""Tests for the Setu annotation subsystem.

Run with no arguments. Everything happens in a temporary database built from a
small synthetic corpus, so the suite takes seconds and needs no textbooks::

    python3 test_annotation.py
    python3 test_annotation.py -v

Two tests are different:

* ``test_alignment_accuracy_on_real_corpus`` measures the aligner against the
  page-parallel Maharashtra editions, where the right answer is known to be on
  the same page. It skips itself when the corpus is not present, because a
  number nobody can reproduce is worse than no number.
* ``test_legacy_tables_untouched`` hashes every pre-existing table before and
  after a full workload. It is the one test that, if it fails, means stop.

The suite is order-independent and re-runnable: each test gets its own
database.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

_TMP = Path(tempfile.mkdtemp(prefix="setu-test-"))
os.environ["TULANA_STATE_DIR"] = str(_TMP / "state")
os.environ.setdefault("TULANA_DATA_DIR", str(_TMP / "data"))
(_TMP / "state").mkdir(parents=True, exist_ok=True)
(_TMP / "data").mkdir(parents=True, exist_ok=True)

import config                                    # noqa: E402
import db as legacy_db                           # noqa: E402
from annotation.core import (                     # noqa: E402
    align, annotate, corpus, exporters, ids, search, sources, store, workspace)
from annotation.core.models import (              # noqa: E402
    DONE_STATUSES, STATUSES, STATUS_BY_KEY, fold_digits, has_math, item_number,
    kind_for, math_fingerprints, normalise, structural_numbers, valid_status,
)
from annotation.core.store import Conflict, Invalid, NotFound  # noqa: E402
from annotation.ui import session as uisession    # noqa: E402

LEGACY_TABLES = ("documents", "projects", "clips", "pairs", "labels",
                 "pair_labels", "exports", "audit")


# ── a small synthetic corpus ───────────────────────────────────────────────

def _parsed_book(book: str, relpath: str, blocks_per_page, lang_text):
    """Build one parsed-layout book directly in pl_* form."""
    pages = []
    for pi, specs in enumerate(blocks_per_page):
        blocks = []
        for order, (label, btype, text) in enumerate(specs):
            blocks.append({"order": order, "label": label, "type": btype,
                           "bbox_xyxy": [10 + order * 5, 20 + order * 30,
                                         500, 60 + order * 30],
                           "conf": 0.9, "text": lang_text(text)})
        pages.append({"image": f"{book}_p{pi:04d}.png", "width": 1000,
                      "height": 1400, "page": pi, "blocks": blocks})
    return {"book": book, "relpath": relpath, "num_pages": len(pages), "pages": pages}


EN_PAGES = [
    [("Chapter-title", "Title", "Sets 1"),
     ("Section-title", "SectionHeader", "1.1 Introduction"),
     ("Paragraph", "Text", "A set is a collection of objects."),
     ("Equation", "Equation", r"$A = \{1, 3, 5, 7, 9\}$"),
     ("Header", "PageHeader", "")],
    [("Section-title", "SectionHeader", "Practice set 1.2"),
     ("Solved-example", "Text", r"Ex (1) $B = \{2, 4, 6, 8, 10\}$ is finite."),
     ("Question", "Text", "Write the following sets."),
     ("Table", "Table", "<table><tr><td>Name</td></tr></table>")],
]

# Deliberately not a perfect mirror of EN_PAGES: the Marathi edition carries an
# extra paragraph that the English one does not. Real editions do this
# constantly, and a synthetic corpus that aligns perfectly would never exercise
# the one-sided-row path that most of the interesting behaviour lives on.
MR_PAGES = [
    [("Chapter-title", "Title", "संच 1"),
     ("Section-title", "SectionHeader", "1.1 प्रस्तावना"),
     ("Paragraph", "Text", "संच म्हणजे वस्तूंचा संग्रह."),
     ("Paragraph", "Text", "ही संकल्पना मागील इयत्तेत पाहिली आहे."),
     ("Equation", "Equation", r"$A = \{1, 3, 5, 7, 9\}$"),
     ("Header", "PageHeader", "")],
    [("Section-title", "SectionHeader", "सरावसंच 1.2"),
     ("Solved-example", "Text", r"उदा (1) $B = \{2, 4, 6, 8, 10\}$ सांत आहे."),
     ("Question", "Text", "पुढील संच लिहा."),
     ("Table", "Table", "<table><tr><td>नाव</td></tr></table>")],
]


def seed_corpus(con) -> tuple[str, str]:
    """Insert two parallel books into pl_* and build Setu's source layer."""
    import blocks as blocks_mod
    blocks_mod.ensure_schema(con)

    def insert(doc, meta):
        cur = con.execute(
            "INSERT INTO pl_books(book, relpath, source_json, num_pages, n_blocks,"
            " board, class, subject, language, script, volume, title, pdf_present,"
            " imported_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (doc["book"], doc["relpath"], "", doc["num_pages"],
             sum(len(p["blocks"]) for p in doc["pages"]), meta["board"], meta["class"],
             meta["subject"], meta["language"], meta["script"], "", doc["book"], 0,
             time.time()))
        bid = cur.lastrowid
        for pg in doc["pages"]:
            pc = con.execute(
                "INSERT INTO pl_pages(book_id, page, width, height, image, n_blocks)"
                " VALUES(?,?,?,?,?,?)",
                (bid, pg["page"], pg["width"], pg["height"], pg["image"],
                 len(pg["blocks"]))).lastrowid
            for b in pg["blocks"]:
                x0, y0, x1, y1 = b["bbox_xyxy"]
                con.execute(
                    "INSERT INTO pl_blocks(page_id, ord, label, type, x0, y0, x1, y1,"
                    " fx0, fy0, fx1, fy1, conf, text) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (pc, b["order"], b["label"], b["type"], x0, y0, x1, y1,
                     x0 / pg["width"], y0 / pg["height"], x1 / pg["width"],
                     y1 / pg["height"], b["conf"], b["text"]))
        return bid

    insert(_parsed_book("TT_EN_9", "TEST/TT_EN_9.pdf", EN_PAGES, lambda t: t),
           {"board": "MH", "class": 9, "subject": "Mathematics",
            "language": "English", "script": "Latin"})
    insert(_parsed_book("TT_MR_9", "TEST/TT_MR_9.pdf", MR_PAGES, lambda t: t),
           {"board": "MH", "class": 9, "subject": "Mathematics",
            "language": "Marathi", "script": "Devanagari"})
    con.commit()

    corpus.build(con, rebuild=True, log_fn=lambda *a: None)
    repo = corpus.CorpusRepo(con)
    en = repo.books(board="MH", language="English")[0]["book_key"]
    mr = repo.books(board="MH", language="Marathi")[0]["book_key"]
    return en, mr


class SetuCase(unittest.TestCase):
    """A fresh database per test, so order never matters."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="setu-case-", dir=_TMP))
        self.dbpath = self.dir / "studio.db"
        self._old_db = config.DB_PATH
        self._old_exports = config.EXPORT_DIR
        config.DB_PATH = self.dbpath
        config.EXPORT_DIR = self.dir / "exports"
        config.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        store._schema_ready.clear()
        store.FTS_AVAILABLE = None
        with legacy_db.tx() as con:                # create the legacy schema too
            pass
        self.con = store.connect()
        self.en, self.mr = seed_corpus(self.con)

    def tearDown(self):
        try:
            self.con.close()
        except Exception:
            pass
        config.DB_PATH = self._old_db
        config.EXPORT_DIR = self._old_exports
        store._schema_ready.clear()
        shutil.rmtree(self.dir, ignore_errors=True)

    def project(self, **kw):
        return workspace.create_project(self.con, src_book=self.en,
                                        tgt_book=self.mr, annotator="tester", **kw)


# ── identifiers ────────────────────────────────────────────────────────────

class TestIds(unittest.TestCase):

    def test_deterministic(self):
        a = ids.derive("sg", "book", 1, 2)
        b = ids.derive("sg", "book", 1, 2)
        self.assertEqual(a, b)
        self.assertNotEqual(a, ids.derive("sg", "book", 1, 3))

    def test_never_derived_from_text(self):
        """The property the whole design rests on."""
        bk = ids.book_key("X/Y.pdf")
        before = ids.segment_id(bk, 3, 5, 5)
        after = ids.segment_id(bk, 3, 5, 5)
        self.assertEqual(before, after,
                         "a segment id must not depend on anything but position")

    def test_book_key_normalises_separators(self):
        self.assertEqual(ids.book_key("A/B/C.pdf"), ids.book_key("A\\B\\C.pdf"))
        self.assertEqual(ids.book_key("A/B/C.pdf"), ids.book_key("/a/b/c.PDF"))

    def test_dedup_key_groups_same_book(self):
        self.assertEqual(ids.dedup_key("MH_EN_9", 148, 1839),
                         ids.dedup_key("mh_en_9", 148, 1839))
        self.assertNotEqual(ids.dedup_key("MH_EN_9", 148, 1839),
                            ids.dedup_key("MH_EN_9", 148, 1840))

    def test_minted_ids_are_unique(self):
        seen = {ids.mint("rw") for _ in range(4000)}
        self.assertEqual(len(seen), 4000)

    def test_validation_rejects_junk(self):
        for bad in ("", None, 42, "../../etc/passwd", "sg_", "x" * 200,
                    "sg_LOWERCASE", "rw_ILOU12"):
            self.assertFalse(ids.is_id(bad), f"{bad!r} should be rejected")
        self.assertTrue(ids.is_id(ids.mint("rw"), "rw"))
        self.assertFalse(ids.is_id(ids.mint("rw"), "sg"))


# ── text handling ──────────────────────────────────────────────────────────

class TestText(unittest.TestCase):

    def test_all_unicode_breaks_become_newline(self):
        """splitlines() breaks on more than \\n; line formats must not shift."""
        raw = "a b c\rd\r\ne\x0bf\x0cg"
        out = normalise(raw)
        self.assertEqual(out, "a\nb\nc\nd\ne\nf\ng")
        self.assertEqual(len(out.splitlines()), len(out.split("\n")))

    def test_nfc(self):
        decomposed = "क्ष"          # क + ् + ष
        self.assertEqual(normalise(decomposed), normalise(normalise(decomposed)))
        import unicodedata
        self.assertEqual(normalise("é"), unicodedata.normalize("NFC", "é"))

    def test_math_is_never_altered(self):
        tex = r"$$\frac{a}{b} \times \begin{matrix}1&2\\3&4\end{matrix}$$"
        self.assertEqual(normalise(tex), tex)

    def test_tabs_and_newlines_survive(self):
        self.assertEqual(normalise("a\tb\nc"), "a\tb\nc")

    def test_control_characters_removed(self):
        self.assertEqual(normalise("a\x00b\x07c"), "abc")

    def test_math_fingerprints(self):
        fps = math_fingerprints(r"see $x^2 + 3x = 0$ and $$\frac{1}{2}$$ and $a$")
        self.assertIn("x^2+3x=0", fps)
        self.assertIn(r"\frac{1}{2}", fps)
        self.assertNotIn("a", fps)                 # too short to be evidence

    def test_fingerprints_survive_translation(self):
        en = r"So $2 \times 3 \times 5 = 30$ follows."
        mr = r"म्हणून $2 \times 3 \times 5 = 30$ मिळते."
        self.assertTrue(set(math_fingerprints(en)) & set(math_fingerprints(mr)))

    def test_native_digits_fold(self):
        self.assertEqual(fold_digits("सराव १.२"), "सराव 1.2")
        self.assertEqual(fold_digits("పాఠం ౩"), "పాఠం 3")
        self.assertEqual(structural_numbers("सरावसंच १.२"), ["1.2"])

    def test_structural_numbers(self):
        self.assertEqual(structural_numbers("Practice set 1.2"), ["1.2"])
        self.assertEqual(structural_numbers("Theorem 3.4.1 says"), ["3.4.1"])
        self.assertEqual(structural_numbers("no numbers here"), [])

    def test_item_number(self):
        self.assertEqual(item_number("Ex (3) prove that"), "3")
        self.assertEqual(item_number("उदा (4) सिद्ध करा"), "4")

    def test_kind_from_label_and_cues(self):
        self.assertEqual(kind_for("Chapter-title", "Sets"), "chapter")
        self.assertEqual(kind_for("Paragraph", "Theorem 1.1 states"), "theorem")
        self.assertEqual(kind_for("Paragraph", "प्रमेय 2.1"), "theorem")
        self.assertEqual(kind_for("Section-title", "Practice set 1.2"), "exercise")
        # A heading label is never demoted by a cue that is not exercise/example
        self.assertEqual(kind_for("Section-title", "Definition of a set"), "section")
        self.assertEqual(kind_for("Unknown-Label", "x"), "other")

    def test_status_validation(self):
        self.assertEqual(valid_status("EXACT"), "exact")
        with self.assertRaises(ValueError):
            valid_status("banana")
        self.assertNotIn("pending", DONE_STATUSES)


# ── the alignment engine ───────────────────────────────────────────────────

class TestAlign(unittest.TestCase):

    @staticmethod
    def seg(i, kind="paragraph", math=(), num=(), n=100, item=""):
        return {"kind": kind, "anchor_math": list(math), "anchor_num": list(num),
                "n_chars": n, "item_no": item, "page": i}

    def test_monotone_chain_removes_crossings(self):
        cands = [(0, 5, 5.0, "math"), (1, 1, 5.0, "math"), (2, 6, 5.0, "math")]
        chain = align.monotone_chain(cands, 10)
        tgts = [c[1] for c in chain]
        self.assertEqual(tgts, sorted(tgts), "the chain must not cross")
        self.assertEqual(len(chain), 2)

    def test_every_segment_reaches_a_row(self):
        src = [self.seg(i) for i in range(7)]
        tgt = [self.seg(i) for i in range(4)]
        props = align.suggest(src, tgt)
        self.assertEqual(sorted(p.src for p in props if p.src >= 0), list(range(7)))
        self.assertEqual(sorted(p.tgt for p in props if p.tgt >= 0), list(range(4)))

    def test_shared_math_anchors(self):
        src = [self.seg(0), self.seg(1, math=["x^2+1=0"]), self.seg(2)]
        tgt = [self.seg(0), self.seg(1, math=["x^2+1=0"]), self.seg(2)]
        props = align.suggest(src, tgt)
        anchored = [p for p in props if p.basis == "math"]
        self.assertEqual(len(anchored), 1)
        self.assertEqual((anchored[0].src, anchored[0].tgt), (1, 1))
        self.assertGreater(anchored[0].confidence, 0)

    def test_boilerplate_formula_is_not_an_anchor(self):
        """A formula on every page carries no information."""
        src = [self.seg(0, math=["a=b"])]
        tgt = [self.seg(i, math=["a=b"]) for i in range(align.MAX_POSTING + 5)]
        self.assertEqual(align.candidates(src, tgt), [])

    def test_empty_sides(self):
        self.assertEqual(align.suggest([], []), [])
        self.assertEqual(len(align.suggest([self.seg(0)], [])), 1)
        self.assertEqual(len(align.suggest([], [self.seg(0)])), 1)

    def test_quality_counts(self):
        q = align.quality([align.Proposal(0, 0, 9.0, "math"),
                           align.Proposal(1, -1, 0.0, "unpaired"),
                           align.Proposal(2, 1, 0.5, "fill")])
        self.assertEqual((q["rows"], q["anchored"], q["strong"], q["one_sided"]),
                         (3, 1, 1, 1))

    def test_large_input_is_fast(self):
        src = [self.seg(i, math=[f"eq{i}"]) for i in range(4000)]
        tgt = [self.seg(i, math=[f"eq{i}"]) for i in range(4000)]
        t0 = time.time()
        props = align.suggest(src, tgt)
        self.assertLess(time.time() - t0, 5.0)
        self.assertEqual(len(props), 4000)


# ── segmentation over the synthetic corpus ─────────────────────────────────

class TestCorpus(SetuCase):

    def test_books_and_segments_exist(self):
        repo = corpus.CorpusRepo(self.con)
        self.assertEqual(len(repo.books(board="MH")), 2)
        segs = repo.segments(self.en, limit=100)
        self.assertEqual(len(segs), sum(len(p) for p in EN_PAGES))

    def test_source_text_matches_the_parser(self):
        segs = corpus.CorpusRepo(self.con).segments(self.en, limit=100)
        texts = [s["source_text"] for s in segs if s["source_text"]]
        self.assertIn("A set is a collection of objects.", texts)

    def test_hierarchy_is_carried_down(self):
        segs = corpus.CorpusRepo(self.con).segments(self.en, limit=100)
        para = next(s for s in segs if s["source_text"].startswith("A set is"))
        self.assertEqual(para["chapter"], "Sets 1")
        self.assertEqual(para["chapter_no"], "1")
        self.assertEqual(para["section_no"], "1.1")

    def test_exercise_heading_keeps_its_number(self):
        segs = corpus.CorpusRepo(self.con).segments(self.en, limit=100)
        ex = next(s for s in segs if s["source_text"] == "Practice set 1.2")
        self.assertEqual(ex["kind"], "exercise")
        self.assertEqual(ex["section_no"], "1.2")

    def test_math_and_table_flags(self):
        segs = corpus.CorpusRepo(self.con).segments(self.en, limit=100)
        self.assertTrue(any(s["has_math"] for s in segs))
        self.assertTrue(any(s["has_table"] for s in segs))

    def test_build_is_idempotent(self):
        before = corpus.CorpusRepo(self.con).counts()
        corpus.build(self.con, log_fn=lambda *a: None)
        corpus.build(self.con, rebuild=True, log_fn=lambda *a: None)
        self.assertEqual(corpus.CorpusRepo(self.con).counts(), before)

    def test_rebuild_keeps_segment_ids(self):
        sids = {s["sid"] for s in corpus.CorpusRepo(self.con).segments(self.en, limit=999)}
        corpus.build(self.con, rebuild=True, log_fn=lambda *a: None)
        again = {s["sid"] for s in corpus.CorpusRepo(self.con).segments(self.en, limit=999)}
        self.assertEqual(sids, again,
                         "a rebuild of unchanged data must not move identifiers")

    def test_duplicate_parse_is_collapsed(self):
        """The real corpus ships 31 books twice; both must not reach a dropdown."""
        dup = _parsed_book("TT_EN_9", "OTHER/TT_EN_9.pdf", EN_PAGES, lambda t: t)
        n_blocks = sum(len(p["blocks"]) for p in dup["pages"])
        self.con.execute(
            "INSERT INTO pl_books(book, relpath, source_json, num_pages, n_blocks,"
            " board, class, subject, language, script, volume, title, pdf_present,"
            " imported_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("TT_EN_9", "OTHER/TT_EN_9.pdf", "", 2, n_blocks, "MH", 9,
             "Mathematics", "English", "Latin", "", "TT_EN_9", 0, time.time()))
        self.con.commit()
        corpus.build(self.con, log_fn=lambda *a: None)
        english = corpus.CorpusRepo(self.con).books(board="MH", language="English")
        self.assertEqual(len(english), 1, "the duplicate parse must not appear twice")
        self.assertEqual(len(corpus.CorpusRepo(self.con).aliases(english[0]["book_key"])), 1)

    def test_cascade_offers_no_impossible_combinations(self):
        repo = corpus.CorpusRepo(self.con)
        for b in repo.boards():
            for c in repo.classes(b["code"]):
                for s in repo.subjects(b["code"], c["value"]):
                    langs = repo.languages(b["code"], c["value"], s["value"])
                    for lg in langs:
                        found = repo.books(board=b["code"], cls=c["value"],
                                           subject=s["value"], language=lg["value"])
                        self.assertTrue(found, "the cascade offered an empty combination")

    def test_unknown_book_raises(self):
        with self.assertRaises(NotFound):
            corpus.CorpusRepo(self.con).book("bk_NOSUCHTHING")


# ── projects and navigation ────────────────────────────────────────────────

class TestWorkspace(SetuCase):

    def test_create_and_rows(self):
        proj = self.project()
        self.assertGreater(proj["n_rows"], 0)
        page = workspace.WorkspaceRepo(self.con).rows(proj["pid"], limit=100)
        self.assertEqual(page["total"], proj["n_rows"])
        self.assertTrue(all(r["src"]["present"] or r["tgt"]["present"]
                            for r in page["rows"]))

    def test_same_book_both_sides_refused(self):
        with self.assertRaises(Invalid):
            workspace.create_project(self.con, src_book=self.en, tgt_book=self.en)

    def test_creating_twice_returns_the_same_project(self):
        a = self.project()
        b = self.project()
        self.assertEqual(a["pid"], b["pid"])

    def test_noise_is_excluded_by_default(self):
        proj = self.project()
        rows = workspace.WorkspaceRepo(self.con).rows(proj["pid"], limit=200)["rows"]
        self.assertNotIn("header", {r["kind"] for r in rows})

    def test_navigation_follows_the_source_book(self):
        """Both sides share one table of contents, not two."""
        proj = self.project()
        chapters = workspace.WorkspaceRepo(self.con).chapters(proj["pid"])
        titles = {c["chapter"] for c in chapters}
        self.assertIn("Sets 1", titles)
        self.assertNotIn("संच 1", titles,
                         "the target book's chapter titles must not split the sidebar")

    def test_progress_counts(self):
        proj = self.project()
        repo = workspace.WorkspaceRepo(self.con)
        p0 = repo.progress(proj["pid"])
        self.assertEqual(p0["done"], 0)
        rid = repo.rows(proj["pid"], limit=1)["rows"][0]["rid"]
        annotate.set_status(self.con, rid, "exact", annotator="t")
        self.assertEqual(repo.progress(proj["pid"])["done"], 1)

    def test_rebuild_refuses_to_discard_work(self):
        proj = self.project()
        repo = workspace.WorkspaceRepo(self.con)
        rid = repo.rows(proj["pid"], limit=1)["rows"][0]["rid"]
        annotate.set_status(self.con, rid, "exact", annotator="t")
        with self.assertRaises(Invalid):
            workspace.build_rows(self.con, proj["pid"])
        workspace.build_rows(self.con, proj["pid"], force=True)   # explicit is fine

    def test_neighbour_navigation(self):
        proj = self.project()
        repo = workspace.WorkspaceRepo(self.con)
        nxt = repo.neighbour(proj["pid"], 0, 1)
        self.assertEqual(nxt["seq"], 1)
        self.assertIsNone(repo.neighbour(proj["pid"], 0, -1))

    def test_unknown_project_is_not_an_empty_list(self):
        with self.assertRaises(NotFound):
            workspace.WorkspaceRepo(self.con).rows("pj_NOSUCH")

    def test_soft_lock_is_advisory(self):
        proj = self.project()
        repo = workspace.WorkspaceRepo(self.con)
        rid = repo.rows(proj["pid"], limit=1)["rows"][0]["rid"]
        self.assertFalse(repo.claim(rid, "s1", "amita")["held"])
        held = repo.claim(rid, "s2", "bharat")
        self.assertTrue(held["held"])
        self.assertEqual(held["by"], "amita")
        # ... and it does not actually prevent the write
        annotate.set_status(self.con, rid, "exact", annotator="bharat")
        repo.release(rid, "s1")
        self.assertFalse(repo.claim(rid, "s2", "bharat")["held"])


# ── editing, autosave, history ─────────────────────────────────────────────

class TestAnnotate(SetuCase):

    def setUp(self):
        super().setUp()
        self.proj = self.project()
        self.repo = workspace.WorkspaceRepo(self.con)
        rows = self.repo.rows(self.proj["pid"], limit=100)["rows"]
        self.row = next(r for r in rows if r["src"]["present"] and r["tgt"]["present"])
        self.rid = self.row["rid"]

    def test_save_creates_a_revision(self):
        r = annotate.save_text(self.con, self.rid, "src", "new text", base_rev=0,
                               annotator="amita")
        self.assertTrue(r["changed"])
        self.assertEqual(r["rev"], 1)
        hist = annotate.AnnotateRepo(self.con).history(self.rid, "src")
        self.assertEqual(len(hist), 1)

    def test_unchanged_save_is_free(self):
        annotate.save_text(self.con, self.rid, "src", "one", base_rev=0, annotator="a")
        again = annotate.save_text(self.con, self.rid, "src", "one", base_rev=1,
                                   annotator="a")
        self.assertFalse(again["changed"])
        self.assertEqual(again["rev"], 1)
        self.assertEqual(len(annotate.AnnotateRepo(self.con).history(self.rid, "src")), 1)

    def test_stale_write_is_refused(self):
        annotate.save_text(self.con, self.rid, "src", "first", base_rev=0, annotator="a")
        with self.assertRaises(Conflict) as cm:
            annotate.save_text(self.con, self.rid, "src", "second", base_rev=0,
                               annotator="b")
        self.assertEqual(cm.exception.current, "first")
        self.assertEqual(cm.exception.attempted, "second")
        self.assertEqual(cm.exception.rev, 1)

    def test_missing_base_rev_refused_once_edited(self):
        annotate.save_text(self.con, self.rid, "src", "first", base_rev=0, annotator="a")
        with self.assertRaises(Conflict):
            annotate.save_text(self.con, self.rid, "src", "blind", annotator="b")

    def test_original_is_never_overwritten(self):
        original = self.row["src"]["source"]
        for i in range(6):
            annotate.save_text(self.con, self.rid, "src", f"version {i}", base_rev=i,
                               annotator="a")
        fresh = self.repo.row(self.rid)
        self.assertEqual(fresh["src"]["source"], original)
        self.assertEqual(fresh["src"]["text"], "version 5")

    def test_restore_original(self):
        original = self.row["src"]["source"]
        annotate.save_text(self.con, self.rid, "src", "mangled", base_rev=0, annotator="a")
        annotate.restore(self.con, self.rid, "src", rev=0, annotator="a")
        self.assertEqual(self.repo.row(self.rid)["src"]["text"], original)

    def test_restore_a_specific_revision(self):
        annotate.save_text(self.con, self.rid, "src", "alpha", base_rev=0, annotator="a")
        annotate.save_text(self.con, self.rid, "src", "beta", base_rev=1, annotator="a")
        annotate.restore(self.con, self.rid, "src", rev=1, annotator="a")
        self.assertEqual(self.repo.row(self.rid)["src"]["text"], "alpha")

    def test_history_survives_everything(self):
        for i in range(4):
            annotate.save_text(self.con, self.rid, "src", f"v{i}", base_rev=i, annotator="a")
        annotate.restore(self.con, self.rid, "src", rev=0, annotator="a")
        hist = annotate.AnnotateRepo(self.con).history(self.rid, "src")
        self.assertEqual(len(hist), 5)
        self.assertEqual(hist[0]["reason"], "restore-original")

    def test_diff_against_original(self):
        annotate.save_text(self.con, self.rid, "src", "completely different",
                           base_rev=0, annotator="a")
        d = annotate.diff(self.con, self.rid, "src", a=0, b="current")
        self.assertFalse(d["identical"])
        self.assertTrue(d["diff"])
        self.assertTrue(annotate.diff(self.con, self.rid, "tgt")["identical"])

    def test_status_history(self):
        annotate.set_status(self.con, self.rid, "exact", annotator="a")
        annotate.set_status(self.con, self.rid, "unclear", note="cannot read",
                            annotator="b")
        hist = annotate.AnnotateRepo(self.con).status_history(self.rid)
        self.assertEqual([h["status"] for h in hist], ["unclear", "exact"])
        self.assertEqual(hist[0]["note"], "cannot read")

    def test_save_many_is_atomic_in_shape(self):
        out = annotate.save_many(self.con, self.rid, src="L", tgt="R",
                                 src_rev=0, tgt_rev=0, status="needs_correction",
                                 annotator="a")
        self.assertEqual(set(out["saved"]), {"src", "tgt", "status"})
        self.assertEqual(out["row"]["src"]["text"], "L")
        self.assertEqual(out["row"]["tgt"]["text"], "R")
        self.assertEqual(out["row"]["status"], "needs_correction")

    def test_edited_flag_clears_when_text_returns(self):
        annotate.save_text(self.con, self.rid, "src", "x", base_rev=0, annotator="a")
        self.assertTrue(self.repo.row(self.rid)["edited"])
        annotate.restore(self.con, self.rid, "src", rev=0, annotator="a")
        self.assertFalse(self.repo.row(self.rid)["edited"])

    def test_cannot_edit_an_absent_side(self):
        rows = self.repo.rows(self.proj["pid"], limit=200)["rows"]
        one_sided = [r for r in rows if not (r["src"]["present"] and r["tgt"]["present"])]
        if not one_sided:
            self.skipTest("this corpus produced no one-sided rows")
        side = "src" if not one_sided[0]["src"]["present"] else "tgt"
        with self.assertRaises(Invalid):
            annotate.save_text(self.con, one_sided[0]["rid"], side, "x", base_rev=0)

    def test_oversized_text_refused(self):
        with self.assertRaises(Invalid):
            annotate.save_text(self.con, self.rid, "src", "x" * (annotate.MAX_TEXT + 1),
                               base_rev=0)

    def test_attach_and_detach(self):
        segs = corpus.CorpusRepo(self.con).segments(self.mr, limit=100)
        free = None
        for s in segs:
            used = self.repo.one("SELECT rid FROM setu_row WHERE pid=? AND tgt_sid=?",
                                 (self.proj["pid"], s["sid"]))
            if not used:
                free = s
                break
        if free is None:
            self.skipTest("every target segment is already attached")
        out = annotate.attach(self.con, self.rid, "tgt", free["sid"], annotator="a")
        self.assertEqual(out["tgt"]["sid"], free["sid"])
        self.assertEqual(out["origin"], "manual")
        out = annotate.attach(self.con, self.rid, "tgt", None, annotator="a")
        self.assertFalse(out["tgt"]["present"])

    def test_attach_refuses_a_segment_already_in_use(self):
        rows = self.repo.rows(self.proj["pid"], limit=200)["rows"]
        taken = next(r for r in rows if r["tgt"]["present"] and r["rid"] != self.rid)
        with self.assertRaises(Invalid):
            annotate.attach(self.con, self.rid, "tgt", taken["tgt"]["sid"])

    def test_split_produces_two_one_sided_rows(self):
        out = annotate.split_row(self.con, self.rid, annotator="a")
        self.assertTrue(out["row"]["src"]["present"])
        self.assertFalse(out["row"]["tgt"]["present"])
        self.assertTrue(out["new_row"]["tgt"]["present"])
        self.assertFalse(out["new_row"]["src"]["present"])
        self.assertEqual(out["new_row"]["seq"], out["row"]["seq"] + 1)

    def test_split_then_merge_round_trips(self):
        before = self.repo.row(self.rid)
        out = annotate.split_row(self.con, self.rid, annotator="a")
        merged = annotate.merge_rows(self.con, self.rid, out["new_row"]["rid"],
                                     annotator="a")
        self.assertEqual(merged["row"]["tgt"]["sid"], before["tgt"]["sid"])

    def test_sequence_stays_dense_after_a_split(self):
        annotate.split_row(self.con, self.rid, annotator="a")
        seqs = [r["seq"] for r in self.repo.rows(self.proj["pid"], limit=500)["rows"]]
        self.assertEqual(seqs, list(range(len(seqs))))


# ── concurrency ────────────────────────────────────────────────────────────

class TestConcurrency(SetuCase):

    def test_parallel_writers_all_succeed(self):
        """Eight threads, each saving its own row, with FULL durability."""
        proj = self.project()
        repo = workspace.WorkspaceRepo(self.con)
        rows = [r for r in repo.rows(proj["pid"], limit=40)["rows"]
                if r["src"]["present"]][:8]
        if len(rows) < 4:
            self.skipTest("not enough rows in the synthetic corpus")

        errors: list[Exception] = []
        done = threading.Barrier(len(rows))

        def work(row):
            try:
                done.wait(timeout=10)
                for i in range(5):
                    with store.tx() as con:
                        annotate.save_text(con, row["rid"], "src", f"t{i}",
                                           base_rev=i, annotator="w",
                                           session=f"s{row['seq']}")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=work, args=(r,)) for r in rows]
        [t.start() for t in threads]
        [t.join(timeout=60) for t in threads]
        self.assertEqual(errors, [], f"concurrent writers failed: {errors[:3]}")
        for r in rows:
            self.assertEqual(repo.row(r["rid"])["src"]["text"], "t4")

    def test_two_writers_one_row_one_wins(self):
        """The loser is told, not silently discarded."""
        proj = self.project()
        repo = workspace.WorkspaceRepo(self.con)
        rid = next(r["rid"] for r in repo.rows(proj["pid"], limit=40)["rows"]
                   if r["src"]["present"])
        results: list[str] = []
        start = threading.Barrier(2)

        def work(name):
            try:
                start.wait(timeout=10)
                with store.tx() as con:
                    annotate.save_text(con, rid, "src", f"by {name}", base_rev=0,
                                       annotator=name)
                results.append(f"{name}:ok")
            except Conflict:
                results.append(f"{name}:conflict")
            except Exception as exc:              # pragma: no cover - diagnostic
                results.append(f"{name}:{type(exc).__name__}")

        threads = [threading.Thread(target=work, args=(n,)) for n in ("amita", "bharat")]
        [t.start() for t in threads]
        [t.join(timeout=30) for t in threads]
        oks = [r for r in results if r.endswith(":ok")]
        self.assertEqual(len(oks), 1, f"expected exactly one winner, got {results}")
        self.assertEqual(len(annotate.AnnotateRepo(self.con).history(rid, "src")), 1)

    def test_durability_pragmas_are_in_force(self):
        self.assertEqual(self.con.execute("PRAGMA journal_mode").fetchone()[0], "wal")
        self.assertEqual(int(self.con.execute("PRAGMA synchronous").fetchone()[0]), 2)
        self.assertGreaterEqual(
            int(self.con.execute("PRAGMA busy_timeout").fetchone()[0]), 5000)

    def test_work_survives_reopening_the_database(self):
        proj = self.project()
        rid = workspace.WorkspaceRepo(self.con).rows(proj["pid"], limit=1)["rows"][0]["rid"]
        with store.tx() as con:
            annotate.save_text(con, rid, "src", "persisted", base_rev=0, annotator="a")
            annotate.set_status(con, rid, "exact", annotator="a")
        self.con.close()
        self.con = store.connect()
        row = workspace.WorkspaceRepo(self.con).row(rid)
        self.assertEqual(row["src"]["text"], "persisted")
        self.assertEqual(row["status"], "exact")


# ── search ─────────────────────────────────────────────────────────────────

class TestSearch(SetuCase):

    def setUp(self):
        super().setUp()
        self.proj = self.project()
        self.pid = self.proj["pid"]
        self.repo = search.SearchRepo(self.con)

    def test_word_search(self):
        r = self.repo.find(self.pid, "collection")
        self.assertGreater(r["total"], 0)

    def test_search_in_indic_script(self):
        r = self.repo.find(self.pid, "संग्रह")
        self.assertGreater(r["total"], 0)

    def test_search_finds_edited_text(self):
        rid = workspace.WorkspaceRepo(self.con).rows(self.pid, limit=1)["rows"][0]["rid"]
        annotate.save_text(self.con, rid, "src", "zqxjkvw unique marker",
                           base_rev=0, annotator="a")
        r = self.repo.find(self.pid, "zqxjkvw")
        self.assertEqual(r["total"], 1)

    def test_page_and_row_queries(self):
        self.assertEqual(self.repo.find(self.pid, "page 1")["mode"], "page")
        self.assertEqual(self.repo.find(self.pid, "#0")["mode"], "row")
        self.assertEqual(self.repo.find(self.pid, "chapter 1")["mode"], "location")

    def test_like_wildcards_are_escaped(self):
        """Searching for % must not match everything."""
        store.FTS_AVAILABLE = False
        try:
            everything = self.repo.find(self.pid, "e", limit=200)["total"]
            percent = self.repo.find(self.pid, "%", limit=200)["total"]
            self.assertLess(percent, everything)
            self.assertLess(self.repo.find(self.pid, "_", limit=200)["total"], everything)
        finally:
            store.FTS_AVAILABLE = None

    def test_fts_syntax_cannot_crash_the_search(self):
        for q in ['"', "AND", "NEAR(", "a OR", "*", "()", "^", "col:val", '""""']:
            r = self.repo.find(self.pid, q)
            self.assertIn("total", r, f"query {q!r} broke search")

    def test_empty_query(self):
        self.assertEqual(self.repo.find(self.pid, "")["mode"], "empty")

    def test_unknown_project(self):
        with self.assertRaises(NotFound):
            self.repo.find("pj_NOSUCH", "x")


# ── exports ────────────────────────────────────────────────────────────────

class TestExport(SetuCase):

    def setUp(self):
        super().setUp()
        self.proj = self.project()
        self.pid = self.proj["pid"]
        repo = workspace.WorkspaceRepo(self.con)
        for r in repo.rows(self.pid, limit=4)["rows"]:
            annotate.set_status(self.con, r["rid"], "exact", annotator="a")

    def test_every_available_format_writes_a_file(self):
        for key, fmt in exporters.REGISTRY.items():
            if not fmt.available:
                continue
            with self.subTest(fmt=key):
                out = exporters.export(self.con, self.pid, key, annotator="a")
                self.assertTrue(Path(out["path"]).is_file())
                self.assertGreater(out["bytes"], 0)
                self.assertGreaterEqual(out["rows_written"], 0)

    def test_jsonl_is_valid_and_carries_the_original(self):
        out = exporters.export(self.con, self.pid, "jsonl")
        lines = Path(out["path"]).read_text(encoding="utf-8").strip().split("\n")
        self.assertEqual(len(lines), out["rows_written"])
        rec = json.loads(lines[0])
        for field in ("source_text", "target_text", "source_original",
                      "target_original", "status", "row_id"):
            self.assertIn(field, rec)

    def test_moses_files_are_line_aligned(self):
        import zipfile
        out = exporters.export(self.con, self.pid, "moses")
        with zipfile.ZipFile(out["path"]) as z:
            names = [n for n in z.namelist() if n.startswith("corpus.")]
            self.assertEqual(len(names), 2)
            a = z.read(names[0]).decode().split("\n")
            b = z.read(names[1]).decode().split("\n")
        self.assertEqual(len(a), len(b), "Moses files must have the same line count")
        self.assertEqual(len([x for x in a if x]), out["rows_written"])

    def test_moses_survives_embedded_line_separators(self):
        """A U+2028 in one side would shift every later pair."""
        rid = workspace.WorkspaceRepo(self.con).rows(self.pid, limit=1)["rows"][0]["rid"]
        annotate.save_text(self.con, rid, "src", "a b c\rd", base_rev=0,
                           annotator="a")
        import zipfile
        out = exporters.export(self.con, self.pid, "moses")
        with zipfile.ZipFile(out["path"]) as z:
            names = [n for n in z.namelist() if n.startswith("corpus.")]
            a = z.read(names[0]).decode().split("\n")
            b = z.read(names[1]).decode().split("\n")
        self.assertEqual(len(a), len(b))

    def test_pairs_only_formats_report_what_they_dropped(self):
        out = exporters.export(self.con, self.pid, "tmx")
        self.assertEqual(out["rows_excluded"],
                         out["rows_considered"] - out["rows_written"])
        self.assertTrue(out["pairs_only"])

    def test_status_filter(self):
        everything = exporters.export(self.con, self.pid, "jsonl")
        only_exact = exporters.export(self.con, self.pid, "jsonl", status="exact")
        self.assertLess(only_exact["rows_written"], everything["rows_written"])
        self.assertEqual(only_exact["rows_written"], 4)

    def test_xml_is_well_formed(self):
        import xml.etree.ElementTree as ET
        out = exporters.export(self.con, self.pid, "xml")
        tree = ET.parse(out["path"])
        self.assertEqual(len(tree.getroot().findall("pair")), out["rows_written"])

    def test_csv_round_trips_indic_text(self):
        import csv as csvmod
        out = exporters.export(self.con, self.pid, "csv")
        with open(out["path"], encoding="utf-8-sig", newline="") as fh:
            rows = list(csvmod.DictReader(fh))
        self.assertEqual(len(rows), out["rows_written"])
        self.assertTrue(any("संच" in (r["target_text"] or "") for r in rows))

    def test_bundle_names_do_not_collide(self):
        import zipfile
        out = exporters.bundle(self.con, self.pid, annotator="a")
        with zipfile.ZipFile(out["path"]) as z:
            names = z.namelist()
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(names), len([f for f in exporters.REGISTRY.values()
                                          if f.available]))

    def test_unknown_format_is_refused(self):
        with self.assertRaises(Invalid):
            exporters.export(self.con, self.pid, "definitely-not-a-format")

    def test_filenames_are_safe(self):
        for evil in ("../../etc/passwd", "a/b\\c", "\x00null", "  ", "." * 50,
                     "x" * 500, "café ☕"):
            name = exporters.safe_filename(evil, "json", suffix="jsonl_1")
            self.assertNotIn("/", name)
            self.assertNotIn("\\", name)
            self.assertNotIn("\x00", name)
            self.assertTrue(name.endswith(".json"))
            self.assertIn("jsonl_1", name,
                          "the format key must survive truncation")

    def test_export_is_recorded(self):
        exporters.export(self.con, self.pid, "jsonl", annotator="amita")
        rec = store.Repository(self.con).one(
            "SELECT * FROM setu_export ORDER BY created_at DESC LIMIT 1")
        self.assertEqual(rec["actor"], "amita")
        self.assertEqual(rec["fmt"], "jsonl")


# ── the guarantee that matters most ────────────────────────────────────────

class TestLegacyUntouched(SetuCase):

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

    def test_legacy_tables_untouched(self):
        """A full workload must not change one byte of the original tables."""
        with legacy_db.tx() as con:
            con.execute(
                "INSERT INTO documents(path, board, class, subject, language,"
                " script, volume, title, pages, checksum, added_at)"
                " VALUES('x/y.pdf','MH',9,'Mathematics','English','Latin','',"
                "'Test',10,'abc',1.0)")
            con.execute("INSERT INTO audit(ts, actor, action, target, detail)"
                        " VALUES(1.0,'someone','did','thing','{}')")

        before = self._fingerprint(self.con)
        self.assertNotEqual(before["documents"], "absent")

        # Everything Setu can do.
        proj = self.project()
        repo = workspace.WorkspaceRepo(self.con)
        rows = repo.rows(proj["pid"], limit=10)["rows"]
        rid = next(r["rid"] for r in rows if r["src"]["present"])
        annotate.save_text(self.con, rid, "src", "edited", base_rev=0, annotator="a")
        annotate.set_status(self.con, rid, "exact", annotator="a")
        annotate.restore(self.con, rid, "src", rev=0, annotator="a")
        search.SearchRepo(self.con).find(proj["pid"], "set")
        exporters.export(self.con, proj["pid"], "jsonl", annotator="a")
        corpus.build(self.con, rebuild=True, log_fn=lambda *a: None)
        workspace.build_rows(self.con, proj["pid"], force=True)
        workspace.delete_project(self.con, proj["pid"])

        after = self._fingerprint(self.con)
        self.assertEqual(before, after,
                         "Setu modified a pre-existing table — this must never happen")

    def test_no_destructive_ddl_anywhere_in_the_package(self):
        """Grep the package for the statements that could lose data."""
        import re
        forbidden = re.compile(
            r"\b(DROP\s+TABLE|DROP\s+INDEX|TRUNCATE|ALTER\s+TABLE\s+\w+\s+DROP)\b", re.I)
        offenders = []
        for path in (HERE / "annotation").rglob("*"):
            if path.suffix not in {".py", ".sql"}:
                continue
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if forbidden.search(line):
                    offenders.append(f"{path.name}:{n}: {line.strip()}")
        self.assertEqual(offenders, [], f"destructive DDL found: {offenders}")

    def test_setu_writes_only_to_its_own_tables(self):
        """Every INSERT/UPDATE/DELETE target must begin with setu_.

        Scans the actual string literals rather than the file text: prose such
        as "makes the update an upsert" is not SQL, and a test that cannot tell
        the difference gets switched off the first time it cries wolf.
        Docstrings are excluded for the same reason.
        """
        import ast
        import re

        # `DO UPDATE SET` inside an upsert names no table; it is excluded
        # explicitly rather than by weakening the assertion.
        pattern = re.compile(
            r"(?<!DO\s)\b(?:INSERT\s+INTO|UPDATE|DELETE\s+FROM)\s+"
            r"(?!SET\b)([A-Za-z_][A-Za-z_0-9]*)", re.I)
        sql_like = re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\b", re.I)

        bad = []
        for path in sorted((HERE / "annotation").rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            docstrings = set()
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                     ast.AsyncFunctionDef)):
                    body = getattr(node, "body", None)
                    if body and isinstance(body[0], ast.Expr) \
                            and isinstance(body[0].value, ast.Constant) \
                            and isinstance(body[0].value.value, str):
                        docstrings.add(id(body[0].value))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                    continue
                if id(node) in docstrings or not sql_like.search(node.value):
                    continue
                for m in pattern.finditer(node.value):
                    table = m.group(1)
                    if not table.lower().startswith("setu_"):
                        bad.append(f"{path.name}:{node.lineno}: writes to {table}")

        # Guard against the scanner silently matching nothing at all.
        self.assertGreater(
            sum(1 for p in (HERE / "annotation").rglob("*.py")), 5, "no sources scanned")
        self.assertEqual(bad, [], f"Setu writes outside its own tables: {bad}")

    def test_the_write_scanner_actually_detects_a_violation(self):
        """A test that cannot fail is not a test."""
        import re
        pattern = re.compile(
            r"(?<!DO\s)\b(?:INSERT\s+INTO|UPDATE|DELETE\s+FROM)\s+"
            r"(?!SET\b)([A-Za-z_][A-Za-z_0-9]*)", re.I)
        self.assertEqual(pattern.findall("DELETE FROM documents WHERE 1"), ["documents"])
        self.assertEqual(pattern.findall("UPDATE audit SET x=1"), ["audit"])
        self.assertEqual(pattern.findall(
            "INSERT INTO setu_row(a) VALUES(1) ON CONFLICT DO UPDATE SET a=2"),
            ["setu_row"])



# ── regressions for bugs this build actually shipped ───────────────────────

class TestStoreTransactions(SetuCase):
    """The FTS table must never end a caller's transaction.

    `executescript` issues an implicit COMMIT. Creating the search index with
    it worked on a fresh database — where the migration ran it before anybody
    had a transaction open — and broke on every run afterwards, when the first
    build opened a transaction and the index was created inside it. Every test
    used a fresh database, so the whole suite passed while the application
    failed on its second start.
    """

    def test_fts_creation_does_not_end_a_transaction(self):
        store.FTS_AVAILABLE = None              # as a fresh process would be
        self.con.execute("BEGIN IMMEDIATE")
        store.fts_ready(self.con)
        self.assertTrue(self.con.in_transaction,
                        "creating the search index ended the open transaction")
        self.con.execute("COMMIT")

    def test_build_twice_against_an_existing_database(self):
        """The exact shape of the failure: second run, index not yet probed."""
        store.FTS_AVAILABLE = None
        report = corpus.build(self.con, rebuild=True, log_fn=lambda *a: None)
        self.assertEqual(report["errors"], [],
                         f"rebuilding an existing database failed: {report['errors']}")

    def test_schema_is_ready_after_connect(self):
        self.assertIsNotNone(store.FTS_AVAILABLE)


class TestSources(SetuCase):
    """Source verification: the bridge to Tulana's existing crop renderer."""

    def _sid(self) -> str:
        return corpus.CorpusRepo(self.con).segments(self.en, limit=5)[2]["sid"]

    def test_missing_pdf_is_a_message_not_an_exception(self):
        view = sources.for_segment(self.con, self._sid())
        self.assertFalse(view.ok)
        self.assertTrue(view.message)
        self.assertNotIn("Traceback", view.message)

    def test_unknown_segment_raises(self):
        with self.assertRaises(NotFound):
            sources.for_segment(self.con, "sg_NOSUCHTHING")

    def test_lfs_pointer_is_recognised(self):
        pointer = self.dir / "fake.pdf"
        pointer.write_bytes(b"version https://git-lfs.github.com/spec/v1\noid sha256:abc\n")
        self.assertTrue(sources._is_lfs_pointer(pointer))
        real = self.dir / "real.pdf"
        real.write_bytes(b"%PDF-1.7\n...")
        self.assertFalse(sources._is_lfs_pointer(real))

    def test_cache_name_is_content_addressed_and_path_safe(self):
        a = sources._cached_path("../../etc/passwd", 3, (0.1, 0.1, 0.9, 0.9), 150)
        b = sources._cached_path("../../etc/passwd", 3, (0.1, 0.1, 0.9, 0.9), 150)
        c = sources._cached_path("../../etc/passwd", 4, (0.1, 0.1, 0.9, 0.9), 150)
        self.assertEqual(a, b, "the same region must reuse one file")
        self.assertNotEqual(a, c, "a different page must not collide")
        self.assertNotIn("..", str(a))
        self.assertTrue(a.parent.samefile(sources.cache_dir()))

    def test_renders_when_a_real_pdf_is_present(self):
        """The whole path, against a PDF built for the purpose."""
        try:
            import pymupdf
        except ImportError:
            self.skipTest("PyMuPDF is not installed")
        book = corpus.CorpusRepo(self.con).book(self.en)
        target = Path(config.DATA_DIR) / book["relpath"]
        target.parent.mkdir(parents=True, exist_ok=True)
        doc = pymupdf.open()
        for i in range(3):
            page = doc.new_page(width=595, height=842)
            page.insert_text((60, 100 + i * 20), f"page {i}", fontsize=14)
        doc.save(str(target))
        doc.close()
        try:
            view = sources.for_segment(self.con, self._sid())
            self.assertTrue(view.ok, view.message)
            self.assertTrue(view.path.is_file())
            self.assertGreater(view.path.stat().st_size, 100)
            again = sources.for_segment(self.con, self._sid())
            self.assertEqual(again.path, view.path, "the second call must hit the cache")
        finally:
            target.unlink(missing_ok=True)


class TestNavigationQueries(SetuCase):
    """Index-backed navigation under filters."""

    def setUp(self):
        super().setUp()
        self.proj = self.project()
        self.repo = workspace.WorkspaceRepo(self.con)

    def test_first_next_previous(self):
        pid = self.proj["pid"]
        first = self.repo.first(pid)
        self.assertEqual(first["seq"], 0)
        nxt = self.repo.neighbour(pid, 0, 1)
        self.assertEqual(nxt["seq"], 1)
        self.assertIsNone(self.repo.neighbour(pid, 0, -1))

    def test_position_counts_within_the_filter(self):
        pid = self.proj["pid"]
        total = self.repo.progress(pid)["total"]
        pos = self.repo.position(pid, 0)
        self.assertEqual((pos["index"], pos["total"]), (1, total))
        rid = self.repo.rows(pid, limit=1)["rows"][0]["rid"]
        annotate.set_status(self.con, rid, "exact", annotator="t")
        filtered = self.repo.position(pid, 0, status="exact")
        self.assertEqual(filtered["total"], 1)

    def test_navigation_respects_the_filter(self):
        pid = self.proj["pid"]
        rows = self.repo.rows(pid, limit=100)["rows"]
        for r in rows[3:5]:
            annotate.set_status(self.con, r["rid"], "unclear", annotator="t")
        nxt = self.repo.neighbour(pid, 0, 1, status="unclear")
        self.assertEqual(nxt["seq"], rows[3]["seq"])

    def test_at_seq_ignores_filters(self):
        """A search hit must open even when the filters would hide it."""
        pid = self.proj["pid"]
        found = self.repo.at_seq(pid, 2)
        self.assertEqual(found["seq"], 2)
        self.assertIsNone(self.repo.at_seq(pid, 10 ** 7))
        self.assertIsNone(self.repo.at_seq(pid, "not a number"))


class TestUISession(unittest.TestCase):
    """The per-session dictionary. No database needed."""

    def test_blank_is_copied_not_shared(self):
        a, b = uisession.blank(), uisession.blank()
        a["filters"]["status"] = "exact"
        self.assertEqual(b["filters"]["status"], "",
                         "two sessions must not share one dictionary")

    def test_ensure_repairs_anything(self):
        for junk in (None, {}, "nonsense", 42, {"pid": "x"}, {"saved": {"src": "a"}}):
            st = uisession.ensure(junk)
            self.assertIn("saved", st)
            self.assertIn("src", st["saved"])
            self.assertIn("status", st["filters"])

    def test_dirty_detects_each_field(self):
        st = uisession.blank()
        st = uisession.mark_saved(st, "a", "b", "exact", "note")
        self.assertFalse(uisession.dirty(st, "a", "b", "exact", "note"))
        self.assertTrue(uisession.dirty(st, "A", "b", "exact", "note"))
        self.assertTrue(uisession.dirty(st, "a", "B", "exact", "note"))
        self.assertTrue(uisession.dirty(st, "a", "b", "unclear", "note"))
        self.assertTrue(uisession.dirty(st, "a", "b", "exact", "other"))

    def test_none_and_empty_compare_equal(self):
        """Gradio sends None for an empty box; that is not an edit."""
        st = uisession.mark_saved(uisession.blank(), "", "", "pending", "")
        self.assertFalse(uisession.dirty(st, None, None, "pending", None))


class TestUIContract(unittest.TestCase):
    """Properties of the interface that can be checked without a browser."""

    def test_no_mutable_module_state_in_the_ui(self):
        """Module-level mutable state is cross-session contamination."""
        import ast
        offenders = []
        allowed = {"_ON_LOAD"}               # cleared inside build(), asserted below
        for path in sorted((HERE / "annotation" / "ui").glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in tree.body:
                targets = []
                if isinstance(node, ast.Assign):
                    targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
                elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    targets = [node.target.id]
                for name in targets:
                    if name in allowed or name.isupper():
                        continue          # UPPER_CASE is the constant convention
                    if name.startswith("__") and name.endswith("__"):
                        continue          # __all__ and friends are not state
                    if isinstance(node.value, (ast.Dict, ast.List, ast.Set,
                                               ast.DictComp, ast.ListComp)):
                        offenders.append(f"{path.name}: {name}")
        self.assertEqual(offenders, [],
                         f"mutable module-level state in the UI: {offenders}")

    def test_build_is_repeatable(self):
        """Building twice must not double-register load handlers."""
        import gradio  # noqa: F401
        from annotation.ui import app as uiapp
        uiapp.build()
        self.assertEqual(uiapp._ON_LOAD, [], "build() left handlers queued")
        uiapp.build()
        self.assertEqual(uiapp._ON_LOAD, [])

    def test_launch_kwargs_carry_the_assets_and_the_state_folder(self):
        """Gradio 6 needs css/js at launch(), and permission to serve state/."""
        from annotation.ui import app as uiapp
        kwargs = uiapp.launch_kwargs(share=False)
        self.assertIn("css", kwargs)
        self.assertIn("head", kwargs)
        self.assertGreater(len(kwargs["css"]), 500)
        self.assertIn("setu_src", kwargs["css"])
        self.assertIn("<script>", kwargs["head"])
        state = str(Path(config.STATE_DIR).resolve())
        self.assertIn(state, kwargs["allowed_paths"],
                      "without this, page images and downloads are refused")

    def test_overrides_cannot_drop_the_state_folder(self):
        from annotation.ui import app as uiapp
        kwargs = uiapp.launch_kwargs(allowed_paths=["/tmp"])
        self.assertIn(str(Path(config.STATE_DIR).resolve()), kwargs["allowed_paths"])
        self.assertIn("/tmp", kwargs["allowed_paths"])

    def test_every_status_has_a_distinct_keyboard_shortcut(self):
        """The browser maps a digit to the radio at that index."""
        shortcuts = [s.shortcut for s in STATUSES]
        self.assertEqual(len(shortcuts), len(set(shortcuts)))
        self.assertEqual(shortcuts, [str(i) for i in range(len(STATUSES))],
                         "the digits must match the radio order the script clicks")

    def test_docs_are_served_from_inside_the_docs_folder_only(self):
        from annotation.ui import panels
        for evil in ("../../config.py", "/etc/passwd", "..%2Fapi.py", "",
                     "../core/store.py"):
            body = panels.read_doc(evil)
            self.assertIn(body, ("", "That page could not be found."),
                          f"{evil!r} was served")
        names = [n for _t, n in panels.doc_choices()]
        self.assertTrue(names)
        self.assertTrue(panels.read_doc(names[0]).strip())


# ── security ───────────────────────────────────────────────────────────────

class TestSecurity(SetuCase):

    def test_export_path_stays_inside_the_export_directory(self):
        out = exporters.export(self.con, self.project()["pid"], "jsonl")
        self.assertTrue(Path(out["path"]).resolve()
                        .is_relative_to(Path(config.EXPORT_DIR).resolve()))

    def test_project_name_cannot_escape_the_filesystem(self):
        proj = self.project()
        store.Repository(self.con).run(
            "UPDATE setu_project SET name = ? WHERE pid = ?",
            ("../../../../tmp/evil", proj["pid"]))
        out = exporters.export(self.con, proj["pid"], "jsonl")
        self.assertTrue(Path(out["path"]).resolve()
                        .is_relative_to(Path(config.EXPORT_DIR).resolve()))
        self.assertNotIn("..", out["filename"])

    def test_paginate_clamps_absurd_input(self):
        for bad in (None, "", "abc", -5, 10 ** 9, float("inf"), [1]):
            lim, off = store.paginate(bad, bad)
            self.assertGreaterEqual(lim, 1)
            self.assertLessEqual(lim, 500)
            self.assertGreaterEqual(off, 0)

    def test_sql_injection_in_search_is_inert(self):
        proj = self.project()
        for q in ("'; DROP TABLE setu_row; --", "' OR 1=1 --", "\\"):
            search.SearchRepo(self.con).find(proj["pid"], q)
        self.assertGreater(
            store.Repository(self.con).scalar("SELECT COUNT(*) FROM setu_row",
                                              default=0), 0)

    def test_status_injection_is_refused(self):
        proj = self.project()
        rid = workspace.WorkspaceRepo(self.con).rows(proj["pid"], limit=1)["rows"][0]["rid"]
        with self.assertRaises(ValueError):
            annotate.set_status(self.con, rid, "exact'; DELETE FROM setu_row; --")

    def test_events_record_shape_not_content(self):
        proj = self.project()
        rid = workspace.WorkspaceRepo(self.con).rows(proj["pid"], limit=1)["rows"][0]["rid"]
        secret = "CONFIDENTIAL-MARKER-9f3a"
        annotate.save_text(self.con, rid, "src", secret, base_rev=0, annotator="a")
        blob = " ".join(
            str(r["detail"]) for r in store.Repository(self.con).all(
                "SELECT detail FROM setu_event"))
        self.assertNotIn(secret, blob, "the event log must not duplicate the corpus")


# ── the real corpus, when it is there ──────────────────────────────────────

class TestRealCorpus(unittest.TestCase):
    """Measures the aligner where the right answer is independently known."""

    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp(prefix="setu-real-", dir=_TMP))
        cls._old = config.DB_PATH
        config.DB_PATH = cls.dir / "real.db"
        store._schema_ready.clear()
        store.FTS_AVAILABLE = None
        try:
            import blocks as blocks_mod
            found = blocks_mod.find_corpus()
            if not found:
                raise unittest.SkipTest("no parsed-layout corpus on this machine")
            cls.con = store.connect()
            blocks_mod.ensure_schema(cls.con)
            blocks_mod.ingest(cls.con, log=lambda *a: None)
            corpus.build(cls.con, rebuild=True, log_fn=lambda *a: None)
        except unittest.SkipTest:
            raise
        except Exception as exc:                   # pragma: no cover - environment
            raise unittest.SkipTest(f"could not load the real corpus: {exc}")

    @classmethod
    def tearDownClass(cls):
        try:
            cls.con.close()
        except Exception:
            pass
        config.DB_PATH = cls._old
        store._schema_ready.clear()
        shutil.rmtree(cls.dir, ignore_errors=True)

    def test_alignment_accuracy_on_page_parallel_editions(self):
        """These editions are typeset page for page, so the page is ground truth."""
        repo = corpus.CorpusRepo(self.con)
        en = repo.books(board="MH", cls=9, language="English")
        if not en:
            self.skipTest("the Maharashtra class 9 editions are not present")
        src = repo.segments(en[0]["book_key"], limit=100000)
        measured = 0
        for lang in ("Marathi", "Hindi", "Gujarati", "Kannada", "Telugu"):
            books = repo.books(board="MH", cls=9, language=lang)
            if not books:
                continue
            tgt = repo.segments(books[0]["book_key"], limit=100000)
            if len(src) != len(tgt) and abs(len(src) - len(tgt)) > len(src) * 0.1:
                continue
            props = align.suggest(src, tgt)
            anchored = [p for p in props
                        if p.basis in {"math", "number"} and p.src >= 0 and p.tgt >= 0]
            if len(anchored) < 50:
                continue
            ok = sum(1 for p in anchored
                     if abs(src[p.src]["page"] - tgt[p.tgt]["page"]) <= 1)
            acc = ok / len(anchored)
            measured += 1
            with self.subTest(language=lang):
                self.assertGreaterEqual(
                    acc, 0.90,
                    f"{lang}: only {acc:.1%} of {len(anchored)} anchors landed "
                    f"within one page")
        if not measured:
            self.skipTest("no page-parallel pair available to measure")

    def test_duplicates_are_collapsed_in_the_real_corpus(self):
        repo = corpus.CorpusRepo(self.con)
        counts = repo.counts()
        self.assertGreater(counts["books"], 0)
        dupes = repo.all(
            "SELECT dedup_key, COUNT(*) n FROM setu_book GROUP BY dedup_key HAVING n > 1")
        self.assertEqual(dupes, [], "two canonical books share a content identity")

    def test_every_parser_label_is_mapped(self):
        unmapped = corpus.CorpusRepo(self.con).all(
            "SELECT label, COUNT(*) n FROM setu_segment WHERE kind = 'other'"
            " AND label <> '' GROUP BY label ORDER BY n DESC")
        from annotation.core.models import KIND_FROM_LABEL
        surprises = [r["label"] for r in unmapped
                     if r["label"].lower() not in KIND_FROM_LABEL]
        self.assertEqual(surprises, [],
                         f"parser labels with no mapping: {surprises}")


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    verbosity = 2 if "-v" in sys.argv else 1
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    shutil.rmtree(_TMP, ignore_errors=True)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
