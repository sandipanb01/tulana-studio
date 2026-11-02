"""The aligned document-MT test set: pre-aligned, pre-corrected pairs to verify.

``data/aligned_v2/`` (an older checkout: ``aligned-docMT-test/`` next to
``board_outputs/``) holds, for 62 book pairs,
the parser's layout JSON for both editions after an alignment model
(gemini-3.5-flash, prompt v4) has

  * aligned each English page to its translation — blocks that share an
    ``align_id`` are translations of each other;
  * merged the OCR blocks of one translation unit into a single block per page,
    keeping the original blocks under ``members`` — and, in the paragraph-level
    export, joined consecutive units of one paragraph (``merged_units``);
  * applied small OCR corrections that passed code checks, and left ``flags``
    for a reviewer where it was not allowed to change anything;
  * (paragraph-level export) said for every block whether it is aligned and,
    if not, why (``aligned``, ``align_state``), and counted it per page
    (``align_summary``) and per book (``alignment.summary``).

Its own README says what it is for: pre-annotation for HUMAN verification, not
a final reference. This module turns each pair into a Setu project whose rows
ARE the model's pairs, so an annotator checks the model's work instead of
starting from Setu's heuristic alignment.

Four rules, in order of how much damage breaking them would do:

1. **What the OCR read stays the source.** Every merged block's
   ``source_text`` is rebuilt from the RAW layout in ``board_outputs`` by
   joining its members — byte for byte what the parser read. Where the model
   changed the text, its version is written as the FIRST REVISION of that
   passage, credited to the model. So "Put back what the parser read" undoes
   the model, the history shows exactly what it changed, and an annotator's own
   corrections land on top.

2. **Importing never overwrites work.** A pair that has been imported is never
   touched again. A NEW delivery in the folder — recognised by a hash of its
   contents — is a new *set*: its pairs become new projects, and the projects
   of every earlier set stay exactly as they are, answers and all.

3. **Nothing outside setu_* is written.** The raw corpus and Tulana Studio's
   tables are read, never changed. The aligned editions get their own books —
   one per side per pair per set, because a delivery merges an English book
   differently for every language and every version — and they are kept out of
   the free textbook dropdowns.

4. **Everything in the folder is untrusted.** Paths, shapes and sizes are
   checked before anything is written; a bad pair is refused whole and named,
   and the others still import.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import threading
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

from . import ids
from .annotate import MODEL_PREFIX, same_text
from .corpus import NOISE_KINDS, _Walk, _index_fts
from .models import (
    DEFAULT_STATUS, has_math, has_table, item_number, kind_for,
    math_fingerprints, normalise, structural_numbers,
)
from .store import Invalid, Repository

log = logging.getLogger("setu.aligned")

#: The name the dataset first shipped under. It is also the namespace of every
#: aligned book's key (book_key_for), so a key never depends on where the
#: folder happens to sit; moving the data does not orphan anyone's work.
DATASET = "aligned-docMT-test"

#: Where the dataset is looked for, in this order, under the repository: the
#: aligner team's served version, then the older folder name.
LOCATIONS = (("data", "aligned_v2"), (DATASET,))

#: Marks a book as an aligned edition. Stored in ``setu_book.dedup_key``, which
#: raw books fill with a content hash, so the two can never collide. The full
#: key is ``aligned:<set_id>:<pair_id>:<side>``; books imported before sets
#: existed carry ``aligned:<pair_id>:<side>`` and belong to LEGACY_SET.
MARK = "aligned:"

#: The set every pair imported before versions existed belongs to: the
#: unit-level delivery, as Setu v7 imported it.
LEGACY_SET = "as_LEGACYUNIT"

#: Block states the paragraph-level export writes (``align_state``). v2 adds
#: ``page_dropped``: text on an English page the aligner team dropped (its
#: page map was wrong, its alignment failed, or nothing on it matched), and the
#: translation of any unit that had a part there — unlinked on both sides.
STATES = ("aligned", "unpaired", "page_failed", "not_processed", "no_text", "page_dropped")
#: The counts kept per page and per pair, in original OCR blocks.
COUNTS = ("text_blocks", "aligned", "unpaired", "page_failed", "not_processed", "page_dropped")
#: Why v2 dropped an English page (``drop_reason``).
DROP_REASONS = ("map_wrong", "alignment_failed", "nothing_matched", "unparseable")
#: The states that mean "text the model could not pair" — what an annotator
#: has to look at. The viewer the aligner team uses draws these in red.
NOT_ALIGNED = ("unpaired", "page_failed")

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
#: Model names and unit ids come from the files; they are labels, kept short.
_SAFE_LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/+-]{0,119}$")

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


def shown_name(name: Any) -> str:
    """A folder name fit to print or send back: as it is when it is a proper
    pair id, otherwise escaped (no control characters reach a terminal) and cut."""
    s = str(name)
    return s if _SAFE_ID.match(s) else ascii(s)[:80]


def parse_mark(dedup_key: Any) -> tuple[str, str, str] | None:
    """``(set_id, pair_id, side)`` for an aligned book's dedup key, else None."""
    key = str(dedup_key or "")
    if not key.startswith(MARK):
        return None
    bits = key[len(MARK):].split(":")
    if len(bits) == 3 and bits[2] in ("src", "tgt"):
        return bits[0], bits[1], bits[2]
    if len(bits) == 2 and bits[1] in ("src", "tgt"):
        return LEGACY_SET, bits[0], bits[1]
    return None


# ── finding things ─────────────────────────────────────────────────────────

