#!/usr/bin/env python3
"""Tests for the two-document browser.

Run with no arguments::

    python3 test_browse.py
    python3 test_browse.py -v

The fixture comes from ``test_annotation`` so both suites build the same small
synthetic corpus in the same throwaway database, and neither needs a textbook
on disk.

What is being defended here is one claim: **the two sides are independent.**
Every other view in Setu assumes row *n* on the left answers row *n* on the
right, and across the real corpus that assumption fails by as much as 111
pages. So these tests are mostly about movement — that one side moving leaves
the other alone, that linking makes it follow by exactly the offset the
annotator saw, and that nothing a browser can send (a page number of
``"; DROP TABLE"``, a float, ``None``, nine million) gets past the clamp.

Two tests are load-bearing rather than merely useful:

* ``test_every_handler_returns_the_same_shape`` — Gradio maps a returned tuple
  onto an output list positionally. A handler that returns eight values in a
  different order puts the Gujarati text into the English column and says
  nothing. This is the test that catches that.
* ``test_legacy_tables_untouched_by_browsing`` — the browser writes exactly one
  thing, the remembered page link, and it goes into ``setu_meta``. If this
  fails, stop.
"""
from __future__ import annotations

import hashlib
import sqlite3
import unittest

from test_annotation import LEGACY_TABLES, SetuCase          # noqa: E402

from annotation.core import annotate, store            # noqa: E402
from annotation.ui import browse, session as uisession        # noqa: E402


class BrowseCase(SetuCase):
    """A project, open in the browser, ready to be driven about."""

    #: The shared fixture puts every segment on page 1, which is fine for the
    #: pair tests it was written for and useless here — a browser whose whole
    #: subject is moving between pages needs more than one. The segments are
    #: spread over pages locally, in this suite only, so the movement tests
    #: exercise real page arithmetic instead of skipping.
    PER_PAGE = 1

    def setUp(self):
        super().setUp()
        self.proj = self.project()
        self._spread_over_pages()
        self.st = uisession.blank()
        self.st["pid"] = self.proj["pid"]
        self.st["annotator"] = "tester"
        self.bs = browse.open_books(self.st, browse.blank())[0]

    def _spread_over_pages(self):
        for book in (self.en, self.mr):
            self.con.execute(
                "UPDATE setu_segment SET page = ((seq - 1) / ?) + 1"
                " WHERE book_key = ?", (self.PER_PAGE, book))
        self.con.commit()

    def rev_of(self, rid, side):
        """The revision a save must quote. 0 until the side has been edited."""
        row = store.Repository(self.con).one(
            "SELECT rev FROM setu_text WHERE rid = ? AND side = ?", (rid, side))
        return row["rev"] if row else 0

    def rendered(self, side="src"):
        """The blocks the browser would actually draw on the current page."""
        with store.ro() as con:
            return browse.blocks(con, pid=self.proj["pid"],
                                 book_key=self.bs[f"{side}_book"], side=side,
                                 page=self.bs[f"{side}_page"],
                                 hide_noise=self.bs["hide_noise"])

    # -- helpers ---------------------------------------------------------
    def pages(self, bs=None):
        bs = self.bs if bs is None else bs
        return (bs["src_page"], bs["tgt_page"])

    def goto(self, side, page):
        self.bs = browse.goto(self.st, self.bs, side, page)[0]
        return self.bs

    def step(self, side, delta):
        self.bs = browse.step(self.st, self.bs, side, delta)[0]
        return self.bs


# ── the whole point: the two sides move apart ──────────────────────────────

