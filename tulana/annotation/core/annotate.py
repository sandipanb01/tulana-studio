"""Setu — editing, autosaving and remembering.

The rules this module exists to enforce, in order of how much damage breaking
them would do:

1. **The parser's extraction is never overwritten.** An edit writes to
   ``setu_text``; ``setu_segment.source_text`` is read-only for the lifetime of
   the database. "Restore the original" therefore always works, on any row, at
   any distance in the future, even after fifty edits.

2. **No write ever lands blind.** Every save carries the revision it was based
   on. If the stored revision has moved, the save is refused and both texts come
   back so a person can decide. Last-writer-wins is how two annotators silently
   destroy each other's afternoon.

3. **Every version is kept.** ``setu_rev`` is append-only. Nothing in Setu
   deletes from it, including project deletion.

4. **Saving is cheap enough to do constantly.** A save that does not change the
   text does no work and allocates no revision, so an autosave firing on a
   cursor move costs one indexed lookup.
"""
from __future__ import annotations

import difflib
import logging
import re
import time
from typing import Any

from .models import DEFAULT_STATUS, normalise, side_of, valid_status
from .store import Conflict, Invalid, NotFound, Repository, paginate
from .workspace import WorkspaceRepo

log = logging.getLogger("setu.annotate")

#: Above this, a single segment's text is almost certainly not a segment — it
#: is a paste accident or an attack. Textbook blocks in this corpus top out
#: around 6,000 characters.
MAX_TEXT = 200_000

#: Notes are for a sentence, not an essay.
MAX_NOTE = 4_000

#: Answers that compare two passages, and so mean nothing on a row that has
#: only one. Marking an English-only row "Exact" is how a corpus ends up with
#: pairs labelled exact whose other half is empty.
TWO_SIDED_ANSWERS = frozenset({"exact", "needs_correction", "structural_mismatch"})

#: Whitespace, plus the zero-width characters a browser can leave behind. Used
#: only to decide whether a text is EMPTY — never to change one. (ZWJ and ZWNJ
#: matter inside Indic words; a text made of nothing else is still empty.)
_INVISIBLE = re.compile(r"[\s​‌‍⁠﻿]+")

#: Trailing characters that are never content. A browser's editable box adds a
#: line break when you click into it and out again; that must not count as a
#: correction.
_TRAIL = " \t\r\n"

#: What an annotator is told when a passage is left empty. Clearing a box to
#: retype it is a normal gesture; saving the emptiness as if it were the
#: correction is how passages vanished from Saved work.
BLANK_REFUSED = (
    "A passage cannot be saved empty, so nothing was saved and the text is "
    "unchanged. Type the corrected text instead. If this passage should not be "
    "in the corpus, answer “Not applicable”; if the other book is missing it, "
    "answer “Missing or incomplete”.")


def is_blank(text: Any) -> bool:
    """True when a text has nothing a reader could see in it."""
    return not _INVISIBLE.sub("", text or "")


def same_text(a: Any, b: Any) -> bool:
    """Equal, ignoring trailing whitespace — which is never content."""
    return (a or "").rstrip(_TRAIL) == (b or "").rstrip(_TRAIL)


class AnnotateRepo(Repository):
    """Reads and writes for the editable annotation state."""

    def row_for_update(self, rid: str) -> dict:
        row = self.one(
            "SELECT r.rid, r.pid, r.seq, r.status, r.src_sid, r.tgt_sid, r.edited"
            "  FROM setu_row r WHERE r.rid = ?", (rid,))
        if not row:
            raise NotFound(f"no such row: {rid}")
        return row

    def source_text(self, rid: str, side: str) -> str:
        col = "src_sid" if side == "src" else "tgt_sid"
        return self.scalar(
            f"SELECT s.source_text FROM setu_row r"
            f"  LEFT JOIN setu_segment s ON s.sid = r.{col}"
            f" WHERE r.rid = ?", (rid,), default="") or ""

    def current(self, rid: str, side: str) -> tuple[str, int, bool]:
        """(text, revision, has_been_edited) for one side of one row."""
        row = self.one("SELECT text, rev FROM setu_text WHERE rid = ? AND side = ?",
                       (rid, side))
        if row:
            return row["text"], int(row["rev"]), True
        return self.source_text(rid, side), 0, False

    def history(self, rid: str, side: str = "", limit: Any = 50,
                offset: Any = 0) -> list[dict]:
        lim, off = paginate(limit, offset, default=50, cap=200)
        if side:
            return self.all(
                "SELECT id, side, rev, actor, session, reason, ts, LENGTH(text) AS n_chars"
                "  FROM setu_rev WHERE rid = ? AND side = ?"
                " ORDER BY rev DESC LIMIT ? OFFSET ?", (rid, side_of(side), lim, off))
        return self.all(
            "SELECT id, side, rev, actor, session, reason, ts, LENGTH(text) AS n_chars"
            "  FROM setu_rev WHERE rid = ? ORDER BY ts DESC LIMIT ? OFFSET ?",
            (rid, lim, off))

    def revision(self, rid: str, side: str, rev: int) -> dict:
        row = self.one("SELECT * FROM setu_rev WHERE rid = ? AND side = ? AND rev = ?",
                       (rid, side_of(side), int(rev)))
        if not row:
            raise NotFound(f"no revision {rev} of {rid}/{side}")
        return row

    def status_history(self, rid: str, limit: Any = 50) -> list[dict]:
        lim, _ = paginate(limit, 0, default=50, cap=200)
        return self.all(
            "SELECT status, note, actor, ts FROM setu_status_rev"
            " WHERE rid = ? ORDER BY ts DESC LIMIT ?", (rid, lim))


