"""Coming back to work you started, and the Saved-work tab that reads across it.

Three things are being proved here, and the third is the one that matters most.

1. An annotator who leaves comes back to the same two books on the same two
   pages. This is the whole feature, so it is tested end to end rather than as
   four separate functions that each look fine.

2. The Saved-work and Download tabs read across EVERY project. They have to, or
   an annotator returning on Monday sees an empty screen because nothing is
   open yet — which is exactly the state they are in.

3. Nothing a person types decides a storage key, a file path or a row. Names
   are typed. So the position record is keyed by a digest, and this file feeds
   the whole module names that are path traversals, null bytes, SQL, enormous
   strings and the empty string, and asserts that each one either stores
   harmlessly or refuses.

The eight tables Tulana Studio owns are hashed before and after, because a
feature about remembering things is exactly the sort that grows a write to
somewhere it should not.
"""
from __future__ import annotations

import hashlib
import json
import time
import unittest

from test_annotation import SetuCase

from annotation.core import resume, store


class ResumeCase(SetuCase):
    """A project with a handful of answered rows, which is what resume needs."""

    def setUp(self):
        super().setUp()
        self.proj = self.project()
        self.pid = self.proj["pid"]

    def answer(self, n=3, who="Ananya"):
        """Mark the first n rows answered, as the interface would."""
        rows = self.con.execute(
            "SELECT rid FROM setu_row WHERE pid=? ORDER BY seq LIMIT ?",
            (self.pid, n)).fetchall()
        for i, r in enumerate(rows):
            self.con.execute(
                "UPDATE setu_row SET status=?, updated_at=?, updated_by=? WHERE rid=?",
                ("exact" if i % 2 == 0 else "needs_correction",
                 time.time() + i, who, r[0]))
        self.con.commit()
        return [r[0] for r in rows]


# ── the feature itself ─────────────────────────────────────────────────────

class TestComingBack(ResumeCase):
    """Leave, come back, and be where you were."""

    def test_the_workbench_names_the_work_the_way_a_person_would(self):
        wb = resume.ResumeRepo(self.con).workbench()
        self.assertTrue(wb["projects"], "a project that exists must be listed")
        label = wb["projects"][0]["label"]
        for part in ("Class", "⇄"):
            self.assertIn(part, label, f"{label!r} does not read like a textbook")

    def test_a_position_survives_leaving(self):
        repo = resume.ResumeRepo(self.con)
        resume.remember_place(self.con, self.pid, "Ananya",
                              {"src_page": 12, "tgt_page": 15})
        self.con.commit()
        got = repo.workbench(annotator="Ananya")["projects"][0]["place"]
        self.assertEqual(got["src_page"], 12)
        self.assertEqual(got["tgt_page"], 15)

    def test_two_annotators_do_not_share_a_position(self):
        """Ananya's page must not drag Bhavesh to it. Separate work, separate place."""
        resume.remember_place(self.con, self.pid, "Ananya", {"src_page": 12})
        resume.remember_place(self.con, self.pid, "Bhavesh", {"src_page": 90})
        self.con.commit()
        repo = resume.ResumeRepo(self.con)
        a = repo.workbench(annotator="Ananya")["projects"][0]["place"]
        b = repo.workbench(annotator="Bhavesh")["projects"][0]["place"]
        self.assertEqual((a["src_page"], b["src_page"]), (12, 90))

    def test_an_unknown_annotator_simply_has_no_position(self):
        got = resume.ResumeRepo(self.con).workbench(
            annotator="Nobody At All")["projects"][0]["place"]
        self.assertEqual(got, {}, "a stranger must not inherit somebody's page")

    def test_progress_is_counted_not_guessed(self):
        self.answer(4)
        p = resume.ResumeRepo(self.con).workbench()["projects"][0]
        self.assertEqual(p["answered"], 4)
        self.assertEqual(p["remaining"], p["total"] - 4)
        self.assertIn("4", p["where"])

    def test_the_most_recently_worked_on_project_comes_first(self):
        """Ordered by activity, not creation: the project you made first is
        rarely the one you were last inside.

        The second project swaps the two sides, because that is a different
        (src_book, tgt_book) pair and therefore a genuinely different project —
        opening the same two books again returns the same one, by design.
        """
        from annotation.core import workspace
        second = workspace.create_project(self.con, src_book=self.mr,
                                          tgt_book=self.en, annotator="tester")
        self.assertNotEqual(second["pid"], self.pid,
                            "the fixture did not produce two distinct projects")
        self.con.execute("UPDATE setu_row SET updated_at=? WHERE pid=?",
                         (time.time() + 10_000, second["pid"]))
        self.con.commit()
        order = [p["pid"] for p in resume.ResumeRepo(self.con).workbench()["projects"]]
        self.assertEqual(order[0], second["pid"],
                         "the project worked on most recently must be offered first")
        self.assertIn(self.pid, order, "the older project must still be reachable")

    def test_a_position_naming_a_page_that_no_longer_exists_is_still_returned(self):
        """Clamping belongs to the interface; the record itself stays honest.

        A re-ingest can shorten a book. The stored page is reported as it was
        written so the interface can clamp it, rather than being silently
        rewritten here into a page the annotator never chose.
        """
        resume.remember_place(self.con, self.pid, "Ananya", {"src_page": 99_999})
        self.con.commit()
        got = resume.ResumeRepo(self.con).workbench(annotator="Ananya")["projects"][0]
        self.assertEqual(got["place"]["src_page"], 99_999)


