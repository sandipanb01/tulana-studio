#!/usr/bin/env python3
"""Tests for the aligned document-MT test set (annotation/core/aligned.py).

    python3 test_aligned.py                         # synthetic pairs, seconds
    python3 test_aligned.py -v
    SETU_ALIGNED_FULL=1 python3 test_aligned.py     # also every real pair (~1 min)

What is protected, in order of how much damage a mistake would do:

* What the OCR read stays the source. The model's corrected text is revision 1
  of the passage, credited to the model, and is never counted — on screen, in
  Saved work or in an export — as a person's correction.
* Importing never overwrites work, and an aligned pair is never rebuilt by
  Setu's own aligner, with or without force.
* Files from outside are untrusted. A hostile relpath, a malformed file, a
  symlink out of the folder: that pair refuses to import, says so without
  quoting its contents, and every other pair still imports.
* Tulana Studio's eight tables are byte-identical afterwards.

The real dataset, when it is present, is checked against its own published
numbers — the units per pair in export_summary.json — and every passage's
source against the raw OCR it was rebuilt from.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import unittest
from pathlib import Path
from unittest import mock

from test_annotation import (EN_PAGES, LEGACY_TABLES, MR_PAGES, SetuCase,  # noqa: F401
                             _parsed_book)

import blocks
import config  # noqa: F401
from annotation import api
from annotation.core import aligned, annotate, corpus, exporters, resume, store, workspace
from annotation.core.models import normalise
from annotation.core.store import Invalid
from annotation.ui import browse

PAIR = "TT9_en-mr"
EN_REL, MR_REL = "TEST/TT_EN_9.pdf", "TEST/TT_MR_9.pdf"
MODEL = "model:gemini-3.5-flash"
FLAG = ("[translation_divergence] [suggested fix not applied: low confidence] "
        "'लिहा' -> 'लिहा.'. Evidence: Write. The Marathi drops the full stop.")
MR_MERGED = "संच म्हणजे वस्तूंचा संग्रह होय.\n\nही संकल्पना मागील इयत्तेत पाहिली आहे."


# ── the dataset's shape, built small ───────────────────────────────────────

def _blk(order, label, btype, text, members, aid=None, rel=None, conf=None,
         part=None, note=None, flags=None):
    b = {"order": order, "label": label, "type": btype,
         "bbox_xyxy": [10, 20 + order * 30, 500, 60 + order * 30], "conf": 0.9,
         "text": text, "align_id": aid,
         "members": [{"order": m, "label": label, "bbox_xyxy": [0, 0, 1, 1]}
                     for m in members]}
    for key, val in (("align_relation", rel), ("align_confidence", conf), ("part", part),
                     ("align_note", note)):
        if val:
            b[key] = val
    if flags:
        b["flags"] = list(flags)
    return b


def _page(n, status, blocks_):
    return {"image": f"p{n:04d}.png", "width": 1000, "height": 1400, "page": n,
            "align_status": status, "blocks": blocks_}


def u(page, n, pair=PAIR):
    return f"{pair}/p{page:03d}/u{n}"


def aligned_docs(pair=PAIR):
    """One pair, written the way the dataset writes one.

    Covers: a model correction on each side, two OCR blocks merged into one
    unit, a unit that runs over a page break, a target block with no English
    partner, page furniture, a reviewer flag, and a page that needed a retry.
    """
    meta = {"pair_id": pair, "lang": "en", "language": "English", "other_book": "TT_MR_9",
            "model": "gemini-3.5-flash", "prompt_version": "v4", "thinking_level": "minimal"}
    en = {"book": "TT_EN_9", "relpath": EN_REL, "num_pages": 2, "alignment": meta, "pages": [
        _page(0, "ok", [
            _blk(0, "Chapter-title", "Title", "Sets 1", [0], u(0, 1, pair), "equivalent", "high"),
            _blk(1, "Section-title", "SectionHeader", "1.1 INTRODUCTION", [1], u(0, 2, pair),
                 "equivalent", "high"),
            _blk(2, "Paragraph", "Text", "A set is a collection of objects.", [2],
                 u(0, 3, pair), "partial", "medium"),
            _blk(3, "Equation", "Equation", r"$A = \{1, 3, 5, 7, 9\}$", [3], u(0, 4, pair),
                 "equivalent", "high", part="1/2"),
            _blk(4, "Header", "PageHeader", "", [4], note="page_furniture"),
        ]),
        _page(1, "retried_ok", [
            _blk(0, "Section-title", "SectionHeader", "Practice set 1.2", [0], u(1, 1, pair),
                 "equivalent", "high"),
            _blk(1, "Solved-example", "Text", r"Ex (1) $B = \{2, 4, 6, 8, 10\}$ is finite.",
                 [1], u(0, 4, pair), "equivalent", "high", part="2/2"),
            _blk(2, "Question", "Text", "Write the following sets.", [2], u(1, 2, pair),
                 "equivalent", "low", flags=[FLAG]),
            _blk(3, "Table", "Table", "<table><tr><td>Name</td></tr></table>", [3],
                 note="no_counterpart"),
        ])]}
    mr = {"book": "TT_MR_9", "relpath": MR_REL, "num_pages": 2,
          "alignment": dict(meta, lang="mr", language="Marathi", other_book="TT_EN_9"),
          "pages": [
              _page(0, "ok", [
                  _blk(0, "Chapter-title", "Title", "संच 1", [0], u(0, 1, pair),
                       "equivalent", "high"),
                  _blk(1, "Section-title", "SectionHeader", "1.1 प्रस्तावना", [1],
                       u(0, 2, pair), "equivalent", "high"),
                  _blk(2, "Paragraph", "Text", MR_MERGED, [2, 3], u(0, 3, pair),
                       "partial", "medium"),
                  _blk(4, "Equation", "Equation", r"$A = \{1, 3, 5, 7, 9\}$", [4],
                       u(0, 4, pair), "equivalent", "high"),
                  _blk(5, "Header", "PageHeader", "", [5], note="page_furniture"),
              ]),
              _page(1, "ok", [
                  _blk(0, "Section-title", "SectionHeader", "सरावसंच 1.2", [0], u(1, 1, pair),
                       "equivalent", "high"),
                  _blk(1, "Solved-example", "Text",
                       r"उदा (1) $B = \{2, 4, 6, 8, 10\}$ सांत आहे.", [1], note="no_counterpart"),
                  _blk(2, "Question", "Text", "पुढील संच लिहा.", [2], u(1, 2, pair),
                       "equivalent", "low", flags=[FLAG]),
                  _blk(3, "Table", "Table", "<table><tr><td>नाव</td></tr></table>", [3],
                       note="no_counterpart"),
              ])]}
    return en, mr


class AlignedCase(SetuCase):
    """The synthetic textbooks, plus a raw-corpus folder and an aligned folder."""

    def setUp(self):
        super().setUp()
        self.raw = self.dir / "board_outputs"
        self.dataset = self.dir / aligned.DATASET
        for doc in (_parsed_book("TT_EN_9", EN_REL, EN_PAGES, lambda t: t),
                    _parsed_book("TT_MR_9", MR_REL, MR_PAGES, lambda t: t)):
            self.write(self.raw / Path(doc["relpath"]).with_suffix(".json"), doc)
        en, mr = aligned_docs()
        self.write_pair(PAIR, ("en.json", en), ("mr.json", mr))
        self._patches = [mock.patch.object(blocks, "find_corpus", return_value=self.raw),
                         mock.patch.dict(os.environ, {"TULANA_ALIGNED_DIR": ""})]
        for p in self._patches:
            p.start()
        aligned._raw_index_cached.cache_clear()
        aligned._raw_pages.cache_clear()

    def tearDown(self):
        for p in self._patches:
            p.stop()
        aligned._raw_index_cached.cache_clear()
        aligned._raw_pages.cache_clear()
        super().tearDown()

    # -- files ---------------------------------------------------------------
    @staticmethod
    def write(path: Path, doc) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        text = doc if isinstance(doc, str) else json.dumps(doc, ensure_ascii=False)
        path.write_text(text, encoding="utf-8")

    def write_pair(self, pair_id, *files) -> Path:
        """Files go to fixed, safe names — never to a path a document names."""
        folder = self.dataset / pair_id / "CLASS-9"
        for name, doc in files:
            self.write(folder / name, doc)
        return folder

    def run_import(self) -> dict:
        return aligned.import_all(store.tx, self.dataset, log_fn=lambda m: None)

    # -- reading back ----------------------------------------------------------
    def pid_of(self, pair=PAIR) -> str:
        return aligned.is_imported(self.con, pair)

    def rows(self, pid=None) -> list[dict]:
        return [dict(r) for r in self.con.execute(
            "SELECT * FROM setu_row WHERE pid = ? ORDER BY seq", (pid or self.pid_of(),))]

    def seg(self, sid) -> dict:
        return dict(self.con.execute("SELECT * FROM setu_segment WHERE sid = ?",
                                     (sid,)).fetchone())

    def hint(self, sid) -> dict | None:
        r = self.con.execute("SELECT * FROM setu_hint WHERE sid = ?", (sid,)).fetchone()
        return dict(r) if r else None

    def book_of(self, side, pair=PAIR) -> str:
        return self.con.execute("SELECT book_key FROM setu_book WHERE dedup_key = ?",
                                (f"{aligned.MARK}{pair}:{side}",)).fetchone()[0]

    def row_of(self, aid, side="src") -> dict:
        sid = self.con.execute(
            "SELECT h.sid FROM setu_hint h JOIN setu_segment s ON s.sid = h.sid"
            " WHERE h.align_id = ? AND s.book_key = ?", (aid, self.book_of(side))).fetchone()[0]
        return dict(self.con.execute(f"SELECT * FROM setu_row WHERE {side}_sid = ?",
                                     (sid,)).fetchone())

    def view(self, rid) -> dict:
        return workspace.WorkspaceRepo(self.con).row(rid)          # already the screen's view

    def text_row(self, rid, side):
        r = self.con.execute("SELECT text, rev, updated_by FROM setu_text"
                             " WHERE rid = ? AND side = ?", (rid, side)).fetchone()
        return tuple(r) if r else None

    def snapshot(self) -> str:
        h = hashlib.sha256()
        for t in ("setu_book", "setu_segment", "setu_hint", "setu_project", "setu_row",
                  "setu_text", "setu_rev"):
            for r in self.con.execute(f"SELECT * FROM {t} ORDER BY 1, 2"):
                h.update(repr(tuple(r)).encode())
        return h.hexdigest()

    def legacy(self) -> dict:
        out = {}
        for t in LEGACY_TABLES:
            rows = self.con.execute(f"SELECT * FROM {t} ORDER BY 1").fetchall()
            out[t] = hashlib.sha256(repr([tuple(r) for r in rows]).encode()).hexdigest()
        return out


# ── importing one pair ─────────────────────────────────────────────────────

class TestImport(AlignedCase):

    def setUp(self):
        super().setUp()
        self.report = self.run_import()
        self.pid = self.pid_of()

    def test_the_report(self):
        self.assertEqual(self.report["errors"], [])
        self.assertEqual((self.report["imported"], self.report["skipped"]), (1, 0))
        self.assertEqual(self.report["raw_missing"], [])
        self.assertEqual(self.report["model_corrections"], 2)
        self.assertTrue(self.pid)

    def test_every_unit_is_a_pair_and_nothing_is_hidden(self):
        rows = self.rows()
        self.assertEqual([r["seq"] for r in rows], list(range(len(rows))), "a gap")
        two = [r for r in rows if r["src_sid"] and r["tgt_sid"]]
        self.assertEqual(len(two), 6, "six units in the fixture")
        for r in two:
            self.assertEqual(r["origin"], "aligned")
            self.assertEqual(self.hint(r["src_sid"])["align_id"],
                             self.hint(r["tgt_sid"])["align_id"],
                             "a pair whose two sides are different units")
        for r in rows:
            if not (r["src_sid"] and r["tgt_sid"]):
                self.assertEqual(r["origin"], "unpaired")
                self.assertEqual(r["confidence"], 0)
        # Every merged block is a passage (the page-two part of the unit that
        # runs over the break is folded into its first part). Each is in at most
        # one row, and the only ones in none are the empty page headers — which
        # Setu leaves out of every project's to-do list.
        for side, want in (("src", 8), ("tgt", 9)):
            sids = [r[0] for r in self.con.execute(
                "SELECT sid FROM setu_segment WHERE book_key = ?", (self.book_of(side),))]
            self.assertEqual(len(sids), want)
            held = [r[f"{side}_sid"] for r in rows if r[f"{side}_sid"]]
            self.assertEqual(len(held), len(set(held)), f"a {side} passage is in two rows")
            for sid in set(sids) - set(held):
                self.assertEqual((self.hint(sid)["note"], self.seg(sid)["source_text"]),
                                 ("page_furniture", ""), "a passage worth checking has no row")
            self.assertEqual(len(set(sids) - set(held)), 1)
        self.assertEqual(len(rows), 9)
        self.assertEqual(self.con.execute("SELECT n_rows FROM setu_project WHERE pid = ?",
                                          (self.pid,)).fetchone()[0], 9)
        # ...and the header is still in the book, shown with the page furniture.
        p0 = browse.blocks(self.con, pid=self.pid, book_key=self.book_of("src"), side="src",
                           page=0, hide_noise=False)
        head = next(b for b in p0 if b["label"] == "Header")
        self.assertIsNone(head["rid"])
        self.assertEqual(head["hint"]["note"], "page_furniture")

    def test_target_only_passages_sit_where_they_fall(self):
        order = [(r["tgt_page"], self.seg(r["tgt_sid"])["ord_start"])
                 for r in self.rows() if r["tgt_sid"]]
        self.assertEqual(order, sorted(order), "the Marathi book read out of order")

    def test_the_source_is_what_the_ocr_read(self):
        raw = {p["page"]: {b["order"]: b["text"] for b in p["blocks"]}
               for p in _parsed_book("TT_MR_9", MR_REL, MR_PAGES, lambda t: t)["pages"]}
        seg = self.seg(self.row_of(u(0, 3), "tgt")["tgt_sid"])
        self.assertEqual(seg["source_text"], normalise(raw[0][2] + "\n\n" + raw[0][3]))
        self.assertNotIn("होय", seg["source_text"], "the model's word leaked into the source")
        self.assertEqual(json.loads(seg["block_ids"]),
                         [{"page": 0, "order": 2}, {"page": 0, "order": 3}])
        en = self.seg(self.row_of(u(0, 2))["src_sid"])
        self.assertEqual(en["source_text"], "1.1 Introduction")

    def test_model_corrections_are_revision_one_by_the_model(self):
        for aid, side, text in ((u(0, 2), "src", "1.1 INTRODUCTION"),
                                (u(0, 3), "tgt", MR_MERGED)):
            with self.subTest(side=side):
                r = self.row_of(aid, side)
                self.assertEqual(self.text_row(r["rid"], side), (text, 1, MODEL))
                hist = self.con.execute("SELECT rev, actor, reason FROM setu_rev"
                                        " WHERE rid = ? AND side = ?", (r["rid"], side)).fetchall()
                self.assertEqual([tuple(x) for x in hist], [(1, MODEL, "model-correction")])
                self.assertEqual(r["edited"], 0, "the model's correction counted as a person's")
                v = self.view(r["rid"])[side]
                self.assertTrue(v["model_edited"])
                self.assertFalse(v["edited"])
                self.assertEqual(v["text"], text)
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM setu_text").fetchone()[0], 2)
        # Start-up recomputes every flag; it must agree.
        annotate.resync_edited_flags(self.con)
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM setu_row WHERE edited = 1"
                                          ).fetchone()[0], 0)

    def test_a_person_corrects_on_top_and_can_undo_the_model(self):
        r = self.row_of(u(0, 3), "tgt")
        annotate.save_text(self.con, r["rid"], "tgt", "संच म्हणजे वस्तूंचा संग्रह.",
                           base_rev=1, annotator="asha")
        self.assertEqual(self.text_row(r["rid"], "tgt")[1:], (2, "asha"))
        v = self.view(r["rid"])["tgt"]
        self.assertTrue(v["edited"])
        self.assertFalse(v["model_edited"])
        annotate.restore(self.con, r["rid"], "tgt", rev=0, annotator="asha")
        v = self.view(r["rid"])["tgt"]
        self.assertEqual(v["text"], v["source"], "put back did not reach the parser's text")
        self.assertFalse(v["edited"] or v["model_edited"])
        reasons = [x[0] for x in self.con.execute(
            "SELECT reason FROM setu_rev WHERE rid = ? AND side = 'tgt' ORDER BY rev",
            (r["rid"],))]
        self.assertEqual(reasons[0], "model-correction", "the model's version left the history")

    def test_a_save_based_on_the_parser_text_is_a_conflict_not_an_overwrite(self):
        """A screen that never saw the model's revision must not silently replace it."""
        r = self.row_of(u(0, 3), "tgt")
        with self.assertRaises(store.Conflict):
            annotate.save_text(self.con, r["rid"], "tgt", "something else", base_rev=0,
                               annotator="asha")
        self.assertEqual(self.text_row(r["rid"], "tgt"), (MR_MERGED, 1, MODEL))

    def test_importing_again_changes_nothing(self):
        rid = self.rows()[0]["rid"]
        annotate.set_status(self.con, rid, "exact", annotator="asha")
        before = self.snapshot()
        rep = self.run_import()
        self.assertEqual((rep["imported"], rep["skipped"], rep["errors"]), (0, 1, []))
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.rows()[0]["status"], "exact")

    def test_a_deleted_pair_comes_back_as_imported(self):
        r = self.row_of(u(0, 3), "tgt")
        annotate.save_text(self.con, r["rid"], "tgt", "हाताने दुरुस्त.", base_rev=1,
                           annotator="asha")
        workspace.delete_project(self.con, self.pid, annotator="admin")
        self.assertEqual(self.pid_of(), "")
        rep = self.run_import()
        self.assertEqual((rep["imported"], rep["errors"]), (1, []))
        r2 = self.row_of(u(0, 3), "tgt")
        text, rev, by = self.text_row(r2["rid"], "tgt")
        self.assertEqual((text, by), (MR_MERGED, MODEL))
        self.assertGreater(rev, 2, "the kept history was overwritten or collided")
        self.assertEqual(len(self.rows()), 9)

    def test_never_rebuilt_by_setus_own_aligner(self):
        before = self.snapshot()
        for force in (False, True):
            with self.subTest(force=force), self.assertRaises(Invalid):
                workspace.build_rows(self.con, self.pid, force=force)
        self.assertEqual(self.snapshot(), before)

    def test_an_aligned_book_only_opens_beside_its_partner(self):
        src, tgt = self.book_of("src"), self.book_of("tgt")
        self.assertEqual(workspace.create_project(self.con, src_book=src, tgt_book=tgt)["pid"],
                         self.pid, "opening the pair again made a second project")
        for a, b in ((src, self.mr), (self.en, tgt), (tgt, src)):
            with self.subTest(a=a, b=b), self.assertRaises(Invalid):
                workspace.create_project(self.con, src_book=a, tgt_book=b)

    def test_kept_out_of_the_textbook_dropdowns(self):
        repo = corpus.CorpusRepo(self.con)
        mine = {self.book_of("src"), self.book_of("tgt")}
        self.assertFalse(mine & {b["book_key"] for b in repo.books()})
        langs = repo.languages("MH", 9, "Mathematics")
        self.assertEqual({(x["value"], x["n_books"]) for x in langs},
                         {("English", 1), ("Marathi", 1)})
        self.assertEqual(repo.counts()["aligned_pairs"], 1)

    def test_a_unit_over_a_page_break_is_one_passage(self):
        r = self.row_of(u(0, 4))
        seg = self.seg(r["src_sid"])
        self.assertEqual(json.loads(seg["block_ids"]),
                         [{"page": 0, "order": 3}, {"page": 1, "order": 1}])
        self.assertIn("is finite", seg["source_text"])
        h = self.hint(r["src_sid"])
        self.assertEqual((h["parts"], json.loads(h["pages"])), (2, [0, 1]))
        on_p1 = self.con.execute("SELECT COUNT(*) FROM setu_segment WHERE book_key = ?"
                                 " AND page = 1", (self.book_of("src"),)).fetchone()[0]
        self.assertEqual(on_p1, 3, "the second part also became a passage of its own")

    def test_the_models_notes_reach_the_page(self):
        p1 = browse.blocks(self.con, pid=self.pid, book_key=self.book_of("src"),
                           side="src", page=1)
        q = next(b for b in p1 if b["label"] == "Question")
        self.assertEqual((q["hint"]["confidence"], q["hint"]["flags"], q["hint"]["page_status"]),
                         ("low", [FLAG], "retried_ok"))
        p0 = browse.blocks(self.con, pid=self.pid, book_key=self.book_of("src"),
                           side="src", page=0)
        eq = next(b for b in p0 if b["label"] == "Equation")
        self.assertEqual((eq["hint"]["parts"], eq["hint"]["pages"]), (2, [1, 2]),
                         "pages are shown as printed, counting from 1")
        intro = next(b for b in p0 if b["label"] == "Section-title")
        self.assertTrue(intro["model_edited"])
        self.assertFalse(intro["edited"])
        self.assertIn("corrected by the model", browse.block_heading(intro))

    def test_the_row_list_agrees_with_the_row(self):
        """The list endpoint must not call the model's correction a person's."""
        page = workspace.WorkspaceRepo(self.con).rows(self.pid, limit=50)["rows"]
        got = {r["rid"]: r for r in page}
        for aid, side in ((u(0, 2), "src"), (u(0, 3), "tgt")):
            r = got[self.row_of(aid, side)["rid"]][side]
            self.assertEqual((r["edited"], r["model_edited"]), (False, True))
        self.assertEqual(workspace.WorkspaceRepo(self.con).rows(self.pid, edited=True)["total"], 0)

    def test_the_row_carries_the_notes(self):
        v = self.view(self.row_of(u(1, 2))["rid"])
        self.assertEqual(v["origin"], "aligned")
        self.assertEqual(v["src"]["hint"]["flags"], [FLAG])
        self.assertEqual(v["src"]["hint"]["page_status"], "retried_ok")
        self.assertEqual(v["tgt"]["hint"]["page_status"], "ok")
        self.assertAlmostEqual(v["confidence"], aligned.CONFIDENCE["low"])

    def test_exports_say_who_corrected_what(self):
        recs = {r["unit_id"]: r for r in exporters.records(self.con, self.pid) if r["unit_id"]}
        self.assertEqual(len(recs), 6)
        x = recs[u(0, 3)]
        self.assertTrue(set(exporters.FIELDS) <= set(x))
        self.assertTrue(x["target_model_corrected"])
        self.assertFalse(x["target_edited"])
        self.assertFalse(x["source_model_corrected"])
        self.assertEqual((x["target_text"], x["target_original"] != x["target_text"]),
                         (MR_MERGED, True))
        self.assertEqual(recs[u(1, 2)]["model_flags"], FLAG, "a note on both sides, twice")
        annotate.save_text(self.con, self.row_of(u(0, 3))["rid"], "src",
                           "A set is a well-defined collection of objects.", base_rev=0,
                           annotator="asha")
        x = {r["unit_id"]: r for r in exporters.records(self.con, self.pid)}[u(0, 3)]
        self.assertTrue(x["source_edited"])
        self.assertFalse(x["source_model_corrected"])

    def test_unpairing_keeps_the_models_credit(self):
        r = self.row_of(u(0, 3), "tgt")
        annotate.split_row(self.con, r["rid"], annotator="asha")
        holder = self.con.execute("SELECT rid, edited FROM setu_row WHERE tgt_sid = ?",
                                  (r["tgt_sid"],)).fetchone()
        self.assertNotEqual(holder[0], r["rid"], "the passage did not move")
        self.assertEqual(self.text_row(holder[0], "tgt")[::2], (MR_MERGED, MODEL),
                         "moving the passage made the model's text a person's")
        self.assertEqual(holder[1], 0)
        self.assertTrue(self.view(holder[0])["tgt"]["model_edited"])

    def test_lists_name_aligned_pairs_as_such(self):
        repo = resume.ResumeRepo(self.con)
        mine = next(p for p in repo.workbench()["projects"] if p["pid"] == self.pid)
        self.assertTrue(mine["aligned"])
        self.assertIn("aligned test set", mine["label"])
        self.assertTrue(next(p for p in repo.projects_with_work()
                             if p["pid"] == self.pid)["aligned"])
        (p,) = aligned.pairs(self.con)
        self.assertEqual((p["pair_id"], p["units"], p["flagged"], p["answered"], p["n_rows"]),
                         (PAIR, 6, 1, 0, 9))
        st = aligned.status(self.con, self.dataset)
        self.assertEqual((st["on_disk"], st["imported"], st["waiting"]), (1, 1, []))
        saved = repo.saved_rows(pid=self.pid, limit=50)
        by_rid = {r["rid"]: r for r in saved["rows"]}
        x = by_rid[self.row_of(u(0, 3))["rid"]]
        self.assertTrue(x["tgt_model_edited"])
        self.assertFalse(x["tgt_edited"])
        self.assertEqual(repo.saved_rows(pid=self.pid, edited=True)["total"], 0,
                         "“only ones I corrected” listed the model's corrections")

    def test_nobody_can_sign_as_the_model(self):
        class Req:
            headers = {"x-annotator": "model: gemini"}
        for name, want in (("model:gemini-3.5-flash", "gemini-3.5-flash"),
                           ("MODEL:model:x", "x"), ("asha", "asha"), ("", "gemini")):
            with self.subTest(name=name):
                self.assertEqual(api._actor(Req(), name)[0], want)

    def test_tulana_studios_tables_are_untouched(self):
        before = self.legacy()
        r = self.row_of(u(0, 3), "tgt")
        annotate.save_text(self.con, r["rid"], "tgt", "x y z", base_rev=1, annotator="asha")
        annotate.set_status(self.con, r["rid"], "needs_correction", annotator="asha")
        annotate.split_row(self.con, r["rid"], annotator="asha")
        workspace.delete_project(self.con, self.pid, annotator="admin")
        self.run_import()
        list(exporters.records(self.con, self.pid_of()))
        self.assertEqual(self.legacy(), before)