def find_dataset(root: Any = None) -> Path | None:
    """Locate the aligned test set.

    ``TULANA_ALIGNED_DIR`` wins if set, then *root* (a folder named on the
    command line). Otherwise ``data/aligned_v2`` in the repository — the
    version the aligner team serves — and, for an older checkout, the
    ``aligned-docMT-test`` folder beside ``board_outputs/``.
    """
    env = os.environ.get("TULANA_ALIGNED_DIR", "").strip()
    candidates: list[Path] = []
    if env:
        candidates.append(Path(env))
    if root:
        # A repository named as the root holds the data inside it: look there
        # first, or its board_outputs/ would pass for the dataset itself.
        candidates += [Path(root).joinpath(*loc) for loc in LOCATIONS]
        candidates.append(Path(root))
    here = Path(__file__).resolve()
    bases = [here.parents[3], here.parents[2]]   # the repository, then tulana/
    try:
        import config
        data = Path(config.DATA_DIR)
        bases += [data, data.parent, data.parent.parent]
    except Exception:                            # pragma: no cover - config shape
        pass
    for loc in LOCATIONS:                        # the newer location first, wherever it is
        candidates += [base.joinpath(*loc) for base in bases]
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


# ── which delivery is in the folder ────────────────────────────────────────

_DESC_CACHE: dict[str, tuple[tuple, dict]] = {}
_DESC_LOCK = threading.Lock()


def _set_files(root: Path) -> list[Path]:
    """The files that make up a delivery: its JSON and TSV, nothing hidden."""
    out = []
    for f in root.rglob("*"):
        try:
            rel = f.relative_to(root)
            if any(part.startswith((".", "__")) for part in rel.parts):
                continue
            if f.suffix.lower() in (".json", ".tsv") and f.is_file() and _inside(f, root):
                out.append(f)
        except (OSError, ValueError):
            continue
    return sorted(out, key=lambda f: f.relative_to(root).as_posix())


def describe(root: Path) -> dict:
    """What delivery is in the folder: a hash of its contents, and its shape.

    The hash is what tells one delivery from the next — a re-export in the
    same folder, with the same pair ids, is still a different set of pairs. It
    is computed once and kept until a file in the folder changes size or time,
    so asking is cheap.
    """
    root = Path(root)
    files = _set_files(root)
    sig = tuple((f.relative_to(root).as_posix(), f.stat().st_size, f.stat().st_mtime_ns)
                for f in files)
    with _DESC_LOCK:
        hit = _DESC_CACHE.get(str(root))
        if hit and hit[0] == sig:
            return dict(hit[1])
    h = hashlib.sha256()
    for f in files:
        h.update(f.relative_to(root).as_posix().encode("utf-8") + b"\0")
        size = f.stat().st_size
        if size > MAX_FILE_BYTES:                # never imported; its size is enough
            h.update(str(size).encode())
        else:
            # Line endings as git wrote them on this machine (Windows checks
            # text out with CRLF) must not make the same delivery look new.
            h.update(f.read_bytes().replace(b"\r\n", b"\n"))
        h.update(b"\0")
    desc = {"fingerprint": h.hexdigest(), "folder": root.name[:120], "level": "unit",
            "version": "", "pairs": len(_pair_dirs(root)), "segments": 0, "units": 0,
            "model": "", "prompt": ""}
    try:
        summary = json.loads((root / "export_summary.json").read_text(encoding="utf-8"))
        if isinstance(summary, list):
            entries = [e for e in summary if isinstance(e, dict)]
            # v2 keeps v1's unit count and says how many it unlinked.
            desc["segments"] = sum(max(0, _int(e.get("units")) - _int(_v2(e).get("units_removed")))
                                   for e in entries)
            desc["units"] = sum(_int(e.get("units_before_merge") or e.get("units"))
                                for e in entries)
            merges = {str(e.get("merge")) for e in entries if e.get("merge")}
            if "paragraph" in merges:
                desc["level"] = "paragraph"
            if any(_v2(e) for e in entries):
                desc["version"] = "v2"
    except (OSError, ValueError):
        pass
    for pair_dir in _pair_dirs(root)[:1]:
        for f in _side_files(pair_dir)[:1]:
            try:
                if f.stat().st_size <= MAX_FILE_BYTES:
                    meta = json.loads(f.read_text(encoding="utf-8")).get("alignment") or {}
                    desc["model"] = _label(meta.get("model"), "")
                    desc["prompt"] = _label(meta.get("prompt_version"), "")
            except (OSError, ValueError, AttributeError):
                pass
    with _DESC_LOCK:
        _DESC_CACHE[str(root)] = (sig, desc)
    return dict(desc)


def _v2(entry: dict) -> dict:
    v = entry.get("v2")
    return v if isinstance(v, dict) else {}


def set_label(level: str, version: str = "") -> str:
    name = {"paragraph": "paragraph-level", "unit": "unit-level"}.get(level, level or "")
    return f"{name} {version}".strip() if version in ("v2",) else name


def _legacy_books(con) -> bool:
    """Whether Setu v7 left aligned books here (keys without a set id)."""
    for (key,) in con.execute("SELECT dedup_key FROM setu_book WHERE dedup_key LIKE ?",
                              (MARK + "%",)):
        m = parse_mark(key)
        if m and m[0] == LEGACY_SET:
            return True
    return False