# ── the operations ─────────────────────────────────────────────────────────

def save_text(con, rid: str, side: str, text: Any, *, base_rev: Any = None,
              annotator: str = "", session: str = "", reason: str = "edit",
              force: bool = False) -> dict:
    """Store an edit to one side of one row.

    *base_rev* is the revision the editor was showing when the person started
    typing. Omitting it is allowed only for a first edit; once a row has a
    stored revision, a save without one is refused rather than guessed at.

    Returns the new state. Raises :class:`~setu.store.Conflict` when the save
    would overwrite somebody else's work.
    """
    side = side_of(side)
    body = normalise(text)
    if len(body) > MAX_TEXT:
        raise Invalid(f"text is {len(body)} characters; the limit is {MAX_TEXT}")
    if not force:
        # Trailing whitespace is never content, and an editable box in a
        # browser adds a line break just from being clicked into. A restore
        # (force) puts the original back byte for byte, so it is left alone.
        body = body.rstrip(_TRAIL)

    repo = AnnotateRepo(con)
    row = repo.row_for_update(rid)
    sid = row["src_sid"] if side == "src" else row["tgt_sid"]
    if sid is None:
        raise Invalid(
            f"this pair has nothing on the {'left' if side == 'src' else 'right'} "
            "to correct. If the matching passage is on another page, select it "
            "there and press Pair.")

    stored = repo.one("SELECT text, rev FROM setu_text WHERE rid = ? AND side = ?",
                      (rid, side))
    cur_text = stored["text"] if stored else repo.source_text(rid, side)
    cur_rev = int(stored["rev"]) if stored else 0

    if body == cur_text or (not force and same_text(body, cur_text)):
        # Autosave fires on a timer, so most saves are this one. Do nothing,
        # allocate no revision, and say so.
        return {"rid": rid, "side": side, "rev": cur_rev, "text": cur_text,
                "changed": False, "saved_at": None}

    if not force and is_blank(body) and not is_blank(repo.source_text(rid, side)):
        # Clearing a box to retype it is normal. What a browser leaves in a
        # cleared box is a lone line break, and that used to be saved as the
        # correction — the passage then read as empty everywhere.
        raise Invalid(BLANK_REFUSED)

    if not force:
        if base_rev is None:
            if cur_rev != 0:
                raise Conflict(
                    "this row has been edited since your editor loaded it",
                    current=cur_text, attempted=body, rev=cur_rev)
        else:
            try:
                base = int(base_rev)
            except (TypeError, ValueError):
                raise Invalid(f"base_rev must be a whole number, got {base_rev!r}")
            if base != cur_rev:
                raise Conflict(
                    "somebody else saved this row while you were editing it",
                    current=cur_text, attempted=body, rev=cur_rev)

    now = time.time()
    # Taken from the history as well as the live text — see _next_rev.
    new_rev = _next_rev(con, rid, side)
    repo.run(
        "INSERT INTO setu_text(rid, side, text, rev, updated_at, updated_by)"
        " VALUES(?,?,?,?,?,?) ON CONFLICT(rid, side) DO UPDATE SET"
        "   text=excluded.text, rev=excluded.rev, updated_at=excluded.updated_at,"
        "   updated_by=excluded.updated_by",
        (rid, side, body, new_rev, now, annotator[:120]))
    repo.run(
        "INSERT INTO setu_rev(rid, side, rev, text, actor, session, reason, ts)"
        " VALUES(?,?,?,?,?,?,?,?)",
        (rid, side, new_rev, body, annotator[:120], session[:64], reason[:32], now))

    edited = int(sync_edited(con, rid))
    repo.run("UPDATE setu_row SET updated_at = ?, updated_by = ?"
             " WHERE rid = ?", (now, annotator[:120], rid))
    repo.event("text.save", rid, {"side": side, "rev": new_rev,
                                  "chars": len(body), "reason": reason},
               actor=annotator, session=session)
    return {"rid": rid, "side": side, "rev": new_rev, "text": body,
            "changed": True, "saved_at": now, "edited": bool(edited)}


