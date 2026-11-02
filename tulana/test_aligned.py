#!/usr/bin/env python3
"""Tests for the aligned document-MT test set (annotation/core/aligned.py).

    python3 test_aligned.py                         # synthetic pairs, seconds
    python3 test_aligned.py -v
    SETU_ALIGNED_FULL=1 python3 test_aligned.py     # also every real pair (~1 min)

What is protected, in order of how much damage a mistake would do:

* What the OCR read stays the source. The model's corrected text is the first
  revision of the passage, credited to the model, and is never counted — on
  screen, in Saved work or in an export — as a person's correction.
* Importing never overwrites work. A new delivery in the folder becomes a new
  set of projects; the projects of every earlier one, answers and all, stay.
  An aligned pair is never rebuilt by Setu's own aligner, with or without force.
* Files from outside are untrusted. A hostile relpath, a malformed file, a
  symlink out of the folder: that pair refuses to import, says so without
  quoting its contents, and every other pair still imports.
* Tulana Studio's eight tables are byte-identical afterwards.

The real dataset, when it is present, is checked against its own published
numbers — the pairs per book pair in export_summary.json, every page's counts,
the share aligned — and every passage's source against the raw OCR.
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
EQ = r"$A = \{1, 3, 5, 7, 9\}$"

# The raw books as the OCR delivered them, with a third page: answers the
# model was never sent (English) and could not align (Marathi).
EN_RAW = EN_PAGES + [[("Paragraph", "Text", "Answers to practice set 1.2")]]
MR_RAW = MR_PAGES + [[("Paragraph", "Text", "सरावसंच 1.2 ची उत्तरे")]]


# ── the dataset's shape, built small ───────────────────────────────────────

def _blk(order, label, btype, text, members, aid=None, rel=None, conf=None,
         part=None, note=None, flags=None, state=None, units=None):
    b = {"order": order, "label": label, "type": btype,
         "bbox_xyxy": [10, 20 + order * 30, 500, 60 + order * 30], "conf": 0.9,
         "text": text, "align_id": aid,
         "members": [{"order": m, "label": label,
                      "bbox_xyxy": [10, 20 + m * 30, 500, 60 + m * 30]} for m in members]}
    for key, val in (("align_relation", rel), ("align_confidence", conf), ("part", part),
                     ("align_note", note), ("align_state", state)):
        if val:
            b[key] = val
    if state:
        b["aligned"] = state == "aligned"
    if flags:
        b["flags"] = list(flags)
    if units:
        b["merged_units"] = list(units)
    return b


def _page(n, status, blocks_, meta=True):
    p = {"image": f"p{n:04d}.png", "width": 1000, "height": 1400, "page": n,
         "align_status": status, "blocks": blocks_}
    if meta:
        p["align_summary"] = _summary(p)
    return p


def _summary(p):
    """A page's counts, the way the exporter counts them: OCR blocks, by state."""
    c = {"text_blocks": 0, "aligned": 0, "unpaired": 0, "page_failed": 0, "not_processed": 0,
         "page_dropped": 0}
    for b in p["blocks"]:
        st = b.get("align_state")
        if st and st != "no_text":
            n = len(b["members"])
            c["text_blocks"] += n
            c[st] += n
    return c


def _file_summary(doc):
    c = {"text_blocks": 0, "aligned": 0, "unpaired": 0, "page_failed": 0, "not_processed": 0,
         "page_dropped": 0}
    for p in doc["pages"]:
        for k, v in _summary(p).items():
            c[k] += v
    c["aligned_pct"] = round(100 * c["aligned"] / c["text_blocks"], 2) if c["text_blocks"] else 0
    return c


def u(page, n, pair=PAIR):
    return f"{pair}/p{page:03d}/u{n}"


def aligned_docs(pair=PAIR):
    """One pair, written the way the paragraph-level export writes one.

    Covers: a model correction on each side, OCR blocks merged into one
    passage, two of the model's units joined into one paragraph that runs over
    a page break, an empty block, text the model could not pair, a page it was
    never sent, a page it could not align, a reviewer flag, and a retried page.
    """
    meta = {"pair_id": pair, "lang": "en", "language": "English", "other_book": "TT_MR_9",
            "model": "gemini-3.5-flash", "prompt_version": "v4", "thinking_level": "minimal"}
    joined = [u(0, 3, pair), u(0, 4, pair)]
    en = {"book": "TT_EN_9", "relpath": EN_REL, "num_pages": 3, "alignment": dict(meta), "pages": [
        _page(0, "ok", [
            _blk(0, "Chapter-title", "Title", "Sets 1", [0], u(0, 1, pair), "equivalent", "high",
                 state="aligned"),
            _blk(1, "Section-title", "SectionHeader", "1.1 INTRODUCTION", [1], u(0, 2, pair),
                 "equivalent", "high", state="aligned"),
            _blk(2, "Paragraph", "Text", "A set is a collection of objects.\n\n" + EQ, [2, 3],
                 u(0, 3, pair), "partial", "medium", part="1/2", state="aligned", units=joined),
            _blk(4, "Header", "PageHeader", "", [4], state="no_text"),
        ]),
        _page(1, "retried_ok", [
            _blk(0, "Section-title", "SectionHeader", "Practice set 1.2", [0], u(1, 1, pair),
                 "equivalent", "high", state="aligned"),
            _blk(1, "Solved-example", "Text", r"Ex (1) $B = \{2, 4, 6, 8, 10\}$ is finite.",
                 [1], u(0, 3, pair), "partial", "medium", part="2/2", state="aligned"),
            _blk(2, "Question", "Text", "Write the following sets.", [2], u(1, 2, pair),
                 "equivalent", "low", flags=[FLAG], state="aligned"),
            _blk(3, "Table", "Table", "<table><tr><td>Name</td></tr></table>", [3],
                 note="no_counterpart", state="unpaired"),
        ]),
        _page(2, "not_processed", [
            _blk(0, "Paragraph", "Text", "Answers to practice set 1.2", [0],
                 state="not_processed"),
        ])]}
    mr = {"book": "TT_MR_9", "relpath": MR_REL, "num_pages": 3,
          "alignment": dict(meta, lang="mr", language="Marathi", other_book="TT_EN_9"),
          "pages": [
              _page(0, "ok", [
                  _blk(0, "Chapter-title", "Title", "संच 1", [0], u(0, 1, pair),
                       "equivalent", "high", state="aligned"),
                  _blk(1, "Section-title", "SectionHeader", "1.1 प्रस्तावना", [1], u(0, 2, pair),
                       "equivalent", "high", state="aligned"),
                  _blk(2, "Paragraph", "Text", MR_MERGED + "\n\n" + EQ, [2, 3, 4], u(0, 3, pair),
                       "partial", "medium", state="aligned", units=joined),
                  _blk(5, "Header", "PageHeader", "", [5], state="no_text"),
              ]),
              _page(1, "ok", [
                  _blk(0, "Section-title", "SectionHeader", "सरावसंच 1.2", [0], u(1, 1, pair),
                       "equivalent", "high", state="aligned"),
                  _blk(1, "Solved-example", "Text",
                       r"उदा (1) $B = \{2, 4, 6, 8, 10\}$ सांत आहे.", [1], note="no_counterpart",
                       state="unpaired"),
                  _blk(2, "Question", "Text", "पुढील संच लिहा.", [2], u(1, 2, pair), "equivalent",
                       "low", flags=[FLAG], state="aligned"),
                  _blk(3, "Table", "Table", "<table><tr><td>नाव</td></tr></table>", [3],
                       note="no_counterpart", state="unpaired"),
              ]),
              _page(2, "alignment_failed", [
                  _blk(0, "Paragraph", "Text", "सरावसंच 1.2 ची उत्तरे", [0], state="page_failed"),
              ])]}
    for doc in (en, mr):
        doc["alignment"]["summary"] = _file_summary(doc)
    return en, mr


def unit_level_docs(pair=PAIR):
    """The same pair as the earlier, unit-level export: no states, no counts,
    no merged units — what Setu v7 imported."""
    en, mr = aligned_docs(pair)
    for doc in (en, mr):
        doc["alignment"].pop("summary", None)
        for p in doc["pages"]:
            p.pop("align_summary", None)
            for b in p["blocks"]:
                for k in ("align_state", "aligned", "merged_units"):
                    b.pop(k, None)
    return en, mr


