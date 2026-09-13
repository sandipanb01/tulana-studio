"""The parsed-layout corpus: blocks, reading order and extracted text.

This reads the layout produced by the document parser — one JSON per book,
each page carrying its blocks with a label, a type, a reading-order index, a
confidence and the text found inside. 152 books, ~18,000 pages, ~211,000
blocks in the delivery this was written against.

**Additive.** Every table here is created with `CREATE TABLE IF NOT EXISTS` and
nothing in this module writes to `documents`, `projects`, `clips`, `pairs`,
`labels`, `pair_labels`, `exports` or `audit`. An existing database gains three
tables and loses nothing.

Two facts about the source data drive the design:

**Boxes are in image pixels, not PDF points.** Each page records the width and
height of the raster it was parsed from — 1627×2249 in the sample — and
`bbox_xyxy` is relative to that. The page images are not shipped. So boxes are
stored as given *and* as fractions of the page, and the interface scales the
fractions to whatever size it renders at. That makes the overlay correct at any
zoom and at any DPI, and correct even when the PDF is rendered at a completely
different aspect than the parser used.

**The PDF may not be present.** `relpath` names the PDF a book came from, but a
checkout need not carry it. Where the PDF is there, pages are rendered and
blocks overlay them. Where it is not, the blocks are still served with their
geometry and text, so the layout corpus remains usable rather than
disappearing.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import config
import library

SCHEMA = """
CREATE TABLE IF NOT EXISTS pl_books (
  id INTEGER PRIMARY KEY,
  book TEXT NOT NULL,
  relpath TEXT UNIQUE NOT NULL,
  source_json TEXT,
  num_pages INTEGER DEFAULT 0,
  n_blocks INTEGER DEFAULT 0,
  board TEXT, class INTEGER, subject TEXT, language TEXT, script TEXT,
  volume TEXT, title TEXT,
  pdf_present INTEGER DEFAULT 0,
  imported_at REAL
);
CREATE INDEX IF NOT EXISTS ix_pl_book_dims ON pl_books(board, class, subject, language);

CREATE TABLE IF NOT EXISTS pl_pages (
  id INTEGER PRIMARY KEY,
  book_id INTEGER NOT NULL,
  page INTEGER NOT NULL,               -- 0-based, as the parser emits
  width REAL, height REAL,             -- the raster the parser measured against
  image TEXT,
  n_blocks INTEGER DEFAULT 0,
  UNIQUE(book_id, page)
);
CREATE INDEX IF NOT EXISTS ix_pl_page ON pl_pages(book_id, page);