class TestIndependence(BrowseCase):

    def test_opening_gives_both_sides_a_real_page(self):
        self.assertGreaterEqual(self.bs["src_page"], self.bs["src_lo"])
        self.assertGreaterEqual(self.bs["tgt_page"], self.bs["tgt_lo"])
        self.assertLessEqual(self.bs["src_page"], self.bs["src_hi"])
        self.assertLessEqual(self.bs["tgt_page"], self.bs["tgt_hi"])

    def test_moving_one_side_leaves_the_other_alone(self):
        before = self.pages()
        self.step("src", 1)
        self.assertEqual(self.bs["tgt_page"], before[1],
                         "the right-hand book moved when only the left was asked to")
        moved = self.bs["src_page"]
        self.step("tgt", 1)
        self.assertEqual(self.bs["src_page"], moved,
                         "the left-hand book moved when only the right was asked to")

    def test_the_sides_can_sit_at_different_pages(self):
        """English p4 beside the other edition's p2 — the reported case."""
        hi = min(self.bs["src_hi"], self.bs["tgt_hi"])
        if hi < 4:
            self.skipTest("fixture book is shorter than four pages")
        self.goto("src", 4)
        self.goto("tgt", 2)
        self.assertEqual(self.pages(), (4, 2))

    def test_chapter_is_chosen_per_side(self):
        self.bs = browse.jump_chapter(self.st, self.bs, "src", "1")[0]
        self.assertEqual(self.bs["src_chapter"], "1")
        self.assertEqual(self.bs["tgt_chapter"], "",
                         "choosing a chapter on the left changed the right")

    def test_two_sessions_do_not_share_state(self):
        other = browse.open_books(self.st, browse.blank())[0]
        self.goto("src", self.bs["src_hi"])
        self.assertNotEqual(self.bs["src_page"], other["src_page"]) \
            if self.bs["src_hi"] != other["src_page"] else None
        self.assertIsNot(self.bs, other)


# ── linking the two pages ──────────────────────────────────────────────────