def _find_set(con, desc: dict) -> str:
    """The set a description belongs to, without creating anything, or ''."""
    row = con.execute("SELECT set_id FROM setu_aligned_set WHERE fingerprint = ?",
                      (desc["fingerprint"],)).fetchone()
    if row:
        return row[0]
    # The unit-level delivery Setu v7 imported, still in the folder: those are
    # the legacy pairs, not a new set to import a second time — whether or not
    # they have been adopted yet (status() asks before anything is written).
    if desc.get("level") == "unit":
        row = con.execute("SELECT fingerprint FROM setu_aligned_set WHERE set_id = ?",
                          (LEGACY_SET,)).fetchone()
        if (row and str(row[0]).startswith("legacy:")) or (not row and _legacy_books(con)):
            return LEGACY_SET
    return ""


def resolve_set(con, desc: dict) -> str:
    """The set the folder holds — created if it is new — made the current one.

    Must run inside a transaction.
    """
    adopt_legacy(con)
    sid = _find_set(con, desc)
    now = time.time()
    if sid == LEGACY_SET:
        # Legacy books whose projects were all deleted leave no set row behind.
        con.execute(
            "INSERT OR IGNORE INTO setu_aligned_set(set_id, fingerprint, level, label, folder,"
            " n_pairs, n_segments, n_units, model, prompt, first_seen, current)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,0)",
            (LEGACY_SET, desc["fingerprint"], "unit", set_label("unit"), desc["folder"],
             desc["pairs"], desc["segments"], desc["units"], desc["model"], desc["prompt"], now))
        con.execute("UPDATE setu_aligned_set SET fingerprint = ? WHERE set_id = ?"
                    "   AND fingerprint LIKE 'legacy:%'", (desc["fingerprint"], LEGACY_SET))
    elif not sid:
        sid = ids.derive("as", desc["fingerprint"])
        con.execute(
            "INSERT INTO setu_aligned_set(set_id, fingerprint, level, label, folder, n_pairs,"
            " n_segments, n_units, model, prompt, first_seen, current)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,0)",
            (sid, desc["fingerprint"], desc["level"],
             set_label(desc["level"], desc.get("version", "")), desc["folder"],
             desc["pairs"], desc["segments"], desc["units"], desc["model"], desc["prompt"], now))
    con.execute("UPDATE setu_aligned_set SET current = CASE WHEN set_id = ? THEN 1 ELSE 0 END",
                (sid,))
    return sid


def adopt_legacy(con) -> int:
    """Put the projects imported before sets existed into LEGACY_SET.

    Setu v7 imported the unit-level delivery with no notion of versions; its
    books carry ``aligned:<pair_id>:<side>``. They become one set, so they can
    be listed — and never imported a second time. Idempotent.
    """
    rows = con.execute(
        "SELECT p.pid, b.dedup_key FROM setu_project p"
        "  JOIN setu_book b ON b.book_key = p.src_book"
        " WHERE b.dedup_key LIKE ? AND NOT EXISTS"
        "       (SELECT 1 FROM setu_aligned_pair a WHERE a.pid = p.pid)", (MARK + "%",)).fetchall()
    legacy = []
    for pid, key in rows:
        m = parse_mark(key)
        if m and m[0] == LEGACY_SET:
            legacy.append((pid, m[1]))
    if not legacy:
        return 0
    now = time.time()
    con.execute(
        "INSERT OR IGNORE INTO setu_aligned_set(set_id, fingerprint, level, label, folder,"
        " n_pairs, n_segments, n_units, model, prompt, first_seen, current)"
        " VALUES(?, 'legacy:unit', 'unit', ?, ?, ?, 0, 0, 'gemini-3.5-flash', 'v4', ?, 0)",
        (LEGACY_SET, set_label("unit"), DATASET, len(legacy), now))
    con.executemany(
        "INSERT OR IGNORE INTO setu_aligned_pair(pid, set_id, pair_id, summary, imported_at)"
        " VALUES(?,?,?,'{}',?)", [(pid, LEGACY_SET, pair_id, now) for pid, pair_id in legacy])
    return len(legacy)


def current_set(con) -> dict:
    row = con.execute("SELECT * FROM setu_aligned_set WHERE current = 1"
                      " ORDER BY first_seen DESC LIMIT 1").fetchone()
    return dict(row) if row else {}


# ── reading the raw OCR ────────────────────────────────────────────────────

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
        except (TypeError, ValueError, KeyError, OverflowError):
            continue
        blocks_ = out.setdefault(page, {})
        for b in p.get("blocks") or []:
            try:
                blocks_[int(b["order"])] = str(b.get("text") or "")
            except (TypeError, ValueError, KeyError, AttributeError, OverflowError):
                continue
    return out


def _int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except (TypeError, ValueError, OverflowError):      # OverflowError: int(inf)
        return default


def _dim(v: Any) -> float:
    """A page's width or height in pixels — or 1 when it is not a sane number.

    Python's json reads NaN and Infinity, and a NaN that reached a response
    would make the whole page's JSON unsendable."""
    try:
        x = float(v)
    except (TypeError, ValueError, OverflowError):
        return 1.0
    return x if 0 < x < 1e7 else 1.0                    # NaN fails both comparisons


def _label(v: Any, default: str = "") -> str:
    s = str(v or "").strip()
    return s if _SAFE_LABEL.match(s) else default


def _counts(d: Any) -> dict | None:
    """A page or book summary from a file: non-negative counts, or None."""
    if not isinstance(d, dict):
        return None
    out = {}
    for k in COUNTS:
        v = d.get(k, 0)
        if isinstance(v, bool) or not isinstance(v, int) or v < 0 or v > 10_000_000:
            return None
        out[k] = v
    return out