def save_many(con, rid: str, *, src: Any = None, tgt: Any = None,
              src_rev: Any = None, tgt_rev: Any = None, status: Any = None,
              note: Any = None, annotator: str = "", session: str = "",
              reason: str = "edit") -> dict:
    """Save both sides and the status in one transaction.

    This is what the autosave calls. Doing it as one unit means a row is never
    left with the left side saved and the right side lost, which is exactly the
    state that makes an annotator distrust the tool.
    """
    out: dict[str, Any] = {"rid": rid, "saved": []}
    if src is not None:
        out["src"] = save_text(con, rid, "src", src, base_rev=src_rev,
                               annotator=annotator, session=session, reason=reason)
        if out["src"]["changed"]:
            out["saved"].append("src")
    if tgt is not None:
        out["tgt"] = save_text(con, rid, "tgt", tgt, base_rev=tgt_rev,
                               annotator=annotator, session=session, reason=reason)
        if out["tgt"]["changed"]:
            out["saved"].append("tgt")
    if status is not None or note is not None:
        out["status"] = set_status(con, rid, status, note=note,
                                   annotator=annotator, session=session)
        if out["status"]["changed"]:
            out["saved"].append("status")
    out["row"] = WorkspaceRepo(con).row(rid)
    return out


def set_status(con, rid: str, status: Any = None, *, note: Any = None,
               annotator: str = "", session: str = "") -> dict:
    """Record a judgement about a row, and the reason if one was given."""
    repo = AnnotateRepo(con)
    row = repo.row_for_update(rid)
    new_status = row["status"] if status is None else valid_status(status)
    new_note = row.get("note", "") if note is None else normalise(note)[:MAX_NOTE]
    cur_note = repo.scalar("SELECT note FROM setu_row WHERE rid = ?", (rid,), default="") or ""
    if note is None:
        new_note = cur_note

    # "Exact" compares two passages. On a row with only one it records a pair
    # that does not exist — which is what selecting a block on each side of two
    # DIFFERENT rows used to produce. Refused only as a change, so a row that
    # already carries such an answer can still have its note saved.
    if new_status in TWO_SIDED_ANSWERS and new_status != row["status"] \
            and not (row["src_sid"] and row["tgt_sid"]):
        missing = "right" if row["src_sid"] else "left"
        raise Invalid(
            f"this pair has nothing on the {missing}, so it cannot be "
            f"compared. If the matching passage is on another page, select it "
            f"there and press Pair; otherwise answer “Missing or incomplete”.")

    if new_status == row["status"] and new_note == cur_note:
        return {"rid": rid, "status": new_status, "note": new_note, "changed": False}

    now = time.time()
    repo.run("UPDATE setu_row SET status = ?, note = ?, updated_at = ?, updated_by = ?"
             " WHERE rid = ?", (new_status, new_note, now, annotator[:120], rid))
    repo.run("INSERT INTO setu_status_rev(rid, status, note, actor, session, ts)"
             " VALUES(?,?,?,?,?,?)",
             (rid, new_status, new_note, annotator[:120], session[:64], now))
    repo.event("status.set", rid, {"status": new_status}, actor=annotator, session=session)
    return {"rid": rid, "status": new_status, "note": new_note, "changed": True}


def restore(con, rid: str, side: str, *, rev: Any = None, annotator: str = "",
            session: str = "") -> dict:
    """Put back an earlier version — or the parser's original, with ``rev=0``.

    A restore is itself an edit: it appends a new revision rather than rewinding
    the history, so the fact that somebody restored is as recoverable as
    anything else they did.
    """
    side = side_of(side)
    repo = AnnotateRepo(con)
    repo.row_for_update(rid)
    if rev in (None, "", 0, "0"):
        text = repo.source_text(rid, side)
        reason = "restore-original"
    else:
        text = repo.revision(rid, side, int(rev))["text"]
        reason = f"restore-r{int(rev)}"
    _, cur_rev, _ = repo.current(rid, side)
    return save_text(con, rid, side, text, base_rev=cur_rev, annotator=annotator,
                     session=session, reason=reason, force=True)


def diff(con, rid: str, side: str, *, a: Any = 0, b: Any = None) -> dict:
    """A unified diff between two revisions, for the "View changes" panel.

    Revision 0 means the parser's original, which is the comparison people
    actually want: *what did I change about what the machine read?*
    """
    side = side_of(side)
    repo = AnnotateRepo(con)
    repo.row_for_update(rid)

    def text_at(r: Any) -> tuple[str, str]:
        if r in (None, "", 0, "0"):
            return repo.source_text(rid, side), "original"
        if str(r).lower() == "current":
            t, rv, _ = repo.current(rid, side)
            return t, f"r{rv}" if rv else "original"
        return repo.revision(rid, side, int(r))["text"], f"r{int(r)}"

    left, left_label = text_at(a)
    right, right_label = text_at(b if b is not None else "current")
    lines = list(difflib.unified_diff(
        left.splitlines(), right.splitlines(),
        fromfile=left_label, tofile=right_label, lineterm="", n=2))
    ratio = difflib.SequenceMatcher(None, left, right).ratio()
    return {"rid": rid, "side": side, "from": left_label, "to": right_label,
            "identical": left == right, "similarity": round(ratio, 4),
            "diff": lines, "left": left, "right": right}


