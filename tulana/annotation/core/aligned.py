"""The aligned document-MT test set: pre-aligned, pre-corrected pairs to verify.

``aligned-docMT-test/`` (next to ``board_outputs/``) holds, for 62 book pairs,
the parser's layout JSON for both editions after an alignment model
(gemini-3.5-flash, prompt v4) has

  * aligned each English page to its translation — blocks that share an
    ``align_id`` are translations of each other;
  * merged the OCR blocks of one translation unit into a single block per page,
    keeping the original blocks under ``members``;
  * applied small OCR corrections that passed code checks, and left ``flags``
    for a reviewer where it was not allowed to change anything.

Its own README says what it is for: pre-annotation for HUMAN verification, not
a final reference. This module turns each pair into a Setu project whose rows
ARE the model's units, so an annotator checks the model's work instead of
starting from Setu's heuristic alignment.

Three rules, in order of how much damage breaking them would do:

1. **What the OCR read stays the source.** Every merged block's
   ``source_text`` is rebuilt from the RAW layout in ``board_outputs`` by
   joining its members — byte for byte what the parser read. Where the model
   changed the text, its version is written as the FIRST REVISION of that
   passage, credited to the model. So "Put back what the parser read" undoes
   the model, the history shows exactly what it changed, and an annotator's own
   corrections land on top. The model's edits were never checked by a person
   at scale; they must never be mistaken for the original.

2. **Importing never overwrites work.** A pair that has been imported before is
   skipped, whatever has happened to it since. Re-running is free.

3. **Nothing outside setu_* is written.** The raw corpus and Tulana Studio's
   tables are read, never changed. The aligned editions get their own books —
   one per side per pair, because the dataset merges an English book
   differently for every language it is paired with — and they are kept out of
   the free textbook dropdowns, where pairing an aligned English book with a
   raw Marathi one would mean nothing.
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Iterable

from . import ids
from .annotate import MODEL_PREFIX, same_text
from .corpus import NOISE_KINDS, _Walk, _index_fts
from .models import (
    DEFAULT_STATUS, has_math, has_table, item_number, kind_for,
    math_fingerprints, normalise, structural_numbers,
)
from .store import Invalid, Repository

log = logging.getLogger("setu.aligned")

#: The folder name the dataset ships under.
DATASET = "aligned-docMT-test"

#: Marks a book as an aligned edition. Stored in ``setu_book.dedup_key``, which
#: raw books fill with a content hash, so the two can never collide.
MARK = "aligned:"

#: Corrections credited to a model start with MODEL_PREFIX ("model:"), defined
#: in annotate.py where "corrected" is decided. A person's name is stripped of
#: it on the way in (see api._actor), so nobody can type their way into looking
#: like the model, or the model into looking like a person.

#: The model's own confidence label, as a number Setu can sort and filter by.
#: Not a calibrated probability — the dataset says so — only an ordering.
CONFIDENCE = {"high": 0.9, "medium": 0.6, "low": 0.3}

#: The README's pair codes for boards, for when the raw book is not ingested.
BOARD_FROM_PAIR = {"MH": "MH", "KER": "KL", "AP": "AP", "KT": "KA", "PUN": "PB",
                   "TM": "TN", "GUJ": "GJ", "NCERT": "NCERT"}

_PAIR_RE = re.compile(r"^(?P<board>[A-Z]+?)_?(?P<cls>\d{1,2})")
_EN_PAGE = re.compile(r"/p(\d+)/u\d+$")

#: A pair id is the folder's name, and it ends up in identifiers and labels —
#: never in a path. Anything outside this shape is refused rather than cleaned.
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.+-]{0,79}$")

#: No file in the set is near this; a file far past it is not a layout file.
MAX_FILE_BYTES = 64 * 1024 * 1024


def safe_relpath(rel: Any) -> str:
    """A book's relative path from a layout file, or Invalid.

    The relpath decides which raw file is read to rebuild the OCR text and,
    later, which PDF a page picture is cut from. It comes from a JSON file, so
    it is treated as untrusted: relative, inside its folder, no "..", no drive,
    no NUL — or the pair is not imported at all.
    """
    if not isinstance(rel, str):
        raise Invalid("a layout file has no relpath")
    r = rel.replace("\\", "/").strip()
    parts = [x for x in r.split("/") if x not in ("", ".")]
    if (not r or len(r) > 400 or "\x00" in r or r.startswith("/")
            or re.match(r"^[A-Za-z]:", r) or ".." in parts or not parts):
        raise Invalid("a layout file names an unsafe relpath")
    return "/".join(parts)


# ── finding things ─────────────────────────────────────────────────────────

def find_dataset(root: Any = None) -> Path | None:
    """Locate the aligned test set. ``TULANA_ALIGNED_DIR`` wins if set."""
    env = os.environ.get("TULANA_ALIGNED_DIR", "").strip()
    candidates: list[Path] = []
    if env:
        candidates.append(Path(env))
    if root:
        candidates += [Path(root), Path(root) / DATASET]
    here = Path(__file__).resolve()
    repo = here.parents[3]                       # tulana/annotation/core/ → repo
    candidates += [repo / DATASET, here.parents[2] / DATASET]
    try:
        import config
        data = Path(config.DATA_DIR)
        candidates += [data / DATASET, data.parent / DATASET, data.parent.parent / DATASET]
    except Exception:                            # pragma: no cover - config shape
        pass
    for c in candidates:
        try:
            if c.is_dir() and any(c.glob("*/**/*.json")):
                return c.resolve()
        except OSError:
            continue
    return None


def _pair_dirs(dataset: Path) -> list[Path]:
    return sorted(p for p in dataset.iterdir()
                  if p.is_dir() and not p.name.startswith((".", "__")))


def _inside(path: Path, folder: Path) -> bool:
    """True when *path*, symlinks followed, really is inside *folder*."""
    try:
        return path.resolve().is_relative_to(folder.resolve())
    except (OSError, ValueError):
        return False


def _side_files(pair_dir: Path) -> list[Path]:
    return sorted(f for f in pair_dir.rglob("*.json")
                  if not any(part.startswith((".", "__"))
                             for part in f.relative_to(pair_dir).parts)
                  and f.is_file() and _inside(f, pair_dir))


@lru_cache(maxsize=1)
def _raw_index_cached(raw_root: str) -> dict[str, str]:
    """relpath → raw layout JSON, for rebuilding what the OCR read."""
    import blocks
    out: dict[str, str] = {}
    root = Path(raw_root)
    for f in root.rglob("*.json"):
        try:
            if blocks._is_junk(f.relative_to(root)):
                continue
            with f.open(encoding="utf-8") as fh:
                head = json.load(fh)
        except Exception:
            continue
        if isinstance(head, dict) and "pages" in head and "alignment" not in head:
            rel = str(head.get("relpath") or "").replace("\\", "/")
            if rel and rel not in out:
                out[rel] = str(f)
    return out


def raw_index() -> dict[str, str]:
    import blocks
    root = blocks.find_corpus()
    return _raw_index_cached(str(root)) if root else {}


def raw_path_for(relpath: str) -> str:
    """The raw layout file for a book, found where it should be first.

    The delivery stores each book's JSON at its PDF's relative path with the
    extension changed, so that is tried before falling back to reading every
    file in the corpus to find it.
    """
    import blocks
    root = blocks.find_corpus()
    if not root:
        return ""
    try:
        rel = Path(safe_relpath(relpath)).with_suffix(".json")
    except Invalid:
        return ""
    for base in (root, root / "output"):
        f = base / rel
        try:
            if f.is_file() and _inside(f, root) and f.stat().st_size <= MAX_FILE_BYTES:
                with f.open(encoding="utf-8") as fh:
                    head = json.load(fh)
                if str(head.get("relpath", "")).replace("\\", "/") == str(relpath) \
                        and "alignment" not in head:
                    return str(f)
        except Exception:
            continue
    return raw_index().get(str(relpath), "")


@lru_cache(maxsize=6)
def _raw_pages(path: str) -> dict[int, dict[int, str]]:
    """page → block order → text, for one raw book (cached: an English book is
    the source of up to five pairs). A malformed page or block is skipped, not
    fatal: what can be read is still the OCR, and the rest falls back below."""
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    out: dict[int, dict[int, str]] = {}
    for p in (doc.get("pages") or []) if isinstance(doc, dict) else []:
        try:
            page = int(p["page"])
        except (TypeError, ValueError, KeyError):
            continue
        blocks_ = out.setdefault(page, {})
        for b in p.get("blocks") or []:
            try:
                blocks_[int(b["order"])] = str(b.get("text") or "")
            except (TypeError, ValueError, KeyError, AttributeError):
                continue
    return out


def _int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _load(path: Path) -> dict:
    """One aligned layout file, checked for the shape the importer relies on.

    Everything in it is data from outside: a page or block of the wrong shape
    makes the whole pair refuse to import (and say which file), rather than
    import half of it.
    """
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            raise Invalid(f"{path.name} is too large to be a layout file")
        with path.open(encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Invalid(f"{path.name} could not be read ({type(exc).__name__})") from None
    if not isinstance(doc, dict) or not isinstance(doc.get("pages"), list) \
            or not isinstance(doc.get("alignment"), dict):
        raise Invalid(f"{path.name} is not an aligned layout file")
    doc["relpath"] = safe_relpath(doc.get("relpath"))
    doc["book"] = str(doc.get("book") or Path(doc["relpath"]).stem)[:120]
    for p in doc["pages"]:
        if not isinstance(p, dict) or not isinstance(p.get("blocks"), list) \
                or isinstance(p.get("page"), bool) or not isinstance(p.get("page"), int) \
                or p["page"] < 0:
            raise Invalid(f"{path.name}: a page is malformed")
        for b in p["blocks"]:
            if not isinstance(b, dict) or not isinstance(b.get("text", ""), str):
                raise Invalid(f"{path.name}: a block on page {p['page'] + 1} is malformed")
            members = b.get("members")
            if members is not None and not (isinstance(members, list) and all(
                    isinstance(m, dict) and isinstance(m.get("order"), int) for m in members)):
                raise Invalid(f"{path.name}: a block on page {p['page'] + 1} has bad members")
            if not isinstance(b.get("flags", []), list):
                b["flags"] = [str(b["flags"])]
            for key in ("align_id", "align_relation", "align_confidence", "align_note", "label",
                        "type"):
                if b.get(key) is not None and not isinstance(b.get(key), str):
                    b[key] = str(b[key])
    return doc


# ── reading one pair ───────────────────────────────────────────────────────

def read_pair(pair_dir: Path) -> dict:
    """Both sides of one pair, as {"pair_id", "src": side, "tgt": side}.

    A side is {"doc", "pages", "language", "lang", "relpath", "book"}. The two
    bilingual Andhra Pradesh books hold both languages in ONE file — English on
    the odd pages, from 13 on, and the Telugu on the even page after — so that
    file is split into two sides by page.
    """
    # The folder's name IS the pair id (the dataset's README says so), and it
    # is what the importer checks before reading anything, so it is the one
    # used — whatever the files say.
    pair_id = pair_dir.name
    if not _SAFE_ID.match(pair_id):
        raise Invalid("a pair folder has a name that is not a pair id")
    files = _side_files(pair_dir)
    if len(files) > 4:
        raise Invalid(f"{pair_id}: more layout files than one pair can have")
    docs = [(f, _load(f)) for f in files]
    if not docs:
        raise Invalid(f"{pair_id}: no layout files")

    def side(doc, pages, language, lang):
        return {"doc": doc, "pages": pages, "language": language, "lang": lang,
                "relpath": doc["relpath"], "book": doc["book"]}

    if len(docs) == 1:
        doc = docs[0][1]
        meta = doc["alignment"]
        langs = [s.strip() for s in str(meta.get("language", "")).split("+")]
        if len(langs) != 2 or not all(langs):
            raise Invalid(f"{pair_id}: one file, but not a bilingual book")
        en_pages = _english_pages_of_bilingual(doc)
        src = [p for p in doc["pages"] if p["page"] in en_pages]
        tgt = [p for p in doc["pages"] if p["page"] not in en_pages]
        return {"pair_id": pair_id, "bilingual": True,
                "src": side(doc, src, langs[0], "en"),
                "tgt": side(doc, tgt, langs[1], str(meta.get("lang", "")).split("+")[-1])}

    by_lang = {d["alignment"].get("lang"): (f, d) for f, d in docs}
    if "en" not in by_lang or len(docs) != 2 or len(by_lang) != 2:
        raise Invalid(f"{pair_id}: expected one English file and one other")
    en = by_lang.pop("en")[1]
    (lang, (_, tg)), = by_lang.items()
    return {"pair_id": pair_id, "bilingual": False,
            "src": side(en, en["pages"], en["alignment"].get("language") or "English", "en"),
            "tgt": side(tg, tg["pages"], tg["alignment"].get("language") or "", lang)}


def _english_pages_of_bilingual(doc: dict) -> set[int]:
    """Pages that hold the English side of a bilingual book.

    The unit id says it outright: ``…/p013/u4`` names the English page. Pages
    no unit touches (front matter, failed pages) follow the book's pattern —
    odd pages English — so the two sides stay complete.
    """
    named = set()
    for p in doc["pages"]:
        for b in p["blocks"]:
            m = _EN_PAGE.search(b.get("align_id") or "")
            if m:
                named.add(int(m.group(1)))
    odd = sum(1 for n in named if n % 2) >= len(named) / 2 if named else True
    return {p["page"] for p in doc["pages"]
            if p["page"] in named or (p["page"] % 2 == (1 if odd else 0))}


# ── building one side ──────────────────────────────────────────────────────

def _side_segments(side: dict, book_key: str, raw: dict[int, dict[int, str]]) -> tuple[list, dict]:
    """Segments for one side, in reading order, plus their hints.

    One segment per merged block. A unit that runs onto a second page is ONE
    passage to an annotator, so its later parts are folded into the segment of
    its first part: text joined, members joined, the box and page of the first
    part kept, and the pages it covers recorded in the hint.
    """
    state = _Walk()
    segs: list[dict] = []
    by_unit: dict[str, dict] = {}
    for p in sorted(side["pages"], key=lambda x: x["page"]):
        page = int(p["page"])
        try:
            w = float(p.get("width") or 0) or 1.0
            h = float(p.get("height") or 0) or 1.0
        except (TypeError, ValueError):
            w = h = 1.0
        status = p.get("align_status") or ""
        for b in sorted(p["blocks"], key=lambda x: _int(x.get("order"))):
            members = b.get("members") or [{"order": _int(b.get("order"))}]
            page_raw = raw.get(page, {})
            raw_text = "\n\n".join(page_raw.get(_int(m.get("order"), -1), "") for m in members)
            if not raw and not raw_text:
                raw_text = b.get("text") or ""     # no raw book: the delivered text is all there is
            corrected = normalise(b.get("text") or "")
            raw_text = normalise(raw_text)
            aid = b.get("align_id") or ""
            if aid and aid in by_unit:            # a later part of a unit already met
                seg = by_unit[aid]
                seg["source"] = "\n\n".join(x for x in (seg["source"], raw_text) if x)
                seg["corrected"] = "\n\n".join(x for x in (seg["corrected"], corrected) if x)
                seg["members"] += [{"page": page, "order": _int(m.get("order"))} for m in members]
                seg["pages"].append(page)
                seg["flags"] += list(b.get("flags") or [])
                continue
            label = (b.get("label") or "").strip()
            state.observe(label, corrected)
            seg = {
                "page": page, "order": _int(b.get("order")), "label": label,
                "type": b.get("type") or "", "source": raw_text, "corrected": corrected,
                "box": _box(b.get("bbox_xyxy")),
                "w": w, "h": h, "members": [{"page": page, "order": _int(m.get("order"))}
                                            for m in members],
                "pages": [page], "align_id": aid,
                "relation": b.get("align_relation") or "",
                "confidence": b.get("align_confidence") or "",
                "note": b.get("align_note") or "", "flags": list(b.get("flags") or []),
                "page_status": status,
                "chapter": state.chapter, "chapter_no": state.chapter_no,
                "section": state.section, "section_no": state.section_no,
                "depth": state.depth,
            }
            segs.append(seg)
            if aid:
                by_unit[aid] = seg
    for i, seg in enumerate(segs):
        seg["seq"] = i
        seg["sid"] = ids.segment_id(book_key, seg["page"], seg["order"], seg["order"])
    return segs, by_unit


_NCERT = re.compile(r"^NCERT_(\d{4})_")
_PART_NO = re.compile(r"^[A-Za-z]+\d{1,2}_(?:sem)?(\d)_", re.I)


def part_of(pair_id: str, volume: str = "") -> str:
    """Which part of a book a pair is, as a person would name it.

    The raw book's own volume ("Part 1") when it has one; for NCERT, whose
    pairs are single chapters, the chapter file's code ("1001") — kept as a
    code on purpose: the class-12 codes do not equal chapter numbers (1211 is
    Chapter 7), so turning them into "Chapter 11" would be wrong.
    """
    if volume:
        return volume
    m = _NCERT.match(pair_id or "")
    if m:
        return m.group(1)
    m = _PART_NO.match(pair_id or "")
    return f"Part {m.group(1)}" if m else ""


def _box(v: Any) -> list[float]:
    """x0, y0, x1, y1 — or a zero box when the file's is not four numbers."""
    try:
        box = [float(x) for x in v]
        if len(box) == 4 and all(x == x and abs(x) < 1e7 for x in box):   # x == x: not NaN
            return box
    except (TypeError, ValueError):
        pass
    return [0.0, 0.0, 0.0, 0.0]