def _load(path: Path) -> dict:
    """One aligned layout file, checked for the shape the importer relies on.

    Everything in it is data from outside: a page or block of the wrong shape
    makes the whole pair refuse to import (and say which file), rather than
    import half of it. Optional metadata of the wrong shape is dropped and
    worked out again from the blocks instead.
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
    doc["alignment"]["summary"] = _counts(doc["alignment"].get("summary"))
    for p in doc["pages"]:
        if not isinstance(p, dict) or not isinstance(p.get("blocks"), list) \
                or isinstance(p.get("page"), bool) or not isinstance(p.get("page"), int) \
                or p["page"] < 0:
            raise Invalid(f"{path.name}: a page is malformed")
        p["align_summary"] = _counts(p.get("align_summary"))
        if not isinstance(p.get("align_status", ""), str):
            p["align_status"] = ""
        if p.get("drop_reason") not in (None, *DROP_REASONS):
            p["drop_reason"] = "other"           # an unknown reason is still a dropped page
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
                        "type", "part"):
                if b.get(key) is not None and not isinstance(b.get(key), str):
                    b[key] = str(b[key])
            if b.get("align_state") not in (None, *STATES):
                b.pop("align_state", None)       # unknown: worked out from the page instead
            units = b.get("merged_units")
            b["merged_units"] = ([_label(u)[:120] for u in units[:64] if _label(u)]
                                 if isinstance(units, list) else [])
            b["markup_restored"] = b.get("markup_restored") is True
    return doc


def block_state(b: dict, page: dict) -> str:
    """aligned / unpaired / page_failed / not_processed / no_text / page_dropped.

    The paragraph-level export says it on every block (``align_state``). For
    an export without it, it is worked out the way the aligner team's viewer
    does, from the block's text and id and the page's status.
    """
    st = b.get("align_state")
    if st in STATES:
        return st
    if not (b.get("text") or "").strip():
        return "no_text"
    if b.get("align_id"):
        return "aligned"
    status = page.get("align_status") or "not_processed"
    if status in ("alignment_failed", "unparseable"):
        return "page_failed"
    if status == "dropped_page_mismatch":
        return "page_dropped"
    return "not_processed" if status == "not_processed" else "unpaired"


def _page_counts(p: dict) -> dict:
    """A page's counts, from its blocks.

    Counts are in original OCR blocks (members), not merged blocks, as the
    export counts them; blocks without text are not counted. The file states
    them too (``align_summary``) and on every page of the delivery the two
    agree (test_aligned checks it), but the blocks are what is drawn and what
    becomes rows: a page whose stated counts said "nothing unpaired" while its
    blocks held unpaired text would be skipped by "only pages with text not
    aligned", and its text missed. So the blocks decide.
    """
    c = {k: 0 for k in COUNTS}
    for b in p["blocks"]:
        st = block_state(b, p)
        if st == "no_text":
            continue
        n = len(b.get("members") or [b])
        c["text_blocks"] += n
        c[st] = c.get(st, 0) + n
    return c


def pct(c: dict) -> float | None:
    """Share of OCR text aligned, pages never sent for alignment left out — the
    figure the aligner team's viewer shows next to each pair."""
    n = _int(c.get("text_blocks")) - _int(c.get("not_processed"))
    return round(100.0 * _int(c.get("aligned")) / n, 1) if n > 0 else None


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
                "model": _label(meta.get("model"), "alignment-model"),
                "src": side(doc, src, langs[0], "en"),
                "tgt": side(doc, tgt, langs[1], str(meta.get("lang", "")).split("+")[-1])}

    by_lang = {d["alignment"].get("lang"): (f, d) for f, d in docs}
    if "en" not in by_lang or len(docs) != 2 or len(by_lang) != 2:
        raise Invalid(f"{pair_id}: expected one English file and one other")
    en = by_lang.pop("en")[1]
    (lang, (_, tg)), = by_lang.items()
    return {"pair_id": pair_id, "bilingual": False,
            "model": _label(en["alignment"].get("model"), "alignment-model"),
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

def _frac(box: list[float], w: float, h: float) -> list[float]:
    """A box as fractions of its page, kept on the page."""
    x0, y0, x1, y1 = box
    return [round(min(max(v, 0.0), 1.0), 5) for v in (x0 / w, y0 / h, x1 / w, y1 / h)]


def _side_segments(side: dict, book_key: str,
                   raw: dict[int, dict[int, str]]) -> tuple[list, dict, list]:
    """Segments for one side, in reading order, their units, and page counts.

    One segment per merged block. A passage that runs onto further pages is ONE
    passage to an annotator, so its later parts are folded into the segment of
    its first part: text joined, members joined, the box and page of the first
    part kept — and every part's box, with the boxes of the OCR blocks merged
    into it, kept page by page for drawing.
    """
    walk = _Walk()
    segs: list[dict] = []
    by_unit: dict[str, dict] = {}
    pages_meta: list[dict] = []
    for p in sorted(side["pages"], key=lambda x: x["page"]):
        page = int(p["page"])
        w, h = _dim(p.get("width")), _dim(p.get("height"))
        status = p.get("align_status") or ""
        pages_meta.append({"page": page, "status": status, "width": w, "height": h,
                           "drop_reason": p.get("drop_reason") or "", **_page_counts(p)})
        for b in sorted(p["blocks"], key=lambda x: _int(x.get("order"))):
            members = b.get("members") or [{"order": _int(b.get("order"))}]
            page_raw = raw.get(page, {})
            raw_text = "\n\n".join(page_raw.get(_int(m.get("order"), -1), "") for m in members)
            if not raw and not raw_text:
                raw_text = b.get("text") or ""     # no raw book: the delivered text is all there is
            corrected = normalise(b.get("text") or "")
            raw_text = normalise(raw_text)
            aid = b.get("align_id") or ""
            part = {"page": page, "box": _frac(_box(b.get("bbox_xyxy")), w, h),
                    "members": [_frac(_box(m.get("bbox_xyxy")), w, h) for m in members
                                if m.get("bbox_xyxy") is not None] if len(members) > 1 else []}
            if aid and aid in by_unit:            # a later part of a passage already met
                seg = by_unit[aid]
                seg["source"] = "\n\n".join(x for x in (seg["source"], raw_text) if x)
                seg["corrected"] = "\n\n".join(x for x in (seg["corrected"], corrected) if x)
                seg["members"] += [{"page": page, "order": _int(m.get("order"))} for m in members]
                seg["pages"].append(page)
                seg["parts"].append(part)
                seg["flags"] += list(b.get("flags") or [])
                seg["markup"] = seg["markup"] or bool(b.get("markup_restored"))
                for u in b.get("merged_units") or []:
                    if u not in seg["units"]:
                        seg["units"].append(u)
                continue
            label = (b.get("label") or "").strip()
            walk.observe(label, corrected)
            seg = {
                "page": page, "order": _int(b.get("order")), "label": label,
                "type": b.get("type") or "", "source": raw_text, "corrected": corrected,
                "box": _box(b.get("bbox_xyxy")),
                "w": w, "h": h, "members": [{"page": page, "order": _int(m.get("order"))}
                                            for m in members],
                "pages": [page], "parts": [part], "align_id": aid,
                "relation": b.get("align_relation") or "",
                "confidence": b.get("align_confidence") or "",
                "note": b.get("align_note") or "", "flags": list(b.get("flags") or []),
                "page_status": status, "state": block_state(b, p),
                "units": list(b.get("merged_units") or []),
                "markup": bool(b.get("markup_restored")),
                "chapter": walk.chapter, "chapter_no": walk.chapter_no,
                "section": walk.section, "section_no": walk.section_no,
                "depth": walk.depth,
            }
            segs.append(seg)
            if aid:
                by_unit[aid] = seg
    for i, seg in enumerate(segs):
        seg["seq"] = i
        seg["sid"] = ids.segment_id(book_key, seg["page"], seg["order"], seg["order"])
    return segs, by_unit, pages_meta


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

def book_key_for(set_id: str, pair_id: str, side: str, relpath: str) -> str:
    return ids.book_key(f"{DATASET}/{set_id}/{pair_id}/{side}/{relpath}")


def _marks(set_id: str, pair_id: str) -> list[str]:
    """Every dedup key the books of one pair of one set can carry."""
    keys = [f"{MARK}{set_id}:{pair_id}:{s}" for s in ("src", "tgt")]
    if set_id == LEGACY_SET:
        keys += [f"{MARK}{pair_id}:{s}" for s in ("src", "tgt")]
    return keys


def _raw_book(con, relpath: str) -> dict:
    row = con.execute("SELECT * FROM setu_book WHERE relpath = ? AND dedup_key NOT LIKE ?"
                      " ORDER BY length(book_key) LIMIT 1", (relpath, MARK + "%")).fetchone()
    return dict(row) if row else {}


def _insert_book(con, pair: dict, which: str, book_key: str, set_id: str,
                 n_segments: int) -> dict:
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
        (book_key, int(raw.get("pl_book_id") or 0), f"{MARK}{set_id}:{pair['pair_id']}:{which}",
         side["book"], side["relpath"], board, board_name, cls,
         raw.get("subject") or "Mathematics", side["language"], raw.get("script") or script,
         raw.get("volume") or "", title, max(0, _int(side["doc"].get("num_pages"))),
         sum(len(p["blocks"]) for p in side["pages"]), n_segments,
         int(raw.get("pdf_present") or 0), time.time()))
    return {"board": board, "board_name": board_name, "class": cls,
            "volume": raw.get("volume") or ""}


