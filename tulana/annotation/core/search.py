"""Setu — finding a row again.

Annotators search for three different things and do not distinguish between
them when they type: a phrase they remember, an identifier somebody sent them,
and a place in the book ("chapter 4", "page 88"). This module works out which
of those a query is and answers accordingly, rather than making a person choose
a search mode first.

Text search runs against FTS5 when the SQLite build has it, and falls back to
``LIKE`` when it does not. The fallback is slower but returns the same rows, and
the response says which one ran so nobody has to guess why a search took a
second.

Edited text is searched separately from source text. ``setu_seg_fts`` indexes
the parser's extraction, which never changes; a person's corrections live in
``setu_text``, which is small (only edited rows exist in it) and can be scanned
directly. Searching both is what stops "I fixed that typo, now I can't find it".
"""
from __future__ import annotations

import logging
import re
from typing import Any

from . import ids
from .models import STATUS_BY_KEY, normalise
from .store import NotFound, Repository, fts_ready, paginate
from .workspace import view

log = logging.getLogger("setu.search")

_PAGE_Q = re.compile(r"^\s*(?:p|pg|page)\s*\.?\s*(\d{1,4})\s*$", re.I)
_CHAPTER_Q = re.compile(r"^\s*(?:ch|chap|chapter)\s*\.?\s*(\d{1,2}(?:\.\d{1,3})*)\s*$", re.I)
_SECTION_Q = re.compile(r"^\s*(\d{1,2}\.\d{1,3})\s*$")
_ROW_Q = re.compile(r"^\s*(?:#|row\s*)(\d{1,7})\s*$", re.I)

#: FTS5 treats a lot of punctuation as syntax. Queries come from a search box,
#: not from someone writing FTS expressions, so the syntax is escaped away and
#: the words are ANDed. A query of `"exact phrase"` keeps its quotes and is
#: passed through as a phrase, which is the one piece of syntax worth having.
_FTS_UNSAFE = re.compile(r'[^\w\s"]+', re.U)


def _fts_query(text: str) -> str:
    cleaned = _FTS_UNSAFE.sub(" ", text).strip()
    if not cleaned:
        return ""
    if cleaned.count('"') >= 2:
        return cleaned
    terms = [t for t in cleaned.split() if t]
    return " AND ".join(f'"{t}"' for t in terms)