class TestLinking(BrowseCase):

    def link_at(self, src, tgt):
        self.goto("src", src)
        self.goto("tgt", tgt)
        self.bs = browse.link_pages(self.st, self.bs)[0]

    def test_offset_is_what_the_annotator_saw(self):
        if self.bs["src_hi"] < 4 or self.bs["tgt_hi"] < 2:
            self.skipTest("fixture book too short")
        self.link_at(4, 2)
        self.assertTrue(self.bs["linked"])
        self.assertEqual(self.bs["offset"], 2)

    def test_the_other_side_follows_in_both_directions(self):
        if self.bs["src_hi"] < 6 or self.bs["tgt_hi"] < 4:
            self.skipTest("fixture book too short")
        self.link_at(4, 2)
        self.step("src", 1)
        self.assertEqual(self.pages(), (5, 3), "right did not follow the left")
        self.step("tgt", 1)
        self.assertEqual(self.pages(), (6, 4), "left did not follow the right")
        self.step("src", -2)
        self.assertEqual(self.pages(), (4, 2), "the link did not hold going back")

    def test_both_buttons_keep_the_gap_even_unlinked(self):
        if self.bs["src_hi"] < 5 or self.bs["tgt_hi"] < 3:
            self.skipTest("fixture book too short")
        self.goto("src", 3)
        self.goto("tgt", 1)
        self.bs = browse.step_both(self.st, self.bs, 2)[0]
        self.assertEqual(self.pages(), (5, 3))
        self.assertEqual(self.bs["src_page"] - self.bs["tgt_page"], 2)

    def test_both_buttons_stop_at_the_edge_without_lying(self):
        self.bs = browse.step_both(self.st, self.bs, -10_000)[0]
        self.assertEqual(self.pages(), (self.bs["src_lo"], self.bs["tgt_lo"]))
        out = browse.step_both(self.st, self.bs, -1)
        self.assertIn("first page", out[7])

    def test_a_chapter_jump_on_one_side_drags_the_other_when_linked(self):
        self.link_at(self.bs["src_lo"], self.bs["tgt_lo"])
        before = self.bs["tgt_page"]
        self.bs = browse.jump_chapter(self.st, self.bs, "src", "1")[0]
        if self.bs["src_page"] != self.bs["src_lo"]:
            self.assertNotEqual(self.bs["tgt_page"], before,
                                "linked, but the other side stayed put")

    def test_unlink_frees_the_sides_again(self):
        self.link_at(self.bs["src_lo"], self.bs["tgt_lo"])
        self.bs = browse.unlink_pages(self.st, self.bs)[0]
        self.assertFalse(self.bs["linked"])
        held = self.bs["tgt_page"]
        self.step("src", 1)
        self.assertEqual(self.bs["tgt_page"], held)

    def test_the_link_outlives_the_session(self):
        """An annotator's finding must reach the next annotator."""
        if self.bs["src_hi"] < 3:
            self.skipTest("fixture book too short")
        self.link_at(3, 1)
        fresh = browse.open_books(
            uisession.ensure({"pid": self.proj["pid"]}), browse.blank())[0]
        self.assertEqual((fresh["src_page"], fresh["tgt_page"]), (3, 1))
        self.assertTrue(fresh["linked"])
        self.assertEqual(fresh["offset"], 2)

    def test_unlink_removes_it_for_everyone(self):
        self.link_at(self.bs["src_lo"], self.bs["tgt_lo"])
        browse.unlink_pages(self.st, self.bs)
        with store.ro() as con:
            self.assertEqual(browse.load_link(con, self.proj["pid"]), {})

    def test_the_meta_key_cannot_be_driven_by_anything_typed(self):
        """The key is derived from the project id, never from user text."""
        self.con.execute("UPDATE setu_project SET name = ? WHERE pid = ?",
                         ("../../etc/passwd\n'; DROP TABLE setu_row;--",
                          self.proj["pid"]))
        self.con.commit()
        self.link_at(self.bs["src_lo"], self.bs["tgt_lo"])
        with store.ro() as con:
            keys = [r["key"] for r in store.Repository(con).all(
                "SELECT key FROM setu_meta WHERE key LIKE 'browse.link:%'", ())]
        self.assertEqual(keys, [f"browse.link:{self.proj['pid']}"])
        self.assertTrue(store.Repository(self.con).one(
            "SELECT 1 AS ok FROM setu_row LIMIT 1"), "setu_row survived, as it must")

    def test_a_corrupt_stored_link_is_ignored_not_fatal(self):
        with store.tx() as con:
            con.execute("INSERT INTO setu_meta(key, value) VALUES(?, ?)"
                        " ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                        (f"browse.link:{self.proj['pid']}", "{not json at all"))
        bs = browse.open_books(self.st, browse.blank())[0]
        self.assertFalse(bs["linked"])
        self.assertGreaterEqual(bs["src_page"], bs["src_lo"])


# ── nothing a browser can send gets through ────────────────────────────────

class TestHostileInput(BrowseCase):

    def test_page_numbers_are_clamped(self):
        for value in (10 ** 9, -10 ** 9, 0, "99999999999999999999"):
            with self.subTest(value=value):
                self.goto("src", value)
                self.assertGreaterEqual(self.bs["src_page"], self.bs["src_lo"])
                self.assertLessEqual(self.bs["src_page"], self.bs["src_hi"])

    def test_nonsense_page_numbers_change_nothing(self):
        for value in (None, "", "  ", "abc", "3; DROP TABLE setu_row",
                      "../../etc/passwd", "1e400", [], {}, object()):
            with self.subTest(value=value):
                before = self.pages()
                self.goto("src", value)
                self.assertEqual(self.pages(), before)

    def test_a_float_page_is_accepted_as_gradio_sends_it(self):
        """gr.Number hands back 3.0, not 3."""
        if self.bs["src_hi"] < 3:
            self.skipTest("fixture book too short")
        self.goto("src", 3.0)
        self.assertEqual(self.bs["src_page"], 3)

    def test_an_unknown_side_is_refused_at_the_query(self):
        with store.ro() as con:
            with self.assertRaises(ValueError):
                browse.blocks(con, pid=self.proj["pid"],
                              book_key=self.bs["src_book"], side="../../etc")

    def test_chapter_numbers_are_parameters_not_string_building(self):
        hostile = "1'; DROP TABLE setu_segment;--"
        self.bs = browse.jump_chapter(self.st, self.bs, "src", hostile)[0]
        self.assertTrue(store.Repository(self.con).one(
            "SELECT 1 AS ok FROM setu_segment LIMIT 1"),
            "setu_segment survived a hostile chapter number")

    def test_a_ruined_browser_state_is_repaired_not_fatal(self):
        for junk in (None, [], "state", {"src_page": "x", "linked": "yes"},
                     {"pid": 17, "offset": None}):
            with self.subTest(junk=junk):
                bs = browse.ensure(junk)
                self.assertIsInstance(bs["src_page"], int)
                self.assertIsInstance(bs["linked"], bool)

    def test_every_handler_survives_having_no_project(self):
        blank_state, blank_bs = uisession.blank(), browse.blank()
        for name, call in (
                ("open", lambda: browse.open_books(blank_state, blank_bs)),
                ("goto", lambda: browse.goto(blank_state, blank_bs, "src", 3)),
                ("step", lambda: browse.step(blank_state, blank_bs, "src", 1)),
                ("both", lambda: browse.step_both(blank_state, blank_bs, 1)),
                ("chapter", lambda: browse.jump_chapter(blank_state, blank_bs, "src", "1")),
                ("link", lambda: browse.link_pages(blank_state, blank_bs)),
                ("unlink", lambda: browse.unlink_pages(blank_state, blank_bs)),
                ("whole", lambda: browse.set_whole_chapter(blank_state, blank_bs, True)),
                ("noise", lambda: browse.set_hide_noise(blank_state, blank_bs, False))):
            with self.subTest(handler=name):
                out = call()
                self.assertIn(len(out), (8, 10))
                self.assertIsInstance(out[0], dict)


# ── the shape Gradio maps positionally ─────────────────────────────────────

class TestOutputShape(BrowseCase):

    HANDLERS = ("goto", "step", "step_both", "jump_chapter", "link_pages",
                "unlink_pages", "set_whole_chapter", "set_hide_noise")

    def test_every_handler_returns_the_same_shape(self):
        calls = {
            "goto": lambda: browse.goto(self.st, self.bs, "src", 2),
            "step": lambda: browse.step(self.st, self.bs, "src", 1),
            "step_both": lambda: browse.step_both(self.st, self.bs, 1),
            "jump_chapter": lambda: browse.jump_chapter(self.st, self.bs, "tgt", "1"),
            "link_pages": lambda: browse.link_pages(self.st, self.bs),
            "unlink_pages": lambda: browse.unlink_pages(self.st, self.bs),
            "set_whole_chapter": lambda: browse.set_whole_chapter(self.st, self.bs, True),
            "set_hide_noise": lambda: browse.set_hide_noise(self.st, self.bs, False),
        }
        for name in self.HANDLERS:
            with self.subTest(handler=name):
                out = calls[name]()
                self.assertEqual(len(out), 8, f"{name} returned {len(out)} values")
                self.assertIsInstance(out[0], dict, "slot 0 must be the state")
                self.assertIsInstance(out[1], str, "slot 1 must be the left HTML")
                self.assertIsInstance(out[2], str, "slot 2 must be the right HTML")
                self.assertIsInstance(out[5], str, "slot 5 must be the left tally")
                self.assertIsInstance(out[6], str, "slot 6 must be the right tally")
                self.assertIsInstance(out[7], str, "slot 7 must be the note")

    def test_open_returns_the_two_extra_dropdowns(self):
        out = browse.open_books(self.st, browse.blank())
        self.assertEqual(len(out), 10)

    def test_the_left_html_is_the_left_book(self):
        """The failure this guards is silent: the panes swap and nothing errors."""
        out = browse.goto(self.st, self.bs, "src", self.bs["src_lo"])
        self.assertIn('setu-doc-src', out[1])
        self.assertIn('setu_scroll_src', out[1])
        self.assertIn('setu-doc-tgt', out[2])
        self.assertIn('setu_scroll_tgt', out[2])
        self.assertNotIn('setu_scroll_tgt', out[1])
        self.assertNotIn('setu_scroll_src', out[2])

    def test_both_columns_carry_their_own_scroller(self):
        """The reported bug was one side not scrolling. Both get the class."""
        out = browse.goto(self.st, self.bs, "src", self.bs["src_lo"])
        for html_ in (out[1], out[2]):
            self.assertEqual(html_.count('class="setu-doc-scroll"'), 1)


# ── what the columns actually show ─────────────────────────────────────────

class TestContent(BrowseCase):

    def test_segments_with_no_counterpart_are_shown_not_hidden(self):
        """About a quarter of the real corpus. The old view could not show it."""
        with store.ro() as con:
            rows = browse.blocks(con, pid=self.proj["pid"],
                                 book_key=self.bs["src_book"], side="src",
                                 limit=browse.CHAPTER_BLOCKS)
        self.assertTrue(rows)
        # A segment belonging to no pair must still come back.
        self.con.execute("DELETE FROM setu_row WHERE pid = ? AND seq = ("
                         "  SELECT MIN(seq) FROM setu_row WHERE pid = ?)",
                         (self.proj["pid"], self.proj["pid"]))
        self.con.commit()
        with store.ro() as con:
            after = browse.blocks(con, pid=self.proj["pid"],
                                  book_key=self.bs["src_book"], side="src",
                                  limit=browse.CHAPTER_BLOCKS)
        self.assertEqual(len(after), len(rows),
                         "a segment vanished when its pair was removed")
        self.assertTrue(any(r["rid"] is None for r in after))

    def test_an_unpaired_block_says_so(self):
        self.con.execute("DELETE FROM setu_row WHERE pid = ?", (self.proj["pid"],))
        self.con.commit()
        out = browse.goto(self.st, self.bs, "src", self.bs["src_lo"])
        self.assertIn("not paired", out[1])

    def test_a_saved_edit_shows_immediately(self):
        """"Save and see what was saved" has to hold in this view too."""
        block = next(b for b in self.rendered("src") if b["rid"])
        rev = self.rev_of(block["rid"], "src")
        annotate.save_text(self.con, block["rid"], "src",
                           "EDITED-BY-THE-TEST", base_rev=rev,
                           annotator="tester")
        self.con.commit()
        out = browse.goto(self.st, self.bs, "src", self.bs["src_page"])
        self.assertIn("EDITED-BY-THE-TEST", out[1])

    def test_the_original_ocr_is_never_overwritten(self):
        block = next(b for b in self.rendered("src") if b["rid"])
        original = block["source_text"]
        annotate.save_text(self.con, block["rid"], "src", "something else",
                           base_rev=self.rev_of(block["rid"], "src"),
                           annotator="tester")
        self.con.commit()
        after = next(b for b in self.rendered("src")
                     if b["rid"] == block["rid"])
        self.assertEqual(after["source_text"], original,
                         "editing destroyed the original OCR")
        self.assertEqual(after["edited_text"], "something else")

    def test_text_from_the_corpus_cannot_inject_markup(self):
        sid = self.rendered("src")[0]["sid"]
        self.con.execute(
            "UPDATE setu_segment SET source_text = ? WHERE sid = ?",
            ("<script>alert('x')</script><img src=x onerror=alert(1)>", sid))
        self.con.commit()
        out = browse.goto(self.st, self.bs, "src", self.bs["src_page"])
        combined = out[1] + out[2]
        # The test is that no *tag* is formed. "onerror=" surviving as visible
        # text inside an escaped string is harmless and is what should happen.
        self.assertNotIn("<script", combined)
        self.assertNotIn("<img", combined)
        self.assertIn("&lt;script&gt;", combined)
        self.assertIn("&lt;img", combined)

    def test_an_edit_full_of_markup_is_escaped_too(self):
        """The edited text is annotator-supplied; it gets the same treatment."""
        block = next(b for b in self.rendered("src") if b["rid"])
        annotate.save_text(self.con, block["rid"], "src",
                           "<img src=x onerror=alert(1)>",
                           base_rev=self.rev_of(block["rid"], "src"),
                           annotator="tester")
        self.con.commit()
        out = browse.goto(self.st, self.bs, "src", self.bs["src_page"])
        self.assertNotIn("<img", out[1])
        self.assertIn("&lt;img", out[1])

    def test_a_block_never_comes_from_the_other_book(self):
        with store.ro() as con:
            for side, book in (("src", self.bs["src_book"]),
                               ("tgt", self.bs["tgt_book"])):
                rows = browse.blocks(con, pid=self.proj["pid"], book_key=book,
                                     side=side, limit=browse.CHAPTER_BLOCKS)
                sids = {r["sid"] for r in rows}
                wrong = store.Repository(con).all(
                    "SELECT sid FROM setu_segment WHERE book_key <> ?", (book,))
                self.assertFalse(sids & {r["sid"] for r in wrong})

    def test_noise_is_hidden_by_default_and_can_be_shown(self):
        with store.ro() as con:
            quiet = browse.blocks(con, pid=self.proj["pid"],
                                  book_key=self.bs["src_book"], side="src",
                                  hide_noise=True, limit=browse.CHAPTER_BLOCKS)
            loud = browse.blocks(con, pid=self.proj["pid"],
                                 book_key=self.bs["src_book"], side="src",
                                 hide_noise=False, limit=browse.CHAPTER_BLOCKS)
        self.assertLessEqual(len(quiet), len(loud))
        self.assertFalse({b["kind"] for b in quiet} & set(browse.NOISE_KINDS))

    def test_the_block_cap_is_enforced(self):
        with store.ro() as con:
            rows = browse.blocks(con, pid=self.proj["pid"],
                                 book_key=self.bs["src_book"], side="src",
                                 limit=10 ** 9)
        self.assertLessEqual(len(rows), browse.CHAPTER_BLOCKS)

    def test_each_book_gets_its_own_chapter_list(self):
        with store.ro() as con:
            left = browse.chapter_choices(con, self.bs["src_book"])
            right = browse.chapter_choices(con, self.bs["tgt_book"])
        self.assertEqual(left[0], ("Whole book", ""))
        self.assertEqual(right[0], ("Whole book", ""))
        self.assertTrue(len(left) > 1 or len(right) > 1)

    def test_a_page_with_nothing_on_it_explains_itself(self):
        out = browse.goto(self.st, self.bs, "src", self.bs["src_hi"])
        self.bs = out[0]
        with store.ro() as con:
            rows = browse.blocks(con, pid=self.proj["pid"],
                                 book_key=self.bs["src_book"], side="src",
                                 page=self.bs["src_page"])
        if not rows:
            self.assertIn("no text in this edition", out[1])

    def test_the_tally_counts_what_is_on_the_page(self):
        out = browse.goto(self.st, self.bs, "src", self.bs["src_lo"])
        self.assertRegex(out[5], r"\d+ blocks?|nothing here")


# ── the one that means stop ────────────────────────────────────────────────

class TestLegacyUntouchedByBrowsing(BrowseCase):

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

    def test_legacy_tables_untouched_by_browsing(self):
        before = self._fingerprint(self.con)
        # Everything the browser can be made to do.
        browse.open_books(self.st, self.bs)
        for side in ("src", "tgt"):
            self.bs = browse.step(self.st, self.bs, side, 1)[0]
            self.bs = browse.step(self.st, self.bs, side, -1)[0]
            self.bs = browse.goto(self.st, self.bs, side, 2)[0]
            self.bs = browse.jump_chapter(self.st, self.bs, side, "1")[0]
        self.bs = browse.step_both(self.st, self.bs, 1)[0]
        self.bs = browse.set_whole_chapter(self.st, self.bs, True)[0]
        self.bs = browse.set_hide_noise(self.st, self.bs, False)[0]
        self.bs = browse.link_pages(self.st, self.bs)[0]
        self.bs = browse.unlink_pages(self.st, self.bs)[0]
        self.assertEqual(before, self._fingerprint(self.con),
                         "browsing changed one of Tulana's own tables")

    def test_browsing_writes_nothing_but_the_link(self):
        """Read-only, except setu_meta. Proven by counting every Setu table."""
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
            self.bs = browse.step(self.st, self.bs, side, 1)[0]
            self.bs = browse.jump_chapter(self.st, self.bs, side, "1")[0]
        browse.set_whole_chapter(self.st, self.bs, True)
        after = census()
        for table, count in before.items():
            if table == "setu_meta":
                continue
            self.assertEqual(after[table], count,
                             f"browsing changed the row count of {table}")


if __name__ == "__main__":                         # pragma: no cover
    unittest.main(verbosity=2)