def _segment_rows(book_key: str, segs: list[dict]) -> list[tuple]:
    """The same 26 columns, in the same order, as corpus._build_book writes."""
    out = []
    for s in segs:
        text = s["source"]
        kind = kind_for(s["label"], s["corrected"] or text)
        x0, y0, x1, y1 = s["box"]
        out.append((
            s["sid"], book_key, s["seq"], s["page"], s["order"], s["order"], kind,
            s["label"], s["type"], s["chapter"], s["chapter_no"], s["section"],
            s["section_no"],
            item_number(s["corrected"]) if kind in
            {"example", "exercise", "question", "mcq", "theorem"} else "",
            s["depth"], text, len(text), int(has_math(text)), int(has_table(text)),
            json.dumps(s["members"]),
            x0 / s["w"], y0 / s["h"], x1 / s["w"], y1 / s["h"],
            json.dumps(math_fingerprints(s["corrected"]), ensure_ascii=False),
            json.dumps(structural_numbers(s["corrected"]), ensure_ascii=False),
        ))
    return out


# ── importing ──────────────────────────────────────────────────────────────

def book_key_for(pair_id: str, side: str, relpath: str) -> str:
    return ids.book_key(f"{DATASET}/{pair_id}/{side}/{relpath}")


def _raw_book(con, relpath: str) -> dict:
    row = con.execute("SELECT * FROM setu_book WHERE relpath = ? AND dedup_key NOT LIKE ?"
                      " ORDER BY length(book_key) LIMIT 1", (relpath, MARK + "%")).fetchone()
    return dict(row) if row else {}


