"""Setu — the immutable source layer.

Everything here is about turning the parsed-layout corpus into the units an
annotator can work on, once, and then never touching them again. Two jobs:

**Deduplication.** The corpus ships 152 parsed files describing 80 distinct
books: 31 books appear twice under different folders, differing only in the
folder and the raster filenames. Left alone, every board would show every
textbook twice. :func:`build` elects one copy canonical and records the rest as
aliases, so provenance survives without the duplicate reaching a dropdown.

**Segmentation.** A block is what the layout parser found; a *segment* is what
a person annotates. They are nearly the same thing, and Setu keeps them
one-to-one on purpose — merging blocks would make the units bigger but would
also throw away the parser's own boundaries, which is the only structure the
corpus actually has. What segmentation adds is the document hierarchy: as the
walk passes a chapter title, a section title, a numbered exercise heading, it
remembers them, so every later segment knows where in the book it sits.

Segment text is copied into ``setu_segment.source_text`` and never updated. An
annotator's edits live in a different table entirely. That is what makes
"the original OCR is preserved forever" a property of the schema rather than a
promise in a document.
"""
from __future__ import annotations

import json
import logging
import re
import sqlite3
import time
from contextlib import contextmanager
from typing import Any, Callable, Iterable

from . import ids
from .models import (
    KIND_BY_KEY, KIND_FROM_LABEL, fold_digits, has_math, has_table, item_number,
    kind_for, math_fingerprints, normalise, structural_numbers,
)
from .store import Invalid, NotFound, Repository, paginate

log = logging.getLogger("setu.corpus")

#: Leading "1.2 " or trailing " 1" on a heading — how the corpus writes chapter
#: and section numbers in every edition examined.
_LEAD_NO = re.compile(r"^\s*(\d{1,2}(?:\.\d{1,3})*)[\s.:)–-]")
_TRAIL_NO = re.compile(r"[\s(](\d{1,2}(?:\.\d{1,3})*)\)?\s*$")

#: Kinds that are structurally noise: they repeat on every page and carry no
#: translatable content. Segments are still created for them — throwing source
#: data away is never right — but projects skip them by default.
NOISE_KINDS = frozenset({"header", "footer", "page_number", "figure"})