# ── the bookkeeping every structural change needs ─────────────────────────
#
# A row is a pair of segment pointers plus the judgements made about that
# pairing. Changing which segments a row points at is the riskiest thing Setu
# does, so the bookkeeping lives here once and every operation uses it:
#
#   * a correction belongs to its SEGMENT, not to the row it happens to sit in,
#     so when a segment moves between rows its correction moves with it;
#   * history is append-only, and revision numbers come from the history, not
#     from the live text (setu_rev is UNIQUE(rid, side, rev));
#   * the "corrected" flag is derived, so it is recomputed, never patched;
#   * a judgement was about one particular pairing, so when the pairing
#     changes the judgement goes back to "Not checked yet" — kept in the
#     status history, never thrown away;
#   * pair numbers stay dense (0, 1, 2 …), exactly as a split already keeps them.

def _next_rev(con, rid: str, side: str) -> int:
    """The next free revision number for one side of one row.

    Counted from the history as well as the live text. Once a side has been
    detached and something attached again, setu_text starts from nothing while
    setu_rev still holds every earlier revision — and counting from setu_text
    alone collided with them, so pair → unpair → pair failed outright.
    """
    hist = con.execute("SELECT COALESCE(MAX(rev), 0) FROM setu_rev"
                       " WHERE rid = ? AND side = ?", (rid, side)).fetchone()[0]
    live = con.execute("SELECT COALESCE(MAX(rev), 0) FROM setu_text"
                       " WHERE rid = ? AND side = ?", (rid, side)).fetchone()[0]
    return int(max(hist or 0, live or 0)) + 1


def sync_edited(con, rid: str) -> bool:
    """Recompute the row's "corrected" flag from what is actually stored.

    True only when a side that HAS a passage carries text different from what
    the parser read. A flag left over from text that has since moved to another
    row was how a pair could say "corrected" with nothing to show for it.
    """
    row = con.execute("SELECT src_sid, tgt_sid FROM setu_row WHERE rid = ?",
                      (rid,)).fetchone()
    if not row:
        return False
    edited = False
    for side, sid in (("src", row[0]), ("tgt", row[1])):
        if not sid:
            continue
        t = con.execute("SELECT text FROM setu_text WHERE rid = ? AND side = ?",
                        (rid, side)).fetchone()
        if t is None:
            continue
        src = con.execute("SELECT source_text FROM setu_segment WHERE sid = ?",
                          (sid,)).fetchone()
        if not same_text(t[0], (src[0] if src else "") or ""):
            edited = True
    con.execute("UPDATE setu_row SET edited = ? WHERE rid = ?", (int(edited), rid))
    return edited


def _move_text(con, from_rid: str, side: str, to_rid: str, *, actor: str,
               session: str, reason: str) -> bool:
    """Carry one side's correction from one row to another.

    Both rows record it: the one it leaves gets a revision saying so, the one it
    arrives in starts its history with it. A plain INSERT on arrival means a
    programming mistake that would overwrite a correction fails loudly and
    rolls the whole operation back, instead of losing somebody's text.
    """
    got = con.execute("SELECT text FROM setu_text WHERE rid = ? AND side = ?",
                      (from_rid, side)).fetchone()
    if not got:
        return False
    text, now = got[0], time.time()
    out_rev = _next_rev(con, from_rid, side)
    con.execute("INSERT INTO setu_rev(rid, side, rev, text, actor, session, reason, ts)"
                " VALUES(?,?,?,?,?,?,?,?)",
                (from_rid, side, out_rev, text, actor[:120], session[:64],
                 f"{reason}-out"[:32], now))
    con.execute("DELETE FROM setu_text WHERE rid = ? AND side = ?", (from_rid, side))
    in_rev = _next_rev(con, to_rid, side)
    con.execute("INSERT INTO setu_text(rid, side, text, rev, updated_at, updated_by)"
                " VALUES(?,?,?,?,?,?)", (to_rid, side, text, in_rev, now, actor[:120]))
    con.execute("INSERT INTO setu_rev(rid, side, rev, text, actor, session, reason, ts)"
                " VALUES(?,?,?,?,?,?,?,?)",
                (to_rid, side, in_rev, text, actor[:120], session[:64],
                 f"{reason}-in"[:32], now))
    return True


def _drop_text(con, rid: str, side: str, *, actor: str, session: str,
               reason: str) -> None:
    """Clear one side's correction, recording it first. Never silent."""
    got = con.execute("SELECT text FROM setu_text WHERE rid = ? AND side = ?",
                      (rid, side)).fetchone()
    if not got:
        return
    con.execute("INSERT INTO setu_rev(rid, side, rev, text, actor, session, reason, ts)"
                " VALUES(?,?,?,?,?,?,?,?)",
                (rid, side, _next_rev(con, rid, side), got[0], actor[:120],
                 session[:64], reason[:32], time.time()))
    con.execute("DELETE FROM setu_text WHERE rid = ? AND side = ?", (rid, side))


