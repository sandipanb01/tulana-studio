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


ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7,
         "viii": 8, "ix": 9, "x": 10, "xi": 11, "xii": 12}
CLASS_WORDS = ("class", "std", "standard", "grade", "cls", "kaksha")


def _split_glued(items):
    """Separate a word glued to its number: `class10` -> `class`, `10`.

    People write `Kerala_Class10_Malayalam.pdf` at least as often as
    `Kerala_Class_10_...`. Splitting only on separators dropped the class for
    every such file, and a file with no class never reaches the dropdown — which
    is how a textbook can sit in the folder, be indexed, and still be invisible.
    """
    out = []
    for t in items:
        m = re.fullmatch(r"([A-Za-z]+)(\d{1,2})", t)
        if m:
            out.extend([m.group(1), m.group(2)]); continue
        m = re.fullmatch(r"(\d{1,2})([A-Za-z]+)", t)
        if m:
            out.extend([m.group(1), m.group(2)]); continue
        out.append(t)
    return out


def _class_from(items):
    """A class number written in any of the ways people write one."""
    tk = [t.lower() for t in items]
    for i, t in enumerate(tk):
        if t in CLASS_WORDS and i + 1 < len(tk):
            nxt = tk[i + 1]
            if nxt.isdigit() and 1 <= int(nxt) <= 12:
                return int(nxt)
            if nxt in ROMAN:
                return ROMAN[nxt]
        m = re.fullmatch(r"(?:%s)(\d{1,2})" % "|".join(CLASS_WORDS), t)
        if m and 1 <= int(m.group(1)) <= 12:
            return int(m.group(1))
    for t in tk:
        if re.fullmatch(r"\d{1,2}", t) and 1 <= int(t) <= 12:
            return int(t)
    for t in tk:
        # Digits were preferred above, so a roman numeral here is the only
        # candidate. `i` and `v` alone are far more often an initial or a part
        # marker; `x` is kept, because "Class X" is very common.
        if t in ROMAN and t not in ("i", "v"):
            return ROMAN[t]
    return None