class SearchRepo(Repository):
    """Search within one project."""

    def find(self, pid: str, query: Any, *, limit: Any = 40, offset: Any = 0,
             status: str = "", chapter_no: str = "", kind: str = "",
             side: str = "both") -> dict:
        if not self.one("SELECT 1 AS ok FROM setu_project WHERE pid = ?", (pid,)):
            raise NotFound(f"no such project: {pid}")
        lim, off = paginate(limit, offset, default=40, cap=200)
        q = normalise(query).strip()
        if not q:
            return {"query": "", "mode": "empty", "total": 0, "rows": [],
                    "limit": lim, "offset": off}

        direct = self._direct(pid, q)
        if direct is not None:
            return {**direct, "query": q, "limit": lim, "offset": off}

        filters, args = self._filters(pid, status, chapter_no, kind)
        mode = "fts" if fts_ready(self.con) else "like"
        sids = self._matching_sids(q, mode)
        edited = self._matching_edited(pid, q)

        if not sids and not edited:
            return {"query": q, "mode": mode, "total": 0, "rows": [],
                    "limit": lim, "offset": off}

        clauses = []
        params: list[Any] = []
        if sids:
            marks = ",".join("?" * len(sids))
            if side in ("src", "both"):
                clauses.append(f"r.src_sid IN ({marks})")
                params.extend(sids)
            if side in ("tgt", "both"):
                clauses.append(f"r.tgt_sid IN ({marks})")
                params.extend(sids)
        if edited:
            marks = ",".join("?" * len(edited))
            clauses.append(f"r.rid IN ({marks})")
            params.extend(edited)
        match = " OR ".join(clauses)

        where = f"{filters} AND ({match})"
        total = self.scalar(f"SELECT COUNT(*) FROM setu_row r WHERE {where}",
                            args + params, default=0)
        rows = self.all(
            f"""SELECT r.*, ss.source_text AS src_source, ss.page AS src_pg,
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
                 WHERE {where} ORDER BY r.seq LIMIT ? OFFSET ?""",
            args + params + [lim, off])
        return {"query": q, "mode": mode, "total": total, "limit": lim,
                "offset": off, "rows": [view(r) for r in rows]}

    # -- the three kinds of query ----------------------------------------
    def _direct(self, pid: str, q: str) -> dict | None:
        """Identifiers and locations resolve without touching the text index."""
        if ids.is_id(q, "rw") or ids.is_id(q, "sg"):
            col = "rid" if q.startswith("rw_") else None
            if col:
                rows = self.all(_ROW_SQL + " WHERE r.pid = ? AND r.rid = ?", (pid, q))
            else:
                rows = self.all(
                    _ROW_SQL + " WHERE r.pid = ? AND (r.src_sid = ? OR r.tgt_sid = ?)",
                    (pid, q, q))
            return {"mode": "id", "total": len(rows), "rows": [view(r) for r in rows]}

        m = _ROW_Q.match(q)
        if m:
            rows = self.all(_ROW_SQL + " WHERE r.pid = ? AND r.seq = ?",
                            (pid, int(m.group(1))))
            return {"mode": "row", "total": len(rows), "rows": [view(r) for r in rows]}

        m = _PAGE_Q.match(q)
        if m:
            page = int(m.group(1))
            rows = self.all(
                _ROW_SQL + " WHERE r.pid = ? AND (r.src_page = ? OR r.tgt_page = ?)"
                           " ORDER BY r.seq LIMIT 200", (pid, page, page))
            return {"mode": "page", "total": len(rows), "rows": [view(r) for r in rows]}

        m = _CHAPTER_Q.match(q) or _SECTION_Q.match(q)
        if m:
            num = m.group(1)
            rows = self.all(
                _ROW_SQL + " WHERE r.pid = ? AND (r.chapter_no = ? OR r.section_no = ?)"
                           " ORDER BY r.seq LIMIT 200", (pid, num, num))
            if rows:
                return {"mode": "location", "total": len(rows),
                        "rows": [view(r) for r in rows]}
        return None

    def _matching_sids(self, q: str, mode: str) -> list[str]:
        """Segment ids whose parser text matches. Capped — this feeds an IN()."""
        if mode == "fts":
            expr = _fts_query(q)
            if not expr:
                return []
            try:
                return [r["sid"] for r in self.all(
                    "SELECT sid FROM setu_seg_fts WHERE setu_seg_fts MATCH ?"
                    " LIMIT 4000", (expr,))]
            except Exception as exc:             # a malformed expression, not a crash
                log.info("FTS query rejected (%s); falling back to LIKE", exc)
        return [r["sid"] for r in self.all(
            "SELECT sid FROM setu_segment WHERE source_text LIKE ? ESCAPE '\\' LIMIT 4000",
            (_escape_like(q),))]

    def _matching_edited(self, pid: str, q: str) -> list[str]:
        """Row ids whose *edited* text matches. Small table; a scan is fine."""
        return [r["rid"] for r in self.all(
            "SELECT DISTINCT t.rid FROM setu_text t JOIN setu_row r ON r.rid = t.rid"
            " WHERE r.pid = ? AND t.text LIKE ? ESCAPE '\\' LIMIT 2000",
            (pid, _escape_like(q)))]

    def _filters(self, pid: str, status: str, chapter_no: str,
                 kind: str) -> tuple[str, list[Any]]:
        where = ["r.pid = ?"]
        args: list[Any] = [pid]
        if status:
            keys = [s.strip() for s in status.split(",") if s.strip() in STATUS_BY_KEY]
            if keys:
                where.append(f"r.status IN ({','.join('?' * len(keys))})")
                args.extend(keys)
        if chapter_no:
            where.append("r.chapter_no = ?")
            args.append(chapter_no)
        if kind:
            where.append("r.kind = ?")
            args.append(kind)
        return " AND ".join(where), args


def _escape_like(term: str) -> str:
    """Wrap *term* as a LIKE pattern with its own wildcards neutralised.

    Takes the bare search term, not a pattern: searching for ``100%`` must find
    the string ``100%``, and searching for ``_`` must not match every single
    character in the corpus. The caller pairs this with ``ESCAPE '\\'``.
    """
    body = (term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_"))
    return f"%{body}%"


_ROW_SQL = """SELECT r.*, ss.source_text AS src_source, ss.page AS src_pg,
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
                LEFT JOIN setu_text tt ON tt.rid = r.rid AND tt.side = 'tgt'"""