def _reset_status(con, rid: str, *, actor: str, session: str, why: str) -> bool:
    """A judgement was about one pairing; a different pairing starts unjudged."""
    cur = con.execute("SELECT status, note FROM setu_row WHERE rid = ?", (rid,)).fetchone()
    if not cur or cur[0] == DEFAULT_STATUS:
        return False
    now = time.time()
    con.execute("UPDATE setu_row SET status = ?, updated_at = ?, updated_by = ?"
                " WHERE rid = ?", (DEFAULT_STATUS, now, actor[:120], rid))
    con.execute("INSERT INTO setu_status_rev(rid, status, note, actor, session, ts)"
                " VALUES(?,?,?,?,?,?)",
                (rid, DEFAULT_STATUS, cur[1] or "", actor[:120], session[:64], now))
    Repository(con).event("status.reset", rid, {"was": cur[0], "why": why},
                          actor=actor, session=session)
    return True


def _count_rows(con, pid: str) -> None:
    con.execute("UPDATE setu_project SET n_rows = (SELECT COUNT(*) FROM setu_row"
                " WHERE pid = ?) WHERE pid = ?", (pid, pid))


def _delete_empty_row(con, rid: str) -> bool:
    """Remove a row that points at nothing, and close the gap it leaves.

    Only ever deletes a row with no passage on either side. Its history in
    setu_rev and setu_status_rev is kept — those tables are append-only.
    """
    row = con.execute("SELECT pid, seq, src_sid, tgt_sid FROM setu_row WHERE rid = ?",
                      (rid,)).fetchone()
    if not row or row[2] or row[3]:
        return False
    pid, seq = row[0], row[1]
    for side in ("src", "tgt"):
        _drop_text(con, rid, side, actor="", session="", reason="orphan")
    con.execute("DELETE FROM setu_row WHERE rid = ?", (rid,))
    # Two steps through negative numbers, so UNIQUE(pid, seq) holds at every
    # moment whatever order SQLite visits the rows in. The mirror of how
    # _insert_after opens a gap.
    con.execute("UPDATE setu_row SET seq = -(seq - 1) WHERE pid = ? AND seq > ?",
                (pid, seq))
    con.execute("UPDATE setu_row SET seq = -seq WHERE pid = ? AND seq < 0", (pid,))
    _count_rows(con, pid)
    return True


def _seq_of(con, rid: str) -> int:
    return int(con.execute("SELECT seq FROM setu_row WHERE rid = ?", (rid,)).fetchone()[0])


def _settle(con, rids: list[str]) -> None:
    """Locators and flags for every row an operation touched."""
    for rid in dict.fromkeys(r for r in rids if r):
        if con.execute("SELECT 1 FROM setu_row WHERE rid = ?", (rid,)).fetchone():
            _refresh_locators(con, rid)
            sync_edited(con, rid)


# ── re-pointing one side ───────────────────────────────────────────────────

def attach(con, rid: str, side: str, sid: Any, *, annotator: str = "",
           session: str = "") -> dict:
    """Point one side of a row at a different segment, or at nothing.

    The low-level form, kept for the API. A correction made to the segment
    that is leaving no longer applies to this row, so it is cleared — recorded
    as a revision first, never silently dropped. The interface uses
    :func:`pair_segments`, which carries corrections along instead.
    """
    side = side_of(side)
    repo = AnnotateRepo(con)
    row = repo.row_for_update(rid)
    col = "src_sid" if side == "src" else "tgt_sid"

    if sid in (None, "", "null"):
        new_sid = None
    else:
        seg = repo.one("SELECT sid FROM setu_segment WHERE sid = ?", (str(sid),))
        if not seg:
            raise NotFound(f"no such segment: {sid}")
        new_sid = seg["sid"]
        clash = repo.one(
            f"SELECT rid FROM setu_row WHERE pid = ? AND {col} = ? AND rid <> ?",
            (row["pid"], new_sid, rid))
        if clash:
            raise Invalid(
                f"that segment is already on the {'left' if side=='src' else 'right'} "
                f"of row {clash['rid']}; detach it there first")

    if new_sid == row[col]:
        return WorkspaceRepo(con).row(rid)

    _drop_text(con, rid, side, actor=annotator, session=session, reason="detach")
    now = time.time()
    repo.run(f"UPDATE setu_row SET {col} = ?, origin = 'manual', confidence = 0,"
             f" updated_at = ?, updated_by = ? WHERE rid = ?",
             (new_sid, now, annotator[:120], rid))
    _reset_status(con, rid, actor=annotator, session=session, why="attach")
    _settle(con, [rid])
    repo.event("row.attach", rid, {"side": side, "sid": new_sid},
               actor=annotator, session=session)
    return WorkspaceRepo(con).row(rid)


# ── pairing, the operation the interface uses ──────────────────────────────