def _drop_orphans(con, set_id: str, pair_id: str) -> int:
    """Clear one pair's aligned books when no project uses them any more.

    That happens only when the pair's project was deleted on purpose. Nothing a
    person did can be lost here — answers and corrections live under the
    project, which is already gone — and the books are rebuilt from the files
    straight after, so a deleted pair comes back exactly as imported.
    """
    marks = _marks(set_id, pair_id)
    keys = [r[0] for r in con.execute(
        f"SELECT b.book_key FROM setu_book b WHERE b.dedup_key IN ({','.join('?' * len(marks))})"
        "   AND NOT EXISTS (SELECT 1 FROM setu_project p"
        "                    WHERE p.src_book = b.book_key OR p.tgt_book = b.book_key)", marks)]
    from .store import fts_ready
    for key in keys:
        if fts_ready(con):
            con.execute("DELETE FROM setu_seg_fts WHERE book_key = ?", (key,))
        con.execute("DELETE FROM setu_book WHERE book_key = ? AND dedup_key LIKE ?",
                    (key, MARK + "%"))
    if keys:
        log.info("aligned pair %s: its project had been deleted; re-importing it", pair_id)
    return len(keys)


def is_imported(con, pair_id: str, set_id: str = "") -> str:
    """The project id of a pair imported in a set (the current one by default), or ''."""
    set_id = set_id or current_set(con).get("set_id", "")
    row = con.execute("SELECT pid FROM setu_aligned_pair WHERE set_id = ? AND pair_id = ?",
                      (set_id, pair_id)).fetchone()
    if row:
        return row[0]
    if set_id == LEGACY_SET:                    # imported by v7, not adopted yet
        row = con.execute(
            "SELECT p.pid FROM setu_project p JOIN setu_book b ON b.book_key = p.src_book"
            " WHERE b.dedup_key = ?", (f"{MARK}{pair_id}:src",)).fetchone()
        return row[0] if row else ""
    return ""