class CorpusRepo(Repository):
    """Read access to the immutable source layer."""

    # -- cascade ----------------------------------------------------------
    def boards(self) -> list[dict]:
        """Boards, the ones that can actually be annotated first.

        Ordering this list alphabetically put Andhra Pradesh at the top, and
        Andhra Pradesh holds a single language — its books are bilingual in one
        file, so there is no second edition to read beside the first. Every
        annotator therefore opened the workspace on a selection that could not
        be annotated: no target language, no books, nothing to scroll, no
        printed page to check. The interface looked broken and was not.

        So: boards that offer two or more languages come first, the richest
        first, and the count travels with the row so the list can say which is
        which.
        """
        return self.all(
            "SELECT board AS code, COALESCE(NULLIF(board_name,''), board) AS name,"
            "       COUNT(*) AS n_books,"
            "       COUNT(DISTINCT CASE WHEN language <> '' THEN language END)"
            "           AS n_languages"
            "  FROM setu_book WHERE board <> ''"
            " GROUP BY board, board_name"
            " ORDER BY (COUNT(DISTINCT CASE WHEN language <> '' THEN language END)"
            "           >= 2) DESC,"
            "          COUNT(DISTINCT CASE WHEN language <> '' THEN language END) DESC,"
            "          name")

    def classes(self, board: str) -> list[dict]:
        return self.all(
            "SELECT class AS value, COUNT(*) AS n_books FROM setu_book"
            " WHERE board = ? AND class IS NOT NULL"
            " GROUP BY class ORDER BY class", (board,))

    def subjects(self, board: str, cls: Any) -> list[dict]:
        """Subjects for a board and class, with how many languages each has.

        The language count is carried here because it decides whether the
        selection can be annotated at all: annotating means reading one
        language beside another, so a subject holding a single language is a
        dead end. Knowing that before the languages are chosen lets the
        interface say so rather than presenting a list of one.
        """
        return self.all(
            "SELECT COALESCE(NULLIF(subject,''),'Mathematics') AS value,"
            "       COUNT(*) AS n_books,"
            "       COUNT(DISTINCT CASE WHEN language <> '' THEN language END)"
            "           AS n_languages"
            "  FROM setu_book"
            " WHERE board = ? AND class IS ? GROUP BY value ORDER BY value",
            (board, _int_or_none(cls)))

    def languages(self, board: str, cls: Any, subject: str,
                  exclude: str = "") -> list[dict]:
        """Languages available for a selection, optionally minus one.

        ``exclude`` is what makes the two sides of the workspace different.
        Both lists used to be built from the same query, so whatever was
        chosen on the left was still offered on the right — and a corpus with
        one language offered that language on both sides, which is not a pair
        of anything.
        """
        sql = ["SELECT language AS value, script, COUNT(*) AS n_books"
               "  FROM setu_book"
               " WHERE board = ? AND class IS ?"
               "   AND COALESCE(NULLIF(subject,''),'Mathematics') = ?"
               "   AND language <> ''"]
        args: list[Any] = [board, _int_or_none(cls), subject]
        if exclude:
            sql.append(" AND language <> ?")
            args.append(exclude)
        sql.append(" GROUP BY language, script"
                   " ORDER BY (language='English') DESC, language")
        return self.all("".join(sql), args)

    def books(self, board: str = "", cls: Any = None, subject: str = "",
              language: str = "", exclude: str = "") -> list[dict]:
        """Books matching the cascade so far. Every filter is optional."""
        sql = ["SELECT book_key, book, title, language, script, volume, num_pages,"
               "       n_segments, pdf_present, relpath"
               "  FROM setu_book WHERE 1=1"]
        args: list[Any] = []
        if board:
            sql.append(" AND board = ?"); args.append(board)
        if cls not in (None, "", "any"):
            sql.append(" AND class IS ?"); args.append(_int_or_none(cls))
        if subject:
            sql.append(" AND COALESCE(NULLIF(subject,''),'Mathematics') = ?")
            args.append(subject)
        if language:
            sql.append(" AND language = ?"); args.append(language)
        if exclude:
            sql.append(" AND book_key <> ?"); args.append(exclude)
        sql.append(" ORDER BY volume, book")
        return self.all("".join(sql), args)

    def book(self, book_key: str) -> dict:
        row = self.one("SELECT * FROM setu_book WHERE book_key = ?", (book_key,))
        if not row:
            raise NotFound(f"no such book: {book_key}")
        return row

    def aliases(self, book_key: str) -> list[dict]:
        return self.all(
            "SELECT pl_book_id, relpath FROM setu_book_alias WHERE book_key = ?"
            " ORDER BY relpath", (book_key,))

    # -- segments ---------------------------------------------------------
    def segment(self, sid: str) -> dict:
        row = self.one("SELECT * FROM setu_segment WHERE sid = ?", (sid,))
        if not row:
            raise NotFound(f"no such segment: {sid}")
        return _decode(row)

    def segments(self, book_key: str, *, limit: Any = 200, offset: Any = 0,
                 kinds: Iterable[str] | None = None,
                 chapter_no: str = "", page: Any = None) -> list[dict]:
        lim, off = paginate(limit, offset, default=200, cap=2000)
        sql = ["SELECT * FROM setu_segment WHERE book_key = ?"]
        args: list[Any] = [book_key]
        if kinds:
            keys = [k for k in kinds if k in KIND_BY_KEY]
            if keys:
                sql.append(f" AND kind IN ({','.join('?' * len(keys))})")
                args.extend(keys)
        if chapter_no:
            sql.append(" AND chapter_no = ?"); args.append(chapter_no)
        if page is not None:
            sql.append(" AND page = ?"); args.append(int(page))
        sql.append(" ORDER BY seq LIMIT ? OFFSET ?")
        args.extend([lim, off])
        return [_decode(r) for r in self.all("".join(sql), args)]

    def outline(self, book_key: str) -> list[dict]:
        """Chapters and their sections, for the navigation sidebar."""
        rows = self.all(
            "SELECT chapter_no, chapter, section_no, section, COUNT(*) AS n,"
            "       MIN(seq) AS first_seq, MIN(page) AS first_page"
            "  FROM setu_segment WHERE book_key = ?"
            " GROUP BY chapter_no, chapter, section_no, section"
            " ORDER BY first_seq", (book_key,))
        chapters: list[dict] = []
        index: dict[str, dict] = {}
        for r in rows:
            ckey = r["chapter_no"] or r["chapter"] or "—"
            ch = index.get(ckey)
            if ch is None:
                ch = {"chapter_no": r["chapter_no"], "chapter": r["chapter"] or "Front matter",
                      "first_seq": r["first_seq"], "first_page": r["first_page"],
                      "n": 0, "sections": []}
                index[ckey] = ch
                chapters.append(ch)
            ch["n"] += r["n"]
            if r["section"] or r["section_no"]:
                ch["sections"].append(
                    {"section_no": r["section_no"], "section": r["section"],
                     "n": r["n"], "first_seq": r["first_seq"],
                     "first_page": r["first_page"]})
        return chapters

    def counts(self) -> dict:
        return {
            "books": self.scalar("SELECT COUNT(*) FROM setu_book", default=0),
            "aliases": self.scalar("SELECT COUNT(*) FROM setu_book_alias", default=0),
            "segments": self.scalar("SELECT COUNT(*) FROM setu_segment", default=0),
            "pages": self.scalar("SELECT COALESCE(SUM(num_pages),0) FROM setu_book", default=0),
        }


