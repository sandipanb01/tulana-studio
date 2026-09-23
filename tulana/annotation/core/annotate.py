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

    repo = AnnotateRepo(con)
    row = repo.row_for_update(rid)
    sid = row["src_sid"] if side == "src" else row["tgt_sid"]
    if sid is None:
        raise Invalid(
            f"this row has nothing on the {'left' if side == 'src' else 'right'}; "
            "attach a segment to it before editing")

    stored = repo.one("SELECT text, rev FROM setu_text WHERE rid = ? AND side = ?",
                      (rid, side))
    cur_text = stored["text"] if stored else repo.source_text(rid, side)
    cur_rev = int(stored["rev"]) if stored else 0

    if body == cur_text:
        # Autosave fires on a timer, so most saves are this one. Do nothing,
        # allocate no revision, and say so.
        return {"rid": rid, "side": side, "rev": cur_rev, "text": cur_text,
                "changed": False, "saved_at": None}

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
    new_rev = cur_rev + 1
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

    source = repo.source_text(rid, side)
    other = "tgt" if side == "src" else "src"
    other_text, _, _ = repo.current(rid, other)
    other_source = repo.source_text(rid, other)
    edited = int(body != source or other_text != other_source)
    repo.run("UPDATE setu_row SET edited = ?, updated_at = ?, updated_by = ?"
             " WHERE rid = ?", (edited, now, annotator[:120], rid))
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


def attach(con, rid: str, side: str, sid: Any, *, annotator: str = "",
           session: str = "") -> dict:
    """Point one side of a row at a different segment, or at nothing.

    This is how an annotator fixes a structural mismatch: the aligner put the
    wrong paragraph on the right, so they choose the right one. Any text they
    had already typed on that side is kept in the history but no longer applies,
    so it is cleared — recorded as a revision first, never silently dropped.
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

    stored = repo.one("SELECT text, rev FROM setu_text WHERE rid = ? AND side = ?",
                      (rid, side))
    if stored:
        repo.run("INSERT INTO setu_rev(rid, side, rev, text, actor, session, reason, ts)"
                 " VALUES(?,?,?,?,?,?,?,?)",
                 (rid, side, int(stored["rev"]) + 1, stored["text"], annotator[:120],
                  session[:64], "detach", time.time()))
        repo.run("DELETE FROM setu_text WHERE rid = ? AND side = ?", (rid, side))

    now = time.time()
    repo.run(f"UPDATE setu_row SET {col} = ?, origin = 'manual', confidence = 0,"
             f" updated_at = ?, updated_by = ? WHERE rid = ?",
             (new_sid, now, annotator[:120], rid))
    _refresh_locators(con, rid)
    repo.event("row.attach", rid, {"side": side, "sid": new_sid},
               actor=annotator, session=session)
    return WorkspaceRepo(con).row(rid)


def split_row(con, rid: str, *, annotator: str = "", session: str = "") -> dict:
    """Break a paired row into two one-sided rows.

    The commonest structural fix after "wrong partner": the two sides are both
    real text but they are not each other's translation.
    """
    repo = AnnotateRepo(con)
    row = repo.row_for_update(rid)
    if not row["src_sid"] or not row["tgt_sid"]:
        raise Invalid("this row only has one side already")

    tgt_sid = row["tgt_sid"]
    stored = repo.one("SELECT text, rev FROM setu_text WHERE rid = ? AND side = 'tgt'",
                      (rid,))
    new_rid = _insert_after(con, row["pid"], row["seq"], tgt_sid=tgt_sid,
                            annotator=annotator)
    if stored:
        save_text(con, new_rid, "tgt", stored["text"], base_rev=0,
                  annotator=annotator, session=session, reason="split", force=True)
    attach(con, rid, "tgt", None, annotator=annotator, session=session)
    repo.event("row.split", rid, {"new_row": new_rid}, actor=annotator, session=session)
    return {"row": WorkspaceRepo(con).row(rid),
            "new_row": WorkspaceRepo(con).row(new_rid)}


def merge_rows(con, rid: str, other_rid: str, *, annotator: str = "",
               session: str = "") -> dict:
    """Pull the populated side of *other_rid* onto the empty side of *rid*.

    The inverse of a split, and the fix for "the aligner left these two halves
    of one pair sitting next to each other".
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
    donor_sid = b["tgt_sid"] if side == "tgt" else b["src_sid"]
    if not donor_sid:
        raise Invalid(f"the other row has nothing on its {side} side")

    stored = repo.one("SELECT text FROM setu_text WHERE rid = ? AND side = ?",
                      (other_rid, side))
    attach(con, other_rid, side, None, annotator=annotator, session=session)
    attach(con, rid, side, donor_sid, annotator=annotator, session=session)
    if stored:
        save_text(con, rid, side, stored["text"], base_rev=0, annotator=annotator,
                  session=session, reason="merge", force=True)

    leftover = repo.one("SELECT src_sid, tgt_sid FROM setu_row WHERE rid = ?", (other_rid,))
    removed = False
    if leftover and not leftover["src_sid"] and not leftover["tgt_sid"]:
        repo.run("DELETE FROM setu_row WHERE rid = ?", (other_rid,))
        removed = True
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
    repo.run("UPDATE setu_project SET n_rows = (SELECT COUNT(*) FROM setu_row WHERE pid = ?)"
             " WHERE pid = ?", (pid, pid))
    _refresh_locators(con, rid)
    return rid


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