class AlignedCase(SetuCase):
    """The synthetic textbooks, plus a raw-corpus folder and an aligned folder."""

    def setUp(self):
        super().setUp()
        self.raw = self.dir / "board_outputs"
        self.dataset = self.dir / aligned.DATASET
        for doc in (_parsed_book("TT_EN_9", EN_REL, EN_RAW, lambda t: t),
                    _parsed_book("TT_MR_9", MR_REL, MR_RAW, lambda t: t)):
            self.write(self.raw / Path(doc["relpath"]).with_suffix(".json"), doc)
        self.deliver(*aligned_docs())
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

    def deliver(self, en, mr, pair=PAIR, merge="paragraph"):
        """Put a delivery in the folder: the pair and its export summary."""
        self.write_pair(pair, ("en.json", en), ("mr.json", mr))
        units = len({b["align_id"] for p in en["pages"] for b in p["blocks"] if b.get("align_id")})
        entry = {"pair": pair, "files": [f"data/aligned/{pair}/CLASS-9/en.json",
                                         f"data/aligned/{pair}/CLASS-9/mr.json"],
                 "units": units, "units_before_merge": units + 1, "overlap_drops": 0}
        if merge:
            entry["merge"] = merge
        self.write(self.dataset / "export_summary.json", [entry])

    def run_import(self) -> dict:
        return aligned.import_all(store.tx, self.dataset, log_fn=lambda m: None)

    # -- reading back ----------------------------------------------------------
    def set_id(self) -> str:
        return aligned.current_set(self.con).get("set_id", "")

    def pid_of(self, pair=PAIR, set_id="") -> str:
        return aligned.is_imported(self.con, pair, set_id)

    def rows(self, pid=None) -> list[dict]:
        return [dict(r) for r in self.con.execute(
            "SELECT * FROM setu_row WHERE pid = ? ORDER BY seq", (pid or self.pid_of(),))]

    def seg(self, sid) -> dict:
        return dict(self.con.execute("SELECT * FROM setu_segment WHERE sid = ?",
                                     (sid,)).fetchone())

    def hint(self, sid) -> dict | None:
        r = self.con.execute("SELECT * FROM setu_hint WHERE sid = ?", (sid,)).fetchone()
        return dict(r) if r else None

    def book_of(self, side, pair=PAIR, set_id="") -> str:
        set_id = set_id or self.set_id()
        return self.con.execute("SELECT book_key FROM setu_book WHERE dedup_key = ?",
                                (f"{aligned.MARK}{set_id}:{pair}:{side}",)).fetchone()[0]

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
                  "setu_text", "setu_rev", "setu_aligned_set", "setu_aligned_pair",
                  "setu_page_meta", "setu_seg_part"):
            for r in self.con.execute(f"SELECT * FROM {t} ORDER BY 1, 2"):
                h.update(repr(tuple(r)).encode())
        return h.hexdigest()

    def legacy(self) -> dict:
        out = {}
        for t in LEGACY_TABLES:
            rows = self.con.execute(f"SELECT * FROM {t} ORDER BY 1").fetchall()
            out[t] = hashlib.sha256(repr([tuple(r) for r in rows]).encode()).hexdigest()
        return out