def infer(path: Path, root: Path) -> dict:
    """Board, class, language, subject and volume from a file's own path.

    Board and language vocabularies overlap — `guj` names both Gujarat and
    Gujarati, `pun` both Punjab and Punjabi — so the board is identified and
    consumed before languages are read. Tokens come from the whole relative
    path, so a file organised into folders works as well as a long file name.
    """
    stem_tokens = _split_glued([t for t in re.split(r"[^A-Za-z0-9]+", path.stem) if t])
    folder_tokens = _split_glued(tokens(path.parent, root))
    rest = list(stem_tokens)
    board = None

    # Two-word board names first. "Tamil Nadu" splits into `tamil` + `nadu`,
    # and `tamil` is a language token — reading it as the language would lose
    # both the board and the book.
    phrases = getattr(config, "BOARD_PHRASES", {})

    def consume(pool, phrase):
        low = [t.lower() for t in pool]
        for w in phrase:
            if w in low:
                i = low.index(w); pool.pop(i); low.pop(i)

    for pool in (stem_tokens, folder_tokens):
        low = [t.lower() for t in pool]
        for phrase, code in phrases.items():
            n = len(phrase)
            if any(tuple(low[i:i + n]) == phrase for i in range(len(low) - n + 1)):
                board = code
                consume(pool, phrase)
                if pool is stem_tokens:
                    consume(rest, phrase)
                break
        if board:
            break

    if board is None and rest and rest[0].lower() in config.BOARD_TOKENS:
        board = config.BOARD_TOKENS[rest[0].lower()]
        rest = rest[1:]
    if board is None:
        for t in folder_tokens + [x.lower() for x in stem_tokens]:
            if t in config.BOARD_TOKENS:
                board = config.BOARD_TOKENS[t]
                break
        if board is not None:
            for n, t in enumerate(rest):
                if config.BOARD_TOKENS.get(t.lower()) == board:
                    rest.pop(n); break

    langs = [config.LANG_TOKENS[t.lower()] for t in rest
             if t.lower() in config.LANG_TOKENS]
    if not langs:
        langs = [config.LANG_TOKENS[t] for t in folder_tokens
                 if t in config.LANG_TOKENS]
    language = langs[0] if langs else None

    all_tk = folder_tokens + [t.lower() for t in stem_tokens]
    cls = _class_from(stem_tokens) or _class_from(folder_tokens)
    if cls is None:
        m = re.fullmatch(r"(\d{2})(\d{2})", path.stem)      # NCERT 1001, 1201
        if m and 1 <= int(m.group(1)) <= 12:
            cls = int(m.group(1))

    vol = None
    for t in rest + folder_tokens:
        m = re.fullmatch(r"(?:sem|semester)(\d)", t.lower())
        if m:
            vol = "Semester " + m.group(1); break
        m = re.fullmatch(r"(?:part|vol|p)(\d)", t.lower())
        if m:
            vol = "Part " + m.group(1); break
    if vol is None and rest and re.fullmatch(r"[1-4]", rest[-1]):
        vol = "Part " + rest[-1]

    subject = None
    ts = set(all_tk)
    for name, words in (("Mathematics", ("math", "maths", "mathematics", "ganit",
                                         "ganita", "kanakku")),
                        ("Science", ("science", "vigyan", "vignan")),
                        ("Physics", ("physics", "bhautiki")),
                        ("Chemistry", ("chemistry", "rasayan")),
                        ("Biology", ("biology", "bio", "jeev")),
                        ("Social Science", ("social", "sst", "samajik")),
                        ("History", ("history", "itihas")),
                        ("Geography", ("geography", "bhugol")),
                        ("English", ("english",))):
        if ts & set(words):
            subject = name; break
    if subject is None:
        subject = "Mathematics"          # the corpus default, stated not hidden

    # The NCERT chapter set carries no board token anywhere in its path, so it
    # needs a fallback — but only when the path actually looks like that set.
    # Assuming "English with no board" means NCERT silently relabelled an Assam
    # or Odisha textbook as NCERT, which is worse than leaving it unresolved.
    if board is None and language in ("English", "Hindi"):
        looks_like_ncert = (re.fullmatch(r"\d{4}", path.stem) is not None
                            or any(t in ("input", "ncert", "cbse") for t in folder_tokens))
        if looks_like_ncert:
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
    skipped = []
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
            # Say *why* rather than echoing PyMuPDF. A Git LFS pointer is by far
            # the commonest cause and the least obvious from the error text.
            why = file_problem(pdf) or str(e)
            log(f"  [skip] {pdf.name}: {why}")
            skipped.append((pdf.name, why))
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
    lfs = [x for x in skipped if "LFS" in x[1]]
    if lfs:
        log(f"  [warn] {len(lfs)} file(s) are Git LFS pointers, not PDFs, and were "
            f"skipped — run `git lfs pull` to fetch them, then rescan")
    elif skipped:
        log(f"  [warn] {len(skipped)} file(s) could not be opened — "
            f"see GET /api/library/diagnose for each one and why")
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



LFS_MAGIC = b"version https://git-lfs.github.com/spec/v1"


def file_problem(path: Path) -> str | None:
    """Why this file cannot be used, or None if it looks like a real PDF.

    The commonest cause in practice is not a bad name at all: `git clone`
    without `git lfs pull` — or an exhausted LFS bandwidth quota — leaves a
    132-byte text pointer where the PDF should be. It has the right name and
    the right extension, so it looks present in every listing, and the scanner
    quietly skips it. That is how a textbook can be in the repository, be on
    disk, and still never appear in the dropdown.
    """
    try:
        size = path.stat().st_size
    except OSError as e:
        return f"cannot be read from disk ({e.strerror or e})"
    if size == 0:
        return "the file is empty (0 bytes)"
    try:
        with open(path, "rb") as fh:
            head = fh.read(200)
    except OSError as e:
        return f"cannot be opened ({e.strerror or e})"
    if head.startswith(LFS_MAGIC):
        return ("this is a Git LFS pointer, not the PDF itself — the file was "
                "never downloaded")
    if not head.startswith(b"%PDF-"):
        snippet = head[:40].decode("utf-8", "replace").strip().replace("\n", " ")
        return f"not a PDF — the file begins with {snippet!r}"
    return None