def _int_or_none(v: Any) -> Any:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _decode(row: dict) -> dict:
    """Turn the JSON columns back into Python without trusting their contents."""
    out = dict(row)
    for key, default in (("block_ids", []), ("anchor_math", []), ("anchor_num", [])):
        raw = out.get(key)
        if isinstance(raw, str):
            try:
                val = json.loads(raw)
                out[key] = val if isinstance(val, list) else default
            except (ValueError, TypeError):
                out[key] = default
        elif not isinstance(raw, list):
            out[key] = default
    return out


# ── building the source layer ──────────────────────────────────────────────

def build(con, *, rebuild: bool = False, log_fn: Callable[[str], None] = log.info) -> dict:
    """Derive ``setu_book`` and ``setu_segment`` from the parsed-layout tables.

    Idempotent: running it twice changes nothing, because both identifiers are
    positional. Books already built are skipped unless *rebuild* is set, so a
    newly added textbook costs only its own segmentation.

    Returns a report — including any parser label it did not recognise, so an
    unmapped label surfaces as a number rather than as silently mis-filed data.
    """
    started = time.time()
    if not _has_parsed_layout(con):
        raise Invalid(
            "the parsed-layout corpus has not been imported yet; run the "
            "Blocks ingest first (POST /api/blocks/ingest)")

    repo = CorpusRepo(con)
    report = {"books_seen": 0, "books_built": 0, "books_skipped": 0,
              "aliases": 0, "segments": 0, "unmapped_labels": {}, "errors": []}

    groups = _dedup_groups(con)
    report["books_seen"] = sum(len(g) for g in groups.values())

    for dkey, members in groups.items():
        canonical = members[0]
        book_key = ids.book_key(canonical["relpath"])
        try:
            existing = repo.one("SELECT book_key, n_segments FROM setu_book"
                                " WHERE book_key = ?", (book_key,))
            # One transaction per book, not one for the whole corpus. A full
            # build is around two minutes of work; holding a single write lock
            # for two minutes would stall every annotator on the instance,
            # whereas a second per book is invisible to them. It also means a
            # crash half way through leaves the books already built intact.
            with _book_tx(con):
                if existing and not rebuild:
                    report["books_skipped"] += 1
                else:
                    n = _build_book(con, canonical, book_key, dkey, report)
                    report["segments"] += n
                    report["books_built"] += 1
                # Aliases are cheap and must reflect the current corpus even
                # when the book itself was skipped, so a second copy appearing
                # later is still recorded.
                for other in members[1:]:
                    con.execute(
                        "INSERT INTO setu_book_alias(pl_book_id, book_key, relpath)"
                        " VALUES(?,?,?) ON CONFLICT(pl_book_id) DO UPDATE SET"
                        "   book_key=excluded.book_key, relpath=excluded.relpath",
                        (other["id"], book_key, other["relpath"]))
                    report["aliases"] += 1
        except Exception as exc:                 # one bad book must not stop the rest
            log.exception("failed to build %s", canonical.get("relpath"))
            report["errors"].append({"book": canonical.get("relpath"),
                                     "error": f"{type(exc).__name__}: {exc}"})

    report["seconds"] = round(time.time() - started, 2)
    log_fn(f"Setu source layer: {report['books_built']} built, "
           f"{report['books_skipped']} unchanged, {report['segments']} segments, "
           f"{report['seconds']}s")
    return report