def _insert_book(con, pair: dict, which: str, book_key: str, n_segments: int) -> dict:
    side = pair[which]
    raw = _raw_book(con, side["relpath"])
    m = _PAIR_RE.match(pair["pair_id"])
    board = raw.get("board") or (BOARD_FROM_PAIR.get(m.group("board"), m.group("board")) if m else "")
    cls = raw.get("class") or (int(m.group("cls")) if m else None)
    try:
        import config
        board_name = raw.get("board_name") or (config.board_name(board) if board else "")
        script = config.script_of(side["language"]) if side["language"] else ""
    except Exception:                            # pragma: no cover - config shape
        board_name, script = raw.get("board_name") or board, ""
    other = pair["tgt" if which == "src" else "src"]["language"]
    base = raw.get("title") or side["book"]
    if pair["bilingual"]:
        # The raw book is filed under one language, so its title names it —
        # "… · English · Part 1" — and would put "English" on the Telugu side.
        bits = [board_name or board, f"Class {cls}" if cls else "",
                raw.get("subject") or "Mathematics", raw.get("volume") or ""]
        title = (" · ".join(b for b in bits if b) +
                 f" · {side['language']} pages of the two-language book · aligned with {other}")
    else:
        part = part_of(pair["pair_id"], raw.get("volume") or "")
        extra = f" · {part}" if part and part not in base else ""
        title = f"{base}{extra} · aligned with {other}"
    con.execute(
        "INSERT INTO setu_book(book_key, pl_book_id, dedup_key, book, relpath, board,"
        " board_name, class, subject, language, script, volume, title, num_pages,"
        " n_blocks, n_segments, pdf_present, ingested_at)"
        " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (book_key, int(raw.get("pl_book_id") or 0), f"{MARK}{pair['pair_id']}:{which}",
         side["book"], side["relpath"], board, board_name, cls,
         raw.get("subject") or "Mathematics", side["language"], raw.get("script") or script,
         raw.get("volume") or "", title, int(side["doc"].get("num_pages") or 0),
         sum(len(p["blocks"]) for p in side["pages"]), n_segments,
         int(raw.get("pdf_present") or 0), time.time()))
    return {"board": board, "board_name": board_name, "class": cls,
            "volume": raw.get("volume") or ""}


