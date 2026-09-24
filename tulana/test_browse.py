#!/usr/bin/env python3
"""Tests for the annotator's workspace.

Run with no arguments::

    python3 test_browse.py
    python3 test_browse.py -v

The fixture comes from ``test_annotation`` so both suites build the same small
synthetic corpus in the same throwaway database, and neither needs a textbook
on disk.

Three claims are defended here, in order of how much damage their failure does.

**Page numbers.** ``setu_segment.page`` counts from zero, because the layout
JSON does and PyMuPDF does, and the crop renderer depends on that agreement.
People count from one. A version of this workspace showed the stored number to
the annotator, so "page 57" on screen was page 58 of the printed book — on all
121 books, silently, in the one place an annotator goes to check the machine's
reading against the paper. :class:`TestPageNumbers` exists for that alone.

**Independence.** Chapter-start offsets between an English edition and its
counterpart run from 0 to 114 pages across this corpus, and two board pairs
share no chapter page at all. Moving one side must never move the other unless
an annotator has said the two pages match.

**Provenance.** Editing a block must never destroy what the parser read.
``setu_segment.source_text`` and ``setu_text.text`` are different columns in
different tables for that reason, and :class:`TestWork` proves the first
survives the second.
"""
from __future__ import annotations

import hashlib
import sqlite3
import unittest

from test_annotation import LEGACY_TABLES, SetuCase          # noqa: E402

from annotation.core import store                            # noqa: E402
from annotation.ui import browse, session as uisession       # noqa: E402


class WorkspaceCase(SetuCase):
    """A project, open in the workspace, ready to be driven about."""

    #: The shared fixture puts every segment on page 0, which is fine for the
    #: pair tests it was written for and useless here — a workspace whose whole
    #: subject is moving between pages needs more than one. Segments are spread
    #: over pages in this suite only.
    PER_PAGE = 1

    def setUp(self):
        super().setUp()
        self.proj = self.project()
        for book in (self.en, self.mr):
            # seq starts at 0 in the fixture, and so must page: the renderer
            # indexes PDF pages from zero and a page of -1 is not a page.
            self.con.execute(
                "UPDATE setu_segment SET page = seq / ? WHERE book_key = ?",
                (self.PER_PAGE, book))
        self.con.commit()
        self.st = uisession.blank()
        self.st["pid"] = self.proj["pid"]
        self.st["annotator"] = "tester"
        self.bs = browse.open_books(self.st, browse.blank())

    # -- helpers ---------------------------------------------------------
    def pages(self):
        return (self.bs["src_page"], self.bs["tgt_page"])

    def shown(self):
        return (browse.to_display(self.bs["src_page"]),
                browse.to_display(self.bs["tgt_page"]))

    def rendered(self, side="src"):
        with store.ro() as con:
            return browse.blocks(con, pid=self.proj["pid"],
                                 book_key=self.bs[f"{side}_book"], side=side,
                                 page=self.bs[f"{side}_page"],
                                 hide_noise=self.bs["hide_noise"])

    def rev_of(self, rid, side):
        row = store.Repository(self.con).one(
            "SELECT rev FROM setu_text WHERE rid = ? AND side = ?", (rid, side))
        return row["rev"] if row else 0


# ── the bug that shipped ───────────────────────────────────────────────────

class TestPageNumbers(WorkspaceCase):
    """Storage counts from zero; people count from one; convert exactly once."""

    def test_the_first_page_is_called_one(self):
        self.assertEqual(browse.to_display(0), 1)

    def test_what_is_typed_comes_back_as_stored(self):
        for shown in (1, 2, 57, 188):
            with self.subTest(shown=shown):
                self.assertEqual(browse.to_display(browse.from_display(shown)),
                                 shown)

    def test_stored_zero_is_never_shown_as_zero(self):
        """A page numbered 0 on screen is the symptom that was reported."""
        self.assertGreaterEqual(browse.to_display(self.bs["src_lo"]), 1)

    def test_typing_a_page_lands_on_that_printed_page(self):
        want = min(3, browse.to_display(self.bs["src_hi"]))
        self.bs = browse.goto(self.bs, "src", want)
        self.assertEqual(browse.to_display(self.bs["src_page"]), want)
        self.assertEqual(self.bs["src_page"], want - 1,
                         "the stored page must be one less than the printed one")

    def test_every_block_reports_its_printed_page(self):
        for b in self.rendered("src"):
            self.assertEqual(b["display_page"], b["page"] + 1)
            self.assertGreaterEqual(b["display_page"], 1)

    def test_the_chapter_list_offers_printed_pages(self):
        with store.ro() as con:
            choices = browse.chapter_choices(con, self.bs["src_book"])
        for label, _value in choices:
            if "from page" in label:
                number = int(label.rsplit("from page", 1)[1].strip())
                self.assertGreaterEqual(number, 1, f"page 0 offered in {label!r}")

    def test_the_stored_page_still_matches_the_pdf_convention(self):
        """The renderer indexes from zero. Nothing here may change that."""
        with store.ro() as con:
            lo, _hi = browse.page_range(con, self.bs["src_book"])
        self.assertEqual(lo, 0, "segments must still be stored counting from 0")

    def test_a_page_typed_as_zero_or_less_is_refused_not_wrapped(self):
        self.bs = browse.goto(self.bs, "src", 3)
        for bad in (0, -1, -999):
            with self.subTest(bad=bad):
                self.bs = browse.goto(self.bs, "src", bad)
                self.assertGreaterEqual(self.bs["src_page"], self.bs["src_lo"])