class _Same:
    """store.ro() for a test: the test's own connection, not closed afterwards."""

    def __init__(self, con):
        self.con = con

    def __enter__(self):
        return self.con

    def __exit__(self, *exc):
        return False


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
        self.assertEqual((self.report["level"], self.report["new_set"]), ("paragraph", True))
        self.assertTrue(self.pid)

    def test_every_pair_is_a_row_and_nothing_to_check_is_hidden(self):
        rows = self.rows()
        self.assertEqual([r["seq"] for r in rows], list(range(len(rows))), "a gap")
        two = [r for r in rows if r["src_sid"] and r["tgt_sid"]]
        self.assertEqual(len(two), 5, "five of the model's pairs in the fixture")
        for r in two:
            self.assertEqual(r["origin"], "aligned")
            self.assertEqual(self.hint(r["src_sid"])["align_id"],
                             self.hint(r["tgt_sid"])["align_id"])
        for r in rows:
            if not (r["src_sid"] and r["tgt_sid"]):
                self.assertEqual((r["origin"], r["confidence"]), ("unpaired", 0))
        self.assertEqual(len(rows), 9)
        # Each passage is in at most one row. The ones in none are exactly the
        # empty blocks and the page the model was never sent.
        for side, want_left_out in (("src", {"no_text", "not_processed"}), ("tgt", {"no_text"})):
            sids = [r[0] for r in self.con.execute(
                "SELECT sid FROM setu_segment WHERE book_key = ?", (self.book_of(side),))]
            held = [r[f"{side}_sid"] for r in rows if r[f"{side}_sid"]]
            self.assertEqual(len(held), len(set(held)), f"a {side} passage is in two rows")
            left_out = {self.hint(sid)["state"] for sid in set(sids) - set(held)}
            self.assertEqual(left_out, want_left_out, side)
        self.assertEqual(self.con.execute("SELECT n_rows FROM setu_project WHERE pid = ?",
                                          (self.pid,)).fetchone()[0], 9)

    def test_text_the_model_could_not_pair_stands_alone(self):
        states = {self.hint(r["tgt_sid"])["state"] for r in self.rows()
                  if r["tgt_sid"] and not r["src_sid"]}
        self.assertEqual(states, {"unpaired", "page_failed"})

    def test_target_only_passages_sit_where_they_fall(self):
        order = [(r["tgt_page"], self.seg(r["tgt_sid"])["ord_start"])
                 for r in self.rows() if r["tgt_sid"]]
        self.assertEqual(order, sorted(order), "the Marathi book read out of order")

    def test_the_source_is_what_the_ocr_read(self):
        raw = {p["page"]: {b["order"]: b["text"] for b in p["blocks"]}
               for p in _parsed_book("TT_MR_9", MR_REL, MR_RAW, lambda t: t)["pages"]}
        seg = self.seg(self.row_of(u(0, 3), "tgt")["tgt_sid"])
        self.assertEqual(seg["source_text"],
                         normalise(raw[0][2] + "\n\n" + raw[0][3] + "\n\n" + raw[0][4]))
        self.assertNotIn("होय", seg["source_text"], "the model's word leaked into the source")
        self.assertEqual(json.loads(seg["block_ids"]),
                         [{"page": 0, "order": 2}, {"page": 0, "order": 3},
                          {"page": 0, "order": 4}])
        en = self.seg(self.row_of(u(0, 2))["src_sid"])
        self.assertEqual(en["source_text"], "1.1 Introduction")

    def test_model_corrections_are_revision_one_by_the_model(self):
        for aid, side, text in ((u(0, 2), "src", "1.1 INTRODUCTION"),
                                (u(0, 3), "tgt", MR_MERGED + "\n\n" + EQ)):
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
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM setu_text").fetchone()[0], 2)
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
        r = self.row_of(u(0, 3), "tgt")
        with self.assertRaises(store.Conflict):
            annotate.save_text(self.con, r["rid"], "tgt", "something else", base_rev=0,
                               annotator="asha")
        self.assertEqual(self.text_row(r["rid"], "tgt"), (MR_MERGED + "\n\n" + EQ, 1, MODEL))

    def test_importing_again_changes_nothing(self):
        rid = self.rows()[0]["rid"]
        annotate.set_status(self.con, rid, "exact", annotator="asha")
        before = self.snapshot()
        rep = self.run_import()
        self.assertEqual((rep["imported"], rep["skipped"], rep["errors"], rep["new_set"]),
                         (0, 1, [], False))
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.rows()[0]["status"], "exact")

    def test_a_deleted_pair_comes_back_as_imported(self):
        r = self.row_of(u(0, 3), "tgt")
        annotate.save_text(self.con, r["rid"], "tgt", "हाताने दुरुस्त.", base_rev=1,
                           annotator="asha")
        workspace.delete_project(self.con, self.pid, annotator="admin")
        self.assertEqual(self.pid_of(), "")
        rep = self.run_import()
        self.assertEqual((rep["imported"], rep["errors"], rep["new_set"]), (1, [], False))
        r2 = self.row_of(u(0, 3), "tgt")
        text, rev, by = self.text_row(r2["rid"], "tgt")
        self.assertEqual((text, by), (MR_MERGED + "\n\n" + EQ, MODEL))
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

    def test_a_paragraph_over_a_page_break_is_one_passage(self):
        r = self.row_of(u(0, 3))
        seg = self.seg(r["src_sid"])
        self.assertEqual(json.loads(seg["block_ids"]),
                         [{"page": 0, "order": 2}, {"page": 0, "order": 3},
                          {"page": 1, "order": 1}])
        self.assertIn("is finite", seg["source_text"])
        h = self.hint(r["src_sid"])
        self.assertEqual((h["parts"], json.loads(h["pages"])), (2, [0, 1]))
        self.assertEqual(json.loads(h["units"]), [u(0, 3), u(0, 4)])
        on_p1 = self.con.execute("SELECT COUNT(*) FROM setu_segment WHERE book_key = ?"
                                 " AND page = 1", (self.book_of("src"),)).fetchone()[0]
        self.assertEqual(on_p1, 3, "the second part also became a passage of its own")

    def test_states_and_counts_are_kept(self):
        st = dict(self.con.execute(
            "SELECT h.state, COUNT(*) FROM setu_hint h JOIN setu_segment s ON s.sid = h.sid"
            " WHERE s.book_key = ? GROUP BY h.state", (self.book_of("tgt"),)).fetchall())
        self.assertEqual(st, {"aligned": 5, "no_text": 1, "unpaired": 2, "page_failed": 1})
        en, mr = aligned_docs()
        for side, doc in (("src", en), ("tgt", mr)):
            for p in doc["pages"]:
                m = aligned.page_meta(self.con, self.book_of(side), p["page"])
                self.assertEqual({k: m[k] for k in p["align_summary"]}, p["align_summary"])
                self.assertEqual((m["status"], m["width"], m["height"]),
                                 (p["align_status"], 1000, 1400))
        (p,) = aligned.pairs(self.con)
        # The viewer's figure: OCR text aligned, pages never sent left out.
        n = sum(d["alignment"]["summary"]["text_blocks"] - d["alignment"]["summary"]["not_processed"]
                for d in (en, mr))
        a = sum(d["alignment"]["summary"]["aligned"] for d in (en, mr))
        self.assertEqual(p["aligned_pct"], round(100 * a / n, 1))
        self.assertEqual(p["not_aligned"], 4)    # 1 + 1 unpaired tables, 1 example, 1 failed page

    def test_attention_pages_and_parts_for_the_page_view(self):
        src = self.book_of("src")
        tgt = self.book_of("tgt")
        self.assertEqual(aligned.attention_near(self.con, tgt, 0), (None, 1))
        self.assertEqual(aligned.attention_near(self.con, tgt, 1), (None, 2))
        self.assertEqual(aligned.attention_near(self.con, src, 2), (1, None))
        parts = aligned.parts_on_page(self.con, src, 1, self.pid, "src")
        cont = [p for p in parts if p["seg_page"] == 0]
        self.assertEqual(len(cont), 1, "the paragraph begun on page 1 is not drawn on page 2")
        self.assertEqual((cont[0]["part"], cont[0]["of_parts"], bool(cont[0]["rid"])), (2, 2, True))
        first = [p for p in aligned.parts_on_page(self.con, src, 0, self.pid, "src")
                 if p["sid"] == cont[0]["sid"]][0]
        self.assertEqual(len(first["members"]), 2, "the merged OCR boxes are not kept")
        self.assertTrue(all(0 <= v <= 1 for m in first["members"] for v in m))

    def test_the_page_api_gives_the_model_view(self):
        with mock.patch.object(store, "ro", lambda: _Same(self.con)):
            got = api.page_blocks(self.book_of("tgt"), 1, pid=self.pid)
        self.assertTrue(got["book"]["aligned"])
        self.assertEqual(got["page_meta"]["unpaired"], 2)
        self.assertEqual((got["attention_prev"], got["attention_next"]), (None, 2))
        self.assertEqual(len(got["parts"]), 4)
        self.assertEqual({p["state"] for p in got["parts"]}, {"aligned", "unpaired"})
        ex = next(b for b in got["blocks"] if b["label"] == "Solved-example")
        self.assertEqual(ex["hint"]["state"], "unpaired")

    def test_the_models_notes_reach_the_page(self):
        p1 = browse.blocks(self.con, pid=self.pid, book_key=self.book_of("src"),
                           side="src", page=1)
        q = next(b for b in p1 if b["label"] == "Question")
        self.assertEqual((q["hint"]["confidence"], q["hint"]["flags"], q["hint"]["page_status"]),
                         ("low", [FLAG], "retried_ok"))
        p0 = browse.blocks(self.con, pid=self.pid, book_key=self.book_of("src"),
                           side="src", page=0)
        par = next(b for b in p0 if b["label"] == "Paragraph")
        self.assertEqual((par["hint"]["parts"], par["hint"]["pages"]), (2, [1, 2]),
                         "pages are shown as printed, counting from 1")
        self.assertEqual(par["hint"]["units"], [u(0, 3), u(0, 4)])
        intro = next(b for b in p0 if b["label"] == "Section-title")
        self.assertTrue(intro["model_edited"])
        self.assertFalse(intro["edited"])
        self.assertIn("corrected by the model", browse.block_heading(intro))

    def test_the_row_list_agrees_with_the_row(self):
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
        self.assertEqual((v["src"]["hint"]["page_status"], v["src"]["hint"]["state"]),
                         ("retried_ok", "aligned"))
        self.assertEqual(v["tgt"]["hint"]["page_status"], "ok")
        self.assertAlmostEqual(v["confidence"], aligned.CONFIDENCE["low"])
        v = self.view(self.row_of(u(0, 3))["rid"])
        self.assertEqual(v["src"]["hint"]["units"], [u(0, 3), u(0, 4)])

    def test_exports_say_who_corrected_what(self):
        recs = {r["unit_id"]: r for r in exporters.records(self.con, self.pid) if r["unit_id"]}
        self.assertEqual(len(recs), 5)
        x = recs[u(0, 3)]
        self.assertTrue(set(exporters.FIELDS) <= set(x))
        self.assertTrue(x["target_model_corrected"])
        self.assertFalse(x["target_edited"])
        self.assertFalse(x["source_model_corrected"])
        self.assertEqual(x["model_units"], f"{u(0, 3)} {u(0, 4)}")
        self.assertEqual(recs[u(1, 2)]["model_units"], "")
        self.assertEqual(recs[u(1, 2)]["model_flags"], FLAG, "a note on both sides, twice")
        annotate.save_text(self.con, self.row_of(u(0, 3))["rid"], "src",
                           "A set is a well-defined collection of objects.", base_rev=0,
                           annotator="asha")
        x = {r["unit_id"]: r for r in exporters.records(self.con, self.pid)}[u(0, 3)]
        self.assertTrue(x["source_edited"])
        self.assertFalse(x["source_model_corrected"])

    def test_maths_starting_with_equals_stays_text_in_the_spreadsheet(self):
        """openpyxl writes a string that starts with "=" as a formula, which
        Excel would run: a line of maths opened as #NAME?, or worse."""
        try:
            from openpyxl import load_workbook
        except ImportError:                                  # pragma: no cover
            self.skipTest("openpyxl is not installed")
        import io
        r = self.row_of(u(0, 3), "tgt")
        text = '= (1 + 80) + (2 + 79) =HYPERLINK("http://example.invalid","x")'
        annotate.save_text(self.con, r["rid"], "tgt", text, base_rev=1, annotator="asha")
        buf = io.BytesIO()
        exporters.get("xlsx").writer(exporters.records(self.con, self.pid), buf, {"project": "=1+1"})
        buf.seek(0)
        wb = load_workbook(buf)
        cells = [c for row in wb["Pairs"].iter_rows() for c in row]
        self.assertFalse([c.coordinate for c in cells if c.data_type == "f"])
        self.assertIn(text, [c.value for c in cells])
        self.assertIn("=1+1", [c.value for row in wb["About"].iter_rows() for c in row])

    def test_unpairing_keeps_the_models_credit(self):
        r = self.row_of(u(0, 3), "tgt")
        annotate.split_row(self.con, r["rid"], annotator="asha")
        holder = self.con.execute("SELECT rid, edited FROM setu_row WHERE tgt_sid = ?",
                                  (r["tgt_sid"],)).fetchone()
        self.assertNotEqual(holder[0], r["rid"], "the passage did not move")
        self.assertEqual(self.text_row(holder[0], "tgt")[::2], (MR_MERGED + "\n\n" + EQ, MODEL),
                         "moving the passage made the model's text a person's")
        self.assertEqual(holder[1], 0)
        self.assertTrue(self.view(holder[0])["tgt"]["model_edited"])

    def test_lists_name_aligned_pairs_as_such(self):
        repo = resume.ResumeRepo(self.con)
        mine = next(p for p in repo.workbench()["projects"] if p["pid"] == self.pid)
        self.assertTrue(mine["aligned"])
        self.assertFalse(mine["aligned_earlier"])
        self.assertIn("aligned test set, paragraph-level", mine["label"])
        self.assertTrue(next(p for p in repo.projects_with_work()
                             if p["pid"] == self.pid)["aligned"])
        (p,) = aligned.pairs(self.con)
        self.assertEqual((p["pair_id"], p["units"], p["flagged"], p["answered"], p["n_rows"]),
                         (PAIR, 5, 1, 0, 9))
        st = aligned.status(self.con, self.dataset)
        self.assertEqual((st["on_disk"], st["imported"], st["waiting"], st["new_set"],
                          st["level"]), (1, 1, [], False, "paragraph"))
        self.assertEqual(st["current"]["level"], "paragraph")
        saved = repo.saved_rows(pid=self.pid, limit=50)
        x = {r["rid"]: r for r in saved["rows"]}[self.row_of(u(0, 3))["rid"]]
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


