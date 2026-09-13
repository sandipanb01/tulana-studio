"""Saved pairs — aligned selections of parsed blocks, across pages.

What an annotator produces here is a **pair**: a set of blocks on the English
side and a set on the target side that say the same thing. Either set may span
several pages, because a worked example that fits on one page in English often
runs onto the next in Marathi — the translation is longer, the page reflows, and
a selection confined to one page could not express the alignment at all.

**Additive.** Two new tables, created with `CREATE TABLE IF NOT EXISTS`. Nothing
here writes to `documents`, `projects`, `clips`, `pairs`, `labels`,
`pair_labels`, `exports` or `audit` — the earlier PDF-clipping work stays in the
database, untouched and still exportable.

Three things this module is careful about:

**Nothing is lost.** A selection is written as a draft while it is being made,
not only when it is saved, so closing a tab costs nothing. See `save_draft`.

**A pair keeps its own copy of the text.** Blocks are referenced by id *and*
their text is denormalised into the pair. Re-running the parser renumbers
blocks; a corpus reload must not silently change what an approved pair says.

**Export is not one format.** A parallel corpus goes to different places — a
training pipeline wants JSONL, a translator wants TMX, a reviewer wants a
spreadsheet, a paper wants a table. All of them come from the same rows.
"""
from __future__ import annotations

import csv
import io
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

import blocks as blocks_mod
import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS bp_pairs (
  id INTEGER PRIMARY KEY,
  seq INTEGER DEFAULT 0,
  src_book_id INTEGER, tgt_book_id INTEGER,
  src_book TEXT, tgt_book TEXT,
  board TEXT, class INTEGER, subject TEXT,
  src_language TEXT, tgt_language TEXT,
  src_script TEXT, tgt_script TEXT,
  src_pages TEXT DEFAULT '[]',        -- the pages each side touches
  tgt_pages TEXT DEFAULT '[]',
  src_text TEXT DEFAULT '',           -- denormalised: a pair keeps its own copy
  tgt_text TEXT DEFAULT '',
  src_labels TEXT DEFAULT '[]',
  tgt_labels TEXT DEFAULT '[]',
  label TEXT DEFAULT '',              -- what the annotator calls this passage
  note TEXT DEFAULT '',
  status TEXT DEFAULT 'draft',        -- draft | saved | approved | excluded
  annotator TEXT DEFAULT '',
  created_at REAL, updated_at REAL
);
CREATE INDEX IF NOT EXISTS ix_bp_pairs_books ON bp_pairs(src_book_id, tgt_book_id);
CREATE INDEX IF NOT EXISTS ix_bp_pairs_status ON bp_pairs(status);