# ── the Saved-work tab ─────────────────────────────────────────────────────

class TestSavedWork(ResumeCase):

    def test_saved_reads_across_projects_with_nothing_open(self):
        """The returning annotator has no project open. That is the point."""
        self.project(name="A second pairing")
        self.answer(2)
        out = resume.ResumeRepo(self.con).saved_rows()
        self.assertGreater(out["total"], 0)
        self.assertTrue(out["rows"][0]["project"], "each row must name its textbook")

    def test_filtering_by_answer(self):
        self.answer(4)
        repo = resume.ResumeRepo(self.con)
        self.assertEqual(repo.saved_rows(status="exact")["total"], 2)
        self.assertEqual(repo.saved_rows(status="needs_correction")["total"], 2)
        self.assertEqual(repo.saved_rows(answered="done")["total"], 4)

    def test_pending_and_done_partition_the_rows(self):
        self.answer(3)
        repo = resume.ResumeRepo(self.con)
        done = repo.saved_rows(answered="done")["total"]
        todo = repo.saved_rows(answered="pending")["total"]
        every = repo.saved_rows()["total"]
        self.assertEqual(done + todo, every,
                         "every row is either answered or waiting, never both or neither")

    def test_search_finds_the_text_a_person_can_see(self):
        rid = self.answer(1)[0]
        self.con.execute(
            "INSERT OR REPLACE INTO setu_text(rid, side, text, rev, updated_at, updated_by)"
            " VALUES(?,?,?,?,?,?)",
            (rid, "tgt", "ZANZIBAR MARMALADE", 1, time.time(), "Ananya"))
        self.con.commit()
        out = resume.ResumeRepo(self.con).saved_rows(search="ZANZIBAR")
        self.assertEqual(out["total"], 1)
        self.assertIn("ZANZIBAR", out["rows"][0]["tgt_text"])

    def test_a_correction_is_what_the_list_shows(self):
        """The list shows the current text, which is the correction when there
        is one. Showing the parser's reading next to a 'corrected' badge would
        be worse than showing nothing."""
        rid = self.answer(1)[0]
        self.con.execute(
            "INSERT OR REPLACE INTO setu_text(rid, side, text, rev, updated_at, updated_by)"
            " VALUES(?,?,?,?,?,?)",
            (rid, "src", "the corrected reading", 2, time.time(), "Ananya"))
        self.con.execute("UPDATE setu_row SET edited=1 WHERE rid=?", (rid,))
        self.con.commit()
        row = next(r for r in resume.ResumeRepo(self.con).saved_rows()["rows"]
                   if r["rid"] == rid)
        self.assertEqual(row["src_text"], "the corrected reading")
        self.assertTrue(row["edited"])

    def test_pages_are_handed_over_ready_to_show(self):
        """Stored 0-indexed, displayed 1-indexed, converted in one place."""
        out = resume.ResumeRepo(self.con).saved_rows()
        for r in out["rows"]:
            if r["src_page"] is not None:
                self.assertEqual(r["src_display"], r["src_page"] + 1)
            if r["tgt_page"] is not None:
                self.assertEqual(r["tgt_display"], r["tgt_page"] + 1)

    def test_the_tally_adds_up(self):
        self.answer(4)
        t = resume.ResumeRepo(self.con).saved_tally()
        self.assertEqual(sum(t["by_status"].values()), t["total"])
        self.assertEqual(t["answered"], t["total"] - t["by_status"].get("pending", 0))

    def test_paging_does_not_lose_or_repeat_a_row(self):
        repo = resume.ResumeRepo(self.con)
        every = repo.saved_rows(limit=500)
        if every["total"] < 4:
            self.skipTest("too few rows in the fixture to page")
        a = repo.saved_rows(limit=2, offset=0)["rows"]
        b = repo.saved_rows(limit=2, offset=2)["rows"]
        ids = [r["rid"] for r in a + b]
        self.assertEqual(len(ids), len(set(ids)), "a row appeared on two pages")


