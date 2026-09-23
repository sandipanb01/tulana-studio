"""Setu — projects, navigation, progress, sessions.

A *project* is one pair of books opened together: the English edition on the
left and one Indian-language edition on the right. Creating it runs the aligner
once and writes a row per proposal, so an annotator arriving for the first time
finds work already laid out in reading order rather than an empty screen and a
pair of dropdowns.

Rows are generated once and then belong to the annotators. Rebuilding a project
is possible but deliberately awkward: :func:`build_rows` refuses to discard rows
that carry human work unless the caller says so in as many words, because the
alternative is a background job quietly deleting an afternoon.

Sessions are per browser tab, which is what makes "this row is open in another
tab" a thing Setu can actually detect rather than guess at.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Iterable, Sequence

from . import align, ids
from .corpus import CorpusRepo, NOISE_KINDS
from .models import DEFAULT_STATUS, DONE_STATUSES, STATUS_BY_KEY, valid_status
from .store import Invalid, NotFound, Repository, paginate

log = logging.getLogger("setu.workspace")

#: How long a soft lock survives without a heartbeat. Long enough that a slow
#: page load does not drop it, short enough that a closed laptop frees the row
#: before anybody notices.
LOCK_TTL = 120.0

#: A session with no heartbeat for this long is treated as gone.
SESSION_TTL = 900.0


class WorkspaceRepo(Repository):
    """Projects, rows, sessions and locks."""

    # -- projects ---------------------------------------------------------
    def projects(self, *, annotator: str = "", limit: Any = 50,
                 offset: Any = 0) -> list[dict]:
        lim, off = paginate(limit, offset)
        sql = ["""SELECT p.*, sb.title AS src_title, sb.book AS src_book_name,
                         tb.title AS tgt_title, tb.book AS tgt_book_name,
                         sb.board_name AS board_name
                    FROM setu_project p
                    JOIN setu_book sb ON sb.book_key = p.src_book
                    JOIN setu_book tb ON tb.book_key = p.tgt_book"""]
        args: list[Any] = []
        if annotator:
            sql.append(" WHERE p.created_by = ?")
            args.append(annotator)
        sql.append(" ORDER BY p.created_at DESC LIMIT ? OFFSET ?")
        args.extend([lim, off])
        rows = self.all("".join(sql), args)
        for r in rows:
            r["progress"] = self.progress(r["pid"])
        return rows

    def project(self, pid: str) -> dict:
        row = self.one(
            """SELECT p.*, sb.title AS src_title, sb.book AS src_book_name,
                      sb.language AS src_lang, sb.script AS src_script,
                      sb.num_pages AS src_pages, sb.pdf_present AS src_pdf,
                      tb.title AS tgt_title, tb.book AS tgt_book_name,
                      tb.language AS tgt_lang, tb.script AS tgt_script,
                      tb.num_pages AS tgt_pages, tb.pdf_present AS tgt_pdf,
                      sb.board_name AS board_name
                 FROM setu_project p
                 JOIN setu_book sb ON sb.book_key = p.src_book
                 JOIN setu_book tb ON tb.book_key = p.tgt_book
                WHERE p.pid = ?""", (pid,))
        if not row:
            raise NotFound(f"no such project: {pid}")
        row["progress"] = self.progress(pid)
        return row

    def progress(self, pid: str) -> dict:
        """Counts by status, plus the one number an annotator actually wants."""
        rows = self.all(
            "SELECT status, COUNT(*) AS n FROM setu_row WHERE pid = ? GROUP BY status",
            (pid,))
        by = {s: 0 for s in STATUS_BY_KEY}
        for r in rows:
            by[r["status"]] = r["n"]
        total = sum(by.values())
        done = sum(by[s] for s in DONE_STATUSES)
        return {"total": total, "done": done, "pending": by.get(DEFAULT_STATUS, 0),
                "percent": round(100.0 * done / total, 1) if total else 0.0,
                "by_status": by,
                "edited": self.scalar(
                    "SELECT COUNT(*) FROM setu_row WHERE pid = ? AND edited = 1",
                    (pid,), default=0)}

    # -- rows -------------------------------------------------------------
    def rows(self, pid: str, *, limit: Any = 50, offset: Any = 0,
             status: str = "", chapter_no: str = "", kind: str = "",
             edited: Any = None, order: str = "seq") -> dict:
        """A page of rows, with the total so the interface can show "of N".

        A project id that does not exist is an error, not an empty result. The
        two look identical in the interface — an empty list — and "this
        workspace has no pairs" sends somebody looking for a data problem that
        is really a mistyped link.
        """
        if not self.one("SELECT 1 AS ok FROM setu_project WHERE pid = ?", (pid,)):
            raise NotFound(f"no such project: {pid}")
        where = ["r.pid = ?"]
        args: list[Any] = [pid]
        if status:
            keys = [valid_status(s) for s in str(status).split(",") if s.strip()]
            where.append(f"r.status IN ({','.join('?' * len(keys))})")
            args.extend(keys)
        if chapter_no:
            where.append("r.chapter_no = ?")
            args.append(chapter_no)
        if kind:
            where.append("r.kind = ?")
            args.append(kind)
        if edited is not None:
            where.append("r.edited = ?")
            args.append(1 if edited else 0)
        clause = " AND ".join(where)
        total = self.scalar(f"SELECT COUNT(*) FROM setu_row r WHERE {clause}", args, default=0)

        lim, off = paginate(limit, offset, default=50, cap=200)
        direction = "DESC" if str(order).lower() == "recent" else "ASC"
        sort = "r.updated_at DESC, r.seq ASC" if direction == "DESC" else "r.seq ASC"
        page = self.all(
            f"""SELECT r.*,
                       ss.source_text AS src_source, ss.page AS src_pg,
                       ss.kind AS src_kind, ss.has_math AS src_math,
                       ss.has_table AS src_table, ss.item_no AS src_item,
                       ts.source_text AS tgt_source, ts.page AS tgt_pg,
                       ts.kind AS tgt_kind, ts.has_math AS tgt_math,
                       ts.has_table AS tgt_table, ts.item_no AS tgt_item,
                       st.text AS src_edit, st.rev AS src_rev,
                       tt.text AS tgt_edit, tt.rev AS tgt_rev
                  FROM setu_row r
                  LEFT JOIN setu_segment ss ON ss.sid = r.src_sid
                  LEFT JOIN setu_segment ts ON ts.sid = r.tgt_sid
                  LEFT JOIN setu_text st ON st.rid = r.rid AND st.side = 'src'
                  LEFT JOIN setu_text tt ON tt.rid = r.rid AND tt.side = 'tgt'
                 WHERE {clause} ORDER BY {sort} LIMIT ? OFFSET ?""",
            args + [lim, off])
        return {"total": total, "limit": lim, "offset": off,
                "rows": [view(r) for r in page]}

    def row(self, rid: str) -> dict:
        row = self.one(
            """SELECT r.*,
                      ss.source_text AS src_source, ss.page AS src_pg,
                      ss.kind AS src_kind, ss.has_math AS src_math,
                      ss.has_table AS src_table, ss.item_no AS src_item,
                      ss.block_ids AS src_blocks, ss.fx0 AS src_fx0, ss.fy0 AS src_fy0,
                      ss.fx1 AS src_fx1, ss.fy1 AS src_fy1,
                      ts.source_text AS tgt_source, ts.page AS tgt_pg,
                      ts.kind AS tgt_kind, ts.has_math AS tgt_math,
                      ts.has_table AS tgt_table, ts.item_no AS tgt_item,
                      ts.block_ids AS tgt_blocks, ts.fx0 AS tgt_fx0, ts.fy0 AS tgt_fy0,
                      ts.fx1 AS tgt_fx1, ts.fy1 AS tgt_fy1,
                      st.text AS src_edit, st.rev AS src_rev,
                      tt.text AS tgt_edit, tt.rev AS tgt_rev
                 FROM setu_row r
                 LEFT JOIN setu_segment ss ON ss.sid = r.src_sid
                 LEFT JOIN setu_segment ts ON ts.sid = r.tgt_sid
                 LEFT JOIN setu_text st ON st.rid = r.rid AND st.side = 'src'
                 LEFT JOIN setu_text tt ON tt.rid = r.rid AND tt.side = 'tgt'
                WHERE r.rid = ?""", (rid,))
        if not row:
            raise NotFound(f"no such row: {rid}")
        return view(row, full=True)

    def neighbour(self, pid: str, seq: int, direction: int, status: str = "",
                  chapter_no: str = "", kind: str = "") -> dict | None:
        """The next or previous row under the current filters.

        Index-backed: ``WHERE seq > ? ORDER BY seq LIMIT 1`` walks one row, not
        the whole project. Moving through a 200,000-row corpus costs the same
        as moving through a 200-row one, which is the difference between an
        annotator working and an annotator waiting.
        """
        op, order = (">", "ASC") if direction >= 0 else ("<", "DESC")
        args: list[Any] = [pid, int(seq)]
        extra = self._filter_sql(status, chapter_no, kind, args)
        return self.one(
            f"SELECT rid, seq FROM setu_row WHERE pid = ? AND seq {op} ?{extra}"
            f" ORDER BY seq {order} LIMIT 1", args)

    def first(self, pid: str, status: str = "", chapter_no: str = "",
              kind: str = "") -> dict | None:
        """The first row under the current filters."""
        args: list[Any] = [pid]
        extra = self._filter_sql(status, chapter_no, kind, args)
        return self.one(
            f"SELECT rid, seq FROM setu_row WHERE pid = ?{extra}"
            f" ORDER BY seq LIMIT 1", args)

    def at_seq(self, pid: str, seq: Any) -> dict | None:
        """The row at an exact position, whatever the filters are.

        Jumping to a chapter or a search hit lands on a specific row that may
        not match the active filters; refusing to show it because of a filter
        would be baffling, so this ignores them and the interface says so.
        """
        try:
            n = int(seq)
        except (TypeError, ValueError):
            return None
        return self.one("SELECT rid, seq FROM setu_row WHERE pid = ? AND seq = ?",
                        (pid, n))

    def position(self, pid: str, seq: Any, status: str = "", chapter_no: str = "",
                 kind: str = "") -> dict:
        """Where this row sits in the filtered set — "412 of 1,840".

        Two counting queries against the same index rather than fetching rows.
        """
        try:
            n = int(seq)
        except (TypeError, ValueError):
            n = 0
        args: list[Any] = [pid]
        extra = self._filter_sql(status, chapter_no, kind, args)
        total = self.scalar(f"SELECT COUNT(*) FROM setu_row WHERE pid = ?{extra}",
                            args, default=0)
        before_args: list[Any] = [pid]
        before_extra = self._filter_sql(status, chapter_no, kind, before_args)
        before_args.append(n)
        before = self.scalar(
            f"SELECT COUNT(*) FROM setu_row WHERE pid = ?{before_extra} AND seq < ?",
            before_args, default=0)
        return {"index": before + 1, "total": total}

    @staticmethod
    def _filter_sql(status: str, chapter_no: str, kind: str,
                    args: list[Any]) -> str:
        """Append the active filters to *args* and return the SQL for them.

        One place, so navigation, counting and listing can never disagree about
        what "the current filter" means — which is how a Next button ends up
        skipping rows the list is showing.
        """
        out = []
        if status:
            keys = [valid_status(s) for s in str(status).split(",") if s.strip()]
            if keys:
                out.append(f" AND status IN ({','.join('?' * len(keys))})")
                args.extend(keys)
        if chapter_no:
            out.append(" AND chapter_no = ?")
            args.append(chapter_no)
        if kind:
            out.append(" AND kind = ?")
            args.append(kind)
        return "".join(out)

    def chapters(self, pid: str) -> list[dict]:
        """The navigation tree, with per-chapter progress."""
        rows = self.all(
            f"""SELECT chapter_no, chapter, section_no, section,
                       COUNT(*) AS n,
                       SUM(CASE WHEN status IN ({','.join('?' * len(DONE_STATUSES))})
                                THEN 1 ELSE 0 END) AS done,
                       MIN(seq) AS first_seq
                  FROM setu_row WHERE pid = ?
                 GROUP BY chapter_no, chapter, section_no, section
                 ORDER BY first_seq""",
            list(DONE_STATUSES) + [pid])
        out: list[dict] = []
        index: dict[str, dict] = {}
        for r in rows:
            key = r["chapter_no"] or r["chapter"] or "—"
            ch = index.get(key)
            if ch is None:
                ch = {"chapter_no": r["chapter_no"],
                      "chapter": r["chapter"] or "Front matter",
                      "first_seq": r["first_seq"], "n": 0, "done": 0, "sections": []}
                index[key] = ch
                out.append(ch)
            ch["n"] += r["n"]
            ch["done"] += r["done"] or 0
            if r["section"] or r["section_no"]:
                ch["sections"].append({
                    "section_no": r["section_no"], "section": r["section"],
                    "n": r["n"], "done": r["done"] or 0, "first_seq": r["first_seq"]})
        return out

    # -- sessions ---------------------------------------------------------
    def touch_session(self, sess: str, annotator: str = "", pid: str = "",
                      agent: str = "") -> dict:
        now = time.time()
        self.run(
            "INSERT INTO setu_session(sess, annotator, pid, started_at, seen_at, agent)"
            " VALUES(?,?,?,?,?,?)"
            " ON CONFLICT(sess) DO UPDATE SET seen_at=excluded.seen_at,"
            "   annotator=CASE WHEN excluded.annotator <> '' THEN excluded.annotator"
            "                  ELSE setu_session.annotator END,"
            "   pid=CASE WHEN excluded.pid <> '' THEN excluded.pid ELSE setu_session.pid END",
            (sess, annotator[:120], pid, now, now, agent[:200]))
        return self.one("SELECT * FROM setu_session WHERE sess = ?", (sess,)) or {}

    def active_sessions(self, pid: str = "") -> list[dict]:
        cutoff = time.time() - SESSION_TTL
        if pid:
            return self.all("SELECT * FROM setu_session WHERE seen_at > ? AND pid = ?"
                            " ORDER BY seen_at DESC", (cutoff, pid))
        return self.all("SELECT * FROM setu_session WHERE seen_at > ?"
                        " ORDER BY seen_at DESC", (cutoff,))

    # -- soft locks -------------------------------------------------------
    def claim(self, rid: str, sess: str, annotator: str = "") -> dict:
        """Say "I am looking at this row".

        Advisory: it never blocks a write. The authority over concurrent edits
        is the revision check in :mod:`setu.annotate`, which cannot be talked
        out of it. This only exists so the interface can warn a person *before*
        they spend five minutes retyping a paragraph somebody else is also
        retyping.
        """
        now = time.time()
        self.run("DELETE FROM setu_lock WHERE expires_at < ?", (now,))
        held = self.one("SELECT * FROM setu_lock WHERE rid = ?", (rid,))
        if held and held["sess"] != sess and held["expires_at"] > now:
            return {"held": True, "by": held["annotator"] or "another person",
                    "same_person": bool(annotator) and held["annotator"] == annotator,
                    "expires_in": round(held["expires_at"] - now, 1)}
        self.run(
            "INSERT INTO setu_lock(rid, sess, annotator, acquired_at, expires_at)"
            " VALUES(?,?,?,?,?) ON CONFLICT(rid) DO UPDATE SET"
            "   sess=excluded.sess, annotator=excluded.annotator,"
            "   expires_at=excluded.expires_at",
            (rid, sess, annotator[:120], now, now + LOCK_TTL))
        return {"held": False, "by": "", "same_person": False, "expires_in": LOCK_TTL}

    def release(self, rid: str, sess: str) -> None:
        self.run("DELETE FROM setu_lock WHERE rid = ? AND sess = ?", (rid, sess))


# ── shaping a row for the interface ────────────────────────────────────────

def view(r: dict, full: bool = False) -> dict:
    """One row, as the screen needs it.

    ``text`` is what the annotator sees and edits; ``source`` is what the parser
    extracted and never changes. Sending both is what lets the interface offer
    "restore the original" without another request, and what makes it obvious in
    the API that the two are different things.
    """
    def side(prefix: str) -> dict:
        source = r.get(f"{prefix}_source")
        edit = r.get(f"{prefix}_edit")
        out = {
            "sid": r.get(f"{prefix}_sid"),
            "present": r.get(f"{prefix}_sid") is not None,
            "source": source or "",
            "text": edit if edit is not None else (source or ""),
            "rev": int(r.get(f"{prefix}_rev") or 0),
            "edited": edit is not None and edit != (source or ""),
            "page": r.get(f"{prefix}_pg"),
            "kind": r.get(f"{prefix}_kind") or "",
            "item_no": r.get(f"{prefix}_item") or "",
            "has_math": bool(r.get(f"{prefix}_math")),
            "has_table": bool(r.get(f"{prefix}_table")),
        }
        if full:
            out["box"] = {k: r.get(f"{prefix}_f{k}") for k in ("x0", "y0", "x1", "y1")}
            out["block_ids"] = r.get(f"{prefix}_blocks") or "[]"
        return out

    return {
        "rid": r["rid"], "pid": r["pid"], "seq": r["seq"],
        "status": r["status"], "origin": r["origin"],
        "confidence": round(float(r["confidence"] or 0), 3),
        "note": r["note"] or "", "kind": r["kind"] or "",
        "chapter": r["chapter"] or "", "chapter_no": r["chapter_no"] or "",
        "section": r["section"] or "", "section_no": r["section_no"] or "",
        "edited": bool(r["edited"]),
        "updated_at": r["updated_at"], "updated_by": r["updated_by"] or "",
        "src": side("src"), "tgt": side("tgt"),
    }


# ── creating a project ─────────────────────────────────────────────────────

def create_project(con, *, src_book: str, tgt_book: str, name: str = "",
                   annotator: str = "", include_noise: bool = False,
                   build: bool = True) -> dict:
    """Open two books together and lay out the rows.

    Refuses the obvious mistakes up front — the same book twice, a book that is
    not there — because each of them produces a project that looks fine until
    somebody has annotated two hundred rows of it.
    """
    corpus = CorpusRepo(con)
    if src_book == tgt_book:
        raise Invalid("the two sides must be different books")
    src = corpus.book(src_book)
    tgt = corpus.book(tgt_book)

    pid = ids.project_id(name or f"{src['book']}~{tgt['book']}", src_book, tgt_book)
    repo = WorkspaceRepo(con)
    existing = repo.one("SELECT pid FROM setu_project WHERE src_book = ? AND tgt_book = ?",
                        (src_book, tgt_book))
    if existing:
        return repo.project(existing["pid"])

    label = name.strip() or (
        f"{src.get('board_name') or src.get('board') or ''} "
        f"Class {src.get('class') or '?'} — "
        f"{src.get('language') or 'source'} ⇄ {tgt.get('language') or 'target'}"
    ).strip()

    now = time.time()
    repo.run(
        "INSERT INTO setu_project(pid, name, src_book, tgt_book, src_language,"
        " tgt_language, board, class, subject, created_at, created_by, n_rows)"
        " VALUES(?,?,?,?,?,?,?,?,?,?,?,0)",
        (pid, label[:200], src_book, tgt_book, src.get("language") or "",
         tgt.get("language") or "", src.get("board") or "", src.get("class"),
         src.get("subject") or "", now, annotator[:120]))
    repo.event("project.create", pid, {"src": src_book, "tgt": tgt_book},
               actor=annotator)

    if build:
        build_rows(con, pid, include_noise=include_noise, annotator=annotator)
    return repo.project(pid)


def build_rows(con, pid: str, *, include_noise: bool = False,
               annotator: str = "", force: bool = False) -> dict:
    """Generate the project's rows from the aligner.

    Refuses to run over rows that carry human work unless *force* is set. This
    is the one operation in Setu that could destroy an afternoon, so it asks.
    """
    repo = WorkspaceRepo(con)
    proj = repo.one("SELECT * FROM setu_project WHERE pid = ?", (pid,))
    if not proj:
        raise NotFound(f"no such project: {pid}")

    touched = repo.scalar(
        "SELECT COUNT(*) FROM setu_row WHERE pid = ? AND (status <> ? OR edited = 1)",
        (pid, DEFAULT_STATUS), default=0)
    if touched and not force:
        raise Invalid(
            f"{touched} rows in this project already carry annotation work; "
            "rebuilding would discard it. Pass force=true only if that is "
            "what you mean.")

    corpus = CorpusRepo(con)
    kinds = None if include_noise else [
        k for k in _annotatable_kinds() if k not in NOISE_KINDS]
    src = corpus.segments(proj["src_book"], limit=100000, kinds=kinds)
    tgt = corpus.segments(proj["tgt_book"], limit=100000, kinds=kinds)
    if not src and not tgt:
        raise Invalid("neither book has any segments; has the source layer been built?")

    proposals = align.suggest(src, tgt)
    now = time.time()

    repo.run("DELETE FROM setu_row WHERE pid = ?", (pid,))
    batch = []
    # Navigation follows ONE book's table of contents — the source. A row with
    # nothing on the left inherits the chapter of the row above it rather than
    # taking the target book's own title, because mixing the two produces a
    # sidebar with "Sets" and "संच" as separate chapters and every annotator
    # then has to visit both to finish one.
    carried = {"chapter": "", "chapter_no": "", "section": "", "section_no": ""}
    for seq, p in enumerate(proposals):
        s = src[p.src] if p.src >= 0 else None
        t = tgt[p.tgt] if p.tgt >= 0 else None
        if s:
            carried = {k: s.get(k, "") for k in carried}
        elif not any(carried.values()) and t:
            # Nothing from the source book yet — front matter that exists only
            # on the right. The target's own heading is better than nothing.
            carried = {k: t.get(k, "") for k in carried}
        anchor = s or t
        batch.append((
            ids.row_id(pid, seq), pid, seq,
            s["sid"] if s else None, t["sid"] if t else None,
            DEFAULT_STATUS,
            "suggested" if p.basis in {"math", "number"} else
            ("derived" if p.basis == "fill" else "unpaired"),
            p.confidence, "",
            carried["chapter"], carried["chapter_no"],
            carried["section"], carried["section_no"],
            anchor.get("kind", "") if anchor else "",
            s["page"] if s else None, t["page"] if t else None,
            now, now, annotator[:120],
        ))

    repo.runmany(
        "INSERT INTO setu_row(rid, pid, seq, src_sid, tgt_sid, status, origin,"
        " confidence, note, chapter, chapter_no, section, section_no, kind,"
        " src_page, tgt_page, created_at, updated_at, updated_by)"
        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
    repo.run("UPDATE setu_project SET n_rows = ?, built_at = ? WHERE pid = ?",
             (len(batch), now, pid))

    report = align.quality(proposals)
    report["rows"] = len(batch)
    repo.event("project.build", pid, report, actor=annotator)
    log.info("project %s: %s rows (%s anchored)", pid, len(batch), report["anchored"])
    return report


def _annotatable_kinds() -> list[str]:
    from .models import KINDS
    return [k.key for k in KINDS if k.annotatable]


def delete_project(con, pid: str, annotator: str = "") -> dict:
    """Remove a project and everything hanging off it.

    Segments and books are untouched — they are source data and do not belong
    to any one project. Revisions are kept: the history of what a person typed
    outlives the project it was typed in.
    """
    repo = WorkspaceRepo(con)
    proj = repo.one("SELECT pid, n_rows FROM setu_project WHERE pid = ?", (pid,))
    if not proj:
        raise NotFound(f"no such project: {pid}")
    repo.run("DELETE FROM setu_lock WHERE rid IN (SELECT rid FROM setu_row WHERE pid = ?)",
             (pid,))
    repo.run("DELETE FROM setu_project WHERE pid = ?", (pid,))   # cascades to rows/text
    repo.event("project.delete", pid, {"rows": proj["n_rows"]}, actor=annotator)
    return {"deleted": pid, "rows": proj["n_rows"]}