def scan_disk(root: Path = None) -> dict:
    """Every candidate file on disk, and whether it is a usable PDF."""
    root = Path(root or config.DATA_DIR)
    good, bad = [], []
    if not root.is_dir():
        return {"root": str(root), "exists": False, "good": [], "bad": []}
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() != ".pdf":
            continue
        problem = file_problem(p)
        (bad if problem else good).append(
            {"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size,
             "problem": problem})
    return {"root": str(root), "exists": True, "good": good, "bad": bad}


def diagnose(con, root: Path = None) -> dict:
    """Why is a textbook not in the dropdown?

    Silence was the real bug: a PDF could sit in the folder, be indexed, and
    still never appear, with nothing anywhere saying why. Every file is
    accounted for here as exactly one of usable, unpaired, or unreadable, and
    every rejection carries the reason and the fix.
    """
    root = Path(root or config.DATA_DIR)
    usable, unpaired, unreadable = [], [], []

    # Start from the disk. A file that could not be opened never reached the
    # documents table, so a database-only diagnosis cannot see it — which is
    # precisely the case that was going unreported.
    disk = scan_disk(root)
    broken = [{"path": b["path"], "board": None, "class": None, "language": None,
               "subject": None, "pages": None, "bytes": b["bytes"],
               "reason": b["problem"],
               "fix": ("run `git lfs pull` in the repository to fetch the real "
                       "file, then rescan"
                       if "LFS" in (b["problem"] or "")
                       else "replace it with a readable PDF, then rescan")}
              for b in disk["bad"]]

    rows = con.execute("""SELECT id, path, board, class, subject, language,
                          script, volume, pages FROM documents ORDER BY path""").fetchall()
    groups = {}
    for r in rows:
        groups.setdefault((r["board"], r["class"], r["subject"]), []).append(dict(r))

    for r in rows:
        d = dict(r)
        missing = [k for k in ("board", "class", "language") if not d.get(k)]
        if missing:
            unreadable.append({**d, "reason":
                f"could not work out the {', '.join(missing)} from the file name "
                f"or its folders",
                "fix": "rename it like BOARD_LANG_CLASS — for example KER_ML_10.pdf, "
                       "or Kerala_Class10_Malayalam.pdf, or put it in "
                       "Kerala/Class 10/Malayalam/"})
            continue
        peers = groups.get((d["board"], d["class"], d["subject"]), [])
        has_en = any(p["language"] == "English" for p in peers)
        has_other = any(p["language"] != "English" for p in peers)
        if has_en and has_other:
            usable.append(d)
        else:
            want = "an English edition" if not has_en else "a target-language edition"
            have = sorted({p["language"] for p in peers if p["language"]})
            unpaired.append({**d, "reason":
                f"{config.board_name(d['board'])} · Class {d['class']} · "
                f"{d['subject']} has only {', '.join(have)}, so there is no pair to clip",
                "fix": f"add {want} for the same board, class and subject — the "
                       f"subject has to match as well ({d['subject']} here)"})
    unreadable = broken + unreadable
    return {
        "data_dir": str(root),
        "files_on_disk": len(disk["good"]) + len(disk["bad"]),
        "files_unopenable": len(disk["bad"]),
        "lfs_pointers": sum(1 for b in disk["bad"] if "LFS" in (b["problem"] or "")),
        "documents": len(rows), "usable": len(usable),
        "unpaired": unpaired, "unreadable": unreadable,
        "groups": [{"board": k[0], "class": k[1], "subject": k[2],
                    "languages": sorted({p["language"] for p in v if p["language"]}),
                    "pairable": any(p["language"] == "English" for p in v)
                                and bool({p["language"] for p in v} - {"English"})}
                   for k, v in sorted(groups.items(), key=lambda kv: str(kv[0]))],
    }