def import_pair(con, pair_dir: Path, *, set_id: str, level: str = "", version: str = "",
                actor: str = "setu import") -> dict:
    """Import one pair of one set as a project whose rows are the model's pairs.

    Must run inside a transaction: a pair is imported whole or not at all.
    """
    from .workspace import create_project

    pair = read_pair(pair_dir)
    pid = is_imported(con, pair["pair_id"], set_id)
    if pid:
        return {"pair_id": pair["pair_id"], "pid": pid, "skipped": True}
    _drop_orphans(con, set_id, pair["pair_id"])

    built = {}
    for which in ("src", "tgt"):
        side = pair[which]
        key = book_key_for(set_id, pair["pair_id"], which, side["relpath"])
        raw_path = raw_path_for(side["relpath"])
        raw = _raw_pages(raw_path) if raw_path else {}
        if pair["bilingual"]:
            raw = {pg: b for pg, b in raw.items() if pg in {p["page"] for p in side["pages"]}}
        segs, units, pages_meta = _side_segments(side, key, raw)
        rows = _segment_rows(key, segs)
        meta = _insert_book(con, pair, which, key, set_id, len(rows))
        con.executemany(
            "INSERT INTO setu_segment(sid, book_key, seq, page, ord_start, ord_end, kind,"
            " label, block_type, chapter, chapter_no, section, section_no, item_no, depth,"
            " source_text, n_chars, has_math, has_table, block_ids, fx0, fy0, fx1, fy1,"
            " anchor_math, anchor_num) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            rows)
        _index_fts(con, key, rows)
        con.executemany(
            "INSERT INTO setu_hint(sid, pair_id, align_id, relation, confidence, note, flags,"
            " parts, pages, page_status, state, units, markup)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            [(s["sid"], pair["pair_id"], s["align_id"], s["relation"], s["confidence"],
              s["note"], json.dumps(s["flags"], ensure_ascii=False), len(s["pages"]),
              json.dumps(s["pages"]), s["page_status"], s["state"],
              json.dumps(s["units"], ensure_ascii=False), int(s["markup"])) for s in segs])
        con.executemany(
            "INSERT INTO setu_seg_part(sid, book_key, page, part, fx0, fy0, fx1, fy1, members)"
            " VALUES(?,?,?,?,?,?,?,?,?)",
            [(s["sid"], key, prt["page"], i + 1, *prt["box"], json.dumps(prt["members"]))
             for s in segs for i, prt in enumerate(s["parts"])])
        con.executemany(
            "INSERT INTO setu_page_meta(book_key, page, status, text_blocks, aligned, unpaired,"
            " page_failed, not_processed, page_dropped, drop_reason, width, height)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            [(key, m["page"], m["status"][:40], _int(m.get("text_blocks")), _int(m.get("aligned")),
              _int(m.get("unpaired")), _int(m.get("page_failed")), _int(m.get("not_processed")),
              _int(m.get("page_dropped")), str(m.get("drop_reason") or "")[:40],
              m["width"], m["height"]) for m in pages_meta])
        built[which] = {"key": key, "segs": segs, "units": units, "raw_found": bool(raw_path),
                        "meta": meta, "pages": pages_meta}

    proj = create_project(con, src_book=built["src"]["key"], tgt_book=built["tgt"]["key"],
                          name=_project_name(pair, built["src"]["meta"], level, set_id, version),
                          annotator=actor, build=False)
    pid = proj["pid"]
    n_rows, n_model = _insert_rows(con, pid, built, actor, pair.get("model") or "")
    summary = _pair_summary(pair, built)
    con.execute("INSERT INTO setu_aligned_pair(pid, set_id, pair_id, summary, imported_at)"
                " VALUES(?,?,?,?,?)", (pid, set_id, pair["pair_id"],
                                       json.dumps(summary, ensure_ascii=False), time.time()))
    Repository(con).event("aligned.import", pid,
                          {"pair_id": pair["pair_id"], "set": set_id, "rows": n_rows,
                           "model_corrections": n_model}, actor=actor)
    return {"pair_id": pair["pair_id"], "pid": pid, "skipped": False, "rows": n_rows,
            "units": len(built["src"]["units"]), "model_corrections": n_model,
            "raw_found": built["src"]["raw_found"] and built["tgt"]["raw_found"]}


def _pair_summary(pair: dict, built: dict) -> dict:
    """Counts per side, summed from the pages — and the share aligned."""
    out: dict[str, Any] = {}
    total = {k: 0 for k in COUNTS}
    for which in ("src", "tgt"):
        c = {k: 0 for k in total}
        for m in built[which]["pages"]:
            for k in c:
                c[k] += _int(m.get(k))
        c["aligned_pct"] = pct(c)
        out[which] = c
        for k in total:
            total[k] += c[k]
    total["aligned_pct"] = pct(total)
    out["total"] = total
    out["not_aligned"] = total["unpaired"] + total["page_failed"]
    out["dropped"] = total["page_dropped"]
    out["pages_dropped"] = sum(1 for which in ("src", "tgt") for m in built[which]["pages"]
                               if m["status"] == "dropped_page_mismatch")
    out["markup_restored"] = sum(1 for which in ("src", "tgt") for sg in built[which]["segs"]
                                 if sg["markup"])
    out["bilingual"] = bool(pair["bilingual"])
    return out


