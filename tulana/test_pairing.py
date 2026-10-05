"""One-sided pairs, pairing across pages, and saving that never loses text.

Written against two things an annotator actually saw in Saved work:

  #1269  "Not checked yet · corrected" — and nothing on either side.
         Clearing a box in the browser left a lone line break, which was saved
         as the correction, and the screen said "Saved."

  #1263  "Exact" — with nothing on the right. A block was selected on each
         side, on different pages; they sat in two DIFFERENT rows, but the
         screen showed them as a pair, and the answer went to the English-only
         row.

Every shape a pair can take is built here from real rows and pushed through
every operation, and the eight tables Tulana Studio owns are hashed before and
after. The browser side is covered separately by an end-to-end run.
"""
from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path
from unittest import mock

from test_annotation import SetuCase

from annotation.core import annotate, resume, store, workspace
from annotation.core.store import Invalid, NotFound


class PairCase(SetuCase):
    """A project, and helpers for reading rows back the way the database has them."""

    def setUp(self):
        super().setUp()
        self.proj = self.project()
        self.pid = self.proj["pid"]

    # -- reading back ----------------------------------------------------
    def row(self, rid):
        r = self.con.execute("SELECT * FROM setu_row WHERE rid = ?", (rid,)).fetchone()
        return dict(r) if r else None

    def rows(self):
        return [dict(r) for r in self.con.execute(
            "SELECT * FROM setu_row WHERE pid = ? ORDER BY seq", (self.pid,))]

    def two_sided(self):
        return [r for r in self.rows() if r["src_sid"] and r["tgt_sid"]]

    def text(self, rid, side):
        r = self.con.execute("SELECT text FROM setu_text WHERE rid = ? AND side = ?",
                             (rid, side)).fetchone()
        return r[0] if r else None

    def holder(self, sid, side):
        r = self.con.execute(f"SELECT rid FROM setu_row WHERE pid = ? AND {side}_sid = ?",
                             (self.pid, sid)).fetchone()
        return r[0] if r else None

    def assertDense(self):
        seqs = [r["seq"] for r in self.rows()]
        self.assertEqual(seqs, list(range(len(seqs))), "pair numbers have a gap")
        n = self.con.execute("SELECT n_rows FROM setu_project WHERE pid = ?",
                             (self.pid,)).fetchone()[0]
        self.assertEqual(n, len(seqs), "the project's row count is stale")

    def assertOneToOne(self):
        """No passage is in two pairs, and no row is empty."""
        for side in ("src", "tgt"):
            dup = self.con.execute(
                f"SELECT {side}_sid, COUNT(*) FROM setu_row WHERE pid = ? AND {side}_sid"
                f" IS NOT NULL GROUP BY {side}_sid HAVING COUNT(*) > 1", (self.pid,)).fetchall()
            self.assertEqual(dup, [], f"a {side} passage is in two pairs")
        empty = self.con.execute("SELECT COUNT(*) FROM setu_row WHERE pid = ? AND"
                                 " src_sid IS NULL AND tgt_sid IS NULL", (self.pid,)).fetchone()[0]
        self.assertEqual(empty, 0, "a row with nothing on either side was left behind")

    # -- building shapes -------------------------------------------------
    def one_sided_pair(self):
        """(E, —) and (—, M), made by splitting a real pair."""
        r = self.two_sided()[0]
        out = annotate.split_row(self.con, r["rid"], annotator="t")
        return out["row"]["rid"], out["new_row"]["rid"], r["src_sid"], r["tgt_sid"]

    def save(self, rid, side, text):
        cur = self.con.execute("SELECT rev FROM setu_text WHERE rid = ? AND side = ?",
                               (rid, side)).fetchone()
        return annotate.save_text(self.con, rid, side, text,
                                  base_rev=cur[0] if cur else 0, annotator="t")


# ── 1. a cleared box is not a correction ───────────────────────────────────