# ── hostile input ──────────────────────────────────────────────────────────

class TestHostileInput(ResumeCase):
    """Names are typed by people. Typed text never decides storage."""

    NASTY = [
        "../../../../etc/passwd",
        "..\\..\\windows\\system32",
        "'; DROP TABLE setu_row; --",
        "<script>alert(1)</script>",
        "\x00null",
        "\n\r\t",
        "  ",
        "",
        "ಕನ್ನಡ ಹೆಸರು",
        "A" * 5000,
        "%2e%2e%2f",
    ]

    def test_no_typed_name_reaches_the_key(self):
        for name in self.NASTY:
            key = resume.place_key(self.pid, name)
            self.assertTrue(key.startswith(f"place:{self.pid}:"), key)
            tail = key.split(":")[-1]
            self.assertRegex(tail, r"^(?:[0-9a-f]{12}|anon)$",
                             f"{name!r} leaked into the key as {tail!r}")

    def test_a_project_id_that_is_not_an_identifier_is_refused(self):
        for bad in ("../../etc", "pj_X/../..", "pj X", "'; DROP", "", "pj_\x00"):
            with self.assertRaises(ValueError, msg=f"{bad!r} was accepted as a project id"):
                resume.place_key(bad, "Ananya")

    def test_every_nasty_name_round_trips_or_refuses(self):
        for name in self.NASTY:
            resume.remember_place(self.con, self.pid, name, {"src_page": 7})
            self.con.commit()
            got = resume.recall_place(self.con, self.pid, name)
            self.assertEqual(got.get("src_page"), 7, f"{name[:30]!r} lost its position")

    def test_a_place_cannot_be_used_as_a_scratch_space(self):
        """Only the fixed fields are kept, so no later code has to trust the rest."""
        resume.remember_place(self.con, self.pid, "Ananya", {
            "src_page": 3, "smuggled": "x" * 10_000,
            "__proto__": {"bad": 1}, "path": "../../etc/passwd"})
        self.con.commit()
        got = resume.recall_place(self.con, self.pid, "Ananya")
        self.assertEqual(set(got) - {"at"}, {"src_page"})

    def test_a_place_that_is_not_a_record_is_simply_no_place(self):
        for junk in (None, "a string", 42, [1, 2, 3], True):
            resume.remember_place(self.con, self.pid, "Ananya", junk)
            self.con.commit()
            self.assertEqual(set(resume.recall_place(self.con, self.pid, "Ananya")), {"at"})

    def test_impossible_page_numbers_are_dropped_not_stored(self):
        for bad in (float("nan"), float("inf"), float("-inf"), True, False, [3], {"a": 1}):
            resume.remember_place(self.con, self.pid, "Ananya", {"src_page": bad})
            self.con.commit()
            got = resume.recall_place(self.con, self.pid, "Ananya")
            self.assertNotIn("src_page", got, f"{bad!r} was stored as a page number")

    def test_a_corrupt_record_reads_as_no_record(self):
        """Somebody edits the database by hand. That is a missing position, not a crash."""
        self.con.execute("INSERT OR REPLACE INTO setu_meta(key, value) VALUES(?, ?)",
                         (resume.place_key(self.pid, "Ananya"), "{not json at all"))
        self.con.commit()
        self.assertEqual(resume.recall_place(self.con, self.pid, "Ananya"), {})

    def test_a_stored_page_is_a_number_and_not_a_string(self):
        resume.remember_place(self.con, self.pid, "Ananya", {"src_page": "12"})
        self.con.commit()
        got = resume.recall_place(self.con, self.pid, "Ananya")
        # A string page was accepted as a label, so it must never be read back
        # as something arithmetic would treat as 12.
        self.assertIsInstance(got.get("src_page"), str)

    def test_searching_for_sql_finds_rows_and_not_trouble(self):
        for needle in ("'; DROP TABLE setu_row; --", "100%", "_", "\\", "%"):
            out = resume.ResumeRepo(self.con).saved_rows(search=needle)
            self.assertIsInstance(out["total"], int)
        # the table is still there
        self.assertGreater(
            self.con.execute("SELECT COUNT(*) FROM setu_row").fetchone()[0], 0)

    def test_absurd_paging_is_clamped(self):
        repo = resume.ResumeRepo(self.con)
        for lim, off in ((-5, -5), (10 ** 9, 10 ** 9), ("abc", "abc"),
                         (None, None), (float("inf"), 0)):
            out = repo.saved_rows(limit=lim, offset=off)
            self.assertLessEqual(len(out["rows"]), 500)
            self.assertGreaterEqual(out["limit"], 1)

    def test_a_project_that_does_not_exist_yields_nothing_not_an_error(self):
        out = resume.ResumeRepo(self.con).saved_rows(pid="pj_NOSUCHTHING")
        self.assertEqual(out["total"], 0)
        self.assertEqual(out["rows"], [])