def _project_name(pair: dict, meta: dict, level: str = "", set_id: str = "",
                  version: str = "") -> str:
    who = meta.get("board_name") or meta.get("board") or ""
    cls = f" Class {meta['class']}" if meta.get("class") else ""
    part = part_of(pair["pair_id"], meta.get("volume") or "")
    tail = pair["pair_id"] if set_id == LEGACY_SET or not level else \
        f"{pair['pair_id']}, {set_label(level, version)}"
    return (f"{who}{cls}{' · ' + part if part else ''} — {pair['src']['language']} ⇄ "
            f"{pair['tgt']['language']} · aligned test set ({tail})").strip()


def wants_row(seg: dict) -> bool:
    """Whether a passage the model left unpaired gets a row of its own.

    Only when there is something to check: some text, on a page that was sent
    for alignment and kept (v2 drops pages whose alignment could not be
    trusted; the aligner's own viewer shows them grey, outside the set), and
    not a page header, footer, page number or picture — the
    same things Setu leaves out of every other project. The rest stay in the
    book (shown with "Include headers and page numbers", and pairable by hand);
    they are just not a to-do. Every one of the model's pairs is a row whatever
    it holds.
    """
    if seg.get("state") in ("not_processed", "no_text", "page_dropped"):
        return False
    if not (str(seg.get("source") or "").strip() or str(seg.get("corrected") or "").strip()):
        return False
    if seg.get("note") == "page_furniture":
        return False
    return kind_for(seg.get("label") or "",
                    seg.get("corrected") or seg.get("source") or "") not in NOISE_KINDS


def _insert_rows(con, pid: str, built: dict, actor: str, model_name: str = "") -> tuple[int, int]:
    """Rows in English reading order, the model's pairs paired, and every other
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
    model = MODEL_PREFIX + (_label(model_name, "") or "alignment-model")
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


def import_all(connect: Callable, dataset: Any = None, *, actor: str = "setu import",
               log_fn: Callable[[str], None] = log.info) -> dict:
    """Import every pair of the delivery in the folder not imported yet.

    ``connect`` is a context manager factory yielding a connection inside a
    transaction (store.tx). One transaction per pair: a pair that fails is
    reported and skipped; the others still import. Projects of earlier
    deliveries are never touched.
    """
    root = find_dataset(dataset)
    report = {"dataset": str(root or ""), "pairs": 0, "imported": 0, "skipped": 0,
              "rows": 0, "model_corrections": 0, "errors": [], "raw_missing": [],
              "set": "", "level": "", "new_set": False}
    with connect() as con:                       # pairs v7 imported become a set first
        adopt_legacy(con)
    if not root:
        return report
    started = time.time()
    desc = describe(root)
    with connect() as con:
        known = bool(_find_set(con, desc))
        set_id = resolve_set(con, desc)
    report.update({"set": set_id, "level": desc["level"], "new_set": not known})
    for pair_dir in _pair_dirs(root):
        report["pairs"] += 1
        try:
            with connect() as con:
                if is_imported(con, pair_dir.name, set_id):
                    report["skipped"] += 1
                    continue
                out = import_pair(con, pair_dir, set_id=set_id, level=desc["level"],
                                  version=desc.get("version", ""), actor=actor)
            if out.get("skipped"):
                report["skipped"] += 1
                continue
            report["imported"] += 1
            report["rows"] += out["rows"]
            report["model_corrections"] += out["model_corrections"]
            if not out["raw_found"]:
                report["raw_missing"].append(out["pair_id"])
        except Invalid as exc:                   # a bad file: say which, and why, in one line
            log.warning("aligned pair %s not imported: %s", shown_name(pair_dir.name), exc)
            report["errors"].append({"pair": shown_name(pair_dir.name),
                                     "error": f"Invalid: {exc}"})
        except Exception as exc:                 # one bad pair must not stop the rest
            log.exception("aligned import failed for %s", shown_name(pair_dir.name))
            report["errors"].append({"pair": shown_name(pair_dir.name),
                                     "error": f"{type(exc).__name__}"})
    report["seconds"] = round(time.time() - started, 1)
    if report["imported"]:
        log_fn(f"aligned test set ({set_label(desc['level'], desc.get('version', ''))}):"
               f" imported {report['imported']}"
               f" pair(s), {report['rows']:,} rows, {report['model_corrections']:,} model"
               f" corrections in {report['seconds']}s")
    return report


# ── reading it back ────────────────────────────────────────────────────────

_PAIR_SQL = """
SELECT p.pid, p.name, p.board, p.class, p.src_language, p.tgt_language,
       p.src_book, p.tgt_book, p.n_rows, b.board_name, b.volume,
       a.pair_id, a.set_id, a.summary,
       (SELECT COUNT(*) FROM setu_row r WHERE r.pid = p.pid
          AND r.status <> 'pending') AS answered,
       (SELECT COUNT(*) FROM setu_row r WHERE r.pid = p.pid AND r.edited = 1) AS corrected,
       (SELECT COUNT(*) FROM setu_row r WHERE r.pid = p.pid
          AND r.src_sid IS NOT NULL AND r.tgt_sid IS NOT NULL) AS units,
       (SELECT COUNT(*) FROM setu_row r
         WHERE r.pid = p.pid AND EXISTS (
           SELECT 1 FROM setu_hint h WHERE h.sid IN (r.src_sid, r.tgt_sid)
              AND h.flags <> '[]')) AS flagged
  FROM setu_aligned_pair a
  JOIN setu_project p ON p.pid = a.pid
  JOIN setu_book b ON b.book_key = p.src_book