# ── the corpus reader never mistakes the aligned folder for raw books ──────

class TestCorpusIgnoresTheSet(AlignedCase):

    def test_an_aligned_file_is_not_raw_layout(self):
        f = next(self.dataset.rglob("*.json"))
        self.assertFalse(blocks._looks_like_layout(f))
        self.assertTrue(blocks._is_junk(Path(aligned.DATASET) / PAIR / "x.json"))
        raw = next(self.raw.rglob("*.json"))
        self.assertTrue(blocks._looks_like_layout(raw))

    def test_the_raw_lookup_stays_inside_the_corpus(self):
        outside = self.dir / "secret.json"
        self.write(outside, {"relpath": "../secret.pdf", "pages": []})
        for rel in ("../secret.pdf", "../../etc/passwd", "/etc/passwd", "C:\\x\\y.pdf",
                    "a/../../secret.pdf", "TEST/\x00.pdf", "", None, 42):
            with self.subTest(rel=rel):
                self.assertEqual(aligned.raw_path_for(rel), "")
        self.assertTrue(aligned.raw_path_for(EN_REL).endswith("TT_EN_9.json"))


# ── hostile and broken files ───────────────────────────────────────────────

class TestHostileInput(AlignedCase):
    """Each bad pair is refused on its own; the good pair still imports."""

    def check_refused(self, name, *files):
        if files:
            self.write_pair(name, *files)
        before = self.legacy()
        try:
            rep = self.run_import()
        finally:
            shutil.rmtree(self.dataset / name, ignore_errors=True)
        self.assertTrue(self.pid_of(), "the good pair did not import")
        self.assertEqual([e["pair"] for e in rep["errors"]], [name])
        self.assertFalse(self.con.execute("SELECT COUNT(*) FROM setu_book WHERE dedup_key LIKE ?",
                                          (f"{aligned.MARK}{name}:%",)).fetchone()[0],
                         "half of a refused pair was written")
        # The error names the problem, never the contents.
        blob = json.dumps(rep["errors"], ensure_ascii=False)
        for secret in ("Sets 1", "संच", "INTRODUCTION", "passwd"):
            self.assertNotIn(secret, blob)
        self.assertEqual(self.legacy(), before)
        return rep

    def mutated(self, fn):
        en, mr = aligned_docs("BAD1_en-mr")
        fn(en, mr)
        return ("en.json", en), ("mr.json", mr)

    def test_relpaths_that_leave_the_folder(self):
        for i, rel in enumerate(("../../../etc/passwd.pdf", "/etc/passwd.pdf",
                                 "C:\\Windows\\win.ini", "TEST/\x00.pdf", "a/../../b.pdf")):
            with self.subTest(rel=rel):
                name = f"BADREL{i}_en-mr"

                def bad(en, mr, rel=rel):
                    en["relpath"] = rel
                self.check_refused(name, *self.mutated(bad))

    def test_malformed_structure(self):
        cases = {
            "pages_not_list": lambda en, mr: en.update(pages={"0": {}}),
            "page_negative": lambda en, mr: en["pages"][0].update(page=-1),
            "page_not_int": lambda en, mr: en["pages"][0].update(page="0"),
            "text_not_str": lambda en, mr: en["pages"][0]["blocks"][0].update(text={"x": 1}),
            "member_order_str": lambda en, mr: en["pages"][0]["blocks"][0]["members"][0]
                                               .update(order="0; DROP TABLE setu_row"),
            "no_alignment": lambda en, mr: en.pop("alignment"),
            "two_english": lambda en, mr: mr["alignment"].update(lang="en"),
        }
        for i, (what, fn) in enumerate(cases.items()):
            with self.subTest(what=what):
                self.check_refused(f"BADSHAPE{i}_en-mr", *self.mutated(fn))

    def test_corrupt_json(self):
        en, mr = aligned_docs("BADJSON_en-mr")
        self.check_refused("BADJSON_en-mr", ("en.json", "{ this is not json"), ("mr.json", mr))

    def test_an_unsafe_folder_name(self):
        en, mr = aligned_docs()
        self.check_refused("bad name; rm -rf", ("en.json", en), ("mr.json", mr))

    def test_too_many_files(self):
        en, mr = aligned_docs("BADMANY_en-mr")
        self.check_refused("BADMANY_en-mr", *[(f"f{i}.json", en) for i in range(5)])

    @unittest.skipIf(os.name == "nt", "symlinks need privileges on Windows")
    def test_a_symlink_out_of_the_folder_is_not_followed(self):
        en, mr = aligned_docs("BADLINK_en-mr")
        outside = self.dir / "outside"
        self.write(outside / "en.json", en)
        self.write(outside / "mr.json", mr)
        folder = self.dataset / "BADLINK_en-mr" / "CLASS-9"
        folder.mkdir(parents=True)
        (folder / "en.json").symlink_to(outside / "en.json")
        (folder / "mr.json").symlink_to(outside / "mr.json")
        self.check_refused("BADLINK_en-mr")

    def test_a_missing_raw_book_still_imports_with_the_delivered_text(self):
        for f in self.raw.rglob("*.json"):
            f.unlink()
        aligned._raw_index_cached.cache_clear()
        aligned._raw_pages.cache_clear()
        rep = self.run_import()
        self.assertEqual((rep["imported"], rep["errors"]), (1, []))
        self.assertEqual(rep["raw_missing"], [PAIR], "a missing raw book went unreported")