class TestEmptyIsNeverSaved(PairCase):

    def test_what_a_cleared_browser_box_contains_is_refused(self):
        rid = self.two_sided()[0]["rid"]
        before = annotate.AnnotateRepo(self.con).current(rid, "src")
        for blank in ("", "\n", "\n\n", "  \n ", "\t", "​", " ", "‍\n", "\r\n"):
            with self.subTest(blank=repr(blank)):
                with self.assertRaises(Invalid) as cm:
                    annotate.save_text(self.con, rid, "src", blank, base_rev=0)
                self.assertIn("empty", str(cm.exception))
        self.assertEqual(annotate.AnnotateRepo(self.con).current(rid, "src"), before,
                         "a refused save changed something")
        self.assertIsNone(self.text(rid, "src"))

    def test_clearing_then_typing_saves_the_new_text(self):
        rid = self.two_sided()[0]["rid"]
        out = self.save(rid, "src", "the corrected sentence")
        self.assertTrue(out["changed"])
        self.assertEqual(self.text(rid, "src"), "the corrected sentence")
        self.assertEqual(self.row(rid)["edited"], 1)

    def test_a_trailing_line_break_is_not_a_correction(self):
        """Clicking into an editable box and out again adds one."""
        rid = self.two_sided()[0]["rid"]
        source = annotate.AnnotateRepo(self.con).source_text(rid, "src")
        for extra in ("\n", " ", "\n\n", " \t\n"):
            with self.subTest(extra=repr(extra)):
                out = annotate.save_text(self.con, rid, "src", source + extra, base_rev=0)
                self.assertFalse(out["changed"])
        self.assertIsNone(self.text(rid, "src"), "a phantom edit created a revision")
        self.assertEqual(self.row(rid)["edited"], 0)

    def test_trailing_whitespace_is_dropped_from_a_real_correction(self):
        rid = self.two_sided()[0]["rid"]
        self.save(rid, "src", "fixed  \n")
        self.assertEqual(self.text(rid, "src"), "fixed")

    def test_restore_still_puts_the_original_back_byte_for_byte(self):
        rid = self.two_sided()[0]["rid"]
        source = annotate.AnnotateRepo(self.con).source_text(rid, "src")
        self.save(rid, "src", "something else")
        annotate.restore(self.con, rid, "src", rev=0, annotator="t")
        self.assertEqual(self.text(rid, "src"), source)
        self.assertEqual(self.row(rid)["edited"], 0)

    def test_a_side_with_no_passage_cannot_be_typed_into(self):
        e_rid, m_rid, _, _ = self.one_sided_pair()
        with self.assertRaises(Invalid) as cm:
            annotate.save_text(self.con, e_rid, "tgt", "made up", base_rev=0)
        self.assertIn("Pair", str(cm.exception))


# ── 2. answers that compare two passages need two ──────────────────────────

class TestAnswerNeedsTwoSides(PairCase):

    def test_comparing_answers_are_refused_on_a_one_sided_pair(self):
        e_rid, m_rid, _, _ = self.one_sided_pair()
        for rid in (e_rid, m_rid):
            for status in ("exact", "needs_correction", "structural_mismatch"):
                with self.subTest(rid=rid, status=status):
                    with self.assertRaises(Invalid):
                        annotate.set_status(self.con, rid, status, annotator="t")
                    self.assertEqual(self.row(rid)["status"], "pending")

    def test_the_other_answers_are_accepted(self):
        e_rid, _, _, _ = self.one_sided_pair()
        for status in ("incomplete", "unclear", "not_applicable", "pending"):
            with self.subTest(status=status):
                annotate.set_status(self.con, e_rid, status, annotator="t")
                self.assertEqual(self.row(e_rid)["status"], status)

    def test_an_existing_contradiction_can_still_have_its_note_saved(self):
        """Rows answered wrongly by the old version must not become uneditable."""
        e_rid, _, _, _ = self.one_sided_pair()
        self.con.execute("UPDATE setu_row SET status = 'exact' WHERE rid = ?", (e_rid,))
        out = annotate.set_status(self.con, e_rid, None, note="checked with supervisor")
        self.assertEqual(out["note"], "checked with supervisor")
        self.assertEqual(self.row(e_rid)["status"], "exact")

    def test_two_sided_pairs_take_every_answer(self):
        rid = self.two_sided()[0]["rid"]
        for status in ("exact", "needs_correction", "structural_mismatch", "incomplete"):
            annotate.set_status(self.con, rid, status, annotator="t")
            self.assertEqual(self.row(rid)["status"], status)


