"""Setu — connections, schema management and the repository base.

Three things live here and nothing else:

1. **Connections.** Setu opens the same SQLite file as the rest of Tulana but
   with its own durability settings. ``synchronous`` is a *connection-level*
   pragma, so asking for ``FULL`` here makes Setu's writes survive a power cut
   without touching ``db.py`` or the data anybody else already stored. That
   matters: an autosave that returns "saved" and then evaporates is worse than
   no autosave at all.

2. **Schema.** Applied additively from ``schema.sql``, then a numbered
   migration list for anything that has to change later. Migrations only ever
   add; there is no ``DROP`` and no ``ALTER ... DROP COLUMN`` anywhere in this
   package, and a test asserts that.

3. **The repository base.** A thin object that holds a connection and gives the
   service layer typed helpers. Swapping SQLite for PostgreSQL later means
   writing a second subclass here; it does not mean touching the services, the
   API or the interface, because none of them build SQL.

Nothing in this module knows what a segment or a status is. That is deliberate.
"""
from __future__ import annotations

import json
import logging
import os
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

import config

log = logging.getLogger("setu.store")

HERE = Path(__file__).parent.resolve()
SCHEMA_PATH = HERE / "schema.sql"

SCHEMA_VERSION = 3

#: How long a connection waits for a writer to finish before giving up. The
#: worst honest case measured on this corpus is a project build, which holds
#: the write lock for a few seconds on a large book.
BUSY_TIMEOUT_MS = int(os.environ.get("SETU_BUSY_TIMEOUT_MS", "30000"))

#: ``FULL`` fsyncs the WAL on every commit. It costs roughly a millisecond per
#: save on an SSD and it is the difference between "autosaved" being true and
#: being a hope.
SYNCHRONOUS = os.environ.get("SETU_SYNCHRONOUS", "FULL").upper()
if SYNCHRONOUS not in {"OFF", "NORMAL", "FULL", "EXTRA"}:
    SYNCHRONOUS = "FULL"

_schema_lock = threading.Lock()
_schema_ready: set[str] = set()


class StoreError(RuntimeError):
    """Something went wrong that the caller can do nothing about."""


class Conflict(RuntimeError):
    """A write lost a race and must not be applied blindly.

    Carries enough for the interface to show the person both versions, which is
    the only honest way to resolve it.
    """

    def __init__(self, message: str, *, current: Any = None, attempted: Any = None,
                 rev: int = 0):
        super().__init__(message)
        self.current = current
        self.attempted = attempted
        self.rev = rev

    def payload(self) -> dict:
        return {"error": "conflict", "message": str(self),
                "current": self.current, "attempted": self.attempted,
                "rev": self.rev}


class NotFound(LookupError):
    """A referenced object does not exist."""


class Invalid(ValueError):
    """Input failed validation at the edge, before it reached storage."""


# ── connections ────────────────────────────────────────────────────────────

def _db_path() -> Path:
    return Path(config.DB_PATH)


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    """Open a connection configured for durable, concurrent annotation work."""
    target = Path(path) if path else _db_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(target), timeout=BUSY_TIMEOUT_MS / 1000.0,
                          check_same_thread=False, isolation_level=None)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute(f"PRAGMA synchronous={SYNCHRONOUS}")
    con.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS}")
    con.execute("PRAGMA foreign_keys=ON")
    # Keeps the temp store off disk for the sort-heavy navigation queries.
    con.execute("PRAGMA temp_store=MEMORY")
    ensure_schema(con, str(target))
    return con


def ensure_schema(con: sqlite3.Connection, key: str = "") -> None:
    """Create Setu's tables if they are not there, then run migrations.

    Additive only. This never touches a table it did not create.
    """
    key = key or str(_db_path())
    if key in _schema_ready:
        return
    with _schema_lock:
        if key in _schema_ready:
            return
        ddl = SCHEMA_PATH.read_text(encoding="utf-8")
        con.executescript(ddl)
        # Unconditionally, not only during a migration. `_ensure_fts` is the
        # only thing that sets FTS_AVAILABLE, and if it is skipped here it
        # fires later — from inside a caller's transaction, where creating the
        # table would end that transaction underneath them.
        _ensure_fts(con)
        _migrate(con)
        _schema_ready.add(key)


