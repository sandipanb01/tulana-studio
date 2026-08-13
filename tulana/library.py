"""Discover textbook PDFs and pair them across languages.

The annotator picks a board and a class; the studio has to know which PDF is the
English edition and which is the target-language one. Nothing about the folder
layout is assumed — board, class, language and volume are inferred from every
token of a file's own path, the same way for a neatly organised archive and for
a folder someone dropped files into.
"""
import hashlib
import re
import time
from pathlib import Path

import config
from pdflib import fitz


def sha256(path: Path, limit=4 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read(limit))
    return h.hexdigest()


def tokens(path: Path, root: Path):
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    return [t.lower() for t in re.split(r"[^A-Za-z0-9]+", str(rel)) if t]


def infer(path: Path, root: Path) -> dict:
    """Board, class, language and volume from a file's own path.

    Board and language vocabularies overlap — `guj` names both Gujarat and
    Gujarati, `pun` both Punjab and Punjabi — so the board token is identified
    and consumed first. Reading them in plain token order made `GUJ_EN_10.pdf`
    a Gujarati book, which silently removed every Gujarat English edition from
    the pairing list.
    """
    stem = [t for t in re.split(r"[^A-Za-z0-9]+", path.stem) if t]
    folder = tokens(path.parent, root)
    board, rest = None, list(stem)

    # a leading segment that names a board is the board, not a language
    if rest and rest[0].lower() in config.BOARD_TOKENS:
        board = config.BOARD_TOKENS[rest[0].lower()]
        rest = rest[1:]
    if board is None:
        board = next((config.BOARD_TOKENS[t] for t in folder + [x.lower() for x in stem]
                      if t in config.BOARD_TOKENS), None)
        if board is not None:
            # consume the first occurrence so it cannot also be read as a language
            for n, t in enumerate(rest):
                if config.BOARD_TOKENS.get(t.lower()) == board:
                    rest.pop(n)
                    break

    langs = [config.LANG_TOKENS[t.lower()] for t in rest if t.lower() in config.LANG_TOKENS]
    if not langs:
        langs = [config.LANG_TOKENS[t] for t in folder if t in config.LANG_TOKENS]
    language = langs[0] if langs else None

    all_tk = folder + [t.lower() for t in stem]
    cls = None
    for i, t in enumerate(all_tk):
        if t in ("class", "std", "standard", "grade") and i + 1 < len(all_tk) and all_tk[i + 1].isdigit():
            cls = int(all_tk[i + 1]); break
    if cls is None:
        for t in all_tk:
            if re.fullmatch(r"\d{1,2}", t) and 3 <= int(t) <= 12:
                cls = int(t); break
    if cls is None:
        # NCERT chapter files encode class in the first two digits: 1001, 1101
        m = re.fullmatch(r"(\d{2})(\d{2})", path.stem)
        if m and 1 <= int(m.group(1)) <= 12:
            cls = int(m.group(1))

    vol = None
    for t in rest + folder:
        m = re.fullmatch(r"(?:sem|semester)(\d)", t.lower())
        if m:
            vol = "Semester " + m.group(1); break
        m = re.fullmatch(r"(?:part|vol|p)(\d)", t.lower())
        if m:
            vol = "Part " + m.group(1); break
    if vol is None and rest and re.fullmatch(r"[1-4]", rest[-1]):
        vol = "Part " + rest[-1]

    subject = "Mathematics"
    ts = set(all_tk)
    for name, words in (("Science", ("science", "vigyan")),
                        ("Social Science", ("social", "sst"))):
        if ts & set(words):
            subject = name

    # The NCERT chapter set carries no board token anywhere in its path; it is
    # the only English/Hindi collection organised that way.
    if board is None and language in ("English", "Hindi"):
        board = "NCERT"
    return {"board": board, "class": cls, "language": language,
            "volume": vol, "subject": subject,
            "all_languages": list(dict.fromkeys(langs))}


def title_for(meta: dict) -> str:
    bits = [config.board_name(meta.get("board")),
            f"Class {meta['class']}" if meta.get("class") else None,
            meta.get("subject"), meta.get("language"), meta.get("volume")]
    return " · ".join(b for b in bits if b)


def scan(con, root: Path = None, log=print) -> int:
    """Index every PDF under the data folder. Idempotent and cheap to re-run."""
    root = root or config.DATA_DIR
    if not root.is_dir():
        log(f"  data folder not found: {root}")
        return 0
    found = 0
    for pdf in sorted(root.rglob("*.pdf")):
        if any(p.startswith(".") for p in pdf.parts):
            continue
        rel = pdf.relative_to(root).as_posix()
        checksum = sha256(pdf)
        row = con.execute("SELECT id, checksum FROM documents WHERE path=?", (rel,)).fetchone()
        if row and row["checksum"] == checksum:
            found += 1
            continue
        meta = infer(pdf, root)
        try:
            with fitz.open(pdf) as doc:
                pages = doc.page_count
        except Exception as e:
            log(f"  [skip] {pdf.name}: {e}")
            continue
        vals = (rel, meta["board"], meta["class"], meta["subject"], meta["language"],
                config.script_of(meta["language"]), meta["volume"],
                title_for(meta), pages, checksum, time.time())
        if row:
            con.execute("""UPDATE documents SET board=?, class=?, subject=?, language=?,
                           script=?, volume=?, title=?, pages=?, checksum=?, added_at=?
                           WHERE path=?""", vals[1:] + (rel,))
        else:
            con.execute("""INSERT INTO documents(path, board, class, subject, language,
                           script, volume, title, pages, checksum, added_at)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?)""", vals)
        found += 1
    con.commit()
    log(f"  [ok] {found} textbook PDF(s) indexed")
    return found


def pairable(con):
    """Board/class combinations that have an English edition and at least one
    other language — the combinations an annotator can actually work on."""
    rows = con.execute("""
        SELECT board, class, subject FROM documents
        WHERE board IS NOT NULL AND class IS NOT NULL
        GROUP BY board, class, subject
        HAVING SUM(language='English') > 0 AND SUM(language!='English') > 0
        ORDER BY board, class""").fetchall()
    return [dict(r) for r in rows]


def is_excluded(text: str) -> tuple:
    """Does this text look like an excluded topic (geometry, conics, …)?"""
    t = (text or "").lower()
    for term in config.EXCLUDED_TOPICS:
        if term in t:
            return True, term
    return False, ""