# ── the two-language Andhra Pradesh books ──────────────────────────────────

class TestBilingual(AlignedCase):
    """English and Telugu in one file: English on the odd pages, Telugu after."""

    REL = "TEST/TT_EN-TEL_10.pdf"
    PAIR = "TT10_sem1_en-te"

    def setUp(self):
        super().setUp()
        p = self.PAIR
        raw_pages = [
            [("Paragraph", "Text", "Foreword")],
            [("Paragraph", "Text", "Numbers are everywhere."), ("Paragraph", "Text", "Count them.")],
            [("Paragraph", "Text", "సంఖ్యలు అంతటా ఉన్నాయి."), ("Paragraph", "Text", "లెక్కించండి.")],
            [("Paragraph", "Text", "A prime has two factors.")],
            [("Paragraph", "Text", "ప్రధాన సంఖ్యకు రెండు కారణాంకాలు.")],
        ]
        raw = _parsed_book("TT_EN-TEL_10", self.REL, raw_pages, lambda t: t)
        self.write(self.raw / Path(self.REL).with_suffix(".json"), raw)
        meta = {"pair_id": p, "lang": "en+te", "language": "English + Telugu",
                "other_book": "TT_EN-TEL_10", "model": "gemini-3.5-flash",
                "prompt_version": "v4", "thinking_level": "minimal"}
        doc = {"book": "TT_EN-TEL_10", "relpath": self.REL, "num_pages": 5, "alignment": meta,
               "pages": [
                   _page(0, "not_processed", [_blk(0, "Paragraph", "Text", "Foreword", [0])]),
                   _page(1, "ok", [
                       _blk(0, "Paragraph", "Text", "Numbers are everywhere.", [0], u(1, 1, p),
                            "equivalent", "high"),
                       _blk(1, "Paragraph", "Text", "Count them.", [1], u(1, 2, p),
                            "equivalent", "high")]),
                   _page(2, "ok", [
                       _blk(0, "Paragraph", "Text", "సంఖ్యలు అంతటా ఉన్నాయి.", [0], u(1, 1, p),
                            "equivalent", "high"),
                       _blk(1, "Paragraph", "Text", "లెక్కించండి.", [1], u(1, 2, p),
                            "equivalent", "high")]),
                   _page(3, "ok", [
                       _blk(0, "Paragraph", "Text", "A prime has two factors.", [0], u(3, 1, p),
                            "equivalent", "high")]),
                   _page(4, "alignment_failed", [
                       _blk(0, "Paragraph", "Text", "ప్రధాన సంఖ్యకు రెండు కారణాంకాలు.", [0])]),
               ]}
        self.write_pair(p, ("both.json", doc))
        self.report = self.run_import()
        self.pid = self.pid_of(p)

    def pages_of(self, side):
        return sorted({r[0] for r in self.con.execute(
            "SELECT page FROM setu_segment WHERE book_key = ?", (self.book_of(side, self.PAIR),))})

    def test_one_file_becomes_two_sides_by_page(self):
        self.assertEqual(self.report["errors"], [])
        self.assertEqual(self.pages_of("src"), [1, 3])
        self.assertEqual(self.pages_of("tgt"), [0, 2, 4])
        langs = dict(self.con.execute(
            "SELECT dedup_key, language FROM setu_book WHERE dedup_key LIKE ?",
            (f"{aligned.MARK}{self.PAIR}:%",)).fetchall())
        self.assertEqual(langs, {f"{aligned.MARK}{self.PAIR}:src": "English",
                                 f"{aligned.MARK}{self.PAIR}:tgt": "Telugu"})
        titles = [r[0] for r in self.con.execute(
            "SELECT title FROM setu_book WHERE dedup_key LIKE ?",
            (f"{aligned.MARK}{self.PAIR}:%",))]
        self.assertTrue(any("Telugu pages" in t and "English ·" not in t for t in titles),
                        f"the Telugu side is titled as English: {titles}")

    def test_the_units_pair_across_facing_pages(self):
        rows = self.rows(self.pid)
        two = [(r["src_page"], r["tgt_page"]) for r in rows if r["src_sid"] and r["tgt_sid"]]
        self.assertEqual(two, [(1, 2), (1, 2)])
        lone = [(r["src_page"], r["tgt_page"]) for r in rows
                if not (r["src_sid"] and r["tgt_sid"])]
        self.assertIn((3, None), lone)
        self.assertIn((None, 4), lone)

    def test_the_page_view_steps_over_the_other_languages_pages(self):
        from annotation.api import page_blocks
        with mock.patch.object(store, "ro", lambda: _Same(self.con)):
            got = page_blocks(self.book_of("src", self.PAIR), 1, pid=self.pid)
        self.assertTrue(got["book"]["aligned"])
        self.assertEqual((got["prev_page"], got["next_page"]), (None, 3))

    def test_a_page_the_model_could_not_align_says_so(self):
        b = browse.blocks(self.con, pid=self.pid, book_key=self.book_of("tgt", self.PAIR),
                          side="tgt", page=4)
        self.assertEqual(b[0]["hint"]["page_status"], "alignment_failed")
        self.assertFalse(b[0]["paired"])


