-- Setu — the bilingual annotation workspace.
--
-- Every object here is prefixed `setu_` and created with IF NOT EXISTS. This
-- file never writes to, alters or drops anything that existed before it: the
-- eight original Tulana tables (documents, projects, clips, pairs, labels,
-- pair_labels, exports, audit) and the parsed-layout tables (pl_books,
-- pl_pages, pl_blocks) are read-only as far as Setu is concerned.
--
-- The storage is deliberately split into five kinds of thing, because they have
-- five different lifetimes:
--
--   immutable source   setu_book, setu_segment            written once at ingest
--   editable state     setu_row, setu_text                changes constantly
--   version history    setu_rev                           append-only, forever
--   session state      setu_session, setu_lock            expires
--   artifacts          setu_export                        regenerable
--
-- Column types are declared for documentation; SQLite's affinity rules do the
-- rest. Every foreign key is declared so `PRAGMA foreign_keys=ON` actually
-- protects the graph.

CREATE TABLE IF NOT EXISTS setu_meta (
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

-- ── immutable source ──────────────────────────────────────────────────────

-- One row per *canonical* parsed book. Duplicate parses of the same book (the
-- corpus ships 31 of them under two different folders) share a dedup_key; one
-- is elected canonical and the others recorded as aliases in setu_book_alias.
CREATE TABLE IF NOT EXISTS setu_book (
  book_key   TEXT PRIMARY KEY,
  pl_book_id INTEGER NOT NULL,          -- the elected pl_books row
  dedup_key  TEXT NOT NULL,
  book       TEXT NOT NULL,             -- parser's short name, e.g. MH_EN_9_1
  relpath    TEXT NOT NULL,
  board      TEXT DEFAULT '',
  board_name TEXT DEFAULT '',
  class      INTEGER,
  subject    TEXT DEFAULT '',
  language   TEXT DEFAULT '',
  script     TEXT DEFAULT '',
  volume     TEXT DEFAULT '',
  title      TEXT DEFAULT '',
  num_pages  INTEGER DEFAULT 0,
  n_blocks   INTEGER DEFAULT 0,
  n_segments INTEGER DEFAULT 0,
  pdf_present INTEGER DEFAULT 0,
  ingested_at REAL
);
CREATE INDEX IF NOT EXISTS ix_setu_book_cascade
  ON setu_book(board, class, subject, language);
CREATE INDEX IF NOT EXISTS ix_setu_book_dedup ON setu_book(dedup_key);

CREATE TABLE IF NOT EXISTS setu_book_alias (
  pl_book_id INTEGER PRIMARY KEY,
  book_key   TEXT NOT NULL REFERENCES setu_book(book_key) ON DELETE CASCADE,
  relpath    TEXT NOT NULL
);

-- A segment is the unit an annotator works on: one paragraph, one worked
-- example, one exercise, one theorem. `source_text` is what the parser
-- extracted and is NEVER updated after ingest — an annotator's edits live in
-- setu_text. That is the whole reason the two tables are separate.
CREATE TABLE IF NOT EXISTS setu_segment (
  sid         TEXT PRIMARY KEY,
  book_key    TEXT NOT NULL REFERENCES setu_book(book_key) ON DELETE CASCADE,
  seq         INTEGER NOT NULL,         -- 0-based position in the book
  page        INTEGER NOT NULL,         -- 0-based, as the parser emits
  ord_start   INTEGER NOT NULL,         -- reading order of the first block
  ord_end     INTEGER NOT NULL,         -- ... and the last (inclusive)
  kind        TEXT NOT NULL,            -- paragraph | example | exercise | ...
  label       TEXT DEFAULT '',          -- the parser's own label
  block_type  TEXT DEFAULT '',
  chapter     TEXT DEFAULT '',          -- nearest preceding chapter title
  chapter_no  TEXT DEFAULT '',
  section     TEXT DEFAULT '',          -- nearest preceding section title
  section_no  TEXT DEFAULT '',          -- e.g. "1.2", when the text declares one
  item_no     TEXT DEFAULT '',          -- e.g. "3" from "Example 3"
  depth       INTEGER DEFAULT 0,
  source_text TEXT NOT NULL DEFAULT '', -- immutable original extraction
  n_chars     INTEGER DEFAULT 0,
  has_math    INTEGER DEFAULT 0,
  has_table   INTEGER DEFAULT 0,
  block_ids   TEXT DEFAULT '[]',        -- JSON array of pl_blocks.id, provenance
  fx0 REAL, fy0 REAL, fx1 REAL, fy1 REAL,  -- fractional box, for PDF audit
  anchor_math TEXT DEFAULT '[]',        -- JSON: normalised TeX fingerprints
  anchor_num  TEXT DEFAULT '[]'         -- JSON: structural numbers found
);
CREATE INDEX IF NOT EXISTS ix_setu_seg_book ON setu_segment(book_key, seq);
CREATE INDEX IF NOT EXISTS ix_setu_seg_page ON setu_segment(book_key, page, ord_start);
CREATE INDEX IF NOT EXISTS ix_setu_seg_chapter ON setu_segment(book_key, chapter_no, section_no);
CREATE INDEX IF NOT EXISTS ix_setu_seg_kind ON setu_segment(book_key, kind);

-- ── projects: a source book and a target book, opened together ────────────

CREATE TABLE IF NOT EXISTS setu_project (
  pid         TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  src_book    TEXT NOT NULL REFERENCES setu_book(book_key),
  tgt_book    TEXT NOT NULL REFERENCES setu_book(book_key),
  src_language TEXT DEFAULT '',
  tgt_language TEXT DEFAULT '',
  board       TEXT DEFAULT '',
  class       INTEGER,
  subject     TEXT DEFAULT '',
  created_at  REAL,
  created_by  TEXT DEFAULT '',
  built_at    REAL,                     -- when rows were last (re)generated
  n_rows      INTEGER DEFAULT 0,
  notes       TEXT DEFAULT '',
  UNIQUE(src_book, tgt_book)
);

-- One bilingual row. This is what the annotator sees: English on the left,
-- the target language on the right, a status, a note.
CREATE TABLE IF NOT EXISTS setu_row (
  rid        TEXT PRIMARY KEY,
  pid        TEXT NOT NULL REFERENCES setu_project(pid) ON DELETE CASCADE,
  seq        INTEGER NOT NULL,
  src_sid    TEXT REFERENCES setu_segment(sid),   -- NULL = nothing on the left
  tgt_sid    TEXT REFERENCES setu_segment(sid),   -- NULL = nothing on the right
  status     TEXT NOT NULL DEFAULT 'pending',
  origin     TEXT NOT NULL DEFAULT 'suggested',   -- suggested | manual | imported
  confidence REAL DEFAULT 0,
  note       TEXT DEFAULT '',
  chapter    TEXT DEFAULT '',
  chapter_no TEXT DEFAULT '',
  section    TEXT DEFAULT '',
  section_no TEXT DEFAULT '',
  kind       TEXT DEFAULT '',
  src_page   INTEGER,
  tgt_page   INTEGER,
  edited     INTEGER DEFAULT 0,          -- 1 once either side's text diverges
  created_at REAL,
  updated_at REAL,
  updated_by TEXT DEFAULT '',
  UNIQUE(pid, seq)
);
CREATE INDEX IF NOT EXISTS ix_setu_row_nav ON setu_row(pid, seq);
CREATE INDEX IF NOT EXISTS ix_setu_row_status ON setu_row(pid, status, seq);
CREATE INDEX IF NOT EXISTS ix_setu_row_chapter ON setu_row(pid, chapter_no, section_no, seq);
CREATE INDEX IF NOT EXISTS ix_setu_row_src ON setu_row(src_sid);
CREATE INDEX IF NOT EXISTS ix_setu_row_tgt ON setu_row(tgt_sid);

-- ── editable annotation state ─────────────────────────────────────────────

-- Present only once a side has actually been edited. Absent means "the text is
-- still exactly what the parser extracted", which is both the common case and
-- the cheapest thing to store.
CREATE TABLE IF NOT EXISTS setu_text (
  rid        TEXT NOT NULL REFERENCES setu_row(rid) ON DELETE CASCADE,
  side       TEXT NOT NULL CHECK(side IN ('src','tgt')),
  text       TEXT NOT NULL DEFAULT '',
  rev        INTEGER NOT NULL DEFAULT 1,
  updated_at REAL,
  updated_by TEXT DEFAULT '',
  PRIMARY KEY (rid, side)
);

-- ── version history: append-only, never pruned automatically ──────────────

CREATE TABLE IF NOT EXISTS setu_rev (
  id         INTEGER PRIMARY KEY,
  rid        TEXT NOT NULL,
  side       TEXT NOT NULL,
  rev        INTEGER NOT NULL,
  text       TEXT NOT NULL DEFAULT '',
  actor      TEXT DEFAULT '',
  session    TEXT DEFAULT '',
  reason     TEXT DEFAULT 'edit',
  ts         REAL,
  UNIQUE(rid, side, rev)
);
CREATE INDEX IF NOT EXISTS ix_setu_rev_row ON setu_rev(rid, side, rev DESC);

CREATE TABLE IF NOT EXISTS setu_status_rev (
  id      INTEGER PRIMARY KEY,
  rid     TEXT NOT NULL,
  status  TEXT NOT NULL,
  note    TEXT DEFAULT '',
  actor   TEXT DEFAULT '',
  session TEXT DEFAULT '',
  ts      REAL
);
CREATE INDEX IF NOT EXISTS ix_setu_status_rev ON setu_status_rev(rid, ts DESC);

-- ── sessions and soft locks ───────────────────────────────────────────────

-- One row per browser tab. Two tabs of the same person are two sessions, which
-- is what makes "this row is also open in another tab" detectable.
CREATE TABLE IF NOT EXISTS setu_session (
  sess       TEXT PRIMARY KEY,
  annotator  TEXT DEFAULT '',
  pid        TEXT DEFAULT '',
  started_at REAL,
  seen_at    REAL,
  agent      TEXT DEFAULT '',
  n_saves    INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_setu_session_seen ON setu_session(seen_at);

-- Advisory only: it tells another tab that somebody is here, it does not
-- prevent a write. Authority over concurrent writes belongs to the revision
-- check in setu_text, which cannot be bypassed.
CREATE TABLE IF NOT EXISTS setu_lock (
  rid        TEXT PRIMARY KEY,
  sess       TEXT NOT NULL,
  annotator  TEXT DEFAULT '',
  acquired_at REAL,
  expires_at REAL
);
CREATE INDEX IF NOT EXISTS ix_setu_lock_exp ON setu_lock(expires_at);

-- ── observability ─────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS setu_event (
  id      INTEGER PRIMARY KEY,
  ts      REAL,
  actor   TEXT DEFAULT '',
  session TEXT DEFAULT '',
  action  TEXT NOT NULL,
  target  TEXT DEFAULT '',
  detail  TEXT DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS ix_setu_event_ts ON setu_event(ts DESC);
CREATE INDEX IF NOT EXISTS ix_setu_event_target ON setu_event(target, ts DESC);

-- ── export artifacts ──────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS setu_export (
  xid        TEXT PRIMARY KEY,
  pid        TEXT DEFAULT '',
  fmt        TEXT NOT NULL,
  filename   TEXT NOT NULL,
  path       TEXT NOT NULL,
  n_rows     INTEGER DEFAULT 0,
  n_bytes    INTEGER DEFAULT 0,
  filters    TEXT DEFAULT '{}',
  actor      TEXT DEFAULT '',
  created_at REAL
);
CREATE INDEX IF NOT EXISTS ix_setu_export_pid ON setu_export(pid, created_at DESC);