def pair_segments(con, pid: str, src_sid: Any, tgt_sid: Any, *,
                  annotator: str = "", session: str = "") -> dict:
    """Make one left-hand passage and one right-hand passage a pair.

    The gesture behind it: a block clicked on each side — on ANY page of each
    book — and "Pair". Every shape the two rows can be in is handled here, so
    the interface never has to know which primitive applies::

        left block's row   right block's row   afterwards
        ─────────────────  ──────────────────  ────────────────────────────────
        (E, —)             (—, M)              (E, M); the right row is removed
        (E, M_old)         (—, M)              (E, M); M_old alone, just after
        (E, —)             (E_old, M)          (E, M); E_old alone, where it was
        (E, M_old)         (E_old, M)          (E, M); both left alone
        (E, M)             same row            nothing to do

    Corrections travel with their passages. Every pairing whose composition
    changes goes back to "Not checked yet", its old answer kept in the history.
    Nothing is ever paired that the annotator did not pair: E_old and M_old are
    never put together just because both happened to become free.

    Must run inside a transaction; the API wraps it in one, so a failure at
    any step leaves every row exactly as it was.
    """
    repo = AnnotateRepo(con)
    proj = repo.one("SELECT pid, src_book, tgt_book FROM setu_project WHERE pid = ?",
                    (str(pid or ""),))
    if not proj:
        raise NotFound(f"no such project: {pid}")
    e = repo.one("SELECT sid, book_key, seq FROM setu_segment WHERE sid = ?",
                 (str(src_sid or ""),))
    m = repo.one("SELECT sid, book_key, seq FROM setu_segment WHERE sid = ?",
                 (str(tgt_sid or ""),))
    if not e or not m:
        raise NotFound("one of those two blocks no longer exists — turn the page "
                       "and back, then select them again")
    if e["book_key"] != proj["src_book"]:
        raise Invalid("the block chosen on the left is not from this project's "
                      "left-hand book")
    if m["book_key"] != proj["tgt_book"]:
        raise Invalid("the block chosen on the right is not from this project's "
                      "right-hand book")

    def row_with(col: str, sid: str):
        return repo.one(f"SELECT rid, seq, src_sid, tgt_sid FROM setu_row"
                        f" WHERE pid = ? AND {col} = ?", (pid, sid))

    r_s, r_t = row_with("src_sid", e["sid"]), row_with("tgt_sid", m["sid"])
    if r_s and r_t and r_s["rid"] == r_t["rid"]:
        return {"changed": False, "rid": r_s["rid"], "created": [], "removed": [],
                "touched": [r_s["rid"]], "row": WorkspaceRepo(con).row(r_s["rid"])}

    kw = {"actor": annotator, "session": session}
    created: list[str] = []
    removed: list[str] = []
    touched: list[str] = []

    # 1. The left block needs a row. Every block the aligner kept has one; a
    #    header or page number shown with "include headers" may not.
    if not r_s:
        anchor = repo.one(
            "SELECT r.seq FROM setu_row r JOIN setu_segment s ON s.sid = r.src_sid"
            " WHERE r.pid = ? AND s.book_key = ? AND s.seq < ?"
            " ORDER BY s.seq DESC LIMIT 1", (pid, proj["src_book"], e["seq"]))
        rid_s = _insert_after(con, pid, anchor["seq"] if anchor else -1,
                              src_sid=e["sid"], annotator=annotator)
        created.append(rid_s)
        r_s = row_with("src_sid", e["sid"])
    rid_s = r_s["rid"]

    # 2. Whatever the left block was paired with leaves, alone, right after it
    #    — near where the aligner put it — carrying its own correction.
    m_old = r_s["tgt_sid"]
    if not m_old:
        # A side with no passage should hold no text. Older versions could
        # leave some behind; record it and clear it, so the passage arriving
        # below can never collide with it.
        _drop_text(con, rid_s, "tgt", reason="orphan", **kw)
    if m_old:
        rid_new = _insert_after(con, pid, _seq_of(con, rid_s), tgt_sid=m_old,
                                annotator=annotator)
        created.append(rid_new)
        _move_text(con, rid_s, "tgt", rid_new, reason="unpair", **kw)
        con.execute("UPDATE setu_row SET tgt_sid = NULL WHERE rid = ?", (rid_s,))

    # 3. The right block leaves its old row, and arrives — with its correction.
    now = time.time()
    if r_t:
        con.execute("UPDATE setu_row SET tgt_sid = NULL WHERE rid = ?", (r_t["rid"],))
    con.execute("UPDATE setu_row SET tgt_sid = ?, origin = 'manual', confidence = 0,"
                " updated_at = ?, updated_by = ? WHERE rid = ?",
                (m["sid"], now, annotator[:120], rid_s))
    if r_t:
        _move_text(con, r_t["rid"], "tgt", rid_s, reason="pair", **kw)

    # 4. What the right block leaves behind: nothing (removed), or an
    #    English passage that now stands alone.
    if r_t:
        if _delete_empty_row(con, r_t["rid"]):
            removed.append(r_t["rid"])
        else:
            touched.append(r_t["rid"])
            _reset_status(con, r_t["rid"], why="its partner was paired elsewhere", **kw)

    _reset_status(con, rid_s, why="paired by hand", **kw)
    touched.insert(0, rid_s)
    _count_rows(con, pid)
    _settle(con, touched + created)
    repo.event("row.pair", rid_s,
               {"src_sid": e["sid"], "tgt_sid": m["sid"], "created": created,
                "removed": removed, "released_tgt": m_old or "",
                "released_src": (r_t or {}).get("src_sid") or ""},
               actor=annotator, session=session)
    return {"changed": True, "rid": rid_s, "created": created, "removed": removed,
            "touched": touched, "row": WorkspaceRepo(con).row(rid_s)}


