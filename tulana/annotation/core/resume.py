"""Coming back to work you started.

An annotator opens two textbooks, answers a few hundred pairs, closes the tab
and goes home. Three days later they open the link again. Everything they did
is in the database — but until this module existed there was no way for them to
*find* it: they had to remember which board, which class, which language, and
pick the same two editions out of a dropdown of a hundred and twenty books. Get
one wrong and you are looking at an empty project wondering where your work
went.

So this module answers two questions, and only those two:

    what was I working on?      workbench()
    what have I answered?       saved_rows()

Both read across every project rather than requiring one to be open, because an
annotator returning after a weekend has no project open by definition.

WHERE THEY WERE
---------------
Position is remembered in ``setu_meta``, a key/value table Setu owns. The key
is built from the project id and a hash of the annotator's name — never from
the name itself, because a name is typed by a person and typed text must never
decide a storage key. ``place_key`` is the only function that builds one.

NOTHING HERE WRITES TO A PRE-EXISTING TABLE. The eight tables Tulana Studio
owns are read by nothing in this file and written by nothing in this file.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from typing import Any

from .store import Repository, paginate

# A place record is small and fixed-shape. Anything not in this set is dropped
# rather than stored, so a client cannot use the position record as a general
# scratch space that later code would have to trust.
PLACE_FIELDS = ("src_page", "tgt_page", "src_chapter", "tgt_chapter",
                "src_book", "tgt_book", "view", "mode")
PLACE_MAX = 2000                       # bytes of JSON; a position is tiny
_SAFE_KEY = re.compile(r"^[A-Za-z0-9_.:-]+$")


def place_key(pid: str, annotator: str = "") -> str:
    """The setu_meta key holding one annotator's position in one project.

    The project id is already a generated identifier, so it is safe verbatim
    once checked. The annotator's name is *typed*, so it never appears in the
    key — only twelve hex characters of its digest do. Two people with the same
    name share a position, which is the correct trade: the alternative is
    letting a person's keystrokes name a row.
    """
    pid = str(pid or "")
    if not _SAFE_KEY.match(pid):
        raise ValueError("project id is not an identifier")
    who = (annotator or "").strip().lower()
    tag = hashlib.sha256(who.encode("utf-8")).hexdigest()[:12] if who else "anon"
    return f"place:{pid}:{tag}"


def remember_place(con, pid: str, annotator: str, place: Any) -> dict:
    """Store where this annotator is in this project. Never raises on bad input."""
    keep: dict[str, Any] = {}
    if isinstance(place, dict):
        for f in PLACE_FIELDS:
            v = place.get(f)
            if v is None:
                continue
            if isinstance(v, bool):                      # not a page number
                continue
            if isinstance(v, (int, float)):
                if v != v or v in (float("inf"), float("-inf")):
                    continue
                keep[f] = int(v)
            elif isinstance(v, str):
                keep[f] = v[:200]
    keep["at"] = time.time()
    blob = json.dumps(keep, ensure_ascii=False)[:PLACE_MAX]
    key = place_key(pid, annotator)
    con.execute("INSERT INTO setu_meta(key, value) VALUES(?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, blob))
    return keep


def recall_place(con, pid: str, annotator: str) -> dict:
    """Read back a position. A missing or corrupt record is simply no position."""
    try:
        key = place_key(pid, annotator)
    except ValueError:
        return {}
    row = con.execute("SELECT value FROM setu_meta WHERE key = ?", (key,)).fetchone()
    if not row:
        return {}
    try:
        got = json.loads(row[0])
    except (ValueError, TypeError):
        return {}
    return got if isinstance(got, dict) else {}


#: A row answered as if it had two sides, when it has one. Selecting a block
#: on each side of two DIFFERENT rows used to look like a pair on screen, and
#: the answer then landed on a row whose other half was empty.
_CONTRADICTION = ("(r.status IN ('exact', 'needs_correction', 'structural_mismatch')"
                  " AND (r.src_sid IS NULL OR r.tgt_sid IS NULL))")

#: A side that has a passage but whose saved correction is empty. Setu no
#: longer saves these and repairs old ones at start-up; this catches anything
#: that slipped through, so it is never invisible.
_BLANK = ("EXISTS (SELECT 1 FROM setu_text bt WHERE bt.rid = r.rid"
          " AND trim(bt.text, char(32, 9, 13, 10)) = ''"
          " AND ((bt.side = 'src' AND r.src_sid IS NOT NULL)"
          "   OR (bt.side = 'tgt' AND r.tgt_sid IS NOT NULL)))")

ATTENTION = f"({_CONTRADICTION} OR {_BLANK})"


def _like(text: str) -> str:
    """A LIKE pattern that matches *text* literally — "100%" means 100%."""
    t = str(text)[:200].replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{t}%"


class ResumeRepo(Repository):
    """Reads that span projects, for an annotator who has none open."""

    # ── what was I working on? ─────────────────────────────────────────────
    def workbench(self, *, annotator: str = "", limit: Any = 40,
                  offset: Any = 0) -> dict:
        """Every project, most recently worked on first.

        Ordered by real activity — the newest ``setu_row.updated_at`` in the
        project — and not by creation time, because the project you made first
        is rarely the one you were in last.
        """
        lim, off = paginate(limit, offset, default=40, cap=200)
        rows = self.all(
            """SELECT p.pid, p.name, p.board, p.class, p.subject,
                      p.src_language, p.tgt_language, p.src_book, p.tgt_book,
                      p.n_rows, p.created_at, p.created_by,
                      sb.title AS src_title, sb.book AS src_book_name,
                      sb.board_name AS board_name, sb.num_pages AS src_pages,
                      sb.pdf_present AS src_pdf,
                      tb.title AS tgt_title, tb.book AS tgt_book_name,
                      tb.num_pages AS tgt_pages, tb.pdf_present AS tgt_pdf,
                      (SELECT COUNT(*) FROM setu_row r
                        WHERE r.pid = p.pid AND r.status <> 'pending') AS answered,
                      (SELECT COUNT(*) FROM setu_row r
                        WHERE r.pid = p.pid AND r.edited = 1)          AS corrected,
                      (SELECT MAX(r.updated_at) FROM setu_row r
                        WHERE r.pid = p.pid)                           AS touched,
                      (SELECT r.seq FROM setu_row r
                        WHERE r.pid = p.pid AND r.status <> 'pending'
                        ORDER BY r.updated_at DESC, r.seq DESC LIMIT 1) AS last_seq
                 FROM setu_project p
                 JOIN setu_book sb ON sb.book_key = p.src_book
                 JOIN setu_book tb ON tb.book_key = p.tgt_book
                ORDER BY COALESCE(
                    (SELECT MAX(r.updated_at) FROM setu_row r WHERE r.pid = p.pid),
                    p.created_at) DESC
                LIMIT ? OFFSET ?""", (lim, off))

        for r in rows:
            total = int(r.get("n_rows") or 0)
            done = int(r.get("answered") or 0)
            r["total"] = total
            r["percent"] = round(done * 100.0 / total, 1) if total else 0.0
            r["remaining"] = max(0, total - done)
            r["place"] = recall_place(self.con, r["pid"], annotator)
            r["label"] = self._label(r)
            r["where"] = self._where(r)

        total_projects = self.one("SELECT COUNT(*) AS n FROM setu_project") or {"n": 0}
        return {"projects": rows, "total": int(total_projects.get("n") or 0),
                "annotator": annotator}

    @staticmethod
    def _label(r: dict) -> str:
        """One line naming the work, the way an annotator would say it.

        'Maharashtra State Board · Class 10 · Mathematics · English ⇄ Gujarati'
        """
        bits = [r.get("board_name") or r.get("board") or ""]
        if r.get("class"):
            bits.append(f"Class {r['class']}")
        if r.get("subject"):
            bits.append(str(r["subject"]))
        pair = " ⇄ ".join(x for x in (r.get("src_language"), r.get("tgt_language")) if x)
        if pair:
            bits.append(pair)
        return " · ".join(b for b in bits if b)

    @staticmethod
    def _where(r: dict) -> str:
        """A human sentence about how far this project got."""
        done, total = int(r.get("answered") or 0), int(r.get("total") or 0)
        if not total:
            return "nothing to annotate yet"
        if not done:
            return f"not started — {total:,} pairs waiting"
        if done >= total:
            return f"finished — all {total:,} pairs answered"
        return f"{done:,} of {total:,} answered · {total - done:,} left"

    # ── what have I answered? ──────────────────────────────────────────────
    def saved_rows(self, *, pid: str = "", status: str = "", answered: str = "",
                   search: str = "", chapter_no: str = "", kind: str = "",
                   edited: Any = None, attention: Any = False,
                   limit: Any = 40, offset: Any = 0) -> dict:
        """Answered and corrected rows, across one project or all of them.

        The Saved-work tab must work when nothing is open, so ``pid`` is
        optional here in a way it is not on the project endpoints.
        """
        lim, off = paginate(limit, offset, default=40, cap=200)
        where, args = ["1 = 1"], []

        if pid:
            where.append("r.pid = ?")
            args.append(str(pid)[:64])
        if status:
            where.append("r.status = ?")
            args.append(str(status)[:40])
        elif answered == "done":
            where.append("r.status <> 'pending'")
        elif answered == "pending":
            where.append("r.status = 'pending'")
        if chapter_no:
            where.append("r.chapter_no = ?")
            args.append(str(chapter_no)[:40])
        if kind:
            where.append("r.kind = ?")
            args.append(str(kind)[:40])
        if edited is True:
            where.append("r.edited = 1")
        elif edited is False:
            where.append("r.edited = 0")
        if attention in (True, 1, "1", "true", "yes"):
            where.append(ATTENTION)

        # Search runs over the text an annotator can actually see: the current
        # text of either side, which is the correction when one exists and the
        # parser's reading when it does not.
        if search:
            needle = _like(search)
            where.append(
                """EXISTS (SELECT 1 FROM setu_text t
                            WHERE t.rid = r.rid AND t.text LIKE ? ESCAPE '\\')
                   OR EXISTS (SELECT 1 FROM setu_segment s
                               WHERE (s.sid = r.src_sid OR s.sid = r.tgt_sid)
                                 AND s.source_text LIKE ? ESCAPE '\\')""")
            args.extend([needle, needle])

        clause = " AND ".join(f"({w})" for w in where)
        total = self.one(f"SELECT COUNT(*) AS n FROM setu_row r WHERE {clause}",
                         args) or {"n": 0}

        rows = self.all(
            f"""SELECT r.rid, r.pid, r.seq, r.status, r.note, r.kind,
                       r.chapter, r.chapter_no, r.src_page, r.tgt_page,
                       r.edited, r.updated_at, r.updated_by,
                       p.name AS project, p.board, p.class, p.subject,
                       p.src_language, p.tgt_language,
                       r.src_sid, r.tgt_sid,
                       ss.source_text AS src_source, ts.source_text AS tgt_source,
                       st.text AS src_edited, tt.text AS tgt_edited,
                       {_CONTRADICTION} AS contradiction, {_BLANK} AS blank
                  FROM setu_row r
                  JOIN setu_project p ON p.pid = r.pid
             LEFT JOIN setu_segment ss ON ss.sid = r.src_sid
             LEFT JOIN setu_segment ts ON ts.sid = r.tgt_sid
             LEFT JOIN setu_text st ON st.rid = r.rid AND st.side = 'src'
             LEFT JOIN setu_text tt ON tt.rid = r.rid AND tt.side = 'tgt'
                 WHERE {clause}
              ORDER BY r.updated_at DESC, r.seq ASC
                 LIMIT ? OFFSET ?""", [*args, lim, off])

        for r in rows:
            for side in ("src", "tgt"):
                present = r.get(f"{side}_sid") is not None   # kept: "Open" selects it
                edit = r.pop(f"{side}_edited", None)
                source = r.pop(f"{side}_source", None)
                # A saved correction is shown whenever one EXISTS — even an
                # empty one — never swapped for the parser's text behind the
                # annotator's back. "Is there a passage here at all?" is a
                # separate question, answered by `present`.
                r[f"{side}_present"] = present
                r[f"{side}_text"] = "" if not present else (
                    edit if edit is not None else (source or ""))
                r[f"{side}_edited"] = bool(present and edit is not None
                                           and edit.rstrip(" \t\r\n")
                                           != (source or "").rstrip(" \t\r\n"))
            r["src_display"] = None if r.get("src_page") is None else int(r["src_page"]) + 1
            r["tgt_display"] = None if r.get("tgt_page") is None else int(r["tgt_page"]) + 1
            r["attention"] = self._why(r)
            r.pop("contradiction", None)
            r.pop("blank", None)

        return {"rows": rows, "total": int(total.get("n") or 0),
                "limit": lim, "offset": off}

    @staticmethod
    def _why(r: dict) -> str:
        """A sentence saying why this row needs another look, or ''."""
        if r.get("contradiction"):
            missing = "right" if r.get("src_present") else "left"
            return (f"Answered as a pair, but there is nothing on the {missing}. "
                    f"Open it and pair it with its partner, or change the answer "
                    f"to “Missing or incomplete”.")
        if r.get("blank"):
            return ("A side was saved empty. Open it and type the text, or put "
                    "back what the parser read.")
        return ""

    def saved_tally(self, *, pid: str = "") -> dict:
        """Counts by status, for the line above the list."""
        where, args = ("r.pid = ?", [pid]) if pid else ("1 = 1", [])
        rows = self.all(
            f"""SELECT r.status AS status, COUNT(*) AS n
                  FROM setu_row r WHERE {where} GROUP BY r.status""", args)
        by = {r["status"]: int(r["n"]) for r in rows}
        total = sum(by.values())
        answered = total - by.get("pending", 0)
        corrected = self.one(
            f"SELECT COUNT(*) AS n FROM setu_row r WHERE {where} AND r.edited = 1",
            args) or {"n": 0}
        attention = self.one(
            f"SELECT COUNT(*) AS n FROM setu_row r WHERE {where} AND {ATTENTION}",
            args) or {"n": 0}
        return {"by_status": by, "total": total, "answered": answered,
                "corrected": int(corrected.get("n") or 0),
                "attention": int(attention.get("n") or 0)}

    def projects_with_work(self) -> list[dict]:
        """The textbook dropdown for the Saved-work tab.

        Every project, with how many rows have been answered in it, so the
        annotator can tell at a glance which one holds the work they want.
        """
        return self.all(
            """SELECT p.pid, p.name, p.board, p.class, p.subject,
                      p.src_language, p.tgt_language, p.n_rows,
                      (SELECT COUNT(*) FROM setu_row r
                        WHERE r.pid = p.pid AND r.status <> 'pending') AS answered
                 FROM setu_project p
                ORDER BY p.created_at DESC""")