CREATE TABLE IF NOT EXISTS bp_pair_blocks (
  id INTEGER PRIMARY KEY,
  pair_id INTEGER NOT NULL,
  side TEXT NOT NULL,                 -- 'src' or 'tgt'
  block_id INTEGER NOT NULL,
  page INTEGER, ord INTEGER,
  label TEXT, type TEXT,
  fx0 REAL, fy0 REAL, fx1 REAL, fy1 REAL,
  text TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS ix_bp_pb ON bp_pair_blocks(pair_id, side, page, ord);
"""

DRAFT_STATUS = "draft"
STATUSES = ("draft", "saved", "approved", "excluded")


def ensure_schema(con):
    con.executescript(SCHEMA)
    con.commit()


# ── writing ────────────────────────────────────────────────────────────────
def _gather(con, block_ids: list) -> dict:
    """Everything a pair needs to remember about one side's blocks.

    Ordered by page then reading order, so a selection made by clicking around
    the page still reads the way the page does."""
    if not block_ids:
        return {"blocks": [], "text": "", "pages": [], "labels": []}
    qs = ",".join("?" for _ in dict.fromkeys(block_ids))
    rows = [dict(r) for r in con.execute(
        f"""SELECT b.id, b.ord, b.label, b.type, b.fx0, b.fy0, b.fx1, b.fy1,
                   b.text, p.page
            FROM pl_blocks b JOIN pl_pages p ON p.id = b.page_id
            WHERE b.id IN ({qs})
            ORDER BY p.page, b.ord, b.id""", list(dict.fromkeys(block_ids)))]
    text = "\n\n".join((r["text"] or "").strip() for r in rows
                       if (r["text"] or "").strip())
    return {"blocks": rows, "text": text,
            "pages": sorted({r["page"] for r in rows}),
            "labels": sorted({r["label"] for r in rows if r["label"]})}


def save_pair(con, src_book_id: int, tgt_book_id: int, src_block_ids: list,
              tgt_block_ids: list, label: str = "", note: str = "",
              status: str = "saved", annotator: str = "",
              pair_id: int = None) -> dict:
    """Create or update one aligned selection.

    Whole-selection replace rather than incremental edits: an annotator adjusts
    a pair by re-selecting, and a half-applied change would be worse than a
    replaced one."""
    ensure_schema(con)
    if status not in STATUSES:
        raise ValueError(f"status must be one of {', '.join(STATUSES)}")
    if not src_block_ids and not tgt_block_ids:
        raise ValueError("A pair needs at least one block on one side")

    src = _gather(con, src_block_ids)
    tgt = _gather(con, tgt_block_ids)
    sb = blocks_mod.book(con, src_book_id) if src_book_id else {}
    tb = blocks_mod.book(con, tgt_book_id) if tgt_book_id else {}
    now = time.time()

    if pair_id:
        row = con.execute("SELECT id FROM bp_pairs WHERE id=?", (pair_id,)).fetchone()
        if not row:
            raise ValueError("Unknown pair")
        con.execute("""UPDATE bp_pairs SET src_book_id=?, tgt_book_id=?, src_book=?,
            tgt_book=?, board=?, class=?, subject=?, src_language=?, tgt_language=?,
            src_script=?, tgt_script=?, src_pages=?, tgt_pages=?, src_text=?,
            tgt_text=?, src_labels=?, tgt_labels=?, label=?, note=?, status=?,
            annotator=?, updated_at=? WHERE id=?""",
            (src_book_id, tgt_book_id, sb.get("book"), tb.get("book"),
             sb.get("board"), sb.get("class"), sb.get("subject"),
             sb.get("language"), tb.get("language"), sb.get("script"),
             tb.get("script"), json.dumps(src["pages"]), json.dumps(tgt["pages"]),
             src["text"], tgt["text"], json.dumps(src["labels"]),
             json.dumps(tgt["labels"]), label.strip(), note.strip(), status,
             annotator.strip(), now, pair_id))
        con.execute("DELETE FROM bp_pair_blocks WHERE pair_id=?", (pair_id,))
    else:
        seq = con.execute("""SELECT COALESCE(MAX(seq),0)+1 FROM bp_pairs
                             WHERE src_book_id=? AND tgt_book_id=?""",
                          (src_book_id, tgt_book_id)).fetchone()[0]
        pair_id = con.execute("""INSERT INTO bp_pairs(seq, src_book_id, tgt_book_id,
            src_book, tgt_book, board, class, subject, src_language, tgt_language,
            src_script, tgt_script, src_pages, tgt_pages, src_text, tgt_text,
            src_labels, tgt_labels, label, note, status, annotator, created_at,
            updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (seq, src_book_id, tgt_book_id, sb.get("book"), tb.get("book"),
             sb.get("board"), sb.get("class"), sb.get("subject"),
             sb.get("language"), tb.get("language"), sb.get("script"),
             tb.get("script"), json.dumps(src["pages"]), json.dumps(tgt["pages"]),
             src["text"], tgt["text"], json.dumps(src["labels"]),
             json.dumps(tgt["labels"]), label.strip(), note.strip(), status,
             annotator.strip(), now, now)).lastrowid

    rows = []
    for side, gathered in (("src", src), ("tgt", tgt)):
        for b in gathered["blocks"]:
            rows.append((pair_id, side, b["id"], b["page"], b["ord"], b["label"],
                         b["type"], b["fx0"], b["fy0"], b["fx1"], b["fy1"],
                         b["text"]))
    if rows:
        con.executemany("""INSERT INTO bp_pair_blocks(pair_id, side, block_id, page,
            ord, label, type, fx0, fy0, fx1, fy1, text)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    return get_pair(con, pair_id)


def save_draft(con, src_book_id: int, tgt_book_id: int, src_block_ids: list,
               tgt_block_ids: list, annotator: str = "") -> dict:
    """Keep the in-progress selection, without the annotator asking.

    One draft per book pair per annotator, replaced as they work. It exists so
    that a closed tab, a lost connection or a stray reload costs nothing; the
    moment they press Save it becomes an ordinary pair."""
    ensure_schema(con)
    if not src_block_ids and not tgt_block_ids:
        # an empty selection clears the draft rather than storing nothing
        row = con.execute("""SELECT id FROM bp_pairs WHERE status=? AND
                             src_book_id=? AND tgt_book_id=? AND annotator=?""",
                          (DRAFT_STATUS, src_book_id, tgt_book_id,
                           (annotator or "").strip())).fetchone()
        if row:
            delete_pair(con, row["id"])
        return {"draft": None}
    row = con.execute("""SELECT id FROM bp_pairs WHERE status=? AND src_book_id=?
                         AND tgt_book_id=? AND annotator=?""",
                      (DRAFT_STATUS, src_book_id, tgt_book_id,
                       (annotator or "").strip())).fetchone()
    return save_pair(con, src_book_id, tgt_book_id, src_block_ids, tgt_block_ids,
                     status=DRAFT_STATUS, annotator=annotator,
                     pair_id=row["id"] if row else None)


def resolve_current_ids(con, pair_id: int, side: str) -> list:
    """The block ids a saved pair refers to, as the corpus numbers them today.

    Re-running the parser renumbers every block, so the ids stored when a pair
    was saved can stop resolving. The pair also records each block's page and
    reading-order position, and those are properties of the document rather
    than of one import — so they are what a pair is matched on when its ids no
    longer exist. Without this, reopening a pair after a corpus reload would
    silently highlight nothing.
    """
    rows = [dict(r) for r in con.execute(
        """SELECT block_id, page, ord FROM bp_pair_blocks
           WHERE pair_id=? AND side=? ORDER BY page, ord""", (pair_id, side))]
    if not rows:
        return []
    book_col = "src_book_id" if side == "src" else "tgt_book_id"
    book = con.execute(f"SELECT {book_col} FROM bp_pairs WHERE id=?",
                       (pair_id,)).fetchone()
    book_id = book[0] if book else None
    out = []
    for r in rows:
        still = con.execute("SELECT 1 FROM pl_blocks WHERE id=?",
                            (r["block_id"],)).fetchone()
        if still:
            out.append(r["block_id"])
            continue
        if book_id is None:
            continue
        found = con.execute(
            """SELECT b.id FROM pl_blocks b JOIN pl_pages p ON p.id=b.page_id
               WHERE p.book_id=? AND p.page=? AND b.ord=?""",
            (book_id, r["page"], r["ord"])).fetchone()
        if found:
            out.append(found[0])
    return out


def get_pair(con, pair_id: int) -> dict:
    ensure_schema(con)
    r = con.execute("SELECT * FROM bp_pairs WHERE id=?", (pair_id,)).fetchone()
    if not r:
        raise ValueError("Unknown pair")
    d = dict(r)
    for k in ("src_pages", "tgt_pages", "src_labels", "tgt_labels"):
        d[k] = json.loads(d[k] or "[]")
    d["src_blocks"] = [dict(x) for x in con.execute(
        """SELECT * FROM bp_pair_blocks WHERE pair_id=? AND side='src'
           ORDER BY page, ord""", (pair_id,))]
    d["tgt_blocks"] = [dict(x) for x in con.execute(
        """SELECT * FROM bp_pair_blocks WHERE pair_id=? AND side='tgt'
           ORDER BY page, ord""", (pair_id,))]
    d["spans_pages"] = len(d["src_pages"]) > 1 or len(d["tgt_pages"]) > 1
    # what to re-select when this pair is reopened, valid against today's corpus
    d["src_block_ids"] = resolve_current_ids(con, pair_id, "src")
    d["tgt_block_ids"] = resolve_current_ids(con, pair_id, "tgt")
    d["resolves_cleanly"] = (len(d["src_block_ids"]) == len(d["src_blocks"]) and
                             len(d["tgt_block_ids"]) == len(d["tgt_blocks"]))
    return d


def list_pairs(con, src_book_id: int = None, tgt_book_id: int = None,
               status: str = None, board: str = None, language: str = None,
               search: str = None, include_drafts: bool = False,
               limit: int = 500, offset: int = 0) -> dict:
    ensure_schema(con)
    where, args = ["1=1"], []
    if src_book_id:
        where.append("src_book_id=?"); args.append(src_book_id)
    if tgt_book_id:
        where.append("tgt_book_id=?"); args.append(tgt_book_id)
    if status:
        where.append("status=?"); args.append(status)
    elif not include_drafts:
        where.append("status != ?"); args.append(DRAFT_STATUS)
    if board:
        where.append("board=?"); args.append(board)
    if language:
        where.append("tgt_language=?"); args.append(language)
    if search:
        where.append("(src_text LIKE ? OR tgt_text LIKE ? OR label LIKE ?)")
        args += [f"%{search}%"] * 3
    w = " AND ".join(where)
    total = con.execute(f"SELECT COUNT(*) FROM bp_pairs WHERE {w}", args).fetchone()[0]
    rows = [dict(r) for r in con.execute(
        f"""SELECT id, seq, src_book, tgt_book, board, class, subject,
                   src_language, tgt_language, src_pages, tgt_pages, label, note,
                   status, annotator, created_at, updated_at,
                   LENGTH(src_text) src_chars, LENGTH(tgt_text) tgt_chars,
                   substr(src_text,1,160) src_preview, substr(tgt_text,1,160) tgt_preview
            FROM bp_pairs WHERE {w} ORDER BY updated_at DESC LIMIT ? OFFSET ?""",
        args + [limit, offset])]
    for d in rows:
        d["src_pages"] = json.loads(d["src_pages"] or "[]")
        d["tgt_pages"] = json.loads(d["tgt_pages"] or "[]")
        d["spans_pages"] = len(d["src_pages"]) > 1 or len(d["tgt_pages"]) > 1
    return {"total": total, "pairs": rows, "limit": limit, "offset": offset}


def delete_pair(con, pair_id: int) -> dict:
    ensure_schema(con)
    con.execute("DELETE FROM bp_pair_blocks WHERE pair_id=?", (pair_id,))
    n = con.execute("DELETE FROM bp_pairs WHERE id=?", (pair_id,)).rowcount
    return {"deleted": n}


def set_status(con, pair_id: int, status: str, annotator: str = "") -> dict:
    ensure_schema(con)
    if status not in STATUSES:
        raise ValueError(f"status must be one of {', '.join(STATUSES)}")
    con.execute("UPDATE bp_pairs SET status=?, updated_at=? WHERE id=?",
                (status, time.time(), pair_id))
    return get_pair(con, pair_id)


def update_meta(con, pair_id: int, label: str = None, note: str = None) -> dict:
    ensure_schema(con)
    if label is not None:
        con.execute("UPDATE bp_pairs SET label=?, updated_at=? WHERE id=?",
                    (label.strip(), time.time(), pair_id))
    if note is not None:
        con.execute("UPDATE bp_pairs SET note=?, updated_at=? WHERE id=?",
                    (note.strip(), time.time(), pair_id))
    return get_pair(con, pair_id)


def stats(con) -> dict:
    ensure_schema(con)
    by_status = {r[0]: r[1] for r in con.execute(
        "SELECT status, COUNT(*) FROM bp_pairs GROUP BY status")}
    by_lang = [dict(r) for r in con.execute(
        """SELECT tgt_language language, COUNT(*) pairs,
                  SUM(LENGTH(src_text)) src_chars, SUM(LENGTH(tgt_text)) tgt_chars
           FROM bp_pairs WHERE status != 'draft' AND tgt_language IS NOT NULL
           GROUP BY tgt_language ORDER BY pairs DESC""")]
    by_board = [dict(r) for r in con.execute(
        """SELECT board, COUNT(*) pairs FROM bp_pairs
           WHERE status != 'draft' AND board IS NOT NULL
           GROUP BY board ORDER BY pairs DESC""")]
    spanning = con.execute(
        """SELECT COUNT(*) FROM bp_pairs WHERE status != 'draft'
           AND (json_array_length(src_pages) > 1 OR json_array_length(tgt_pages) > 1)"""
    ).fetchone()[0]
    return {"by_status": by_status, "by_language": by_lang, "by_board": by_board,
            "total": sum(by_status.values()),
            "usable": sum(v for k, v in by_status.items() if k != DRAFT_STATUS),
            "spanning_pages": spanning}


# ── export ─────────────────────────────────────────────────────────────────
FORMATS = {
    "jsonl": ("JSON Lines", "application/x-ndjson", "jsonl",
              "one pair per line — what a training pipeline reads"),
    "json": ("JSON", "application/json", "json",
             "a single document with a header describing the corpus"),
    "csv": ("CSV", "text/csv", "csv", "opens in Excel, Sheets or pandas"),
    "tsv": ("TSV", "text/tab-separated-values", "tsv",
            "tab separated — safer than CSV when the text contains commas"),
    "txt": ("Plain text", "text/plain", "txt",
            "source and target line by line, blank line between pairs"),
    "tmx": ("TMX", "application/xml", "tmx",
            "translation memory — opens in OmegaT, memoQ, Trados"),
    "xliff": ("XLIFF", "application/xml", "xlf",
              "the interchange format most CAT tools accept"),
    "markdown": ("Markdown", "text/markdown", "md",
                 "a readable table for a paper or a review"),
    "moses": ("Moses / fairseq", "text/plain", "zip",
              "two parallel files, one line per pair — classic MT training input"),
    "coco": ("COCO", "application/json", "json",
             "the blocks with their boxes, for training a layout model"),
    "huggingface": ("Hugging Face datasets", "application/x-ndjson", "jsonl",
                    "JSONL with a dataset card, ready to push to the Hub"),
}


def _rows_for_export(con, **filters) -> list:
    ensure_schema(con)
    where, args = ["status != ?"], [DRAFT_STATUS]
    if filters.get("status"):
        where, args = ["status=?"], [filters["status"]]
    if filters.get("board"):
        where.append("board=?"); args.append(filters["board"])
    if filters.get("language"):
        where.append("tgt_language=?"); args.append(filters["language"])
    if filters.get("cls"):
        where.append("class=?"); args.append(filters["cls"])
    if not filters.get("include_excluded"):
        where.append("status != 'excluded'")
    rows = [dict(r) for r in con.execute(
        f"SELECT * FROM bp_pairs WHERE {' AND '.join(where)} ORDER BY id", args)]
    for d in rows:
        for k in ("src_pages", "tgt_pages", "src_labels", "tgt_labels"):
            d[k] = json.loads(d[k] or "[]")
    return rows


def _flat(d: dict) -> dict:
    return {
        "id": d["id"], "board": d["board"], "class": d["class"],
        "subject": d["subject"], "source_language": d["src_language"],
        "target_language": d["tgt_language"], "source_script": d["src_script"],
        "target_script": d["tgt_script"], "source_book": d["src_book"],
        "target_book": d["tgt_book"],
        "source_pages": ",".join(str(p) for p in d["src_pages"]),
        "target_pages": ",".join(str(p) for p in d["tgt_pages"]),
        "block_types": ",".join(d["src_labels"]),
        "label": d["label"], "note": d["note"], "status": d["status"],
        "annotator": d["annotator"],
        "source_text": d["src_text"], "target_text": d["tgt_text"],
    }


def export(con, fmt: str, **filters) -> tuple:
    """Return (bytes, media_type, filename) in whichever format was asked for."""
    if fmt not in FORMATS:
        raise ValueError(f"Unknown format. Choose one of: {', '.join(FORMATS)}")
    rows = _rows_for_export(con, **filters)
    if not rows:
        raise ValueError("No pairs match that selection")
    name, media, ext, _ = FORMATS[fmt]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    fn = f"tulana_pairs_{stamp}.{ext}"
    header = {
        "corpus": "Tulana parallel corpus",
        "exported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pairs": len(rows),
        "languages": sorted({r["tgt_language"] for r in rows if r["tgt_language"]}),
        "boards": sorted({r["board"] for r in rows if r["board"]}),
        "note": "source_text and target_text are the text the parser read inside "
                "the selected blocks, joined in reading order across pages.",
    }

    if fmt == "jsonl":
        body = "\n".join(json.dumps(_flat(r), ensure_ascii=False) for r in rows)
    elif fmt == "huggingface":
        body = "\n".join(json.dumps(
            {"translation": {r["src_language"] or "en": r["src_text"],
                             r["tgt_language"] or "xx": r["tgt_text"]},
             "board": r["board"], "class": r["class"], "subject": r["subject"],
             "block_types": r["src_labels"], "id": r["id"]},
            ensure_ascii=False) for r in rows)
    elif fmt == "json":
        body = json.dumps({"header": header, "pairs": [_flat(r) for r in rows]},
                          ensure_ascii=False, indent=1)
    elif fmt in ("csv", "tsv"):
        sio = io.StringIO()
        cols = list(_flat(rows[0]))
        w = csv.DictWriter(sio, fieldnames=cols,
                           delimiter="\t" if fmt == "tsv" else ",",
                           extrasaction="ignore")
        w.writeheader()
        for r in rows:
            f = _flat(r)
            if fmt == "tsv":
                # a literal tab or newline inside a cell would break the format
                for k in ("source_text", "target_text", "note"):
                    f[k] = (f[k] or "").replace("\t", " ").replace("\n", " ⏎ ")
            w.writerow(f)
        body = sio.getvalue()
    elif fmt == "txt":
        parts = []
        for r in rows:
            parts.append(f"# {r['board']} · Class {r['class']} · {r['subject']}"
                         f" · pair {r['id']}"
                         + (f" · {r['label']}" if r["label"] else ""))
            parts.append(f"[{r['src_language']}] {r['src_text']}")
            parts.append(f"[{r['tgt_language']}] {r['tgt_text']}")
            parts.append("")
        body = "\n".join(parts)
    elif fmt == "markdown":
        parts = [f"# Tulana parallel corpus", "",
                 f"{len(rows)} pairs · "
                 f"{', '.join(header['languages'])} · {', '.join(header['boards'])}",
                 ""]
        for r in rows:
            parts.append(f"### Pair {r['id']}"
                         + (f" — {r['label']}" if r["label"] else ""))
            parts.append(f"*{r['board']} · Class {r['class']} · {r['subject']} · "
                         f"pages {r['src_pages']} ↔ {r['tgt_pages']}*")
            parts.append("")
            parts.append(f"| {r['src_language']} | {r['tgt_language']} |")
            parts.append("|---|---|")
            s = (r["src_text"] or "").replace("|", "\\|").replace("\n", "<br>")
            t = (r["tgt_text"] or "").replace("|", "\\|").replace("\n", "<br>")
            parts.append(f"| {s} | {t} |")
            parts.append("")
        body = "\n".join(parts)
    elif fmt == "tmx":
        src_lang = (rows[0]["src_language"] or "en")[:2].lower()
        out = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<tmx version="1.4">',
               f'  <header creationtool="Tulana Studio" creationtoolversion="1.0"'
               f' segtype="paragraph" o-tmf="Tulana" adminlang="en"'
               f' srclang="{src_lang}" datatype="plaintext"/>',
               '  <body>']
        for r in rows:
            sl = (r["src_language"] or "en")[:2].lower()
            tl = (r["tgt_language"] or "xx")[:2].lower()
            out.append(f'    <tu tuid="{r["id"]}">')
            for prop, val in (("board", r["board"]), ("class", r["class"]),
                              ("subject", r["subject"])):
                if val:
                    out.append(f'      <prop type="{prop}">{xml_escape(str(val))}</prop>')
            out.append(f'      <tuv xml:lang="{sl}"><seg>'
                       f'{xml_escape(r["src_text"] or "")}</seg></tuv>')
            out.append(f'      <tuv xml:lang="{tl}"><seg>'
                       f'{xml_escape(r["tgt_text"] or "")}</seg></tuv>')
            out.append("    </tu>")
        out += ["  </body>", "</tmx>"]
        body = "\n".join(out)
    elif fmt == "xliff":
        sl = (rows[0]["src_language"] or "en")[:2].lower()
        tl = (rows[0]["tgt_language"] or "xx")[:2].lower()
        out = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">',
               f'  <file original="tulana" source-language="{sl}"'
               f' target-language="{tl}" datatype="plaintext">',
               "    <body>"]
        for r in rows:
            out.append(f'      <trans-unit id="{r["id"]}">')
            out.append(f'        <source>{xml_escape(r["src_text"] or "")}</source>')
            out.append(f'        <target>{xml_escape(r["tgt_text"] or "")}</target>')
            if r["note"]:
                out.append(f'        <note>{xml_escape(r["note"])}</note>')
            out.append("      </trans-unit>")
        out += ["    </body>", "  </file>", "</xliff>"]
        body = "\n".join(out)
    elif fmt == "coco":
        cats, ann, imgs, cid, aid = {}, [], [], 1, 1
        for r in rows:
            for side in ("src", "tgt"):
                bl = [dict(x) for x in con.execute(
                    """SELECT * FROM bp_pair_blocks WHERE pair_id=? AND side=?
                       ORDER BY page, ord""", (r["id"], side))]
                for b in bl:
                    key = b["label"] or "other"
                    if key not in cats:
                        cats[key] = cid; cid += 1
                    img_id = len(imgs) + 1
                    imgs.append({"id": img_id,
                                 "file_name": f"{r[side + '_book']}_p{b['page']:04d}.png",
                                 "book": r[side + "_book"], "page": b["page"],
                                 "language": r[side + "_language"]})
                    ann.append({"id": aid, "image_id": img_id,
                                "category_id": cats[key],
                                "bbox_normalised": [b["fx0"], b["fy0"],
                                                    b["fx1"] - b["fx0"],
                                                    b["fy1"] - b["fy0"]],
                                "pair_id": r["id"], "side": side,
                                "reading_order": b["ord"], "text": b["text"]})
                    aid += 1
        body = json.dumps({"info": header,
                           "categories": [{"id": v, "name": k} for k, v in cats.items()],
                           "images": imgs, "annotations": ann},
                          ensure_ascii=False, indent=1)
    elif fmt == "moses":
        import zipfile
        sl = (rows[0]["src_language"] or "en").lower()
        tl = (rows[0]["tgt_language"] or "xx").lower()
        buf = io.BytesIO()
        def one(text):
            """Collapse a passage to a single line.

            `splitlines()` breaks on more than `\n` — a carriage return, a
            vertical tab, U+2028 — and text lifted out of a PDF contains them.
            Replacing only `\n` left the two files a different number of lines
            long, which silently misaligns the entire corpus for whoever trains
            on it."""
            return " ".join((text or "").splitlines()).strip()
        # The format is defined by line position: line n of one file is the
        # translation of line n of the other. A pair with an empty side cannot
        # be represented — an empty last line disappears entirely from the file
        # and shifts every pair after it — so those are left out and counted.
        usable = [r for r in rows if one(r["src_text"]) and one(r["tgt_text"])]
        skipped = len(rows) - len(usable)
        if not usable:
            raise ValueError("No pair has text on both sides, so there is "
                             "nothing to align line by line. Use the JSONL "
                             "export instead.")
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr(f"corpus.{sl}", "\n".join(one(r["src_text"]) for r in usable))
            z.writestr(f"corpus.{tl}", "\n".join(one(r["tgt_text"]) for r in usable))
            z.writestr("corpus.meta.jsonl", "\n".join(json.dumps(
                {k: v for k, v in _flat(r).items()
                 if k not in ("source_text", "target_text")},
                ensure_ascii=False) for r in usable))
            z.writestr("README.md",
                       "# Moses-style parallel corpus\n\n"
                       f"`corpus.{sl}` and `corpus.{tl}` are aligned line by line "
                       f"— line *n* of one is the translation of line *n* of the "
                       f"other.\n\nNewlines inside a pair were replaced with "
                       f"spaces, because the format is one segment per line. Use "
                       f"the JSONL export if you need the paragraph breaks.\n\n"
                       + (f"{skipped} pair(s) had text on only one side and were "
                          f"left out — the format cannot represent them without "
                          f"shifting every line after. They are in the JSONL "
                          f"export.\n" if skipped else
                          "Every pair had text on both sides.\n"))
        return buf.getvalue(), "application/zip", f"tulana_pairs_{stamp}.zip"
    else:
        raise ValueError(fmt)

    return body.encode("utf-8"), media, fn


def export_bundle(con, **filters) -> tuple:
    """Every format at once, with a dataset card. For archiving a release."""
    import zipfile
    rows = _rows_for_export(con, **filters)
    if not rows:
        raise ValueError("No pairs match that selection")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for fmt in FORMATS:
            try:
                data, _, fn = export(con, fmt, **filters)
                # two formats can share an extension — coco and json are both
                # .json — so the key goes in the name or one silently overwrites
                # the other inside the archive
                stem, _, ext = fn.rpartition(".")
                z.writestr(f"pairs/{stem}_{fmt}.{ext}", data)
            except Exception as e:
                z.writestr(f"pairs/{fmt}.FAILED.txt", str(e))
        z.writestr("DATASET_CARD.md", dataset_card(rows))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    return buf.getvalue(), "application/zip", f"tulana_corpus_{stamp}.zip"


def dataset_card(rows: list) -> str:
    langs, boards = {}, {}
    for r in rows:
        langs[r["tgt_language"]] = langs.get(r["tgt_language"], 0) + 1
        boards[r["board"]] = boards.get(r["board"], 0) + 1
    spanning = sum(1 for r in rows if len(r["src_pages"]) > 1 or len(r["tgt_pages"]) > 1)
    src_chars = sum(len(r["src_text"] or "") for r in rows)
    tgt_chars = sum(len(r["tgt_text"] or "") for r in rows)
    lines = [
        "# Tulana parallel corpus", "",
        f"{len(rows)} aligned pairs from Indian school textbooks, drawn from the",
        "parsed layout of the original board PDFs.", "",
        "## Contents", "",
        "| target language | pairs |", "|---|---|",
        *[f"| {k or 'unknown'} | {v} |" for k, v in
          sorted(langs.items(), key=lambda kv: -kv[1])],
        "", "| board | pairs |", "|---|---|",
        *[f"| {k or 'unknown'} | {v} |" for k, v in
          sorted(boards.items(), key=lambda kv: -kv[1])],
        "",
        f"- source characters: {src_chars:,}",
        f"- target characters: {tgt_chars:,}",
        f"- pairs spanning more than one page: {spanning}",
        "",
        "## How a pair was made", "",
        "An annotator opened both editions side by side, selected the blocks that",
        "say the same thing on each side, and saved the pair. A selection may span",
        "several pages: translated text reflows, so a passage on one English page",
        "often runs onto the next in the target language.", "",
        "## What the text is, and is not", "",
        "`source_text` and `target_text` are what the document parser read inside",
        "the selected blocks, joined in reading order. They are **not** a human",
        "transcription. A block over a diagram carries no text, and a page without",
        "a usable text layer yields none — empty means *not recovered*, not *empty",
        "on the page*.", "",
        "Alignment is a human judgement and the text is machine-read. Treat the",
        "pairing as reliable and the characters as needing review before the corpus",
        "is used as a reference.", "",
        "## Formats in this bundle", "",
        *[f"- `{ext}` — {desc}" for _, (nm, _m, ext, desc) in FORMATS.items()],
        "",
    ]
    return "\n".join(lines)
