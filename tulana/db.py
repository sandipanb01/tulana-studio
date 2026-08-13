"""Tulana Studio — schema and connection handling.

Everything an annotator produces lives here: which textbooks were opened, every
clipped region, and how regions were paired across languages. Clippings are
append-only in the sense that deleting one is an explicit act; nothing is ever
silently overwritten.
"""
import json
import sqlite3
import time
from contextlib import contextmanager

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY,
  path TEXT UNIQUE NOT NULL,        -- relative to the data folder
  board TEXT, class INTEGER, subject TEXT,
  language TEXT, script TEXT, volume TEXT,
  title TEXT,                       -- human-readable, shown in the interface
  pages INTEGER, checksum TEXT, added_at REAL
);

CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,               -- e.g. NCERT_class_9_math
  board TEXT, class INTEGER, subject TEXT,
  src_doc INTEGER REFERENCES documents(id),
  tgt_doc INTEGER REFERENCES documents(id),
  src_language TEXT, tgt_language TEXT,
  created_at REAL, notes TEXT DEFAULT '',
  UNIQUE(src_doc, tgt_doc)
);

-- One clipped region. `bbox` is in PDF points on that page, so a clipping can
-- be re-rendered at any resolution and stays correct if the viewer changes.
CREATE TABLE IF NOT EXISTS clips (
  id INTEGER PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  pair_id INTEGER,                  -- clips sharing a pair_id are parallel
  side TEXT CHECK(side IN ('src','tgt')),
  doc_id INTEGER REFERENCES documents(id),
  page INTEGER NOT NULL,            -- 1-based
  x0 REAL, y0 REAL, x1 REAL, y1 REAL,
  image_path TEXT,                  -- PNG, relative to the crops folder
  text TEXT DEFAULT '',             -- text extracted from the region, if any
  label TEXT DEFAULT '',            -- annotator's label for the chunk
  chapter_hint TEXT DEFAULT '',
  excluded INTEGER DEFAULT 0,       -- flagged as an excluded topic
  annotator TEXT DEFAULT '',
  created_at REAL
);
CREATE INDEX IF NOT EXISTS ix_clip_project ON clips(project_id, pair_id);
CREATE INDEX IF NOT EXISTS ix_clip_pair ON clips(pair_id);

CREATE TABLE IF NOT EXISTS pairs (
  id INTEGER PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  seq INTEGER,                      -- 1,2,3… as exported (eng_1, hindi_1)
  label TEXT DEFAULT '',
  note TEXT DEFAULT '',
  excluded INTEGER DEFAULT 0,
  reason TEXT DEFAULT '',
  annotator TEXT DEFAULT '',
  created_at REAL
);
CREATE INDEX IF NOT EXISTS ix_pair_project ON pairs(project_id, seq);

-- doccano-style label set: named categories with a colour and a one-key
-- shortcut, defined per project so different corpora can label differently.
CREATE TABLE IF NOT EXISTS labels (
  id INTEGER PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  color TEXT DEFAULT '#0e7a72',
  shortcut TEXT DEFAULT '',
  ord INTEGER DEFAULT 0,
  UNIQUE(project_id, name)
);
CREATE INDEX IF NOT EXISTS ix_label_project ON labels(project_id, ord);

CREATE TABLE IF NOT EXISTS pair_labels (
  pair_id INTEGER REFERENCES pairs(id) ON DELETE CASCADE,
  label_id INTEGER REFERENCES labels(id) ON DELETE CASCADE,
  PRIMARY KEY (pair_id, label_id)
);

CREATE TABLE IF NOT EXISTS exports (
  id INTEGER PRIMARY KEY, project_id INTEGER, name TEXT, path TEXT,
  n_pairs INTEGER, formats TEXT, created_at REAL
);

CREATE TABLE IF NOT EXISTS audit (
  id INTEGER PRIMARY KEY, ts REAL, actor TEXT, action TEXT,
  target TEXT, detail TEXT
);
"""


def connect():
    con = sqlite3.connect(config.DB_PATH, timeout=30, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript(SCHEMA)
    return con


@contextmanager
def tx():
    con = connect()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def log(con, actor, action, target="", detail=None):
    con.execute("INSERT INTO audit(ts, actor, action, target, detail)"
                " VALUES(?,?,?,?,?)",
                (time.time(), actor or "anonymous", action, str(target),
                 json.dumps(detail or {}, ensure_ascii=False)))