"""


def _pair_rows(con, where: str, args: tuple) -> list[dict]:
    out = []
    for r in con.execute(_PAIR_SQL + where + " ORDER BY p.board, p.class, p.tgt_language,"
                         " a.pair_id", args).fetchall():
        d = dict(r)
        d["part"] = part_of(d.get("pair_id") or "", d.pop("volume", "") or "")
        try:
            summary = json.loads(d.pop("summary") or "{}")
        except (TypeError, ValueError):
            summary = {}
        total = summary.get("total") or {}
        d["aligned_pct"] = total.get("aligned_pct")
        d["not_aligned"] = summary.get("not_aligned")
        d["text_blocks"] = total.get("text_blocks")
        d["dropped"] = summary.get("dropped") or 0
        d["pages_dropped"] = summary.get("pages_dropped") or 0
        d["markup_restored"] = summary.get("markup_restored") or 0
        out.append(d)
    return out


def pairs(con, set_id: str = "") -> list[dict]:
    """The pairs of one set (the current one by default), with progress."""
    set_id = set_id or current_set(con).get("set_id", "")
    if not set_id:
        return []
    return _pair_rows(con, " WHERE a.set_id = ?", (set_id,))


def earlier_pairs(con) -> list[dict]:
    """Pairs of earlier deliveries that somebody worked in — never lost from
    view just because a newer delivery replaced them in the folder."""
    rows = _pair_rows(
        con, " WHERE a.set_id IN (SELECT set_id FROM setu_aligned_set WHERE current = 0)"
             "   AND (EXISTS (SELECT 1 FROM setu_row r WHERE r.pid = p.pid"
             "                AND (r.status <> 'pending' OR r.edited = 1)))", ())
    labels = {r[0]: r[1] for r in con.execute("SELECT set_id, label FROM setu_aligned_set")}
    for r in rows:
        r["set_label"] = labels.get(r["set_id"], "")
    return rows


def status(con, dataset: Any = None) -> dict:
    """What is in the folder, and what of it has been imported. Never writes."""
    root = find_dataset(dataset)
    on_disk = [p.name for p in _pair_dirs(root)] if root else []
    desc = describe(root) if root else {}
    set_id = _find_set(con, desc) if desc else ""
    done = {r[0] for r in con.execute(
        "SELECT pair_id FROM setu_aligned_pair WHERE set_id = ?", (set_id,))} if set_id else set()
    if set_id == LEGACY_SET:                    # v7 imports not adopted yet still count
        done |= {m[1] for (key,) in con.execute(
            "SELECT dedup_key FROM setu_book WHERE dedup_key LIKE ?", (MARK + "%",))
                 for m in [parse_mark(key)] if m and m[0] == LEGACY_SET}
    cur = current_set(con)
    known = con.execute("SELECT COUNT(*) FROM setu_aligned_set").fetchone()[0] or \
        int(_legacy_books(con))
    return {"dataset": str(root or ""), "on_disk": len(on_disk),
            "imported": len(done & set(on_disk)),
            "waiting": sorted(set(on_disk) - done),
            "level": desc.get("level", ""),
            "label": set_label(desc.get("level", ""), desc.get("version", "")),
            "segments": desc.get("segments", 0), "units": desc.get("units", 0),
            "new_set": bool(desc) and not set_id, "known_sets": known,
            "current": {k: cur.get(k) for k in ("set_id", "label", "level", "n_segments",
                                                 "n_units", "model", "prompt")} if cur else {}}


def page_meta(con, book_key: str, page: int) -> dict | None:
    """A page's status and counts, for an aligned edition imported with them."""
    row = con.execute("SELECT status, text_blocks, aligned, unpaired, page_failed, not_processed,"
                      "       page_dropped, drop_reason, width, height"
                      "  FROM setu_page_meta WHERE book_key = ? AND page = ?",
                      (book_key, page)).fetchone()
    return dict(row) if row else None


def attention_near(con, book_key: str, page: int) -> tuple[int | None, int | None]:
    """The nearest pages before and after with text the model could not pair."""
    row = con.execute(
        "SELECT (SELECT MAX(page) FROM setu_page_meta WHERE book_key = ? AND page < ?"
        "          AND unpaired + page_failed > 0),"
        "       (SELECT MIN(page) FROM setu_page_meta WHERE book_key = ? AND page > ?"
        "          AND unpaired + page_failed > 0)", (book_key, page, book_key, page)).fetchone()
    return (row[0], row[1]) if row else (None, None)


def parts_on_page(con, book_key: str, page: int, pid: str, side: str) -> list[dict]:
    """Every part of every passage on one page, for drawing it — including a
    passage that began on an earlier page — with the row it belongs to."""
    col = "src_sid" if side == "src" else "tgt_sid"
    out = []
    for r in con.execute(
            f"""SELECT sp.sid, sp.part, sp.fx0, sp.fy0, sp.fx1, sp.fy1, sp.members,
                       s.page AS seg_page, h.parts AS of_parts, h.state,
                       r.rid, r.seq AS row_seq, r.status,
                       (r.src_sid IS NOT NULL AND r.tgt_sid IS NOT NULL) AS paired
                  FROM setu_seg_part sp
                  JOIN setu_segment s ON s.sid = sp.sid
                  LEFT JOIN setu_hint h ON h.sid = sp.sid
                  LEFT JOIN setu_row r ON r.pid = ? AND r.{col} = sp.sid
                 WHERE sp.book_key = ? AND sp.page = ?
                 ORDER BY sp.sid, sp.part""", (pid, book_key, page)):
        d = dict(r)
        try:
            d["members"] = json.loads(d["members"] or "[]")
        except (TypeError, ValueError):
            d["members"] = []
        d["paired"] = bool(d["paired"])
        out.append(d)
    return out