# ── 3. pairing, in every shape ─────────────────────────────────────────────

class TestPairEveryShape(PairCase):

    def test_english_only_with_marathi_only(self):
        """Dipali's case: the counterpart was on another page, in its own row."""
        e_rid, m_rid, e_sid, m_sid = self.one_sided_pair()
        self.save(m_rid, "tgt", "दुरुस्त मराठी")
        out = annotate.pair_segments(self.con, self.pid, e_sid, m_sid, annotator="t")
        self.assertTrue(out["changed"])
        self.assertEqual(out["removed"], [m_rid])
        self.assertIsNone(self.row(m_rid), "the emptied row was left behind")
        self.assertEqual(self.row(e_rid)["tgt_sid"], m_sid)
        self.assertEqual(self.text(e_rid, "tgt"), "दुरुस्त मराठी", "the correction did not travel")
        self.assertDense(); self.assertOneToOne()

    def test_repairing_a_wrong_pair_frees_the_old_partner(self):
        """(E, M_old) + (—, M) → (E, M), and M_old alone straight after."""
        r1, r2 = self.two_sided()[0], self.two_sided()[1]
        split = annotate.split_row(self.con, r2["rid"], annotator="t")   # (—, M2) exists now
        m_free = split["new_row"]
        self.save(r1["rid"], "tgt", "M1 corrected")
        out = annotate.pair_segments(self.con, self.pid, r1["src_sid"], r2["tgt_sid"], annotator="t")
        self.assertEqual(self.row(r1["rid"])["tgt_sid"], r2["tgt_sid"])
        freed = self.holder(r1["tgt_sid"], "tgt")
        self.assertIsNotNone(freed)
        self.assertIsNone(self.row(freed)["src_sid"], "the freed passage was paired with something")
        self.assertEqual(self.row(freed)["seq"], self.row(r1["rid"])["seq"] + 1,
                         "the freed passage is not next to where it was")
        self.assertEqual(self.text(freed, "tgt"), "M1 corrected", "its correction did not go with it")
        self.assertIsNone(self.row(m_free["rid"]))
        self.assertDense(); self.assertOneToOne()

    def test_taking_a_passage_from_another_pair(self):
        """(E, —) + (E_old, M) → (E, M), and E_old alone where it was."""
        e_rid, m_rid, e_sid, m_sid = self.one_sided_pair()
        victim = [r for r in self.two_sided()][0]
        seq_before = self.row(victim["rid"])["seq"]
        out = annotate.pair_segments(self.con, self.pid, e_sid, victim["tgt_sid"], annotator="t")
        self.assertEqual(self.row(e_rid)["tgt_sid"], victim["tgt_sid"])
        self.assertIsNone(self.row(victim["rid"])["tgt_sid"])
        self.assertEqual(self.row(victim["rid"])["src_sid"], victim["src_sid"])
        self.assertIn(victim["rid"], out["touched"])
        self.assertDense(); self.assertOneToOne()
        self.assertLessEqual(abs(self.row(victim["rid"])["seq"] - seq_before), 1)

    def test_swapping_between_two_full_pairs_never_invents_a_pair(self):
        """(E1, M1) + (E2, M2), pairing E1 with M2: E2 and M1 are NOT put together."""
        r1, r2 = self.two_sided()[0], self.two_sided()[1]
        annotate.pair_segments(self.con, self.pid, r1["src_sid"], r2["tgt_sid"], annotator="t")
        self.assertEqual(self.row(r1["rid"])["tgt_sid"], r2["tgt_sid"])
        e2_row = self.row(self.holder(r2["src_sid"], "src"))
        m1_row = self.row(self.holder(r1["tgt_sid"], "tgt"))
        self.assertNotEqual(e2_row["rid"], m1_row["rid"], "two strangers were paired")
        self.assertIsNone(e2_row["tgt_sid"]); self.assertIsNone(m1_row["src_sid"])
        self.assertDense(); self.assertOneToOne()

    def test_pairing_what_is_already_a_pair_does_nothing(self):
        r = self.two_sided()[0]
        before = self.rows()
        out = annotate.pair_segments(self.con, self.pid, r["src_sid"], r["tgt_sid"])
        self.assertFalse(out["changed"])
        self.assertEqual(self.rows(), before)

    def test_answers_go_back_to_unjudged_and_stay_in_the_history(self):
        r1, r2 = self.two_sided()[0], self.two_sided()[1]
        annotate.set_status(self.con, r1["rid"], "exact", annotator="t")
        annotate.set_status(self.con, r2["rid"], "needs_correction", annotator="t")
        annotate.pair_segments(self.con, self.pid, r1["src_sid"], r2["tgt_sid"], annotator="t")
        self.assertEqual(self.row(r1["rid"])["status"], "pending")
        self.assertEqual(self.row(r2["rid"])["status"], "pending")
        kept = [s for (s,) in self.con.execute(
            "SELECT status FROM setu_status_rev WHERE rid = ? ORDER BY id", (r1["rid"],))]
        self.assertIn("exact", kept, "the old answer was thrown away")

    def test_the_corrected_flag_follows_the_text(self):
        e_rid, m_rid, e_sid, m_sid = self.one_sided_pair()
        self.save(m_rid, "tgt", "मराठी दुरुस्ती")
        self.assertEqual(self.row(m_rid)["edited"], 1)
        self.assertEqual(self.row(e_rid)["edited"], 0)
        annotate.pair_segments(self.con, self.pid, e_sid, m_sid, annotator="t")
        self.assertEqual(self.row(e_rid)["edited"], 1, "the arriving correction did not mark the pair")

    def test_a_block_with_no_row_is_given_one_in_reading_order(self):
        """A header shown with "include headers" has no row; pairing it makes one."""
        en_book = self.con.execute("SELECT src_book FROM setu_project WHERE pid=?", (self.pid,)).fetchone()[0]
        loose = self.con.execute(
            "SELECT s.sid, s.seq FROM setu_segment s WHERE s.book_key = ? AND NOT EXISTS"
            " (SELECT 1 FROM setu_row r WHERE r.pid = ? AND r.src_sid = s.sid) ORDER BY s.seq LIMIT 1",
            (en_book, self.pid)).fetchone()
        if not loose:
            self.skipTest("every left-hand segment of the fixture already has a row")
        m = self.two_sided()[0]["tgt_sid"]
        out = annotate.pair_segments(self.con, self.pid, loose[0], m, annotator="t")
        self.assertEqual(len(out["created"]) >= 1, True)
        self.assertEqual(self.row(out["rid"])["src_sid"], loose[0])
        self.assertDense(); self.assertOneToOne()

    def test_refuses_blocks_from_the_wrong_book_or_nowhere(self):
        r = self.two_sided()[0]
        with self.assertRaises(Invalid):
            annotate.pair_segments(self.con, self.pid, r["tgt_sid"], r["tgt_sid"])
        with self.assertRaises(Invalid):
            annotate.pair_segments(self.con, self.pid, r["src_sid"], r["src_sid"])
        with self.assertRaises(NotFound):
            annotate.pair_segments(self.con, self.pid, "sg_NOSUCHTHING00", r["tgt_sid"])
        with self.assertRaises(NotFound):
            annotate.pair_segments(self.con, "pj_NOSUCHPROJECT", r["src_sid"], r["tgt_sid"])

    def test_a_failure_halfway_changes_nothing(self):
        """Inside a transaction, a pairing is all or nothing."""
        r1, r2 = self.two_sided()[0], self.two_sided()[1]
        self.save(r1["rid"], "tgt", "keep me")
        self.con.commit()
        before = self.rows()
        texts = self.con.execute("SELECT rid, side, text FROM setu_text ORDER BY rid, side").fetchall()
        real = annotate._move_text
        calls = {"n": 0}

        def flaky(*a, **kw):
            calls["n"] += 1
            if calls["n"] == 2:
                raise RuntimeError("the disk filled up")
            return real(*a, **kw)

        self.con.execute("BEGIN IMMEDIATE")
        with mock.patch.object(annotate, "_move_text", side_effect=flaky):
            with self.assertRaises(RuntimeError):
                annotate.pair_segments(self.con, self.pid, r1["src_sid"], r2["tgt_sid"])
        self.con.execute("ROLLBACK")
        self.assertEqual(self.rows(), before)
        self.assertEqual(self.con.execute(
            "SELECT rid, side, text FROM setu_text ORDER BY rid, side").fetchall(), texts)