@contextmanager
def _book_tx(con):
    """A transaction around one book, tolerant of an outer one already running.

    ``build`` is useful both on its own connection and inside a caller's
    transaction (the tests do the latter). ``in_transaction`` tells us which
    case we are in, so neither one ends up committing the other's work.
    """
    outer = con.in_transaction
    if not outer:
        con.execute("BEGIN IMMEDIATE")
    try:
        yield
    except Exception:
        if not outer:
            try:
                con.execute("ROLLBACK")
            except sqlite3.Error:                # pragma: no cover - defensive
                pass
        raise
    else:
        if not outer:
            con.execute("COMMIT")


def _has_parsed_layout(con) -> bool:
    row = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='pl_blocks'"
    ).fetchone()
    if not row:
        return False
    return bool(con.execute("SELECT 1 FROM pl_books LIMIT 1").fetchone())


def _dedup_groups(con) -> dict[str, list[dict]]:
    """Group parsed books by content identity, canonical copy first.

    The canonical copy is the one whose path is shortest and then alphabetically
    first — a stable rule, so the same copy is elected on every machine and the
    identifiers do not move.
    """
    rows = [dict(r) for r in con.execute(
        "SELECT id, book, relpath, source_json, num_pages, n_blocks, board, class,"
        "       subject, language, script, volume, title, pdf_present"
        "  FROM pl_books ORDER BY relpath")]
    groups: dict[str, list[dict]] = {}
    for r in rows:
        key = ids.dedup_key(r["book"], r["num_pages"] or 0, r["n_blocks"] or 0)
        groups.setdefault(key, []).append(r)
    for members in groups.values():
        members.sort(key=lambda m: (len(m["relpath"] or ""), m["relpath"] or ""))
    return groups