# ── the two sides move apart ───────────────────────────────────────────────

class TestIndependence(WorkspaceCase):

    def test_moving_one_side_leaves_the_other_alone(self):
        before = self.pages()
        self.bs = browse.step(self.bs, "src", 1)
        self.assertEqual(self.bs["tgt_page"], before[1])
        held = self.bs["src_page"]
        self.bs = browse.step(self.bs, "tgt", 1)
        self.assertEqual(self.bs["src_page"], held)

    def test_the_sides_can_sit_at_different_pages(self):
        """English page 4 beside the other edition's page 2."""
        if browse.to_display(self.bs["src_hi"]) < 4:
            self.skipTest("fixture book too short")
        self.bs = browse.goto(self.bs, "src", 4)
        self.bs = browse.goto(self.bs, "tgt", 2)
        self.assertEqual(self.shown(), (4, 2))

    def test_chapter_is_chosen_per_side(self):
        self.bs = browse.jump_chapter(self.bs, "src", "1")
        self.assertEqual(self.bs["src_chapter"], "1")
        self.assertEqual(self.bs["tgt_chapter"], "")

    def test_the_link_makes_the_other_side_follow(self):
        if browse.to_display(self.bs["src_hi"]) < 6:
            self.skipTest("fixture book too short")
        self.bs = browse.goto(self.bs, "src", 4)
        self.bs = browse.goto(self.bs, "tgt", 2)
        self.bs, _ = browse.link_pages(self.st, self.bs)
        self.assertEqual(self.bs["offset"], 2)
        self.bs = browse.step(self.bs, "src", 1)
        self.assertEqual(self.shown(), (5, 3))
        self.bs = browse.step(self.bs, "tgt", 1)
        self.assertEqual(self.shown(), (6, 4))

    def test_both_buttons_keep_the_distance(self):
        if browse.to_display(self.bs["src_hi"]) < 5:
            self.skipTest("fixture book too short")
        self.bs = browse.goto(self.bs, "src", 3)
        self.bs = browse.goto(self.bs, "tgt", 1)
        self.bs = browse.step_both(self.bs, 2)
        self.assertEqual(self.shown(), (5, 3))

    def test_both_buttons_stop_at_the_edge(self):
        self.bs = browse.step_both(self.bs, -10_000)
        self.assertEqual(self.pages(), (self.bs["src_lo"], self.bs["tgt_lo"]))

    def test_unlink_frees_the_sides(self):
        self.bs, _ = browse.link_pages(self.st, self.bs)
        self.bs = browse.unlink_pages(self.bs)
        self.assertFalse(self.bs["linked"])
        held = self.bs["tgt_page"]
        self.bs = browse.step(self.bs, "src", 1)
        self.assertEqual(self.bs["tgt_page"], held)

    def test_the_link_outlives_the_session(self):
        if browse.to_display(self.bs["src_hi"]) < 3:
            self.skipTest("fixture book too short")
        self.bs = browse.goto(self.bs, "src", 3)
        self.bs = browse.goto(self.bs, "tgt", 1)
        browse.link_pages(self.st, self.bs)
        fresh = browse.open_books(uisession.ensure({"pid": self.proj["pid"]}),
                                  browse.blank())
        self.assertEqual((browse.to_display(fresh["src_page"]),
                          browse.to_display(fresh["tgt_page"])), (3, 1))
        self.assertTrue(fresh["linked"])
        self.assertEqual(fresh["offset"], 2)

    def test_the_offset_sentence_speaks_in_printed_pages(self):
        if browse.to_display(self.bs["src_hi"]) < 3:
            self.skipTest("fixture book too short")
        self.bs = browse.goto(self.bs, "src", 3)
        self.bs = browse.goto(self.bs, "tgt", 1)
        note = browse.offset_note(self.bs)
        self.assertIn("page 3", note)
        self.assertIn("page 1", note)
        self.assertNotIn("page 0", note)

    def test_the_meta_key_cannot_be_driven_by_anything_typed(self):
        self.con.execute("UPDATE setu_project SET name = ? WHERE pid = ?",
                         ("../../etc/passwd\n'; DROP TABLE setu_row;--",
                          self.proj["pid"]))
        self.con.commit()
        browse.link_pages(self.st, self.bs)
        with store.ro() as con:
            keys = [r["key"] for r in store.Repository(con).all(
                "SELECT key FROM setu_meta WHERE key LIKE 'browse.link:%'", ())]
        self.assertEqual(keys, [f"browse.link:{self.proj['pid']}"])
        self.assertTrue(store.Repository(self.con).one(
            "SELECT 1 AS ok FROM setu_row LIMIT 1"))

    def test_a_corrupt_stored_link_is_ignored_not_fatal(self):
        with store.tx() as con:
            con.execute("INSERT INTO setu_meta(key, value) VALUES(?, ?)"
                        " ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                        (f"browse.link:{self.proj['pid']}", "{not json"))
        bs = browse.open_books(self.st, browse.blank())
        self.assertFalse(bs["linked"])


# ── nothing a browser can send gets through ────────────────────────────────

class TestHostileInput(WorkspaceCase):

    def test_page_numbers_are_clamped(self):
        for value in (10 ** 9, -10 ** 9, 0, "99999999999999999999"):
            with self.subTest(value=value):
                self.bs = browse.goto(self.bs, "src", value)
                self.assertGreaterEqual(self.bs["src_page"], self.bs["src_lo"])
                self.assertLessEqual(self.bs["src_page"], self.bs["src_hi"])

    def test_nonsense_page_numbers_change_nothing(self):
        for value in (None, "", "  ", "abc", "3; DROP TABLE setu_row",
                      "../../etc/passwd", [], {}, object()):
            with self.subTest(value=value):
                before = self.pages()
                self.bs = browse.goto(self.bs, "src", value)
                self.assertEqual(self.pages(), before)

    def test_a_float_page_is_accepted_as_gradio_sends_it(self):
        """gr.Number hands back 3.0, not 3, even with precision=0."""
        if browse.to_display(self.bs["src_hi"]) < 3:
            self.skipTest("fixture book too short")
        self.bs = browse.goto(self.bs, "src", 3.0)
        self.assertEqual(browse.to_display(self.bs["src_page"]), 3)

    def test_an_unknown_side_is_refused_at_the_query(self):
        with store.ro() as con:
            with self.assertRaises(ValueError):
                browse.blocks(con, pid=self.proj["pid"],
                              book_key=self.bs["src_book"], side="../../etc")

    def test_chapter_numbers_are_parameters_not_string_building(self):
        self.bs = browse.jump_chapter(self.bs, "src",
                                      "1'; DROP TABLE setu_segment;--")
        self.assertTrue(store.Repository(self.con).one(
            "SELECT 1 AS ok FROM setu_segment LIMIT 1"))

    def test_a_ruined_state_is_repaired_not_fatal(self):
        for junk in (None, [], "state", {"src_page": "x", "linked": "yes"},
                     {"pid": 17, "offset": None}):
            with self.subTest(junk=junk):
                bs = browse.ensure(junk)
                self.assertIsInstance(bs["src_page"], int)
                self.assertIsInstance(bs["editing"], bool)

    def test_every_handler_survives_having_no_project(self):
        empty_state, empty_bs = uisession.blank(), browse.blank()
        cases = {
            "open": lambda: browse.open_books(empty_state, empty_bs),
            "goto": lambda: browse.goto(empty_bs, "src", 3),
            "step": lambda: browse.step(empty_bs, "src", 1),
            "both": lambda: browse.step_both(empty_bs, 1),
            "chapter": lambda: browse.jump_chapter(empty_bs, "src", "1"),
            "unlink": lambda: browse.unlink_pages(empty_bs),
        }
        for name, call in cases.items():
            with self.subTest(handler=name):
                self.assertIsInstance(call(), dict)
        self.assertIsInstance(browse.link_pages(empty_state, empty_bs), tuple)
        self.assertEqual(browse.load(empty_bs)["src"], [])
        self.assertEqual(browse.printed_page(empty_bs, "src"), (None, ""))
        self.assertEqual(browse.offset_note(empty_bs), "")


# ── what the columns show ──────────────────────────────────────────────────

class TestColumns(WorkspaceCase):

    def test_both_sides_come_from_one_load(self):
        data = browse.load(self.bs)
        self.assertIn("src", data)
        self.assertIn("tgt", data)
        self.assertIsInstance(data["src_tally"], str)
        self.assertIsInstance(data["tgt_tally"], str)

    def test_a_block_never_comes_from_the_other_book(self):
        with store.ro() as con:
            for side, book in (("src", self.bs["src_book"]),
                               ("tgt", self.bs["tgt_book"])):
                sids = {r["sid"] for r in browse.blocks(
                    con, pid=self.proj["pid"], book_key=book, side=side)}
                others = {r["sid"] for r in store.Repository(con).all(
                    "SELECT sid FROM setu_segment WHERE book_key <> ?", (book,))}
                self.assertFalse(sids & others)

    def test_segments_with_no_counterpart_are_shown_not_hidden(self):
        self.con.execute("DELETE FROM setu_row WHERE pid = ?", (self.proj["pid"],))
        self.con.commit()
        rows = self.rendered("src")
        self.assertTrue(rows)
        self.assertTrue(all(r["rid"] is None for r in rows))
        self.assertIn("no counterpart", browse.read_only_html(rows[0]))

    def test_noise_is_hidden_by_default_and_can_be_shown(self):
        with store.ro() as con:
            quiet = browse.blocks(con, pid=self.proj["pid"],
                                  book_key=self.bs["src_book"], side="src",
                                  hide_noise=True)
            loud = browse.blocks(con, pid=self.proj["pid"],
                                 book_key=self.bs["src_book"], side="src",
                                 hide_noise=False)
        self.assertLessEqual(len(quiet), len(loud))
        self.assertFalse({b["kind"] for b in quiet} & set(browse.NOISE_KINDS))

    def test_the_block_cap_is_enforced(self):
        with store.ro() as con:
            rows = browse.blocks(con, pid=self.proj["pid"],
                                 book_key=self.bs["src_book"], side="src",
                                 limit=10 ** 9)
        self.assertLessEqual(len(rows), browse.PAGE_BLOCKS)

    def test_text_from_the_corpus_cannot_inject_markup(self):
        sid = self.rendered("src")[0]["sid"]
        self.con.execute("UPDATE setu_segment SET source_text = ? WHERE sid = ?",
                         ("<script>alert('x')</script><img src=x onerror=1>", sid))
        self.con.commit()
        markup = "".join(browse.read_only_html(b) for b in self.rendered("src"))
        self.assertNotIn("<script", markup)
        self.assertNotIn("<img", markup)
        self.assertIn("&lt;script&gt;", markup)

    def test_untouched_text_is_labelled_as_the_machines_reading(self):
        """CMULAB's distinction: generated is not the same as confirmed."""
        block = next(b for b in self.rendered("src") if b["rid"])
        self.assertIn("as the parser read it", browse.block_heading(block))

    def test_the_tally_counts_what_is_on_the_page(self):
        self.assertRegex(browse.tally(self.rendered("src")),
                         r"\d+ blocks?|nothing on this page")

    def test_a_missing_pdf_is_a_sentence_not_a_crash(self):
        path, message = browse.printed_page(self.bs, "src")
        self.assertIsNone(path, "the fixture has no PDFs, so none can be shown")
        self.assertTrue(message)
        self.assertNotIn("Traceback", message)


# ── doing the work ─────────────────────────────────────────────────────────

class TestWork(WorkspaceCase):

    def edit(self, text="CORRECTED BY THE TEST"):
        block = next(b for b in self.rendered("src") if b["rid"])
        message = browse.save_text(self.st, block["rid"], "src", text,
                                   self.rev_of(block["rid"], "src"))
        return block, message

    def test_a_correction_is_saved_and_shows_immediately(self):
        block, message = self.edit()
        self.assertEqual(message, "Saved.")
        after = next(b for b in self.rendered("src") if b["rid"] == block["rid"])
        self.assertEqual(after["current"], "CORRECTED BY THE TEST")

    def test_the_parsers_reading_is_never_destroyed(self):
        block, _ = self.edit()
        after = next(b for b in self.rendered("src") if b["rid"] == block["rid"])
        self.assertEqual(after["source_text"], block["source_text"])
        self.assertNotEqual(after["source_text"], after["current"])

    def test_a_correction_can_be_undone(self):
        block, _ = self.edit()
        browse.restore_original(self.st, block["rid"], "src")
        after = next(b for b in self.rendered("src") if b["rid"] == block["rid"])
        self.assertEqual(after["current"], block["source_text"])

    def test_a_corrected_block_says_so(self):
        block, _ = self.edit()
        after = next(b for b in self.rendered("src") if b["rid"] == block["rid"])
        self.assertIn("corrected by hand", browse.block_heading(after))

    def test_a_stale_save_is_refused_not_applied(self):
        """Two annotators, one block. Neither may silently lose."""
        block, _ = self.edit("first")
        message = browse.save_text(self.st, block["rid"], "src", "second",
                                   base_rev=0)
        self.assertIn("Somebody else", message)
        after = next(b for b in self.rendered("src") if b["rid"] == block["rid"])
        self.assertEqual(after["current"], "first")

    def test_an_answer_is_recorded(self):
        block = next(b for b in self.rendered("src") if b["rid"])
        self.assertEqual(browse.set_answer(self.st, block["rid"], "exact"),
                         "Saved.")
        after = next(b for b in self.rendered("src") if b["rid"] == block["rid"])
        self.assertEqual(after["status"], "exact")
        self.assertIn("Exact", browse.block_heading(after))

    def test_an_unknown_answer_is_refused(self):
        block = next(b for b in self.rendered("src") if b["rid"])
        message = browse.set_answer(self.st, block["rid"],
                                    "definitely-not-a-status")
        self.assertTrue(message)
        self.assertNotEqual(message, "Saved.")

    def test_every_offered_answer_is_one_the_service_accepts(self):
        block = next(b for b in self.rendered("src") if b["rid"])
        for _label, key in browse.ANSWERS:
            with self.subTest(answer=key):
                self.assertEqual(
                    browse.set_answer(self.st, block["rid"], key), "Saved.")

    def test_saving_without_a_block_is_a_no_op(self):
        self.assertEqual(browse.save_text(self.st, "", "src", "x", 0), "")
        self.assertEqual(browse.set_answer(self.st, "", "exact"), "")
        self.assertEqual(browse.restore_original(self.st, "", "src"), "")


# ── the one that means stop ────────────────────────────────────────────────

class TestLegacyUntouched(WorkspaceCase):

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

    def test_a_full_workload_changes_none_of_tulanas_tables(self):
        before = self._fingerprint(self.con)
        for side in ("src", "tgt"):
            self.bs = browse.step(self.bs, side, 1)
            self.bs = browse.step(self.bs, side, -1)
            self.bs = browse.goto(self.bs, side, 2)
            self.bs = browse.jump_chapter(self.bs, side, "1")
        self.bs = browse.step_both(self.bs, 1)
        self.bs, _ = browse.link_pages(self.st, self.bs)
        self.bs = browse.unlink_pages(self.bs)
        browse.load(self.bs)
        browse.printed_page(self.bs, "src")
        block = next(b for b in self.rendered("src") if b["rid"])
        browse.save_text(self.st, block["rid"], "src", "edited",
                         self.rev_of(block["rid"], "src"))
        browse.set_answer(self.st, block["rid"], "exact")
        browse.restore_original(self.st, block["rid"], "src")
        self.assertEqual(before, self._fingerprint(self.con),
                         "the workspace changed one of Tulana's own tables")

    def test_moving_about_writes_nothing_at_all(self):
        """Navigation is read-only. Only the page link and an edit write."""
        def census():
            out = {}
            for r in self.con.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                    " AND name LIKE 'setu_%'"):
                name = r["name"] if hasattr(r, "keys") else r[0]
                try:
                    out[name] = self.con.execute(
                        f"SELECT COUNT(*) FROM {name}").fetchone()[0]
                except sqlite3.OperationalError:
                    out[name] = "unreadable"
            return out

        before = census()
        for side in ("src", "tgt"):
            self.bs = browse.step(self.bs, side, 1)
            self.bs = browse.jump_chapter(self.bs, side, "1")
        browse.load(self.bs)
        self.assertEqual(census(), before)


if __name__ == "__main__":                       # pragma: no cover
    unittest.main(verbosity=2)