CREATE TABLE IF NOT EXISTS pl_blocks (
  id INTEGER PRIMARY KEY,
  page_id INTEGER NOT NULL,
  ord INTEGER DEFAULT 0,               -- reading order within the page
  label TEXT, type TEXT,
  x0 REAL, y0 REAL, x1 REAL, y1 REAL,  -- image pixels, as given
  fx0 REAL, fy0 REAL, fx1 REAL, fy1 REAL,   -- fractions of the page
  conf REAL,
  text TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS ix_pl_block_page ON pl_blocks(page_id, ord);
CREATE INDEX IF NOT EXISTS ix_pl_block_label ON pl_blocks(label);
"""


def ensure_schema(con):
    con.executescript(SCHEMA)
    con.commit()


# ── ingestion ──────────────────────────────────────────────────────────────

# ── inferring a book's identity from its own text ──────────────────────────
# Unicode blocks by script. Used only when the file name cannot say what a book
# is — the extracted text is evidence, whereas a guess from a title is not.
SCRIPT_RANGES = {
    "Devanagari": [(0x0900, 0x097F)], "Bengali": [(0x0980, 0x09FF)],
    "Gurmukhi": [(0x0A00, 0x0A7F)], "Gujarati": [(0x0A80, 0x0AFF)],
    "Odia": [(0x0B00, 0x0B7F)], "Tamil": [(0x0B80, 0x0BFF)],
    "Telugu": [(0x0C00, 0x0C7F)], "Kannada": [(0x0C80, 0x0CFF)],
    "Malayalam": [(0x0D00, 0x0D7F)],
    "Perso-Arabic": [(0x0600, 0x06FF), (0x0750, 0x077F)],
    "Ol Chiki": [(0x1C50, 0x1C7F)], "Latin": [(0x0041, 0x024F)],
}

# A script with exactly one language in Indian school publishing resolves
# outright.
SCRIPT_TO_LANGUAGE = {
    "Gurmukhi": "Punjabi", "Gujarati": "Gujarati", "Odia": "Odia",
    "Tamil": "Tamil", "Telugu": "Telugu", "Kannada": "Kannada",
    "Malayalam": "Malayalam", "Latin": "English",
}

# Devanagari and Bengali script are each shared by several languages, so the
# script alone cannot name one. These are orthographic markers that do — chosen
# because they are frequent in ordinary prose and near-absent in the sibling
# language, and measured against books whose language is already known:
#
#   आहे  appeared 31-40 times in Marathi books and zero times in Hindi ones
#   है    the reverse
#   ৰ     is the Assamese RA; Bengali writes র
#
# Each marker votes; a clear majority wins and a near-tie is left unresolved,
# because a mislabelled book in a benchmark is worse than an unlabelled one.
SHARED_SCRIPT_MARKERS = {
    "Devanagari": {
        "Marathi": ["आहे", "आहेत", "ची ", "चा ", "चे ", "ळ", "व्या", "म्हणून",
                    "असून", "यांची"],
        "Hindi": ["है", "हैं", "और ", "का ", "के ", "की ", "किया", "होता",
                  "इसलिए", "उनके"],
        "Sanskrit": ["अस्ति", "भवति", "एव ", "तथा ", "इति ", "स्य ", "ेषु "],
        "Nepali": ["छ ", "छन्", "गर्न", "भएको", "हुन्छ"],
    },
    "Bengali": {
        "Assamese": ["ৰ", "ৱ", "হৈছে", "কৰি", "আৰু"],
        "Bengali": ["র", "ব", "হয়েছে", "করে", "এবং", "ছিল"],
    },
}

# Words that name a board outright when the file name does not. Only strings
# that identify a board — never a subject word, which would be a guess.
TEXT_BOARD_HINTS = {
    "পশ্চিমবঙ্গ": "WB", "west bengal": "WB", "wbbse": "WB",
    "महाराष्ट्र": "MH", "ಕರ್ನಾಟಕ": "KA", "കേരള": "KL",
    "ਪੰਜਾਬ": "PB", "ગુજરાત": "GJ", "தமிழ்நாடு": "TN",
    "ఆంధ్రప్రదేశ్": "AP", "ଓଡ଼ିଶା": "OD", "অসম": "AS",
}


def detect_script(text: str) -> tuple:
    """The dominant non-Latin script in a sample, and its share.

    Latin is counted but never wins on its own: an Indic textbook carries
    English numerals, units and loan words throughout, and letting Latin win
    would label every one of them English."""
    if not text:
        return None, 0.0
    counts, total = {}, 0
    for ch in text:
        cp = ord(ch)
        for name, ranges in SCRIPT_RANGES.items():
            if any(lo <= cp <= hi for lo, hi in ranges):
                counts[name] = counts.get(name, 0) + 1
                total += 1
                break
    if not total:
        return None, 0.0
    indic = {k: v for k, v in counts.items() if k != "Latin"}
    pool = indic or counts
    best = max(pool, key=pool.get)
    return best, round(pool[best] / total, 3)


def disambiguate(script: str, sample: str) -> tuple:
    """Which language, among those sharing a script, does this text look like?

    Returns (language, confidence) — the winner's share of all marker hits, so
    a lopsided result is trusted and a close one is not."""
    table = SHARED_SCRIPT_MARKERS.get(script)
    if not table or not sample:
        return None, 0.0
    scores = {lang: sum(sample.count(m) for m in marks)
              for lang, marks in table.items()}
    total = sum(scores.values())
    if total < 12:                      # too little evidence to call
        return None, 0.0
    best = max(scores, key=scores.get)
    share = scores[best] / total
    runner = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0
    if share < 0.55 or scores[best] < runner * 1.5:
        return None, round(share, 3)
    return best, round(share, 3)


def infer_from_text(sample: str) -> dict:
    """Board, language and script from the text itself.

    The last resort, used only when the file name says nothing — but not a
    guess. The script is measured from Unicode ranges, and where a script is
    shared the language is decided by markers validated against books whose
    language is already known. Anything undecidable is left unset.
    """
    script, share = detect_script(sample)
    out = {"board": None, "language": None, "script": script,
           "script_confidence": share, "language_confidence": 0.0,
           "evidence": "text"}
    if not script or share < 0.5:
        return out
    direct = SCRIPT_TO_LANGUAGE.get(script)
    if direct:
        out["language"] = direct
        out["language_confidence"] = share
    else:
        lang, conf = disambiguate(script, sample)
        out["language"] = lang
        out["language_confidence"] = conf
    low = sample.lower()
    for needle, board in TEXT_BOARD_HINTS.items():
        if needle in sample or needle in low:
            out["board"] = board
            break
    return out


JUNK_PARTS = ("__MACOSX", ".git", "node_modules", "state", ".ipynb_checkpoints")


def _is_junk(p: Path) -> bool:
    """Archive litter and dot-files, which are not corpus.

    Unpacking a zip made on macOS leaves `__MACOSX/` full of `._name.json`
    resource forks — one per real file. They parse as JSON, they carry the
    right extension, and counting them doubles the apparent corpus while
    poisoning any check that looks at the first file it finds."""
    return any(part in JUNK_PARTS or part.startswith("._") or
               (part.startswith(".") and len(part) > 1) for part in p.parts)


def _looks_like_layout(f: Path) -> bool:
    try:
        head = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return False
    return isinstance(head, dict) and "pages" in head and "relpath" in head


def find_corpus(root: Path = None) -> Path | None:
    """Locate the parsed-layout folder.

    Searched for rather than demanded. The delivery unpacks as `output/`, but
    it has also arrived as `board_outputs/output/` — a folder inside a folder —
    and an interface that shows nothing because a directory had an extra level
    is the failure this project keeps hitting. So: try the obvious places, then
    walk the tree for any folder that actually contains layout JSON.
    """
    root = Path(root or config.DATA_DIR)
    here = Path(__file__).parent
    obvious = [root, root / "output", root.parent / "output",
               root / "layout", root.parent / "layout",
               root.parent / "board_outputs", root.parent / "board_outputs" / "output",
               root / "board_outputs", root / "board_outputs" / "output",
               here / "output", here.parent / "output",
               here.parent / "board_outputs", here.parent / "board_outputs" / "output"]
    for c in obvious:
        try:
            if not c.is_dir():
                continue
        except OSError:
            continue
        for f in c.rglob("*.json"):
            if _is_junk(f.relative_to(c)):
                continue
            if _looks_like_layout(f):
                return c
            break                       # one real candidate is enough to judge

    # Nothing obvious. Walk from the repository root, shallowly, and take the
    # folder that holds the most layout files.
    best, best_n = None, 0
    for base in {root.parent, here.parent, root}:
        try:
            if not base.is_dir():
                continue
        except OSError:
            continue
        counts = {}
        for f in base.rglob("*.json"):
            rel = f.relative_to(base)
            if _is_junk(rel) or len(rel.parts) > 6:
                continue
            counts[f.parent] = counts.get(f.parent, 0) + 1
        for folder, n in sorted(counts.items(), key=lambda kv: -kv[1])[:5]:
            sample = next((x for x in folder.glob("*.json")
                           if not _is_junk(Path(x.name))), None)
            if sample and _looks_like_layout(sample):
                # climb to the shallowest ancestor that still holds only layout
                top = folder
                while top.parent != base and any(
                        top.parent.rglob("*.json")):
                    top = top.parent
                if n > best_n:
                    best, best_n = top, n
    return best


def ingest(con, corpus: Path = None, data_dir: Path = None, log=print) -> dict:
    """Read every layout JSON into the database. Idempotent per relpath."""
    ensure_schema(con)
    corpus = Path(corpus) if corpus else find_corpus()
    if not corpus:
        return {"corpus": None, "books": 0, "pages": 0, "blocks": 0,
                "problems": ["no parsed-layout corpus found — expected a folder "
                             "of JSON files each carrying `relpath` and `pages`"]}
    data_dir = Path(data_dir or config.DATA_DIR)
    files = sorted(corpus.rglob("*.json"))
    books = pages = blocks = 0
    problems = []

    for f in files:
        if _is_junk(f.relative_to(corpus) if f.is_relative_to(corpus) else f):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            problems.append(f"{f.name}: not readable JSON ({str(e)[:60]})")
            continue
        if not isinstance(d, dict) or "pages" not in d or "relpath" not in d:
            continue
        rel = str(d["relpath"]).replace("\\", "/")
        meta = library.infer(Path(rel), Path("."))
        if not (meta.get("board") and meta.get("language")):
            # The name could not tell us. The parser already read the page, so
            # use that: the script of the text is evidence, not a guess.
            sample = "".join((bl.get("text") or "")
                             for p in d["pages"][:12]
                             for bl in (p.get("blocks") or []))[:8000]
            hint = infer_from_text(sample)
            had_board, had_lang = meta.get("board"), meta.get("language")
            meta["board"] = had_board or hint["board"]
            meta["language"] = had_lang or hint["language"]
            meta["script_from_text"] = hint["script"]
            if hint["script"]:
                log(f"  [layout] {Path(rel).name}: the name gave no "
                    f"{'board and language' if not (had_board or had_lang) else ('board' if not had_board else 'language')}"
                    f"; its text is {hint['script']} "
                    f"({int(hint['script_confidence']*100)}%)"
                    + (f", reading as {hint['language']} "
                       f"({int(hint['language_confidence']*100)}% of markers)"
                       if hint["language"] else ", and the script is shared so the "
                       "language was left unset")
                    + f" -> {meta.get('board') or 'board unknown'} / "
                      f"{meta.get('language') or 'language unknown'}")
        pdf = _find_pdf(data_dir, rel)
        n_blocks = sum(len(p.get("blocks") or []) for p in d["pages"])

        con.execute("""INSERT INTO pl_books(book, relpath, source_json, num_pages,
                       n_blocks, board, class, subject, language, script, volume,
                       title, pdf_present, imported_at)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(relpath) DO UPDATE SET
                         book=excluded.book, source_json=excluded.source_json,
                         num_pages=excluded.num_pages, n_blocks=excluded.n_blocks,
                         board=excluded.board, class=excluded.class,
                         subject=excluded.subject, language=excluded.language,
                         script=excluded.script, volume=excluded.volume,
                         title=excluded.title, pdf_present=excluded.pdf_present,
                         imported_at=excluded.imported_at""",
                    (d.get("book") or Path(rel).stem, rel, str(f), d.get("num_pages", 0),
                     n_blocks, meta.get("board"), meta.get("class"),
                     meta.get("subject"), meta.get("language"),
                     config.script_of(meta.get("language")) if meta.get("language") else None,
                     meta.get("volume"), _title(meta, rel),
                     1 if pdf else 0, time.time()))
        book_id = con.execute("SELECT id FROM pl_books WHERE relpath=?", (rel,)).fetchone()[0]

        # replace this book's pages wholesale, so a re-ingest is clean
        old = [r[0] for r in con.execute("SELECT id FROM pl_pages WHERE book_id=?",
                                         (book_id,))]
        if old:
            con.executemany("DELETE FROM pl_blocks WHERE page_id=?",
                            [(i,) for i in old])
            con.execute("DELETE FROM pl_pages WHERE book_id=?", (book_id,))

        prows, brows = [], []
        for p in d["pages"]:
            w = float(p.get("width") or 0) or 1.0
            h = float(p.get("height") or 0) or 1.0
            pg = int(p.get("page", 0))
            bl = p.get("blocks") or []
            prows.append((book_id, pg, w, h, p.get("image"), len(bl)))
        con.executemany("""INSERT INTO pl_pages(book_id, page, width, height, image,
                           n_blocks) VALUES(?,?,?,?,?,?)""", prows)
        ids = {r[1]: r[0] for r in con.execute(
            "SELECT id, page FROM pl_pages WHERE book_id=?", (book_id,))}
        for p in d["pages"]:
            w = float(p.get("width") or 0) or 1.0
            h = float(p.get("height") or 0) or 1.0
            pid = ids.get(int(p.get("page", 0)))
            for b in (p.get("blocks") or []):
                bb = b.get("bbox_xyxy") or [0, 0, 0, 0]
                try:
                    x0, y0, x1, y1 = (float(v) for v in bb[:4])
                except Exception:
                    continue
                brows.append((pid, int(b.get("order", 0)), b.get("label"),
                              b.get("type"), x0, y0, x1, y1,
                              x0 / w, y0 / h, x1 / w, y1 / h,
                              float(b.get("conf") or 0), (b.get("text") or "")))
        if brows:
            con.executemany("""INSERT INTO pl_blocks(page_id, ord, label, type,
                               x0,y0,x1,y1, fx0,fy0,fx1,fy1, conf, text)
                               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", brows)
        books += 1
        pages += len(prows)
        blocks += len(brows)
        if books % 25 == 0:
            log(f"  [layout] {books} books, {blocks} blocks…")

    con.commit()
    missing = con.execute("SELECT COUNT(*) FROM pl_books WHERE pdf_present=0").fetchone()[0]
    if missing:
        problems.append(f"{missing} book(s) have layout but no PDF on disk — their "
                        f"blocks and text are still served, the page image is not")
    return {"corpus": str(corpus), "books": books, "pages": pages,
            "blocks": blocks, "problems": problems}


def _title(meta, rel) -> str:
    bits = [config.board_name(meta["board"]) if meta.get("board") else None,
            f"Class {meta['class']}" if meta.get("class") else None,
            meta.get("subject"), meta.get("language"), meta.get("volume")]
    return " · ".join(b for b in bits if b) or Path(rel).stem


def _find_pdf(data_dir: Path, rel: str) -> Path | None:
    """The PDF for a relpath, tried directly then by name.

    A corpus gets reorganised; the parser's relpath was true when it ran. The
    filename is the stable part, so falling back to it keeps the viewer working
    after a reshuffle instead of silently losing the page image."""
    direct = data_dir / Path(*rel.split("/"))
    if direct.exists():
        return direct
    name = Path(rel).name
    try:
        return next((p for p in data_dir.rglob(name) if p.is_file()), None)
    except OSError:
        return None


# ── reading ────────────────────────────────────────────────────────────────
def labels(con) -> list:
    ensure_schema(con)
    return [dict(r) for r in con.execute(
        """SELECT label, type, COUNT(*) n FROM pl_blocks
           WHERE label IS NOT NULL GROUP BY label ORDER BY n DESC""")]


def pairable(con) -> list:
    """Board/class/subject groups that have English and at least one other
    language, built from the parsed corpus rather than from the PDF folder."""
    ensure_schema(con)
    rows = con.execute("""SELECT board, class, subject, language, COUNT(*) n
                          FROM pl_books WHERE board IS NOT NULL AND class IS NOT NULL
                          GROUP BY board, class, subject, language""").fetchall()
    groups = {}
    for r in rows:
        groups.setdefault((r["board"], r["class"], r["subject"]), set()).add(r["language"])
    out = []
    for (b, c, s), langs in sorted(groups.items(), key=lambda kv: str(kv[0])):
        if "English" in langs and (langs - {"English"}):
            out.append({"board": b, "class": c, "subject": s,
                        "board_name": config.board_name(b),
                        "label": f"{config.board_name(b)} · Class {c} · {s}",
                        "target_languages": sorted(langs - {"English"})})
    return out


def editions(con, board, cls, subject, language=None) -> list:
    ensure_schema(con)
    q = """SELECT id, book, relpath, language, script, volume, num_pages, n_blocks,
                  pdf_present, title FROM pl_books
           WHERE board=? AND class=? AND subject=?"""
    args = [board, cls, subject]
    if language:
        q += " AND language=?"
        args.append(language)
    return [dict(r) for r in con.execute(q + " ORDER BY language, volume", args)]


def book(con, book_id: int) -> dict:
    ensure_schema(con)
    r = con.execute("SELECT * FROM pl_books WHERE id=?", (book_id,)).fetchone()
    if not r:
        raise ValueError("Unknown book")
    return dict(r)


def page_blocks(con, book_id: int, page: int) -> dict:
    """Every block on one page, with fractional geometry for the overlay."""
    ensure_schema(con)
    b = book(con, book_id)
    p = con.execute("SELECT * FROM pl_pages WHERE book_id=? AND page=?",
                    (book_id, page)).fetchone()
    if not p:
        return {"book": b, "page": page, "exists": False, "blocks": [],
                "width": None, "height": None,
                "pages": b["num_pages"]}
    blocks = [dict(r) for r in con.execute(
        """SELECT id, ord, label, type, x0, y0, x1, y1, fx0, fy0, fx1, fy1, conf,
                  text FROM pl_blocks WHERE page_id=? ORDER BY ord, id""", (p["id"],))]
    return {"book": b, "page": page, "exists": True, "pages": b["num_pages"],
            "width": p["width"], "height": p["height"], "image": p["image"],
            "image_available": page_renderable(b, page),
            "blocks": blocks}


_PAGECOUNT = {}


def page_renderable(book_row: dict, page: int) -> bool:
    """Can the page image actually be produced?

    The layout can describe more pages than the PDF on disk contains — a
    truncated copy, or a different edition of the same book. Saying so up
    front lets the interface draw the blocks on a blank page instead of
    discovering the gap through a failed image request."""
    rel = book_row.get("relpath") or ""
    if not book_row.get("pdf_present"):
        return False
    n = _PAGECOUNT.get(rel)
    if n is None:
        pdf = _find_pdf(Path(config.DATA_DIR), rel)
        if not pdf:
            _PAGECOUNT[rel] = 0
            return False
        try:
            from pdflib import fitz
            with fitz.open(pdf) as doc:
                n = doc.page_count
        except Exception:
            n = 0
        _PAGECOUNT[rel] = n
    return 0 <= page < n


def selection_text(con, block_ids: list) -> dict:
    """The text of a set of chosen blocks, in reading order.

    Reading order rather than click order: an annotator selecting a worked
    example out of sequence still wants it to read as it does on the page.
    """
    ensure_schema(con)
    if not block_ids:
        return {"blocks": [], "text": "", "n_blocks": 0, "n_chars": 0}
    qs = ",".join("?" for _ in block_ids)
    rows = [dict(r) for r in con.execute(
        f"""SELECT b.id, b.ord, b.label, b.type, b.text, p.page, k.book, k.language
            FROM pl_blocks b JOIN pl_pages p ON p.id=b.page_id
            JOIN pl_books k ON k.id=p.book_id
            WHERE b.id IN ({qs}) ORDER BY p.page, b.ord""", block_ids)]
    text = "\n\n".join((r["text"] or "").strip() for r in rows if (r["text"] or "").strip())
    return {"blocks": rows, "text": text, "n_blocks": len(rows),
            "n_chars": len(text),
            "labels": sorted({r["label"] for r in rows if r["label"]})}


def stats(con) -> dict:
    ensure_schema(con)
    b = con.execute("""SELECT COUNT(*) books, COALESCE(SUM(num_pages),0) pages,
                       COALESCE(SUM(n_blocks),0) blocks,
                       SUM(pdf_present) with_pdf FROM pl_books""").fetchone()
    by_board = [dict(r) for r in con.execute("""
        SELECT board, COUNT(*) books, COALESCE(SUM(n_blocks),0) blocks
        FROM pl_books WHERE board IS NOT NULL GROUP BY board ORDER BY books DESC""")]
    by_lang = [dict(r) for r in con.execute("""
        SELECT language, script, COUNT(*) books, COALESCE(SUM(n_blocks),0) blocks
        FROM pl_books WHERE language IS NOT NULL
        GROUP BY language ORDER BY books DESC""")]
    by_class = [dict(r) for r in con.execute("""
        SELECT class, COUNT(*) books FROM pl_books WHERE class IS NOT NULL
        GROUP BY class ORDER BY class""")]
    return {"books": b["books"], "pages": b["pages"], "blocks": b["blocks"],
            "books_with_pdf": b["with_pdf"] or 0,
            "by_board": by_board, "by_language": by_lang, "by_class": by_class,
            "labels": labels(con)}


def mapping_report(con, data_dir: Path = None) -> dict:
    """Which books mapped onto an original PDF, and which did not — and why.

    The layout is only useful over the original page, so a book whose PDF is
    absent is a real gap, not a detail. Reporting it by name beats a count.
    The aspect check matters just as much and is easy to miss: the parser
    measured against a raster, and if its proportions disagree with the PDF
    page, every box on that book is skewed. Boxes are stored as fractions
    precisely so they survive a DPI change, but nothing can survive a genuine
    aspect mismatch — so it is checked rather than assumed.
    """
    data_dir = Path(data_dir or config.DATA_DIR)
    ensure_schema(con)
    mapped, missing, skewed = [], [], []
    for r in con.execute("""SELECT id, book, relpath, board, class, language,
                            num_pages, n_blocks FROM pl_books ORDER BY book"""):
        d = dict(r)
        pdf = _find_pdf(data_dir, d["relpath"])
        if not pdf:
            missing.append({**d, "reason": f"no PDF at {d['relpath']}, and no file "
                                           f"named {Path(d['relpath']).name} anywhere "
                                           f"under {data_dir}",
                            "fix": "place the original PDF in the data folder, or run "
                                   "`git lfs pull` if it is an unfetched pointer"})
            continue
        d["pdf"] = str(pdf)
        p = con.execute("""SELECT width, height, page FROM pl_pages
                           WHERE book_id=? ORDER BY page LIMIT 1 OFFSET 2""",
                        (d["id"],)).fetchone()
        try:
            from pdflib import fitz
            with fitz.open(pdf) as doc:
                d["pdf_pages"] = doc.page_count
                rect = doc[min(p["page"] if p else 0, doc.page_count - 1)].rect
            if p and p["width"] and p["height"] and rect.height:
                pa = p["width"] / p["height"]
                da = rect.width / rect.height
                d["aspect_delta_pct"] = round(abs(pa - da) / da * 100, 2)
                # A difference here is usually harmless and was verified to be:
                # the parser normalises each page to a fixed raster, and because
                # boxes are stored as a fraction of width and of height
                # *independently*, a uniform or non-uniform rescale maps back
                # exactly. Checked by drawing the boxes of a 4.76%-different book
                # onto its real page — they landed correctly.
                #
                # What fractions cannot survive is letterboxing, where part of
                # the raster is padding rather than page. That shows up as a
                # large delta, so only a large one is worth a human look.
                if d["aspect_delta_pct"] > 15:
                    skewed.append({**d, "reason":
                        f"the parser measured a {p['width']:.0f}x{p['height']:.0f} raster "
                        f"against a {rect.width:.0f}x{rect.height:.0f} point page — "
                        f"{d['aspect_delta_pct']}% different. A rescale is absorbed by "
                        f"the fractional coordinates, but a gap this large can also mean "
                        f"the raster was padded, which they cannot absorb",
                        "fix": "open a page in the Blocks tab and check the boxes sit on "
                               "their content; if they are offset, the layout was not "
                               "produced from this PDF"})
            if d["pdf_pages"] < d["num_pages"]:
                d["note"] = (f"the layout covers {d['num_pages']} pages but the PDF has "
                             f"{d['pdf_pages']} — later pages show blocks without an image")
        except Exception as e:
            d["note"] = f"PDF present but unreadable: {str(e)[:70]}"
        mapped.append(d)
    return {"data_dir": str(data_dir), "books": len(mapped) + len(missing),
            "mapped": len(mapped), "missing": missing, "skewed": skewed,
            "worst_aspect_delta_pct": max([m.get("aspect_delta_pct") or 0
                                           for m in mapped] or [0]),
            "detail": mapped}