# ── 4. history numbering survives every cycle ──────────────────────────────

class TestHistoryNeverCollides(PairCase):

    def test_pair_unpair_pair_many_times(self):
        """setu_rev is UNIQUE(rid, side, rev); the old code reused numbers and failed."""
        r1, r2 = self.two_sided()[0], self.two_sided()[1]
        self.save(r1["rid"], "tgt", "first correction")
        for i in range(6):
            annotate.pair_segments(self.con, self.pid, r1["src_sid"], r2["tgt_sid"], annotator="t")
            annotate.pair_segments(self.con, self.pid, r1["src_sid"], r1["tgt_sid"], annotator="t")
            rid = self.holder(r1["src_sid"], "src")
            annotate.split_row(self.con, rid, annotator="t")
            annotate.pair_segments(self.con, self.pid, r1["src_sid"], r1["tgt_sid"], annotator="t")
        rid = self.holder(r1["src_sid"], "src")
        self.assertEqual(self.text(rid, "tgt"), "first correction",
                         "the correction did not survive the round trips")
        for (r, side) in self.con.execute("SELECT DISTINCT rid, side FROM setu_rev").fetchall():
            revs = [v for (v,) in self.con.execute(
                "SELECT rev FROM setu_rev WHERE rid=? AND side=? ORDER BY id", (r, side))]
            self.assertEqual(revs, sorted(set(revs)), f"revisions of {r}/{side} are not increasing")
        self.assertDense(); self.assertOneToOne()

    def test_merge_and_attach_use_free_numbers_too(self):
        e_rid, m_rid, e_sid, m_sid = self.one_sided_pair()
        self.save(m_rid, "tgt", "x1")
        annotate.merge_rows(self.con, e_rid, m_rid, annotator="t")
        annotate.attach(self.con, e_rid, "tgt", None, annotator="t")
        annotate.attach(self.con, e_rid, "tgt", m_sid, annotator="t")
        self.save(e_rid, "tgt", "x2")
        self.assertEqual(self.text(e_rid, "tgt"), "x2")
        self.assertDense()