def _drop_orphans(con, pair_id: str) -> int:
    """Clear this pair's aligned books when no project uses them any more.

    That happens only when the pair's project was deleted on purpose. Nothing a
    person did can be lost here — answers and corrections live under the
    project, which is already gone — and the books are rebuilt from the files
    straight after, so a deleted pair comes back exactly as imported.
    """
    keys = [r[0] for r in con.execute(
        "SELECT b.book_key FROM setu_book b WHERE b.dedup_key IN (?, ?)"
        "   AND NOT EXISTS (SELECT 1 FROM setu_project p"
        "                    WHERE p.src_book = b.book_key OR p.tgt_book = b.book_key)",
        (f"{MARK}{pair_id}:src", f"{MARK}{pair_id}:tgt"))]
    from .store import fts_ready
    for key in keys:
        if fts_ready(con):
            con.execute("DELETE FROM setu_seg_fts WHERE book_key = ?", (key,))
        con.execute("DELETE FROM setu_book WHERE book_key = ? AND dedup_key LIKE ?",
                    (key, MARK + "%"))
    if keys:
        log.info("aligned pair %s: its project had been deleted; re-importing it", pair_id)
    return len(keys)


def is_imported(con, pair_id: str) -> str:
    """The project id of an imported pair, or ''."""
    row = con.execute(
        "SELECT p.pid FROM setu_project p JOIN setu_book b ON b.book_key = p.src_book"
        " WHERE b.dedup_key = ?", (f"{MARK}{pair_id}:src",)).fetchone()
    return row[0] if row else ""