def split_row(con, rid: str, *, annotator: str = "", session: str = "") -> dict:
    """Break a paired row into two one-sided rows — "these are not a pair".

    The right-hand passage moves to a new row straight after, carrying its
    correction. The answer goes back to "Not checked yet": it was about a pair
    that no longer exists.
    """
    repo = AnnotateRepo(con)
    row = repo.row_for_update(rid)
    if not row["src_sid"] or not row["tgt_sid"]:
        raise Invalid("this pair only has one side already, so there is "
                      "nothing to unpair")
    kw = {"actor": annotator, "session": session}
    new_rid = _insert_after(con, row["pid"], row["seq"], tgt_sid=row["tgt_sid"],
                            annotator=annotator)
    _move_text(con, rid, "tgt", new_rid, reason="unpair", **kw)
    con.execute("UPDATE setu_row SET tgt_sid = NULL, origin = 'manual', confidence = 0,"
                " updated_at = ?, updated_by = ? WHERE rid = ?",
                (time.time(), annotator[:120], rid))
    _reset_status(con, rid, why="unpaired", **kw)
    _settle(con, [rid, new_rid])
    repo.event("row.split", rid, {"new_row": new_rid}, actor=annotator, session=session)
    return {"row": WorkspaceRepo(con).row(rid),
            "new_row": WorkspaceRepo(con).row(new_rid)}


#: The name the interface uses for it.
unpair = split_row


def merge_rows(con, rid: str, other_rid: str, *, annotator: str = "",
               session: str = "") -> dict:
    """Pull the populated side of *other_rid* onto the empty side of *rid*.

    The inverse of a split. Kept for the API; implemented with the same
    bookkeeping as :func:`pair_segments`, so the merged-away row's correction
    arrives intact and pair numbers stay dense.
    """
    repo = AnnotateRepo(con)
    a = repo.row_for_update(rid)
    b = repo.row_for_update(other_rid)
    if a["pid"] != b["pid"]:
        raise Invalid("those rows are in different projects")
    if rid == other_rid:
        raise Invalid("a row cannot be merged with itself")

    side = "tgt" if a["src_sid"] and not a["tgt_sid"] else (
        "src" if a["tgt_sid"] and not a["src_sid"] else "")
    if not side:
        raise Invalid("the row you are merging into already has both sides filled")
    col = f"{side}_sid"
    donor_sid = b[col]
    if not donor_sid:
        raise Invalid(f"the other row has nothing on its {side} side")

    kw = {"actor": annotator, "session": session}
    _drop_text(con, rid, side, reason="orphan", **kw)
    con.execute(f"UPDATE setu_row SET {col} = NULL WHERE rid = ?", (other_rid,))
    con.execute(f"UPDATE setu_row SET {col} = ?, origin = 'manual', confidence = 0,"
                f" updated_at = ?, updated_by = ? WHERE rid = ?",
                (donor_sid, time.time(), annotator[:120], rid))
    _move_text(con, other_rid, side, rid, reason="merge", **kw)

    removed = _delete_empty_row(con, other_rid)
    if not removed:
        _reset_status(con, other_rid, why="its partner was merged away", **kw)
    _reset_status(con, rid, why="merged", **kw)
    _count_rows(con, a["pid"])
    _settle(con, [rid, other_rid])
    repo.event("row.merge", rid, {"from": other_rid, "side": side, "removed": removed},
               actor=annotator, session=session)
    return {"row": WorkspaceRepo(con).row(rid), "removed_row": other_rid if removed else ""}


def _insert_after(con, pid: str, seq: int, *, src_sid: str | None = None,
                  tgt_sid: str | None = None, annotator: str = "") -> str:
    """Make room after *seq* and create a row there.

    Sequence numbers stay dense because navigation, "row 412 of 1840" and the
    keyboard shortcuts all read better that way than with gaps.
    """
    from . import ids
    repo = Repository(con)
    repo.run("UPDATE setu_row SET seq = -(seq + 1) WHERE pid = ? AND seq > ?",
             (pid, seq))
    repo.run("UPDATE setu_row SET seq = -seq WHERE pid = ? AND seq < 0", (pid,))
    now = time.time()
    new_seq = seq + 1
    rid = ids.mint("rw")
    repo.run(
        "INSERT INTO setu_row(rid, pid, seq, src_sid, tgt_sid, status, origin,"
        " confidence, created_at, updated_at, updated_by)"
        " VALUES(?,?,?,?,?,?,'manual',0,?,?,?)",
        (rid, pid, new_seq, src_sid, tgt_sid, DEFAULT_STATUS, now, now, annotator[:120]))
    _count_rows(con, pid)
    _refresh_locators(con, rid)
    return rid


# ── repairing what earlier versions let through ────────────────────────────