class _Same:
    """store.ro() for a test: the test's own connection, not closed afterwards."""

    def __init__(self, con):
        self.con = con

    def __enter__(self):
        return self.con

    def __exit__(self, *exc):
        return False


# ── the real dataset, when it is here ──────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent
REAL = REPO / aligned.DATASET


@unittest.skipUnless(REAL.is_dir() and (REAL / "export_summary.json").is_file(),
                     "the aligned-docMT-test folder is not in this checkout")
class TestRealDataset(SetuCase):
    """Checked against the dataset's own published numbers, not against itself."""

    def setUp(self):
        super().setUp()
        aligned._raw_index_cached.cache_clear()
        aligned._raw_pages.cache_clear()
        if not blocks.find_corpus():
            self.skipTest("the raw corpus (board_outputs) is not in this checkout")
        summary = json.loads((REAL / "export_summary.json").read_text(encoding="utf-8"))
        self.units = {s["pair"]: s["units"] for s in summary}
        full = os.environ.get("SETU_ALIGNED_FULL") == "1"
        names = sorted(self.units) if full else [
            n for n in ("AP10_sem1_en-te", "MH10_1_en-mr", "NCERT_1211_en-hi", "KT10_2_en-kn")
            if n in self.units]
        # A folder with just these pairs, as links, so the run stays short.
        self.dataset = self.dir / "subset" / aligned.DATASET
        self.dataset.mkdir(parents=True)
        for n in names:
            (self.dataset / n).symlink_to(REAL / n, target_is_directory=True)
        self.names = names
        with mock.patch.dict(os.environ, {"TULANA_ALIGNED_DIR": ""}):
            self.report = aligned.import_all(store.tx, self.dataset, log_fn=lambda m: None)

    def test_units_match_the_published_counts(self):
        self.assertEqual(self.report["errors"], [])
        self.assertEqual(self.report["raw_missing"], [])
        self.assertEqual(self.report["imported"], len(self.names))
        for p in aligned.pairs(self.con):
            with self.subTest(pair=p["pair_id"]):
                self.assertEqual(p["units"], self.units[p["pair_id"]])
                self.assertEqual(self.con.execute(
                    "SELECT COUNT(*) FROM setu_row WHERE pid = ? AND edited = 1",
                    (p["pid"],)).fetchone()[0], 0)

    def test_every_source_is_the_raw_ocr(self):
        """Rebuilt here independently: per page, the members' raw text joined by a
        blank line; the parts of a unit over a page break joined the same way."""
        checked = bad = 0
        where: dict[str, str] = {}
        for book, members, source in self.con.execute(
                "SELECT b.relpath, s.block_ids, s.source_text FROM setu_segment s"
                " JOIN setu_book b ON b.book_key = s.book_key"
                " WHERE b.dedup_key LIKE 'aligned:%' ORDER BY b.book_key, s.seq"):
            if book not in where:
                where[book] = aligned.raw_path_for(book)
            raw = aligned._raw_pages(where[book])
            parts: list[tuple[int, list[int]]] = []
            for m in json.loads(members):
                if parts and parts[-1][0] == m["page"]:
                    parts[-1][1].append(m["order"])
                else:
                    parts.append((m["page"], [m["order"]]))
            want = "\n\n".join(x for x in (
                normalise("\n\n".join(raw.get(pg, {}).get(o, "") for o in orders))
                for pg, orders in parts) if x)
            checked += 1
            bad += source != want
        self.assertGreater(checked, 1000)
        self.assertEqual(bad, 0, f"{bad} of {checked} passages are not what the OCR read")


if __name__ == "__main__":
    unittest.main()