def _build_book(con, row: dict, book_key: str, dkey: str, report: dict) -> int:
    """Segment one book, without breaking anything that points at it.

    Segment ids are positional, so re-segmenting a book whose parse has not
    changed produces exactly the same ids. That makes the update an upsert
    rather than a delete-and-recreate — which matters, because a project's rows
    hold foreign keys into ``setu_segment``, and deleting the row out from under
    a live annotation would either fail or orphan somebody's work.

    Segments that genuinely no longer exist are removed only when nothing
    references them. One that a project still points at is kept, and counted in
    the report, because the alternative is destroying an annotation of text that
    has merely been re-parsed.
    """
    import config

    pages = con.execute(
        "SELECT id, page, width, height FROM pl_pages WHERE book_id = ? ORDER BY page",
        (row["id"],)).fetchall()

    state = _Walk()
    batch: list[tuple] = []
    seq = 0
    for page in pages:
        blocks = con.execute(
            "SELECT id, ord, label, type, text, fx0, fy0, fx1, fy1"
            "  FROM pl_blocks WHERE page_id = ? ORDER BY ord", (page["id"],)).fetchall()
        for blk in blocks:
            label = (blk["label"] or "").strip()
            if label and label.lower() not in KIND_FROM_LABEL:
                report["unmapped_labels"][label] = report["unmapped_labels"].get(label, 0) + 1
            text = normalise(blk["text"])
            kind = kind_for(label, text)
            state.observe(label, text)
            sid = ids.segment_id(book_key, page["page"], blk["ord"], blk["ord"])
            batch.append((
                sid, book_key, seq, page["page"], blk["ord"], blk["ord"], kind,
                label, blk["type"] or "", state.chapter, state.chapter_no,
                state.section, state.section_no, item_number(text) if kind in
                {"example", "exercise", "question", "mcq", "theorem"} else "",
                state.depth, text, len(text), int(has_math(text)), int(has_table(text)),
                json.dumps([blk["id"]]),
                _f(blk["fx0"]), _f(blk["fy0"]), _f(blk["fx1"]), _f(blk["fy1"]),
                json.dumps(math_fingerprints(text), ensure_ascii=False),
                json.dumps(structural_numbers(text), ensure_ascii=False),
            ))
            seq += 1

    board_name = ""
    try:
        board_name = config.board_name(row["board"]) if row["board"] else ""
    except Exception:                            # pragma: no cover - config shape
        board_name = row["board"] or ""

    con.execute(
        "INSERT INTO setu_book(book_key, pl_book_id, dedup_key, book, relpath, board,"
        " board_name, class, subject, language, script, volume, title, num_pages,"
        " n_blocks, n_segments, pdf_present, ingested_at)"
        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        " ON CONFLICT(book_key) DO UPDATE SET"
        "   pl_book_id=excluded.pl_book_id, dedup_key=excluded.dedup_key,"
        "   board=excluded.board, board_name=excluded.board_name, class=excluded.class,"
        "   subject=excluded.subject, language=excluded.language, script=excluded.script,"
        "   volume=excluded.volume, title=excluded.title, num_pages=excluded.num_pages,"
        "   n_blocks=excluded.n_blocks, n_segments=excluded.n_segments,"
        "   pdf_present=excluded.pdf_present, ingested_at=excluded.ingested_at",
        (book_key, row["id"], dkey, row["book"], row["relpath"], row["board"] or "",
         board_name, row["class"], row["subject"] or "", row["language"] or "",
         row["script"] or "", row["volume"] or "", row["title"] or row["book"],
         row["num_pages"] or 0, row["n_blocks"] or 0, len(batch),
         int(row["pdf_present"] or 0), time.time()))

    # The book row has to exist before its segments: setu_segment.book_key is a
    # declared foreign key and foreign_keys=ON is not decorative.
    con.executemany(
        "INSERT INTO setu_segment(sid, book_key, seq, page, ord_start, ord_end, kind,"
        " label, block_type, chapter, chapter_no, section, section_no, item_no, depth,"
        " source_text, n_chars, has_math, has_table, block_ids, fx0, fy0, fx1, fy1,"
        " anchor_math, anchor_num)"
        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        " ON CONFLICT(sid) DO UPDATE SET"
        "   seq=excluded.seq, page=excluded.page, ord_start=excluded.ord_start,"
        "   ord_end=excluded.ord_end, kind=excluded.kind, label=excluded.label,"
        "   block_type=excluded.block_type, chapter=excluded.chapter,"
        "   chapter_no=excluded.chapter_no, section=excluded.section,"
        "   section_no=excluded.section_no, item_no=excluded.item_no,"
        "   depth=excluded.depth, source_text=excluded.source_text,"
        "   n_chars=excluded.n_chars, has_math=excluded.has_math,"
        "   has_table=excluded.has_table, block_ids=excluded.block_ids,"
        "   fx0=excluded.fx0, fy0=excluded.fy0, fx1=excluded.fx1, fy1=excluded.fy1,"
        "   anchor_math=excluded.anchor_math, anchor_num=excluded.anchor_num", batch)

    _retire_stale(con, book_key, {r[0] for r in batch}, report)
    _index_fts(con, book_key, batch)
    return len(batch)


def _retire_stale(con, book_key: str, keep: set[str], report: dict) -> None:
    """Remove segments this book no longer has, sparing any still in use."""
    existing = {r[0] for r in con.execute(
        "SELECT sid FROM setu_segment WHERE book_key = ?", (book_key,))}
    stale = existing - keep
    if not stale:
        return
    marks = ",".join("?" * len(stale))
    referenced = {r[0] for r in con.execute(
        f"SELECT sid FROM (SELECT src_sid AS sid FROM setu_row WHERE src_sid IN ({marks})"
        f" UNION SELECT tgt_sid FROM setu_row WHERE tgt_sid IN ({marks}))",
        list(stale) * 2)}
    removable = stale - referenced
    if removable:
        con.executemany("DELETE FROM setu_segment WHERE sid = ?",
                        [(s,) for s in removable])
    if referenced:
        report["retained_in_use"] = report.get("retained_in_use", 0) + len(referenced)
        log.info("%s: kept %d re-parsed segments that annotations still point at",
                 book_key, len(referenced))