#: Revision reasons that mark a DIFFERENT passage leaving this side of a row.
#: History older than one of these belongs to that other passage, so a repair
#: must never reach back past it.
_DEPARTURES = ("detach", "orphan")


def _last_good_text(con, rid: str, side: str) -> str | None:
    """The newest non-empty text this side held for its CURRENT passage."""
    for text, reason in con.execute(
            "SELECT text, reason FROM setu_rev WHERE rid = ? AND side = ?"
            " ORDER BY rev DESC", (rid, side)):
        reason = reason or ""
        if reason in _DEPARTURES or reason.endswith("-out"):
            return None
        if not is_blank(text):
            return text
    return None


def repair_blank_corrections(con, *, actor: str = "setu (automatic repair)") -> dict:
    """Put text back wherever a correction was saved empty.

    Before this release, clearing a passage in the browser saved what the
    browser left behind — a lone line break — as if it were the correction, and
    the screen said "Saved." The passage then read as empty in Saved work and in
    every export. Nothing was lost: every revision is in setu_rev.

    What is put back is the annotator's OWN last non-empty text for that
    passage if there is one, and the parser's original otherwise. The repair is
    itself a revision, so it can be undone like any other edit. A side whose
    original is also empty — a diagram, say — is left alone.
    """
    found = con.execute(
        """SELECT t.rid, t.side, t.text, s.source_text
             FROM setu_text t
             JOIN setu_row r ON r.rid = t.rid
        LEFT JOIN setu_segment s
               ON s.sid = CASE t.side WHEN 'src' THEN r.src_sid ELSE r.tgt_sid END"""
    ).fetchall()
    fixed: list[dict] = []
    for rid, side, text, source in found:
        if not is_blank(text):
            continue
        mine = _last_good_text(con, rid, side)
        restore_to = mine if mine is not None else (source or "")
        if is_blank(restore_to):
            continue
        rev, now = _next_rev(con, rid, side), time.time()
        con.execute("UPDATE setu_text SET text = ?, rev = ?, updated_at = ?, updated_by = ?"
                    " WHERE rid = ? AND side = ?", (restore_to, rev, now, actor[:120],
                                                    rid, side))
        con.execute("INSERT INTO setu_rev(rid, side, rev, text, actor, session, reason, ts)"
                    " VALUES(?,?,?,?,?,?,?,?)",
                    (rid, side, rev, restore_to, actor[:120], "", "repair-blank", now))
        sync_edited(con, rid)
        fixed.append({"rid": rid, "side": side,
                      "restored": "the annotator's last text" if mine is not None
                                  else "the parser's original"})
    if fixed:
        Repository(con).event("repair.blank", "", {"fixed": len(fixed)}, actor=actor)
    return {"fixed": len(fixed), "rows": fixed, "flags": resync_edited_flags(con)}


def resync_edited_flags(con) -> int:
    """Recompute every row's "corrected" flag. Returns how many were wrong."""
    trail = "char(32, 9, 13, 10)"
    differs = (
        "EXISTS (SELECT 1 FROM setu_text t JOIN setu_segment s ON s.sid = setu_row.{c}"
        " WHERE t.rid = setu_row.rid AND t.side = '{side}'"
        f" AND rtrim(t.text, {trail}) <> rtrim(COALESCE(s.source_text, ''), {trail}))")
    want = (f"({differs.format(c='src_sid', side='src')}"
            f" OR {differs.format(c='tgt_sid', side='tgt')})")
    cur = con.execute(f"UPDATE setu_row SET edited = {want}"
                      f" WHERE COALESCE(edited, 0) <> {want}")
    return int(cur.rowcount or 0)


def _refresh_locators(con, rid: str) -> None:
    """Re-derive a row's kind and pages after its segments change.

    Chapter and section come from the *source* book only, and are left alone
    when the row has no source segment: a target-only row keeps whatever
    position in the source book's table of contents it was given when the
    project was laid out. Taking the target book's own chapter title instead
    would split the sidebar into two parallel tables of contents in two
    different languages, which is how a project ends up looking twice as long
    as it is.
    """
    repo = Repository(con)
    repo.run(
        """UPDATE setu_row SET
             kind     = COALESCE((SELECT kind FROM setu_segment WHERE sid = src_sid),
                                 (SELECT kind FROM setu_segment WHERE sid = tgt_sid), ''),
             src_page = (SELECT page FROM setu_segment WHERE sid = src_sid),
             tgt_page = (SELECT page FROM setu_segment WHERE sid = tgt_sid)
           WHERE rid = ?""", (rid,))
    repo.run(
        """UPDATE setu_row SET
             chapter    = COALESCE((SELECT chapter    FROM setu_segment WHERE sid = src_sid), chapter),
             chapter_no = COALESCE((SELECT chapter_no FROM setu_segment WHERE sid = src_sid), chapter_no),
             section    = COALESCE((SELECT section    FROM setu_segment WHERE sid = src_sid), section),
             section_no = COALESCE((SELECT section_no FROM setu_segment WHERE sid = src_sid), section_no)
           WHERE rid = ? AND src_sid IS NOT NULL""", (rid,))