# ── a new delivery in the same folder ──────────────────────────────────────

class TestVersions(AlignedCase):
    """A re-export of the same pairs is a new set. Nothing done in the old one
    is touched, lost or hidden."""

    def deliver_unit_level(self):
        shutil.rmtree(self.dataset)
        self.deliver(*unit_level_docs(), merge="")

    def test_a_new_delivery_is_a_new_set_and_the_old_work_stays(self):
        self.deliver_unit_level()
        first = self.run_import()
        self.assertEqual((first["imported"], first["level"]), (1, "unit"))
        old_pid, old_set = self.pid_of(), self.set_id()
        rid = self.rows(old_pid)[0]["rid"]
        annotate.set_status(self.con, rid, "exact", annotator="asha")
        old_rows = self.rows(old_pid)
        # The paragraph-level export arrives in the same folder.
        shutil.rmtree(self.dataset)
        self.deliver(*aligned_docs())
        st = aligned.status(self.con, self.dataset)
        self.assertTrue(st["new_set"])
        self.assertEqual(st["waiting"], [PAIR])
        rep = self.run_import()
        self.assertEqual((rep["imported"], rep["new_set"], rep["level"]), (1, True, "paragraph"))
        new_set = self.set_id()
        self.assertNotEqual(new_set, old_set)
        new_pid = self.pid_of()
        self.assertNotEqual(new_pid, old_pid)
        self.assertEqual(self.rows(old_pid), old_rows, "the earlier delivery's rows changed")
        self.assertEqual(self.rows(old_pid)[0]["status"], "exact")
        self.assertEqual([p["pid"] for p in aligned.pairs(self.con)], [new_pid])
        earlier = aligned.earlier_pairs(self.con)
        self.assertEqual([(p["pid"], p["answered"], p["set_label"]) for p in earlier],
                         [(old_pid, 1, "unit-level")])
        wb = {p["pid"]: p for p in resume.ResumeRepo(self.con).workbench()["projects"]}
        self.assertTrue(wb[old_pid]["aligned_earlier"])
        self.assertIn("earlier delivery", wb[old_pid]["label"])
        saved = {p["pid"]: p for p in resume.ResumeRepo(self.con).projects_with_work()}
        self.assertEqual((saved[old_pid]["aligned_earlier"], saved[old_pid]["aligned_label"]),
                         (True, "unit-level"))
        self.assertFalse(saved[new_pid]["aligned_earlier"])
        self.assertFalse(wb[new_pid]["aligned_earlier"])
        # The earlier pair holds work, the new one does not: the work comes
        # first, however many untouched projects a delivery just added.
        first = resume.ResumeRepo(self.con).workbench(limit=1)["projects"]
        self.assertEqual([p["pid"] for p in first], [old_pid])
        # So does a project this annotator only looked at — for them.
        resume.remember_place(self.con, new_pid, "Ravi", {"src_page": 3})
        for who, want in (("ravi", {old_pid, new_pid}), ("asha", {old_pid})):
            got = resume.ResumeRepo(self.con).workbench(annotator=who, limit=2)["projects"]
            self.assertEqual({p["pid"] for p in got[:len(want)]}, want, who)
        # Books of the two sets never collide.
        keys = [r[0] for r in self.con.execute(
            "SELECT dedup_key FROM setu_book WHERE dedup_key LIKE 'aligned:%' ORDER BY 1")]
        self.assertEqual(len(keys), 4)
        self.assertEqual({aligned.parse_mark(k)[0] for k in keys}, {old_set, new_set})

    def test_an_earlier_pair_nobody_touched_is_not_listed(self):
        self.deliver_unit_level()
        self.run_import()
        shutil.rmtree(self.dataset)
        self.deliver(*aligned_docs())
        self.run_import()
        self.assertEqual(aligned.earlier_pairs(self.con), [])

    def test_the_same_files_again_are_the_same_set(self):
        self.run_import()
        before = self.snapshot()
        for f in self.dataset.rglob("*.json"):           # touched, not changed
            os.utime(f, None)
        aligned._DESC_CACHE.clear()
        rep = self.run_import()
        self.assertEqual((rep["imported"], rep["new_set"]), (0, False))
        self.assertEqual(self.snapshot(), before)

    def test_crlf_line_endings_are_the_same_delivery(self):
        """Git for Windows checks text out with CRLF: the same delivery must
        not look new on one machine and old on another."""
        summary = self.dataset / "export_summary.json"
        text = json.dumps(json.loads(summary.read_text(encoding="utf-8")), indent=1)
        summary.write_bytes(text.encode("utf-8"))
        self.run_import()
        first = self.set_id()
        summary.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
        aligned._DESC_CACHE.clear()
        rep = self.run_import()
        self.assertEqual((rep["new_set"], rep["imported"], self.set_id()), (False, 0, first))

    def test_one_changed_byte_is_a_new_delivery(self):
        self.run_import()
        first = self.set_id()
        en, mr = aligned_docs()
        mr["pages"][1]["blocks"][2]["text"] = "पुढील संच लिहा!"
        self.deliver(en, mr)
        rep = self.run_import()
        self.assertTrue(rep["new_set"])
        self.assertNotEqual(self.set_id(), first)
        self.assertEqual(len(aligned.pairs(self.con)), 1)

    def test_switching_back_reuses_the_earlier_set(self):
        self.run_import()
        para = self.set_id()
        self.deliver_unit_level()
        self.run_import()
        unit = self.set_id()
        shutil.rmtree(self.dataset)
        self.deliver(*aligned_docs())
        rep = self.run_import()
        self.assertEqual((rep["new_set"], rep["imported"], self.set_id()), (False, 0, para))
        self.assertNotEqual(unit, para)

    def make_v7(self) -> str:
        """Turn the imported unit-level pair into what Setu v7 left behind:
        books keyed 'aligned:<pair>:<side>', no states, units, page counts or
        passage parts, and no record of sets at all. Returns the project id."""
        pid, sid = self.pid_of(), self.set_id()
        for (key,) in self.con.execute("SELECT dedup_key FROM setu_book WHERE dedup_key LIKE ?",
                                       (f"{aligned.MARK}{sid}:%",)).fetchall():
            self.con.execute("UPDATE setu_book SET dedup_key = ? WHERE dedup_key = ?",
                             (key.replace(f"{sid}:", ""), key))
        books = [r[0] for r in self.con.execute(
            "SELECT book_key FROM setu_book WHERE dedup_key LIKE ?", (aligned.MARK + "%",))]
        for key in books:
            self.con.execute("DELETE FROM setu_seg_part WHERE book_key = ?", (key,))
            self.con.execute("DELETE FROM setu_page_meta WHERE book_key = ?", (key,))
            self.con.execute("UPDATE setu_hint SET state = '', units = '[]' WHERE sid IN"
                             " (SELECT sid FROM setu_segment WHERE book_key = ?)", (key,))
        self.con.execute("DELETE FROM setu_aligned_pair")
        self.con.execute("DELETE FROM setu_aligned_set")
        aligned._DESC_CACHE.clear()
        return pid

    def launch(self) -> str:
        """What the launcher prints at start, with this test's folder in place."""
        import contextlib
        import io
        import launch_annotation
        out = io.StringIO()
        with mock.patch.dict(os.environ, {"TULANA_ALIGNED_DIR": str(self.dataset)}), \
                contextlib.redirect_stdout(out):
            launch_annotation.import_aligned_set()
        return out.getvalue()

    def test_setu_v7_imports_become_the_legacy_set(self):
        self.deliver_unit_level()
        self.run_import()
        pid = self.make_v7()
        rid = self.rows(pid)[0]["rid"]
        annotate.set_status(self.con, rid, "unclear", annotator="asha")
        # The unit-level files are still in the folder: they are the legacy
        # set's own, and must not be imported a second time.
        st = aligned.status(self.con, self.dataset)
        self.assertEqual((st["waiting"], st["new_set"]), ([], False))
        rep = self.run_import()
        self.assertEqual((rep["imported"], rep["new_set"], rep["set"]),
                         (0, False, aligned.LEGACY_SET))
        self.assertEqual([p["pid"] for p in aligned.pairs(self.con)], [pid])
        # Then the paragraph-level delivery arrives.
        shutil.rmtree(self.dataset)
        self.deliver(*aligned_docs())
        rep = self.run_import()
        self.assertEqual((rep["imported"], rep["new_set"]), (1, True))
        (p,) = aligned.earlier_pairs(self.con)
        self.assertEqual((p["pid"], p["set_id"], p["answered"]), (pid, aligned.LEGACY_SET, 1))
        self.assertEqual(self.rows(pid)[0]["status"], "unclear")

    def test_the_launcher_upgrades_a_setu_v7_database(self):
        self.deliver_unit_level()
        self.run_import()
        pid = self.make_v7()
        annotate.set_status(self.con, self.rows(pid)[0]["rid"], "exact", annotator="asha")
        before = self.rows(pid)
        legacy = self.legacy()
        shutil.rmtree(self.dataset)
        self.deliver(*aligned_docs())
        said = self.launch()
        self.assertIn("paragraph-level): a new delivery — importing 1 pair(s)", said)
        self.assertIn("1 pair(s) of an earlier delivery hold answers or corrections", said)
        self.assertEqual(len(aligned.pairs(self.con)), 1)
        self.assertNotEqual(aligned.pairs(self.con)[0]["pid"], pid)
        self.assertEqual([p["pid"] for p in aligned.earlier_pairs(self.con)], [pid])
        self.assertEqual(self.rows(pid), before, "the v7 project changed")
        self.assertEqual(self.legacy(), legacy)
        self.assertIn("(paragraph-level): 1 pair(s) ready", self.launch())

    def test_setu_v7_with_its_own_folder_still_lists_every_pair(self):
        """New code, old folder: the v7 pairs are the delivery in the folder,
        so they stay the ones listed — not hidden as an earlier version."""
        self.deliver_unit_level()
        self.run_import()
        pid = self.make_v7()
        said = self.launch()
        self.assertIn("aligned test set (unit-level): 1 pair(s) ready", said)
        self.assertEqual([p["pid"] for p in aligned.pairs(self.con)], [pid])
        self.assertEqual(aligned.current_set(self.con)["set_id"], aligned.LEGACY_SET)
        self.assertEqual(aligned.earlier_pairs(self.con), [])

    def test_a_folder_put_back_lists_its_own_pairs(self):
        self.run_import()
        para = self.pid_of()
        self.deliver_unit_level()
        self.run_import()
        unit = self.pid_of()
        self.assertNotEqual(unit, para)
        shutil.rmtree(self.dataset)
        self.deliver(*aligned_docs())
        self.assertIn("1 pair(s) ready", self.launch())
        self.assertEqual([p["pid"] for p in aligned.pairs(self.con)], [para])

    def test_a_v7_book_still_turns_its_pages(self):
        """No passage parts or page counts were stored for it: the page view
        falls back to the passages, as before."""
        self.deliver_unit_level()
        self.run_import()
        pid = self.make_v7()
        self.run_import()
        src = self.con.execute("SELECT src_book FROM setu_project WHERE pid = ?",
                               (pid,)).fetchone()[0]
        with mock.patch.object(store, "ro", lambda: _Same(self.con)):
            got = api.page_blocks(src, 0, pid=pid)
        self.assertTrue(got["book"]["aligned"])
        self.assertEqual((got["parts"], got["page_meta"]), ([], None))
        self.assertEqual((got["prev_page"], got["next_page"]), (None, 1))
        self.assertTrue(got["blocks"])

    def test_the_status_never_writes(self):
        self.deliver_unit_level()
        before = self.snapshot()
        st = aligned.status(self.con, self.dataset)
        self.assertEqual((st["waiting"], st["new_set"]), ([PAIR], True))
        self.assertEqual(self.snapshot(), before)