def _f(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _index_fts(con, book_key: str, batch: list[tuple]) -> None:
    """Refresh the search index for one book. Silent no-op without FTS5."""
    from .store import fts_ready
    if not fts_ready(con):
        return
    con.execute("DELETE FROM setu_seg_fts WHERE book_key = ?", (book_key,))
    con.executemany(
        "INSERT INTO setu_seg_fts(sid, book_key, body) VALUES(?,?,?)",
        [(r[0], book_key, r[15]) for r in batch if r[15]])


#: Parser labels that open a level of the document. Heading-ness is decided by
#: the *label*, which layout analysis produced and which is the same in every
#: language, never by the refined kind — "Practice set 1.2" is classified as an
#: exercise but it is still the section heading that carries the number 1.2.
_HEADING_LEVEL = {
    "chapter-title": 1,
    "section-title": 2,
    "sub-section-title": 3,
}


class _Walk:
    """Carries the document hierarchy down the page as the walk proceeds.

    A chapter title resets the section; a section title resets the subsection.
    Nothing here looks ahead, so the state is exactly what a reader would have
    in mind at that point in the book.

    No number is ever invented. Many books in this corpus print the chapter
    number as separate artwork that the parser records as a figure, so the
    title block carries no number at all; in that case ``chapter_no`` stays
    empty and navigation orders by position instead. A fabricated "Chapter 5"
    that disagrees with the printed book would be worse than no number.
    """

    def __init__(self) -> None:
        self.chapter = ""
        self.chapter_no = ""
        self.section = ""
        self.section_no = ""
        self.depth = 0

    def observe(self, label: str, text: str) -> None:
        level = _HEADING_LEVEL.get(str(label or "").strip().lower())
        if not level:
            return
        head = text.strip().split("\n", 1)[0][:160]
        if not head:
            return
        if level == 1:
            # A running header repeats the chapter title on every page. Treat a
            # repeat as the same chapter rather than as a new one.
            if _same_chapter(head, self.chapter):
                # The same chapter, reprinted as a running head. Keep any number
                # the full title declared: the running head usually drops it.
                self.chapter = self.chapter or head
            else:
                self.chapter = head
                self.chapter_no = _heading_number(head)
                self.section = ""
                self.section_no = ""
            self.depth = 1
        elif level == 2:
            self.section = head
            self.section_no = _heading_number(head)
            self.depth = 2
        else:
            # A subsection heading only claims the section slot when no section
            # heading has been seen yet — some books skip the middle level.
            if not self.section:
                self.section = head
                self.section_no = _heading_number(head)
            self.depth = 3


_PLAIN = re.compile(r"[^\w]+", re.U)
_DIGITS = re.compile(r"\d+")


def _plain(s: str) -> str:
    return _PLAIN.sub("", (s or "").lower())


def _same_chapter(head: str, current: str) -> bool:
    """Is *head* the chapter we are already in, reprinted as a running head?

    Running heads routinely drop the chapter number ("REAL NUMBERS 1" at the
    opening, "REAL NUMBERS" on every page after), so the comparison ignores
    digits. Without this every page of a book starts a new chapter.
    """
    if not current:
        return False
    a = _DIGITS.sub("", _plain(head))
    b = _DIGITS.sub("", _plain(current))
    return bool(a) and a == b


def _heading_number(head: str) -> str:
    """The number a heading declares, from either end.

    ``1.1 Introduction`` gives ``1.1``; ``REAL NUMBERS 1`` gives ``1`` — both
    forms occur in this corpus, in different publishers' books.
    """
    folded = fold_digits(head)
    m = _LEAD_NO.match(folded)
    if m:
        return m.group(1)
    m = _TRAIL_NO.search(folded)
    return m.group(1) if m else ""


def ingest_report(con) -> dict:
    """What the source layer currently holds, for the admin screen."""
    repo = CorpusRepo(con)
    c = repo.counts()
    c["by_board"] = repo.all(
        "SELECT COALESCE(NULLIF(board_name,''), board) AS board, COUNT(*) AS books,"
        "       SUM(n_segments) AS segments FROM setu_book"
        " GROUP BY board, board_name ORDER BY board")
    c["by_kind"] = repo.all(
        "SELECT kind, COUNT(*) AS n FROM setu_segment GROUP BY kind ORDER BY n DESC")
    c["fts"] = bool(con.execute(
        "SELECT name FROM sqlite_master WHERE name='setu_seg_fts'").fetchone())
    return c