# ── 5. unpair and merge ────────────────────────────────────────────────────

class TestUnpairAndMerge(PairCase):

    def test_unpair_leaves_two_neighbours_and_keeps_corrections(self):
        r = self.two_sided()[2]
        self.save(r["rid"], "src", "E fixed"); self.save(r["rid"], "tgt", "M fixed")
        annotate.set_status(self.con, r["rid"], "exact", annotator="t")
        out = annotate.unpair(self.con, r["rid"], annotator="t")
        a, b = out["row"], out["new_row"]
        self.assertEqual(b["seq"], a["seq"] + 1)
        self.assertEqual(self.text(a["rid"], "src"), "E fixed")
        self.assertEqual(self.text(b["rid"], "tgt"), "M fixed")
        self.assertIsNone(self.text(a["rid"], "tgt"))
        self.assertEqual(self.row(a["rid"])["status"], "pending")
        self.assertDense(); self.assertOneToOne()

    def test_unpairing_a_one_sided_pair_is_refused(self):
        e_rid, _, _, _ = self.one_sided_pair()
        with self.assertRaises(Invalid):
            annotate.unpair(self.con, e_rid)

    def test_merge_closes_the_gap(self):
        e_rid, m_rid, _, m_sid = self.one_sided_pair()
        out = annotate.merge_rows(self.con, e_rid, m_rid, annotator="t")
        self.assertEqual(out["removed_row"], m_rid)
        self.assertEqual(self.row(e_rid)["tgt_sid"], m_sid)
        self.assertDense(); self.assertOneToOne()