def v2_docs(pair=PAIR, reason="map_wrong"):
    """The same pair as the aligner team's v2 delivery would write it.

    English page 2 dropped (its page map was wrong): every block on it is
    ``page_dropped``, and every unit with an English part there — including
    the paragraph that begins on page 1 — loses its id on both sides. And the
    model put the bold back on one Marathi heading (``markup_restored``).
    """
    en, mr = aligned_docs(pair)
    gone = {b["align_id"] for b in en["pages"][1]["blocks"] if b.get("align_id")}
    en["pages"][1].update(align_status="dropped_page_mismatch", drop_reason=reason,
                          align_status_v1="retried_ok",
                          drop_detail={"mapped_page": 1, "matched_pages": {"3": 2}})
    for doc in (en, mr):
        for p in doc["pages"]:
            for b in p["blocks"]:
                on_dropped = doc is en and p is en["pages"][1]
                if b.get("align_id") in gone or (on_dropped and b.get("align_state") != "no_text"):
                    b.update(align_id=None, aligned=False, align_state="page_dropped",
                             align_note="page_dropped" if on_dropped else "counterpart_page_dropped")
                    for k in ("align_relation", "align_confidence", "merged_units", "part"):
                        b.pop(k, None)
    head = mr["pages"][0]["blocks"][1]
    head.update(text="**1.1 प्रस्तावना**", markup_restored=True)
    for doc in (en, mr):
        for p in doc["pages"]:
            p["align_summary"] = _summary(p)
        doc["alignment"]["summary"] = _file_summary(doc)
    return en, mr