def _migrate(con: sqlite3.Connection) -> None:
    """Bring an older Setu database up to :data:`SCHEMA_VERSION`.

    Each step is additive and idempotent, so running it twice is harmless and
    running it against a fresh database created from ``schema.sql`` is a no-op.
    """
    row = con.execute("SELECT value FROM setu_meta WHERE key='schema_version'").fetchone()
    have = int(row["value"]) if row else 0
    if have >= SCHEMA_VERSION:
        return

    if have < 2:
        _ensure_fts(con)
    if have < 3:
        # Columns added after the first release. `_add_column` is a no-op when
        # the column is already declared, which it will be on a fresh install.
        _add_column(con, "setu_row", "reviewed_by", "TEXT DEFAULT ''")
        _add_column(con, "setu_row", "reviewed_at", "REAL")

    con.execute("INSERT INTO setu_meta(key, value) VALUES('schema_version', ?)"
                " ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (str(SCHEMA_VERSION),))
    con.commit()


def _add_column(con: sqlite3.Connection, table: str, column: str, decl: str) -> None:
    have = {r["name"] for r in con.execute(f"PRAGMA table_info({table})")}
    if column not in have:
        con.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


# ── full-text search ───────────────────────────────────────────────────────

FTS_AVAILABLE: bool | None = None


def _ensure_fts(con: sqlite3.Connection) -> bool:
    """Create the FTS5 search index, if this SQLite build has FTS5.

    Search degrades to ``LIKE`` when it does not, which is slower but correct;
    the interface says which one is in use rather than silently being worse.
    """
    global FTS_AVAILABLE
    if FTS_AVAILABLE is not None:
        return FTS_AVAILABLE
    try:
        # `execute`, never `executescript`. executescript issues an implicit
        # COMMIT before it runs, so creating this table from inside a caller's
        # transaction would silently end that transaction and make its own
        # COMMIT fail with "cannot commit - no transaction is active". That is
        # not hypothetical: it happened on every run after the first, because
        # the migration that used to create this table is skipped once the
        # schema is already current.
        con.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS setu_seg_fts USING fts5("
            " sid UNINDEXED, book_key UNINDEXED, body,"
            " tokenize='unicode61 remove_diacritics 0')")
        FTS_AVAILABLE = True
    except sqlite3.OperationalError as exc:      # pragma: no cover - build-specific
        log.warning("FTS5 unavailable, search falls back to LIKE: %s", exc)
        FTS_AVAILABLE = False
    return FTS_AVAILABLE


def fts_ready(con: sqlite3.Connection) -> bool:
    return _ensure_fts(con)


# ── transactions ───────────────────────────────────────────────────────────

@contextmanager
def tx(path: str | Path | None = None) -> Iterator[sqlite3.Connection]:
    """A short, durable write transaction.

    ``IMMEDIATE`` takes the write lock at ``BEGIN`` rather than at the first
    write, which turns a mid-transaction "database is locked" into a clean wait
    at the start where the busy timeout can do its job.
    """
    con = connect(path)
    try:
        con.execute("BEGIN IMMEDIATE")
        yield con
        con.execute("COMMIT")
    except Exception:
        try:
            con.execute("ROLLBACK")
        except sqlite3.Error:                    # pragma: no cover - already closed
            pass
        raise
    finally:
        con.close()


@contextmanager
def ro(path: str | Path | None = None) -> Iterator[sqlite3.Connection]:
    """A read-only connection. Takes no write lock, so it never blocks a save."""
    con = connect(path)
    try:
        yield con
    finally:
        con.close()


# ── repository base ────────────────────────────────────────────────────────

class Repository:
    """Holds a connection and hands out rows as plain dicts.

    The service layer talks to subclasses of this and never sees a cursor, a
    ``sqlite3.Row`` or a piece of SQL. That is what makes the PostgreSQL port a
    matter of writing a sibling class rather than rewriting the application.
    """

    def __init__(self, con: sqlite3.Connection):
        self.con = con

    # -- helpers ----------------------------------------------------------
    @staticmethod
    def _dict(row: sqlite3.Row | None) -> dict | None:
        return dict(row) if row is not None else None

    def one(self, sql: str, params: Sequence = ()) -> dict | None:
        return self._dict(self.con.execute(sql, params).fetchone())

    def all(self, sql: str, params: Sequence = ()) -> list[dict]:
        return [dict(r) for r in self.con.execute(sql, params)]

    def scalar(self, sql: str, params: Sequence = (), default: Any = None) -> Any:
        row = self.con.execute(sql, params).fetchone()
        return default if row is None else row[0]

    def run(self, sql: str, params: Sequence = ()) -> sqlite3.Cursor:
        return self.con.execute(sql, params)

    def runmany(self, sql: str, rows: Iterable[Sequence]) -> None:
        self.con.executemany(sql, rows)

    # -- observability ----------------------------------------------------
    def event(self, action: str, target: str = "", detail: dict | None = None,
              actor: str = "", session: str = "") -> None:
        """Append to Setu's own audit log.

        Detail is whitelisted by the caller — this method does not decide what
        is safe to record, but it does refuse to store anything that is not
        JSON-serialisable rather than crashing the write that triggered it.
        """
        try:
            blob = json.dumps(detail or {}, ensure_ascii=False, default=str)
        except (TypeError, ValueError):          # pragma: no cover - defensive
            blob = "{}"
        if len(blob) > 4000:
            blob = blob[:3990] + '..."}'
        self.con.execute(
            "INSERT INTO setu_event(ts, actor, session, action, target, detail)"
            " VALUES(?,?,?,?,?,?)",
            (time.time(), actor[:120], session[:64], action[:64], str(target)[:128], blob))


def paginate(limit: Any, offset: Any, *, default: int = 50, cap: int = 500) -> tuple[int, int]:
    """Clamp caller-supplied paging into something the database can serve.

    A missing, negative or absurd limit becomes a sane one rather than an error,
    because paging parameters arrive from a URL and a person typing in a URL
    should not be able to ask for the whole corpus in one response.
    """
    try:
        lim = int(limit)
    except (TypeError, ValueError, OverflowError):
        # OverflowError is float('inf'), which int() refuses. It arrives from a
        # query string as readily as any other number.
        lim = default
    try:
        off = int(offset)
    except (TypeError, ValueError, OverflowError):
        off = 0
    return max(1, min(lim, cap)), max(0, off)