# ── 6. the repair of what the old version saved ────────────────────────────

class TestRepair(PairCase):

    def damage(self, rid, side, text="\n"):
        """Exactly what the old version wrote: a blank 'correction'."""
        rev = annotate._next_rev(self.con, rid, side)
        self.con.execute("INSERT INTO setu_text(rid, side, text, rev) VALUES(?,?,?,?)"
                         " ON CONFLICT(rid, side) DO UPDATE SET text=excluded.text, rev=excluded.rev",
                         (rid, side, text, rev))
        self.con.execute("INSERT INTO setu_rev(rid, side, rev, text, reason) VALUES(?,?,?,?, 'edit')",
                         (rid, side, rev, text))
        self.con.execute("UPDATE setu_row SET edited = 1 WHERE rid = ?", (rid,))

    def test_the_parser_original_comes_back_when_there_was_no_own_text(self):
        rid = self.two_sided()[0]["rid"]
        source = annotate.AnnotateRepo(self.con).source_text(rid, "src")
        self.damage(rid, "src"); self.damage(rid, "tgt")
        out = annotate.repair_blank_corrections(self.con)
        self.assertEqual(out["fixed"], 2)
        self.assertEqual(self.text(rid, "src"), source)
        self.assertEqual(self.row(rid)["edited"], 0, "still marked corrected")

    def test_the_annotators_own_last_text_comes_back_if_they_had_one(self):
        rid = self.two_sided()[0]["rid"]
        self.save(rid, "src", "my careful correction")
        self.damage(rid, "src")
        annotate.repair_blank_corrections(self.con)
        self.assertEqual(self.text(rid, "src"), "my careful correction")

    def test_never_reaches_back_to_a_different_passage(self):
        """History older than a detach belongs to the passage that left."""
        r1, r2 = self.two_sided()[0], self.two_sided()[1]
        self.save(r1["rid"], "tgt", "text of M1")
        annotate.pair_segments(self.con, self.pid, r1["src_sid"], r2["tgt_sid"], annotator="t")
        self.damage(r1["rid"], "tgt")
        annotate.repair_blank_corrections(self.con)
        m2_source = annotate.AnnotateRepo(self.con).source_text(r1["rid"], "tgt")
        self.assertEqual(self.text(r1["rid"], "tgt"), m2_source,
                         "M1's old text was put into M2")

    def test_the_repair_is_a_revision_and_runs_once(self):
        rid = self.two_sided()[0]["rid"]
        self.damage(rid, "src")
        self.assertEqual(annotate.repair_blank_corrections(self.con)["fixed"], 1)
        self.assertEqual(annotate.repair_blank_corrections(self.con)["fixed"], 0)
        reasons = [r for (r,) in self.con.execute(
            "SELECT reason FROM setu_rev WHERE rid=? AND side='src' ORDER BY rev", (rid,))]
        self.assertEqual(reasons[-1], "repair-blank")
        self.assertIn("edit", reasons, "the blank revision was erased instead of kept")

    def test_stale_corrected_flags_are_recomputed(self):
        rid = self.two_sided()[0]["rid"]
        self.con.execute("UPDATE setu_row SET edited = 1 WHERE rid = ?", (rid,))
        self.assertGreaterEqual(annotate.resync_edited_flags(self.con), 1)
        self.assertEqual(self.row(rid)["edited"], 0)