def import_pair(con, pair_dir: Path, *, actor: str = "setu import") -> dict:
    """Import one pair as a project whose rows are the model's units.

    Must run inside a transaction: a pair is imported whole or not at all.
    """
    from .workspace import create_project

    pair = read_pair(pair_dir)
    pid = is_imported(con, pair["pair_id"])
    if pid:
        return {"pair_id": pair["pair_id"], "pid": pid, "skipped": True}
    _drop_orphans(con, pair["pair_id"])

    built = {}
    for which in ("src", "tgt"):
        side = pair[which]
        key = book_key_for(pair["pair_id"], which, side["relpath"])
        raw_path = raw_path_for(side["relpath"])
        raw = _raw_pages(raw_path) if raw_path else {}
        if pair["bilingual"]:
            raw = {pg: b for pg, b in raw.items() if pg in {p["page"] for p in side["pages"]}}
        segs, units = _side_segments(side, key, raw)
        rows = _segment_rows(key, segs)
        meta = _insert_book(con, pair, which, key, len(rows))
        con.executemany(
            "INSERT INTO setu_segment(sid, book_key, seq, page, ord_start, ord_end, kind,"
            " label, block_type, chapter, chapter_no, section, section_no, item_no, depth,"
            " source_text, n_chars, has_math, has_table, block_ids, fx0, fy0, fx1, fy1,"
            " anchor_math, anchor_num) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            rows)
        _index_fts(con, key, rows)
        con.executemany(
            "INSERT INTO setu_hint(sid, pair_id, align_id, relation, confidence, note, flags,"
            " parts, pages, page_status) VALUES(?,?,?,?,?,?,?,?,?,?)",
            [(s["sid"], pair["pair_id"], s["align_id"], s["relation"], s["confidence"],
              s["note"], json.dumps(s["flags"], ensure_ascii=False), len(s["pages"]),
              json.dumps(s["pages"]), s["page_status"]) for s in segs])
        built[which] = {"key": key, "segs": segs, "units": units, "raw_found": bool(raw_path),
                        "meta": meta}

    proj = create_project(con, src_book=built["src"]["key"], tgt_book=built["tgt"]["key"],
                          name=_project_name(pair, built["src"]["meta"]), annotator=actor,
                          build=False)
    pid = proj["pid"]
    n_rows, n_model = _insert_rows(con, pid, built, actor)
    Repository(con).event("aligned.import", pid,
                          {"pair_id": pair["pair_id"], "rows": n_rows,
                           "model_corrections": n_model}, actor=actor)
    return {"pair_id": pair["pair_id"], "pid": pid, "skipped": False, "rows": n_rows,
            "units": len(built["src"]["units"]), "model_corrections": n_model,
            "raw_found": built["src"]["raw_found"] and built["tgt"]["raw_found"]}


def _project_name(pair: dict, meta: dict) -> str:
    who = meta.get("board_name") or meta.get("board") or ""
    cls = f" Class {meta['class']}" if meta.get("class") else ""
    part = part_of(pair["pair_id"], meta.get("volume") or "")
    return (f"{who}{cls}{' · ' + part if part else ''} — {pair['src']['language']} ⇄ "
            f"{pair['tgt']['language']} · aligned test set ({pair['pair_id']})").strip()


def wants_row(seg: dict) -> bool:
    """Whether a passage the model left unpaired gets a row of its own.

    Only when there is something to check: some text, and not a page header,
    footer, page number or picture — the same things Setu leaves out of every
    other project. The rest stay in the book (shown with "Include headers and
    page numbers", and pairable by hand); they are just not a to-do. Every one
    of the model's pairs is a row whatever it holds.
    """
    if not (str(seg.get("source") or "").strip() or str(seg.get("corrected") or "").strip()):
        return False
    if seg.get("note") == "page_furniture":
        return False
    return kind_for(seg.get("label") or "",
                    seg.get("corrected") or seg.get("source") or "") not in NOISE_KINDS


def _insert_rows(con, pid: str, built: dict, actor: str) -> tuple[int, int]:
    """Rows in English reading order, the model's units paired, and every other
    passage worth checking standing alone where it falls — so nothing the model
    left out is hidden from the annotator."""
    src, tgt = built["src"]["segs"], built["tgt"]["segs"]
    tgt_units = built["tgt"]["units"]
    tgt_alone = [t for t in tgt
                 if (not t["align_id"] or t["align_id"] not in built["src"]["units"])
                 and wants_row(t)]
    plan: list[tuple[dict | None, dict | None]] = []
    k = 0
    for s in src:
        t = tgt_units.get(s["align_id"]) if s["align_id"] else None
        if t is not None:
            while k < len(tgt_alone) and tgt_alone[k]["seq"] < t["seq"]:
                plan.append((None, tgt_alone[k])); k += 1
            plan.append((s, t))
        elif wants_row(s):
            plan.append((s, None))
    plan += [(None, t) for t in tgt_alone[k:]]

    now = time.time()
    carried = {"chapter": "", "chapter_no": "", "section": "", "section_no": ""}
    rows, texts, revs = [], [], []
    model = MODEL_PREFIX + _model_name(built)
    for seq, (s, t) in enumerate(plan):
        if s:
            carried = {c: s[c] for c in carried}
        elif not any(carried.values()) and t:
            carried = {c: t[c] for c in carried}
        rid = ids.row_id(pid, seq)
        conf = 0.0
        if s and t:
            conf = min(CONFIDENCE.get(s["confidence"], 0.5), CONFIDENCE.get(t["confidence"], 0.5))
        anchor = s or t
        rows.append((rid, pid, seq, s["sid"] if s else None, t["sid"] if t else None,
                     DEFAULT_STATUS, "aligned" if (s and t) else "unpaired", conf, "",
                     carried["chapter"], carried["chapter_no"], carried["section"],
                     carried["section_no"], kind_for(anchor["label"], anchor["corrected"]),
                     s["page"] if s else None, t["page"] if t else None, now, now, actor[:120]))
        for side, seg in (("src", s), ("tgt", t)):
            if seg and seg["corrected"] and not same_text(seg["corrected"], seg["source"]):
                texts.append([rid, side, seg["corrected"], 1, now, model])
                revs.append([rid, side, 1, seg["corrected"], model, "", "model-correction", now])
    # Revision numbers continue any history these row ids already have. Row ids
    # are positional, so a pair whose project was deleted and is imported again
    # gets the same ids back — and the history of the old one is kept on
    # purpose (setu_rev is append-only). Starting again at 1 would collide.
    held = _last_revs(con, sorted({r[0] for r in revs}))
    for text, rev in zip(texts, revs):
        n = held.get((rev[0], rev[1]), 0) + 1
        text[3] = rev[2] = n
    con.executemany(
        "INSERT INTO setu_row(rid, pid, seq, src_sid, tgt_sid, status, origin, confidence,"
        " note, chapter, chapter_no, section, section_no, kind, src_page, tgt_page,"
        " created_at, updated_at, updated_by) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        rows)
    con.executemany("INSERT INTO setu_text(rid, side, text, rev, updated_at, updated_by)"
                    " VALUES(?,?,?,?,?,?)", texts)
    con.executemany("INSERT INTO setu_rev(rid, side, rev, text, actor, session, reason, ts)"
                    " VALUES(?,?,?,?,?,?,?,?)", revs)
    con.execute("UPDATE setu_project SET n_rows = ?, built_at = ? WHERE pid = ?",
                (len(rows), now, pid))
    return len(rows), len(texts)


def _last_revs(con, rids: list[str]) -> dict[tuple[str, str], int]:
    """(rid, side) → highest revision already recorded, for the given rows."""
    out: dict[tuple[str, str], int] = {}
    for i in range(0, len(rids), 400):
        chunk = rids[i:i + 400]
        marks = ",".join("?" * len(chunk))
        for rid, side, top in con.execute(
                f"SELECT rid, side, MAX(rev) FROM setu_rev WHERE rid IN ({marks})"
                " GROUP BY rid, side", chunk):
            out[(rid, side)] = int(top or 0)
    return out


def _model_name(built: dict) -> str:
    return "gemini-3.5-flash"


def import_all(connect: Callable, dataset: Any = None, *, actor: str = "setu import",
               log_fn: Callable[[str], None] = log.info) -> dict:
    """Import every pair not imported yet. One transaction per pair.

    ``connect`` is a context manager factory yielding a connection inside a
    transaction (store.tx). A pair that fails is reported and skipped; the
    others still import.
    """
    root = find_dataset(dataset)
    report = {"dataset": str(root or ""), "pairs": 0, "imported": 0, "skipped": 0,
              "rows": 0, "model_corrections": 0, "errors": [], "raw_missing": []}
    if not root:
        return report
    started = time.time()
    for pair_dir in _pair_dirs(root):
        report["pairs"] += 1
        try:
            with connect() as con:
                if is_imported(con, _pair_id_of(pair_dir)):
                    report["skipped"] += 1
                    continue
                out = import_pair(con, pair_dir, actor=actor)
            if out.get("skipped"):
                report["skipped"] += 1
                continue
            report["imported"] += 1
            report["rows"] += out["rows"]
            report["model_corrections"] += out["model_corrections"]
            if not out["raw_found"]:
                report["raw_missing"].append(out["pair_id"])
        except Invalid as exc:                   # a bad file: say which, and why, in one line
            log.warning("aligned pair %r not imported: %s", pair_dir.name[:80], exc)
            report["errors"].append({"pair": pair_dir.name, "error": f"Invalid: {exc}"})
        except Exception as exc:                 # one bad pair must not stop the rest
            log.exception("aligned import failed for %r", pair_dir.name[:80])
            report["errors"].append({"pair": pair_dir.name, "error": f"{type(exc).__name__}: {exc}"})
    report["seconds"] = round(time.time() - started, 1)
    if report["imported"]:
        log_fn(f"aligned test set: imported {report['imported']} pair(s), "
               f"{report['rows']:,} rows, {report['model_corrections']:,} model corrections "
               f"in {report['seconds']}s")
    return report


def _pair_id_of(pair_dir: Path) -> str:
    """The pair id without parsing the JSON — the folder is named after it."""
    return pair_dir.name


# ── reading it back ────────────────────────────────────────────────────────

def pairs(con) -> list[dict]:
    """Every imported pair, with how far its verification has got."""
    rows = con.execute(
        """SELECT p.pid, p.name, p.board, p.class, p.src_language, p.tgt_language,
                  p.src_book, p.tgt_book, p.n_rows, b.board_name, b.volume,
                  substr(b.dedup_key, length(?) + 1,
                         length(b.dedup_key) - length(?) - 4) AS pair_id,
                  (SELECT COUNT(*) FROM setu_row r WHERE r.pid = p.pid
                     AND r.status <> 'pending') AS answered,
                  (SELECT COUNT(*) FROM setu_row r WHERE r.pid = p.pid
                     AND r.src_sid IS NOT NULL AND r.tgt_sid IS NOT NULL) AS units,
                  (SELECT COUNT(*) FROM setu_row r
                    WHERE r.pid = p.pid AND EXISTS (
                      SELECT 1 FROM setu_hint h WHERE h.sid IN (r.src_sid, r.tgt_sid)
                         AND h.flags <> '[]')) AS flagged
             FROM setu_project p JOIN setu_book b ON b.book_key = p.src_book
            WHERE b.dedup_key LIKE ?
            ORDER BY p.board, p.class, p.tgt_language, pair_id""",
        (MARK, MARK, MARK + "%")).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["part"] = part_of(d.get("pair_id") or "", d.pop("volume", "") or "")
        out.append(d)
    return out


def status(con, dataset: Any = None) -> dict:
    """What is on disk, and what has been imported from it."""
    root = find_dataset(dataset)
    on_disk = [p.name for p in _pair_dirs(root)] if root else []
    done = {r["pair_id"] for r in pairs(con)}
    return {"dataset": str(root or ""), "on_disk": len(on_disk),
            "imported": len(done & set(on_disk)) if on_disk else len(done),
            "waiting": sorted(set(on_disk) - done)}