class TestV2Delivery(AlignedCase):
    """What the aligner team's v2 changes mean for an annotator: dropped pages
    stay in the books but are not work, and count as not aligned in the share,
    as in their viewer; restored markup is the model's correction."""

    def setUp(self):
        super().setUp()
        self.deliver(*v2_docs())
        entries = json.loads((self.dataset / "export_summary.json").read_text(encoding="utf-8"))
        for e in entries:
            e.update(units=5, units_before_merge=6,
                     v2={"units_removed": 3, "markup_restored": 1, "pages_dropped": 1})
        self.write(self.dataset / "export_summary.json", entries)
        self.report = self.run_import()
        self.pid = self.pid_of()

    def test_the_delivery_is_named_v2_and_counted_as_v2(self):
        self.assertEqual(self.report["errors"], [])
        st = aligned.status(self.con, self.dataset)
        self.assertEqual((st["label"], st["segments"], st["units"]),
                         ("paragraph-level v2", 2, 6))
        self.assertIn("paragraph-level v2)", aligned.pairs(self.con)[0]["name"])

    def test_dropped_text_stays_in_the_book_but_is_not_a_row(self):
        rows = self.rows()
        self.assertEqual(len(rows), 5)
        self.assertEqual(sum(1 for r in rows if r["src_sid"] and r["tgt_sid"]), 2)
        held = {r["src_sid"] for r in rows} | {r["tgt_sid"] for r in rows}
        dropped = [r[0] for r in self.con.execute(
            "SELECT h.sid FROM setu_hint h WHERE h.state = 'page_dropped'"
            "   AND h.pair_id = ?", (PAIR,))]
        self.assertEqual(len(dropped), 8)        # 5 English passages, 3 Marathi — all kept
        self.assertFalse(held & set(dropped), "a dropped passage became work")

    def test_page_counts_and_the_reason_a_page_was_dropped(self):
        m = aligned.page_meta(self.con, self.book_of("src"), 1)
        self.assertEqual((m["status"], m["drop_reason"], m["page_dropped"], m["aligned"]),
                         ("dropped_page_mismatch", "map_wrong", 4, 0))
        m = aligned.page_meta(self.con, self.book_of("tgt"), 1)
        self.assertEqual((m["page_dropped"], m["unpaired"], m["text_blocks"]), (2, 2, 4))

    def test_dropped_text_counts_as_not_aligned_as_in_the_viewer(self):
        (p,) = aligned.pairs(self.con)
        # aligned 4 of 19 OCR text blocks, less the 1 never sent
        self.assertEqual(p["aligned_pct"], round(100 * 4 / 18, 1))
        self.assertEqual((p["dropped"], p["pages_dropped"], p["markup_restored"]), (11, 1, 1))

    def test_dropped_pages_are_not_pages_to_work_on(self):
        self.assertEqual(aligned.attention_near(self.con, self.book_of("src"), 0), (None, None))
        self.assertEqual(aligned.attention_near(self.con, self.book_of("tgt"), 0), (None, 1))

    def test_restored_markup_is_the_models_correction_and_says_so(self):
        b = next(x for x in browse.blocks(self.con, pid=self.pid, book_key=self.book_of("tgt"),
                                          side="tgt", page=0) if x["label"] == "Section-title")
        self.assertTrue(b["hint"]["markup"])
        self.assertTrue(b["model_edited"])
        self.assertEqual(self.seg(b["sid"])["source_text"], "1.1 प्रस्तावना")
        v = self.view(b["rid"])
        self.assertTrue(v["tgt"]["hint"]["markup"])
        self.assertFalse(v["src"]["hint"]["markup"])

    def test_an_unknown_drop_reason_is_still_a_dropped_page(self):
        en, mr = v2_docs("ODDDROP_en-mr", reason="<script>alert(1)</script>")
        self.write_pair("ODDDROP_en-mr", ("en.json", en), ("mr.json", mr))
        self.assertEqual(self.run_import()["errors"], [])
        m = aligned.page_meta(self.con, self.book_of("src", "ODDDROP_en-mr"), 1)
        self.assertEqual((m["status"], m["drop_reason"]), ("dropped_page_mismatch", "other"))


class TestPageTurning(AlignedCase):
    """A page that holds nothing but the rest of a passage from the page before
    is still a page: the buttons stop on it and the page view draws it."""

    def setUp(self):
        super().setUp()
        en, mr = aligned_docs()
        en["pages"][1]["blocks"] = [b for b in en["pages"][1]["blocks"] if b.get("part") == "2/2"]
        en["pages"][1]["align_summary"] = _summary(en["pages"][1])
        en["alignment"]["summary"] = _file_summary(en)
        self.deliver(en, mr)
        self.assertEqual(self.run_import()["errors"], [])
        self.pid = self.pid_of()
        self.src = self.book_of("src")

    def page(self, n):
        with mock.patch.object(store, "ro", lambda: _Same(self.con)):
            return api.page_blocks(self.src, n, pid=self.pid)

    def test_the_buttons_stop_on_it(self):
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM setu_segment WHERE book_key = ?"
                                          " AND page = 1", (self.src,)).fetchone()[0], 0)
        self.assertEqual(self.page(0)["next_page"], 1)
        self.assertEqual(self.page(2)["prev_page"], 1)

    def test_it_draws_the_rest_of_the_passage(self):
        got = self.page(1)
        self.assertEqual(got["blocks"], [])
        (part,) = got["parts"]
        self.assertEqual((part["part"], part["of"], part["seg_page"]), (2, 2, 0))
        self.assertTrue(part["rid"] and part["paired"])
        self.assertEqual(got["page_meta"]["aligned"], 1)


# ── the corpus reader never mistakes the aligned folder for raw books ──────

class TestCorpusIgnoresTheSet(AlignedCase):

    def test_an_aligned_file_is_not_raw_layout(self):
        f = next(self.dataset.rglob("en.json"))
        self.assertFalse(blocks._looks_like_layout(f))
        self.assertTrue(blocks._is_junk(Path(aligned.DATASET) / PAIR / "x.json"))
        raw = next(self.raw.rglob("*.json"))
        self.assertTrue(blocks._looks_like_layout(raw))

    def test_the_raw_lookup_stays_inside_the_corpus(self):
        outside = self.dir / "secret.json"
        self.write(outside, {"relpath": "../secret.pdf", "pages": []})
        for rel in ("../secret.pdf", "../../etc/passwd", "/etc/passwd", "C:\\x\\y.pdf",  # hostile examples, never opened
                    "a/../../secret.pdf", "TEST/\x00.pdf", "", None, 42):
            with self.subTest(rel=rel):
                self.assertEqual(aligned.raw_path_for(rel), "")
        self.assertTrue(aligned.raw_path_for(EN_REL).endswith("TT_EN_9.json"))

    def test_marks_parse_both_ways(self):
        self.assertEqual(aligned.parse_mark("aligned:as_X:MH10_1_en-mr:src"),
                         ("as_X", "MH10_1_en-mr", "src"))
        self.assertEqual(aligned.parse_mark("aligned:MH10_1_en-mr:tgt"),
                         (aligned.LEGACY_SET, "MH10_1_en-mr", "tgt"))
        for bad in ("", None, "abc123", "aligned:", "aligned:x:y:z:src", "aligned:x:mid"):
            self.assertIsNone(aligned.parse_mark(bad))


# ── where the data lives: data/aligned_v2 first, the older folder after ────