# ── 7. what Saved work is told ─────────────────────────────────────────────

class TestSavedWorkTellsTheTruth(PairCase):

    def saved(self, **kw):
        return {r["rid"]: r for r in resume.ResumeRepo(self.con).saved_rows(limit=200, **kw)["rows"]}

    def test_a_missing_side_is_reported_as_missing(self):
        e_rid, m_rid, _, _ = self.one_sided_pair()
        rows = self.saved()
        self.assertTrue(rows[e_rid]["src_present"]); self.assertFalse(rows[e_rid]["tgt_present"])
        self.assertFalse(rows[m_rid]["src_present"]); self.assertTrue(rows[m_rid]["tgt_present"])

    def test_a_stored_correction_is_shown_even_if_empty(self):
        """Never swapped for the parser's text behind the annotator's back."""
        rid = self.two_sided()[0]["rid"]
        TestRepair.damage(self, rid, "src", "")
        self.assertEqual(self.saved()[rid]["src_text"], "")

    def test_contradictions_and_blanks_need_attention(self):
        e_rid, _, _, _ = self.one_sided_pair()
        self.con.execute("UPDATE setu_row SET status='exact' WHERE rid=?", (e_rid,))
        blank = self.two_sided()[0]["rid"]
        TestRepair.damage(self, blank, "tgt")
        rows = self.saved(attention=True)
        self.assertEqual(set(rows), {e_rid, blank})
        self.assertIn("nothing on the right", rows[e_rid]["attention"])
        self.assertIn("empty", rows[blank]["attention"])
        self.assertEqual(resume.ResumeRepo(self.con).saved_tally()["attention"], 2)

    def test_search_is_literal(self):
        rid = self.two_sided()[0]["rid"]
        self.save(rid, "src", "interest at 100% for 2_years")
        self.assertIn(rid, self.saved(search="100%"))
        self.assertIn(rid, self.saved(search="2_y"))
        self.assertEqual(self.saved(search="100%x"), {})
        self.assertEqual(self.saved(search="2xyears"), {})

    def test_every_row_says_where_its_passages_are(self):
        for r in self.saved().values():
            self.assertIn("src_sid", r); self.assertIn("tgt_sid", r)


# ── 8. the HTTP surface ────────────────────────────────────────────────────