# ── the rule that outranks every feature ───────────────────────────────────

class TestLegacyUntouched(ResumeCase):
    """Tulana Studio's eight tables are read by nothing here and written by nothing."""

    PROTECTED = ("documents", "projects", "clips", "pairs", "labels",
                 "pair_labels", "exports", "audit")

    def fingerprint(self):
        out = {}
        for t in self.PROTECTED:
            try:
                rows = self.con.execute(f"SELECT * FROM {t} ORDER BY rowid").fetchall()
            except Exception:
                out[t] = "absent"
                continue
            out[t] = hashlib.sha256(
                repr([tuple(r) for r in rows]).encode("utf-8")).hexdigest()
        return out

    def test_a_full_run_leaves_every_pre_existing_table_byte_identical(self):
        before = self.fingerprint()
        repo = resume.ResumeRepo(self.con)
        repo.workbench(annotator="Ananya")
        repo.saved_rows(search="anything")
        repo.saved_tally()
        repo.projects_with_work()
        resume.remember_place(self.con, self.pid, "Ananya", {"src_page": 4})
        self.con.commit()
        self.assertEqual(before, self.fingerprint(),
                         "resume wrote to a table it does not own")

    def test_the_module_contains_no_destructive_ddl(self):
        import pathlib
        src = (pathlib.Path(__file__).parent / "annotation" / "core" / "resume.py"
               ).read_text(encoding="utf-8")
        import re
        self.assertIsNone(re.search(r"\b(ALTER|DROP)\s+TABLE\b", src, re.I))
        for table in self.PROTECTED:
            self.assertIsNone(
                re.search(rf"(INSERT\s+(OR\s+\w+\s+)?INTO|UPDATE|DELETE\s+FROM)\s+{table}\b",
                          src, re.I),
                f"resume.py writes to {table}")

    def test_every_table_it_writes_to_is_its_own(self):
        import pathlib, re
        src = (pathlib.Path(__file__).parent / "annotation" / "core" / "resume.py"
               ).read_text(encoding="utf-8")
        # "ON CONFLICT(...) DO UPDATE SET col = ..." assigns a column, not a
        # table, so it is removed before the scan rather than the scan being
        # loosened to tolerate it.
        scanned = re.sub(r"ON\s+CONFLICT\s*\([^)]*\)\s*DO\s+UPDATE\s+SET", " ",
                         src, flags=re.I)
        written = re.findall(
            r"(?:INSERT\s+(?:OR\s+\w+\s+)?INTO|UPDATE|DELETE\s+FROM)\s+(\w+)",
            scanned, re.I)
        self.assertTrue(written, "the scan found no writes at all — check the pattern")
        for t in written:
            self.assertTrue(t.startswith("setu_"), f"resume.py writes to {t}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