class TestWhereTheDataLives(AlignedCase):

    def make(self, *parts) -> Path:
        folder = self.dir / "repo" / Path(*parts)
        self.write(folder / PAIR / "CLASS-9" / "en.json", {"pages": []})
        return folder

    def test_data_aligned_v2_is_found_and_preferred(self):
        new = self.make("data", "aligned_v2")
        old = self.make(aligned.DATASET)
        repo = self.dir / "repo"
        self.assertEqual(aligned.find_dataset(repo), new.resolve())
        shutil.rmtree(new)
        self.assertEqual(aligned.find_dataset(repo), old.resolve())

    def test_a_repository_named_as_the_root_is_not_taken_for_the_data(self):
        repo = self.dir / "repo"
        self.write(repo / "board_outputs" / "x" / "raw.json", {"pages": [], "relpath": "x.pdf"})
        new = self.make("data", "aligned_v2")
        self.assertEqual(aligned.find_dataset(repo), new.resolve())

    def test_the_environment_wins(self):
        self.make("data", "aligned_v2")
        other = self.make("elsewhere")
        with mock.patch.dict(os.environ, {"TULANA_ALIGNED_DIR": str(other)}):
            self.assertEqual(aligned.find_dataset(self.dir / "repo"), other.resolve())

    def test_book_keys_do_not_depend_on_the_folder(self):
        # The key namespace is fixed, so moving the data never orphans work.
        from annotation.core import ids
        self.assertEqual(aligned.book_key_for("as_X", PAIR, "src", "a/b.pdf"),
                         ids.book_key(f"aligned-docMT-test/as_X/{PAIR}/src/a/b.pdf"))

    def test_the_corpus_reader_skips_the_new_folder_and_any_aligned_file(self):
        import sqlite3
        self.assertTrue(blocks._is_junk(Path("data") / "aligned_v2" / PAIR / "x.json"))

        def books_read():
            con = sqlite3.connect(":memory:")
            try:
                return blocks.ingest(con, corpus=self.raw, data_dir=self.dir, log=lambda *a: None)["books"]
            finally:
                con.close()

        before = books_read()
        # an aligned export dropped inside the raw corpus is still not a raw book
        doc = json.loads(next(self.dataset.rglob("en.json")).read_text(encoding="utf-8"))
        self.assertIn("alignment", doc)
        self.write(self.raw / "stray" / "copy.json", doc)
        self.assertEqual(books_read(), before)


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
        self.assertEqual([e["pair"] for e in rep["errors"]], [aligned.shown_name(name)])
        self.assertFalse(self.con.execute("SELECT COUNT(*) FROM setu_book WHERE dedup_key LIKE ?",
                                          (f"{aligned.MARK}%:{name}:%",)).fetchone()[0],
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
        for i, rel in enumerate(("../../../etc/passwd.pdf", "/etc/passwd.pdf",  # hostile examples
                                 "C:\\Windows\\win.ini", "TEST/\x00.pdf", "a/../../b.pdf")):
            with self.subTest(rel=rel):
                def bad(en, mr, rel=rel):
                    en["relpath"] = rel
                self.check_refused(f"BADREL{i}_en-mr", *self.mutated(bad))

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

    def test_bad_metadata_is_dropped_not_trusted(self):
        """Counts, states and unit lists are optional: wrong ones are ignored
        and worked out again from the blocks, and the pair still imports."""
        en, mr = aligned_docs("ODDMETA_en-mr")
        mr["alignment"]["summary"] = {"text_blocks": -5, "aligned": "lots"}
        mr["pages"][0]["align_summary"] = {"text_blocks": 1e9}
        # Well formed, and false: it says nothing on the page is unpaired.
        mr["pages"][1]["align_summary"] = {"text_blocks": 4, "aligned": 4, "unpaired": 0,
                                           "page_failed": 0, "not_processed": 0}
        mr["pages"][1]["blocks"][1]["align_state"] = "<script>alert(1)</script>"
        mr["pages"][0]["blocks"][2]["merged_units"] = "not a list"
        en["pages"][0]["blocks"][2]["merged_units"] = [{"x": 1}, "ok/p000/u3", "../../evil"]
        self.write_pair("ODDMETA_en-mr", ("en.json", en), ("mr.json", mr))
        rep = self.run_import()
        self.assertEqual(rep["errors"], [])
        pid = self.pid_of("ODDMETA_en-mr")
        tgt = self.book_of("tgt", "ODDMETA_en-mr")
        m = aligned.page_meta(self.con, tgt, 1)
        self.assertEqual((m["text_blocks"], m["unpaired"]), (4, 2), "counts not worked out again")
        self.assertEqual(aligned.attention_near(self.con, tgt, 0), (None, 1),
                         "a false count hid a page with text to pair")
        m0 = aligned.page_meta(self.con, tgt, 0)
        self.assertEqual((m0["text_blocks"], m0["aligned"]), (5, 5))   # 1 + 1 + 3 members
        states = {r[0] for r in self.con.execute(
            "SELECT h.state FROM setu_hint h JOIN setu_segment s ON s.sid = h.sid"
            " WHERE s.book_key = ?", (tgt,))}
        self.assertTrue(states <= set(aligned.STATES), states)
        units = [json.loads(r[0]) for r in self.con.execute(
            "SELECT h.units FROM setu_hint h JOIN setu_segment s ON s.sid = h.sid"
            " WHERE s.book_key = ?", (self.book_of("src", "ODDMETA_en-mr"),))]
        self.assertIn(["ok/p000/u3"], units)
        self.assertTrue(pid)

    def test_nan_and_infinity_never_reach_a_response(self):
        """Python's json reads NaN and Infinity. One in a response would make
        the page's JSON unsendable (FastAPI refuses it) — a page nobody can open."""
        en, mr = aligned_docs("ODDNUM_en-mr")
        en["pages"][0]["width"] = float("nan")
        en["pages"][0]["height"] = float("inf")
        en["pages"][0]["blocks"][2]["members"][0]["bbox_xyxy"] = [float("nan"), 0, 1e308, 5]
        mr["pages"][1]["width"] = -1000
        self.write_pair("ODDNUM_en-mr", ("en.json", en), ("mr.json", mr))
        self.assertEqual(self.run_import()["errors"], [])
        pid = self.pid_of("ODDNUM_en-mr")
        with mock.patch.object(store, "ro", lambda: _Same(self.con)):
            for side, page in (("src", 0), ("src", 1), ("tgt", 1)):
                got = api.page_blocks(self.book_of(side, "ODDNUM_en-mr"), page, pid=pid)
                json.dumps(got, allow_nan=False)                  # raises on NaN or Infinity
                for part in got["parts"]:
                    self.assertTrue(all(0 <= v <= 1 for v in part["box"]), part)

    def test_corrupt_json(self):
        en, mr = aligned_docs("BADJSON_en-mr")
        self.check_refused("BADJSON_en-mr", ("en.json", "{ this is not json"), ("mr.json", mr))

    def test_an_unsafe_folder_name(self):
        en, mr = aligned_docs()
        self.check_refused("bad name; rm -rf", ("en.json", en), ("mr.json", mr))

    @unittest.skipIf(os.name == "nt", "Windows does not allow control characters in names")
    def test_a_folder_name_cannot_drive_the_terminal(self):
        en, mr = aligned_docs()
        name = "\x1b]0;owned\x07evil\x1b[2J"
        rep = self.check_refused(name, ("en.json", en), ("mr.json", mr))
        shown = rep["errors"][0]["pair"]
        self.assertFalse(any(ord(ch) < 32 or ord(ch) == 127 for ch in shown), shown)

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
                   _page(0, "not_processed", [_blk(0, "Paragraph", "Text", "Foreword", [0],
                                                   state="not_processed")]),
                   _page(1, "ok", [
                       _blk(0, "Paragraph", "Text", "Numbers are everywhere.", [0], u(1, 1, p),
                            "equivalent", "high", state="aligned"),
                       _blk(1, "Paragraph", "Text", "Count them.", [1], u(1, 2, p),
                            "equivalent", "high", state="aligned")]),
                   _page(2, "ok", [
                       _blk(0, "Paragraph", "Text", "సంఖ్యలు అంతటా ఉన్నాయి.", [0], u(1, 1, p),
                            "equivalent", "high", state="aligned"),
                       _blk(1, "Paragraph", "Text", "లెక్కించండి.", [1], u(1, 2, p),
                            "equivalent", "high", state="aligned")]),
                   _page(3, "ok", [
                       _blk(0, "Paragraph", "Text", "A prime has two factors.", [0],
                            note="no_counterpart", state="unpaired")]),
                   _page(4, "alignment_failed", [
                       _blk(0, "Paragraph", "Text", "ప్రధాన సంఖ్యకు రెండు కారణాంకాలు.", [0],
                            state="page_failed")]),
               ]}
        doc["alignment"]["summary"] = _file_summary(doc)
        self.write_pair(p, ("both.json", doc))
        entries = json.loads((self.dataset / "export_summary.json").read_text(encoding="utf-8"))
        entries.append({"pair": p, "files": [f"data/aligned/{p}/CLASS-9/both.json"],
                        "units": 2, "units_before_merge": 2, "merge": "paragraph"})
        self.write(self.dataset / "export_summary.json", entries)
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
            (f"{aligned.MARK}%:{self.PAIR}:%",)).fetchall())
        self.assertEqual(sorted(langs.values()), ["English", "Telugu"])
        titles = [r[0] for r in self.con.execute(
            "SELECT title FROM setu_book WHERE dedup_key LIKE ?",
            (f"{aligned.MARK}%:{self.PAIR}:%",))]
        self.assertTrue(any("Telugu pages" in t and "English ·" not in t for t in titles),
                        f"the Telugu side is titled as English: {titles}")

    def test_the_units_pair_across_facing_pages(self):
        rows = self.rows(self.pid)
        two = [(r["src_page"], r["tgt_page"]) for r in rows if r["src_sid"] and r["tgt_sid"]]
        self.assertEqual(two, [(1, 2), (1, 2)])
        lone = [(r["src_page"], r["tgt_page"]) for r in rows
                if not (r["src_sid"] and r["tgt_sid"])]
        self.assertEqual(sorted(lone, key=str), sorted([(3, None), (None, 4)], key=str),
                         "the front matter (never sent) became a pair to check")

    def test_the_page_view_steps_over_the_other_languages_pages(self):
        with mock.patch.object(store, "ro", lambda: _Same(self.con)):
            got = api.page_blocks(self.book_of("src", self.PAIR), 1, pid=self.pid)
        self.assertTrue(got["book"]["aligned"])
        self.assertEqual((got["prev_page"], got["next_page"]), (None, 3))
        self.assertEqual(got["attention_next"], 3)

    def test_a_page_the_model_could_not_align_says_so(self):
        b = browse.blocks(self.con, pid=self.pid, book_key=self.book_of("tgt", self.PAIR),
                          side="tgt", page=4)
        self.assertEqual((b[0]["hint"]["page_status"], b[0]["hint"]["state"]),
                         ("alignment_failed", "page_failed"))
        self.assertFalse(b[0]["paired"])

    def test_the_share_aligned_is_per_side_and_whole(self):
        p = next(x for x in aligned.pairs(self.con) if x["pair_id"] == self.PAIR)
        # 4 aligned of 6 OCR text blocks sent (the never-sent foreword excluded)
        self.assertEqual(p["aligned_pct"], round(100 * 4 / 6, 1))