class TestApi(PairCase):

    def setUp(self):
        super().setUp()
        self.con.commit()
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from annotation.api import router
        app = FastAPI(); app.include_router(router)
        self.http = TestClient(app)

    def test_pair_unpair_and_where(self):
        e_rid, m_rid, e_sid, m_sid = self.one_sided_pair()
        self.con.commit()
        r = self.http.post(f"/api/setu/projects/{self.pid}/pair",
                           json={"src_sid": e_sid, "tgt_sid": m_sid}, headers={"X-Annotator": "Dipali"})
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["removed"], [m_rid])
        w = self.http.get(f"/api/setu/projects/{self.pid}/where", params={"sid": m_sid}).json()
        self.assertEqual((w["rid"], w["side"]), (e_rid, "tgt"))
        u = self.http.post(f"/api/setu/rows/{e_rid}/unpair", json={})
        self.assertEqual(u.status_code, 200, u.text)

    def test_the_annotators_name_is_recorded(self):
        e_rid, m_rid, e_sid, m_sid = self.one_sided_pair(); self.con.commit()
        self.http.post(f"/api/setu/projects/{self.pid}/pair",
                       json={"src_sid": e_sid, "tgt_sid": m_sid}, headers={"X-Annotator": "Dipali"})
        actor = self.con.execute("SELECT actor FROM setu_event WHERE action='row.pair'"
                                 " ORDER BY id DESC LIMIT 1").fetchone()[0]
        self.assertEqual(actor, "Dipali")

    def test_blank_and_contradictions_come_back_as_sentences(self):
        rid = self.two_sided()[0]["rid"]; self.con.commit()
        r = self.http.patch(f"/api/setu/rows/{rid}", json={"src": "\n", "src_rev": 0})
        self.assertEqual(r.status_code, 400)
        self.assertIn("empty", r.text)
        e_rid, _, _, _ = self.one_sided_pair(); self.con.commit()
        r = self.http.post(f"/api/setu/rows/{e_rid}/status", json={"status": "exact"})
        self.assertEqual(r.status_code, 400)

    def test_blocks_say_whether_they_are_paired(self):
        e_rid, m_rid, e_sid, m_sid = self.one_sided_pair(); self.con.commit()
        en = self.con.execute("SELECT book_key, page FROM setu_segment WHERE sid=?", (e_sid,)).fetchone()
        d = self.http.get(f"/api/setu/pages/{en[0]}/{en[1]}/blocks", params={"pid": self.pid}).json()
        b = next(x for x in d["blocks"] if x["sid"] == e_sid)
        self.assertFalse(b["paired"]); self.assertIsNone(b["mate_sid"])
        other = next(x for x in d["blocks"] if x["paired"])
        self.assertIsNotNone(other["mate_display_page"])

    def test_hostile_input_is_refused_cleanly(self):
        for body in ({}, {"src_sid": "x", "tgt_sid": "y"}, {"src_sid": "../../etc", "tgt_sid": "sg_A"},
                     {"src_sid": "'; DROP TABLE setu_row; --", "tgt_sid": "sg_A"}, {"src_sid": 5, "tgt_sid": None}):
            r = self.http.post(f"/api/setu/projects/{self.pid}/pair", json=body)
            self.assertIn(r.status_code, (400, 404), body)
        self.assertGreater(self.con.execute("SELECT COUNT(*) FROM setu_row").fetchone()[0], 0)
        r = self.http.get(f"/api/setu/projects/{self.pid}/where", params={"sid": "../x"})
        self.assertEqual(r.status_code, 400)

    def test_a_server_error_never_claims_the_work_was_saved(self):
        from annotation import api
        src = Path(api.__file__).read_text(encoding="utf-8")
        self.assertNotIn("Your work is saved", src)


# ── 9. the rule above every feature ────────────────────────────────────────

class TestLegacyUntouched(PairCase):

    PROTECTED = ("documents", "projects", "clips", "pairs", "labels",
                 "pair_labels", "exports", "audit")

    def fingerprint(self):
        out = {}
        for t in self.PROTECTED:
            try:
                rows = self.con.execute(f"SELECT * FROM {t} ORDER BY rowid").fetchall()
            except Exception:
                out[t] = "absent"; continue
            out[t] = hashlib.sha256(repr([tuple(r) for r in rows]).encode()).hexdigest()
        return out

    def test_everything_new_leaves_the_eight_tables_byte_identical(self):
        before = self.fingerprint()
        e_rid, m_rid, e_sid, m_sid = self.one_sided_pair()
        self.save(m_rid, "tgt", "x")
        annotate.pair_segments(self.con, self.pid, e_sid, m_sid, annotator="t")
        annotate.unpair(self.con, e_rid, annotator="t")
        TestRepair.damage(self, self.two_sided()[0]["rid"], "src")
        annotate.repair_blank_corrections(self.con)
        resume.ResumeRepo(self.con).saved_rows(attention=True)
        self.con.commit()
        self.assertEqual(before, self.fingerprint())

    def test_no_destructive_ddl_and_no_writes_outside_setu(self):
        src = (Path(__file__).parent / "annotation" / "core" / "annotate.py").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\b(ALTER|DROP)\s+TABLE\b", src, re.I))
        scanned = re.sub(r"ON\s+CONFLICT\s*\([^)]*\)\s*DO\s+UPDATE\s+SET", " ", src, flags=re.I)
        for t in re.findall(r"(?:INSERT\s+(?:OR\s+\w+\s+)?INTO|UPDATE|DELETE\s+FROM)\s+(\w+)",
                            scanned, re.I):
            self.assertTrue(t.startswith("setu_"), f"annotate.py writes to {t}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