# ── the real dataset, when it is here ──────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent
# data/aligned_v2 in the repository; an older checkout's aligned-docMT-test/.
REAL = next((REPO.joinpath(*loc) for loc in aligned.LOCATIONS
             if REPO.joinpath(*loc).is_dir()), REPO.joinpath(*aligned.LOCATIONS[0]))


@unittest.skipUnless(REAL.is_dir() and (REAL / "export_summary.json").is_file(),
                     "data/aligned_v2 is not in this checkout")
class TestRealDataset(SetuCase):
    """Checked against the dataset's own published numbers, not against itself."""

    def setUp(self):
        super().setUp()
        aligned._raw_index_cached.cache_clear()
        aligned._raw_pages.cache_clear()
        if not blocks.find_corpus():
            self.skipTest("the raw corpus (board_outputs) is not in this checkout")
        summary = json.loads((REAL / "export_summary.json").read_text(encoding="utf-8"))
        # v2 keeps v1's count in "units" and says how many it unlinked.
        self.units = {s["pair"]: s["units"] - int((s.get("v2") or {}).get("units_removed") or 0)
                      for s in summary}
        full = os.environ.get("SETU_ALIGNED_FULL") == "1"
        names = sorted(self.units) if full else [
            n for n in ("AP10_sem1_en-te", "MH10_1_en-mr", "NCERT_1211_en-hi", "KT10_2_en-kn")
            if n in self.units]
        # A folder with just these pairs, as links, so the run stays short.
        self.dataset = self.dir / "subset" / aligned.DATASET
        self.dataset.mkdir(parents=True)
        for n in names:
            (self.dataset / n).symlink_to(REAL / n, target_is_directory=True)
        shutil.copy(REAL / "export_summary.json", self.dataset / "export_summary.json")
        self.names = names
        with mock.patch.dict(os.environ, {"TULANA_ALIGNED_DIR": ""}):
            self.report = aligned.import_all(store.tx, self.dataset, log_fn=lambda m: None)

    def files_of(self, pair):
        return [json.loads(f.read_text(encoding="utf-8"))
                for f in sorted((REAL / pair).rglob("*.json"))]

    def test_pairs_match_the_published_counts(self):
        self.assertEqual(self.report["errors"], [])
        self.assertEqual(self.report["raw_missing"], [])
        self.assertEqual(self.report["imported"], len(self.names))
        for p in aligned.pairs(self.con):
            with self.subTest(pair=p["pair_id"]):
                self.assertEqual(p["units"], self.units[p["pair_id"]])
                self.assertEqual(self.con.execute(
                    "SELECT COUNT(*) FROM setu_row WHERE pid = ? AND edited = 1",
                    (p["pid"],)).fetchone()[0], 0)

    def test_the_share_aligned_is_the_viewers(self):
        """aligned / (OCR text blocks − not sent), over both files, as the
        aligner team's viewer computes it for its pair list."""
        for p in aligned.pairs(self.con):
            with self.subTest(pair=p["pair_id"]):
                tot = {"text_blocks": 0, "aligned": 0, "not_processed": 0}
                for doc in self.files_of(p["pair_id"]):
                    for k in tot:
                        tot[k] += doc["alignment"]["summary"][k]
                want = round(100 * tot["aligned"] / (tot["text_blocks"] - tot["not_processed"]), 1)
                self.assertEqual(p["aligned_pct"], want)

    def test_every_page_count_is_the_files(self):
        checked = 0
        for p in aligned.pairs(self.con):
            books = {r[0]: r[1] for r in self.con.execute(
                "SELECT book_key, dedup_key FROM setu_book WHERE book_key IN (?, ?)",
                (p["src_book"], p["tgt_book"]))}
            want: dict[tuple[str, int], dict] = {}
            docs = self.files_of(p["pair_id"])
            for key in books:
                for (page, st, *c) in self.con.execute(
                        "SELECT page, status, text_blocks, aligned, unpaired, page_failed,"
                        " not_processed, page_dropped FROM setu_page_meta WHERE book_key = ?",
                        (key,)):
                    want[(key, page)] = {"status": st, "c": c}
            seen = 0
            for doc in docs:
                for pg in doc["pages"]:
                    s = pg["align_summary"]
                    hits = [v for (k, page), v in want.items() if page == pg["page"]
                            and v["c"] == [s["text_blocks"], s["aligned"], s["unpaired"],
                                           s["page_failed"], s["not_processed"],
                                           s.get("page_dropped", 0)]
                            and v["status"] == pg["align_status"]]
                    seen += bool(hits)
            self.assertEqual(seen, sum(len(d["pages"]) for d in docs), p["pair_id"])
            checked += seen
        self.assertGreater(checked, 300)

    def test_every_box_is_a_raw_ocr_box_on_the_same_page(self):
        """The annotated data sits exactly on the OCR: each side has the raw
        layout's pages, at the raw raster's size, and every box the model
        merged is made of raw OCR boxes of that same page — their union, never
        moved. (The scan side of the mapping is check_mapping.py's, with PDFs.)"""
        key = lambda bb: tuple(round(float(v), 1) for v in bb)
        for pair in self.names:
            for f in sorted((REAL / pair).rglob("*.json")):
                doc = json.loads(f.read_text(encoding="utf-8"))
                with self.subTest(side=f"{pair}/{f.name}"):
                    raw_path = aligned.raw_path_for(doc["relpath"])
                    self.assertTrue(raw_path, f"no raw OCR for {doc['relpath']}")
                    raw = json.loads(Path(raw_path).read_text(encoding="utf-8"))
                    self.assertEqual(len(doc["pages"]), len(raw["pages"]))
                    for i, (ap, rp) in enumerate(zip(doc["pages"], raw["pages"])):
                        self.assertEqual((ap["page"], ap["width"], ap["height"], ap.get("image")),
                                         (i, rp["width"], rp["height"], rp.get("image")))
                        boxes = {key(b["bbox_xyxy"]) for b in rp["blocks"]}
                        for b in ap["blocks"]:
                            parts = [m["bbox_xyxy"] for m in b.get("members") or []] or [b["bbox_xyxy"]]
                            self.assertTrue(all(key(m) in boxes for m in parts),
                                            f"page {i}: {b.get('align_id')} has a box the OCR never drew")
                            union = (min(float(m[0]) for m in parts), min(float(m[1]) for m in parts),
                                     max(float(m[2]) for m in parts), max(float(m[3]) for m in parts))
                            self.assertLessEqual(max(abs(u - float(v)) for u, v in zip(union, b["bbox_xyxy"])),
                                                 1.0, f"page {i}: {b.get('align_id')} is not its members' union")

    def test_every_source_is_the_raw_ocr(self):
        """Rebuilt here independently: per page, the members' raw text joined by a
        blank line; the parts of a passage over a page break joined the same way."""
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
