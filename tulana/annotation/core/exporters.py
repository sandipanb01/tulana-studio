"""Setu — getting the work back out.

A registry, not a switch statement. Adding a format means writing one function
and decorating it; nothing else in Setu changes, and the interface picks the
new format up automatically because the format list is generated from the
registry rather than written out twice.

Every exporter receives the same thing: an iterable of already-shaped records
and a file handle. That keeps memory flat — a project of 200,000 rows streams
row by row rather than being assembled in a list first — and it keeps the
formats honest, because none of them can quietly see a different set of rows
than the others.

Two properties the formats do not share, and which the registry records so the
interface can say so rather than producing a file that disappoints:

* ``pairs_only`` — TMX, Moses and the plain-text formats describe *parallel*
  data, so a row with one empty side has no representation in them. Those rows
  are excluded and the count of excluded rows is returned. Silently writing an
  empty string instead is how a parallel corpus goes out of alignment.
* ``available`` — Parquet needs pyarrow, XLSX needs openpyxl. A format whose
  dependency is missing is reported unavailable with the install command,
  rather than raising at the moment somebody clicks Download.
"""
from __future__ import annotations

import csv
import io
import json
import logging
import re
import time
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

import config

from . import ids
from .models import DONE_STATUSES, STATUS_BY_KEY
from .store import Invalid, Repository

log = logging.getLogger("setu.exporters")

#: Line separators that split a line in *somebody's* reader. Moses and plain
#: text are one-record-per-line formats, so any of these inside a record would
#: shift every subsequent pair by one. They are replaced by a space, not
#: stripped, so words do not run together.
_BREAKS = re.compile("[\r\n\u2028\u2029\x0b\x0c]+")


@dataclass(frozen=True)
class Format:
    key: str
    label: str
    ext: str
    mime: str
    writer: Callable
    pairs_only: bool = False
    binary: bool = False
    requires: str = ""
    note: str = ""

    @property
    def available(self) -> bool:
        if not self.requires:
            return True
        try:
            __import__(self.requires)
            return True
        except ImportError:
            return False

    def describe(self) -> dict:
        d = {"key": self.key, "label": self.label, "ext": self.ext,
             "mime": self.mime, "pairs_only": self.pairs_only,
             "available": self.available, "note": self.note}
        if not self.available:
            d["install"] = f"pip install {self.requires}"
        return d


REGISTRY: dict[str, Format] = {}


def register(key: str, label: str, ext: str, mime: str, *, pairs_only: bool = False,
             binary: bool = False, requires: str = "", note: str = ""):
    """Add a format. The only thing a new exporter has to do."""
    def wrap(fn: Callable) -> Callable:
        REGISTRY[key] = Format(key, label, ext, mime, fn, pairs_only, binary,
                               requires, note)
        return fn
    return wrap


def formats() -> list[dict]:
    return [f.describe() for f in REGISTRY.values()]


def get(key: Any) -> Format:
    fmt = REGISTRY.get(str(key or "").strip().lower())
    if fmt is None:
        raise Invalid(f"unknown export format {key!r}; available: "
                      + ", ".join(sorted(REGISTRY)))
    if not fmt.available:
        raise Invalid(f"the {fmt.label} exporter needs the {fmt.requires} package "
                      f"(pip install {fmt.requires})")
    return fmt


# ── the records every format sees ──────────────────────────────────────────

FIELDS = ("row_id", "seq", "status", "status_label", "origin", "confidence",
          "note", "kind", "chapter_no", "chapter", "section_no", "section",
          "source_lang", "target_lang", "source_text", "target_text",
          "source_original", "target_original", "source_edited", "target_edited",
          "source_page", "target_page", "source_segment", "target_segment",
          "board", "class", "subject", "updated_at", "updated_by")


def records(con, pid: str, *, status: str = "", chapter_no: str = "",
            kind: str = "", only_done: bool = False,
            include_unpaired: bool = True) -> Iterator[dict]:
    """Stream a project's rows in reading order, already flattened.

    Uses a server-side cursor rather than ``fetchall``: the largest project in
    this corpus is about 2,500 rows, but the design has to survive the day
    somebody points it at a 200-page book in twelve languages.
    """
    repo = Repository(con)
    proj = repo.one(
        "SELECT p.*, sb.board_name, sb.class AS cls, sb.subject AS subj"
        "  FROM setu_project p JOIN setu_book sb ON sb.book_key = p.src_book"
        " WHERE p.pid = ?", (pid,))
    if not proj:
        raise Invalid(f"no such project: {pid}")

    where = ["r.pid = ?"]
    args: list[Any] = [pid]
    if status:
        keys = [s.strip() for s in status.split(",") if s.strip() in STATUS_BY_KEY]
        if keys:
            where.append(f"r.status IN ({','.join('?' * len(keys))})")
            args.extend(keys)
    elif only_done:
        where.append(f"r.status IN ({','.join('?' * len(DONE_STATUSES))})")
        args.extend(DONE_STATUSES)
    if chapter_no:
        where.append("r.chapter_no = ?")
        args.append(chapter_no)
    if kind:
        where.append("r.kind = ?")
        args.append(kind)
    if not include_unpaired:
        where.append("r.src_sid IS NOT NULL AND r.tgt_sid IS NOT NULL")

    cur = con.execute(
        f"""SELECT r.rid, r.seq, r.status, r.origin, r.confidence, r.note, r.kind,
                   r.chapter_no, r.chapter, r.section_no, r.section,
                   r.src_sid, r.tgt_sid, r.src_page, r.tgt_page,
                   r.updated_at, r.updated_by,
                   ss.source_text AS src_source, ts.source_text AS tgt_source,
                   st.text AS src_edit, tt.text AS tgt_edit
              FROM setu_row r
              LEFT JOIN setu_segment ss ON ss.sid = r.src_sid
              LEFT JOIN setu_segment ts ON ts.sid = r.tgt_sid
              LEFT JOIN setu_text st ON st.rid = r.rid AND st.side = 'src'
              LEFT JOIN setu_text tt ON tt.rid = r.rid AND tt.side = 'tgt'
             WHERE {' AND '.join(where)} ORDER BY r.seq""", args)

    for r in cur:
        src_source = r["src_source"] or ""
        tgt_source = r["tgt_source"] or ""
        src_text = r["src_edit"] if r["src_edit"] is not None else src_source
        tgt_text = r["tgt_edit"] if r["tgt_edit"] is not None else tgt_source
        yield {
            "row_id": r["rid"], "seq": r["seq"], "status": r["status"],
            "status_label": STATUS_BY_KEY[r["status"]].label
            if r["status"] in STATUS_BY_KEY else r["status"],
            "origin": r["origin"], "confidence": round(float(r["confidence"] or 0), 3),
            "note": r["note"] or "", "kind": r["kind"] or "",
            "chapter_no": r["chapter_no"] or "", "chapter": r["chapter"] or "",
            "section_no": r["section_no"] or "", "section": r["section"] or "",
            "source_lang": proj["src_language"] or "", "target_lang": proj["tgt_language"] or "",
            "source_text": src_text, "target_text": tgt_text,
            "source_original": src_source, "target_original": tgt_source,
            "source_edited": src_text != src_source,
            "target_edited": tgt_text != tgt_source,
            "source_page": r["src_page"], "target_page": r["tgt_page"],
            "source_segment": r["src_sid"] or "", "target_segment": r["tgt_sid"] or "",
            "board": proj["board_name"] or proj["board"] or "",
            "class": proj["cls"], "subject": proj["subj"] or "",
            "updated_at": r["updated_at"], "updated_by": r["updated_by"] or "",
        }


def _paired(rows: Iterable[dict]) -> Iterator[dict]:
    """Only rows with text on both sides. Used by the parallel-only formats."""
    for r in rows:
        if r["source_text"].strip() and r["target_text"].strip():
            yield r


def _flat(text: str) -> str:
    """One line, for the one-record-per-line formats."""
    return _BREAKS.sub(" ", text or "").strip()


# ── the formats ────────────────────────────────────────────────────────────

@register("jsonl", "JSON Lines", "jsonl", "application/x-ndjson",
          note="One JSON object per line. The usual choice for training data.")
def _jsonl(rows: Iterable[dict], fh, meta: dict) -> int:
    n = 0
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        n += 1
    return n


@register("json", "JSON", "json", "application/json",
          note="A single document with the project's details and every row.")
def _json(rows: Iterable[dict], fh, meta: dict) -> int:
    fh.write('{\n  "setu": ' + json.dumps(meta, ensure_ascii=False) + ',\n  "rows": [\n')
    n = 0
    for r in rows:
        fh.write(("    " if n == 0 else ",\n    ") + json.dumps(r, ensure_ascii=False))
        n += 1
    fh.write("\n  ]\n}\n")
    return n


@register("csv", "CSV", "csv", "text/csv",
          note="Opens in Excel. Written with a BOM so Indic text is not mangled.")
def _csv(rows: Iterable[dict], fh, meta: dict) -> int:
    return _delimited(rows, fh, ",")


@register("tsv", "TSV", "tsv", "text/tab-separated-values",
          note="Tab separated. Tabs inside text are replaced with spaces.")
def _tsv(rows: Iterable[dict], fh, meta: dict) -> int:
    return _delimited(rows, fh, "\t")


def _delimited(rows: Iterable[dict], fh, delim: str) -> int:
    writer = csv.DictWriter(fh, fieldnames=list(FIELDS), delimiter=delim,
                            lineterminator="\n", extrasaction="ignore",
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    n = 0
    for r in rows:
        row = dict(r)
        if delim == "\t":
            # A tab inside a field would create a phantom column that no
            # quoting convention in TSV reliably fixes.
            for k in ("source_text", "target_text", "source_original",
                      "target_original", "note"):
                row[k] = (row.get(k) or "").replace("\t", " ")
        writer.writerow(row)
        n += 1
    return n


@register("xml", "XML", "xml", "application/xml",
          note="One <pair> element per row, with the metadata as attributes.")
def _xml(rows: Iterable[dict], fh, meta: dict) -> int:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<setu')
    for k, v in meta.items():
        if isinstance(v, (str, int, float)) and v not in (None, ""):
            fh.write(f' {k}="{_xml_attr(str(v))}"')
    fh.write(">\n")
    n = 0
    for r in rows:
        el = ET.Element("pair", {
            "id": r["row_id"], "seq": str(r["seq"]), "status": r["status"],
            "kind": r["kind"], "chapter": r["chapter_no"], "section": r["section_no"],
            "confidence": str(r["confidence"]),
        })
        s = ET.SubElement(el, "source", {"lang": r["source_lang"],
                                         "page": str(r["source_page"] or "")})
        s.text = r["source_text"]
        t = ET.SubElement(el, "target", {"lang": r["target_lang"],
                                         "page": str(r["target_page"] or "")})
        t.text = r["target_text"]
        if r["note"]:
            ET.SubElement(el, "note").text = r["note"]
        fh.write("  " + ET.tostring(el, encoding="unicode") + "\n")
        n += 1
    fh.write("</setu>\n")
    return n


def _xml_attr(v: str) -> str:
    return (v.replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


@register("txt", "Plain text", "txt", "text/plain", pairs_only=True,
          note="Readable side-by-side text, one pair per block. For proofreading.")
def _txt(rows: Iterable[dict], fh, meta: dict) -> int:
    n = 0
    for r in _paired(rows):
        fh.write(f"# {r['seq']}  [{r['status_label']}]  {r['chapter']} "
                 f"{r['section']}\n".rstrip() + "\n")
        fh.write(f"{r['source_lang'] or 'source'}: {r['source_text']}\n")
        fh.write(f"{r['target_lang'] or 'target'}: {r['target_text']}\n\n")
        n += 1
    return n


@register("moses", "Moses (two files)", "zip", "application/zip",
          pairs_only=True, binary=True,
          note="Two line-aligned files, the classic parallel-corpus layout.")
def _moses(rows: Iterable[dict], fh, meta: dict) -> int:
    src_lines: list[str] = []
    tgt_lines: list[str] = []
    for r in _paired(rows):
        src_lines.append(_flat(r["source_text"]))
        tgt_lines.append(_flat(r["target_text"]))
    src_tag = _lang_tag(meta.get("source_lang") or "src")
    tgt_tag = _lang_tag(meta.get("target_lang") or "tgt")
    with zipfile.ZipFile(fh, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"corpus.{src_tag}", "\n".join(src_lines) + ("\n" if src_lines else ""))
        z.writestr(f"corpus.{tgt_tag}", "\n".join(tgt_lines) + ("\n" if tgt_lines else ""))
        z.writestr("README.txt",
                   "Moses format: line N of each file is one parallel pair.\n"
                   f"pairs: {len(src_lines)}\n"
                   "Rows with an empty side are excluded — including them would\n"
                   "shift every later line out of alignment.\n")
    return len(src_lines)


@register("tmx", "TMX (translation memory)", "tmx", "application/x-tmx",
          pairs_only=True,
          note="Opens in translation tools such as OmegaT and memoQ.")
def _tmx(rows: Iterable[dict], fh, meta: dict) -> int:
    src = _lang_tag(meta.get("source_lang") or "en")
    tgt = _lang_tag(meta.get("target_lang") or "xx")
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<tmx version="1.4">\n  <header creationtool="Tulana Setu" '
             'creationtoolversion="1.0" segtype="block" o-tmf="Setu" '
             'adminlang="en" srclang="%s" datatype="plaintext"/>\n  <body>\n' % src)
    n = 0
    for r in _paired(rows):
        fh.write(f'    <tu tuid="{_xml_attr(r["row_id"])}">\n'
                 f'      <tuv xml:lang="{src}"><seg>{_xml_text(r["source_text"])}</seg></tuv>\n'
                 f'      <tuv xml:lang="{tgt}"><seg>{_xml_text(r["target_text"])}</seg></tuv>\n'
                 f'    </tu>\n')
        n += 1
    fh.write("  </body>\n</tmx>\n")
    return n


def _xml_text(v: str) -> str:
    return (v or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


@register("xlsx", "Excel workbook", "xlsx",
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          binary=True, requires="openpyxl",
          note="One sheet of pairs, one of the project's details.")
def _xlsx(rows: Iterable[dict], fh, meta: dict) -> int:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font

    wb = Workbook(write_only=False)
    ws = wb.active
    ws.title = "Pairs"
    ws.append(list(FIELDS))
    for cell in ws[1]:
        cell.font = Font(bold=True)
    n = 0
    for r in rows:
        ws.append([_cell(r.get(f)) for f in FIELDS])
        n += 1
    for col, width in (("A", 20), ("O", 60), ("P", 60)):
        ws.column_dimensions[col].width = width
    for row in ws.iter_rows(min_row=2, min_col=15, max_col=16):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"

    info = wb.create_sheet("About")
    info.append(["field", "value"])
    for k, v in meta.items():
        info.append([k, _cell(v)])
    wb.save(fh)
    return n


def _cell(v: Any) -> Any:
    """Excel rejects control characters and silently corrupts very long cells."""
    if isinstance(v, bool):
        return "yes" if v else "no"
    if v is None or isinstance(v, (int, float)):
        return v
    s = str(v)
    s = "".join(ch for ch in s if ch == "\n" or ch == "\t"
                or unicodedata.category(ch)[0] != "C")
    return s[:32000]


@register("parquet", "Parquet", "parquet", "application/vnd.apache.parquet",
          binary=True, requires="pyarrow",
          note="Columnar, compressed. For loading into pandas or Spark.")
def _parquet(rows: Iterable[dict], fh, meta: dict) -> int:
    import pyarrow as pa
    import pyarrow.parquet as pq

    collected = list(rows)
    table = pa.table({f: pa.array([_arrow(r.get(f)) for r in collected])
                      for f in FIELDS})
    table = table.replace_schema_metadata(
        {k: str(v) for k, v in meta.items() if v is not None})
    pq.write_table(table, fh, compression="snappy")
    return len(collected)


def _arrow(v: Any) -> Any:
    return v if not isinstance(v, bool) else bool(v)


@register("huggingface", "Hugging Face dataset", "zip", "application/zip",
          binary=True, pairs_only=True,
          note="JSONL plus a dataset card, ready to push to the Hub.")
def _hf(rows: Iterable[dict], fh, meta: dict) -> int:
    buf = io.StringIO()
    n = 0
    for r in _paired(rows):
        buf.write(json.dumps({
            "id": r["row_id"], "translation": {
                _lang_tag(r["source_lang"]): r["source_text"],
                _lang_tag(r["target_lang"]): r["target_text"]},
            "status": r["status"], "kind": r["kind"],
            "chapter": r["chapter_no"], "section": r["section_no"],
        }, ensure_ascii=False) + "\n")
        n += 1
    with zipfile.ZipFile(fh, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("data/train.jsonl", buf.getvalue())
        z.writestr("README.md", _dataset_card(meta, n))
    return n


def _dataset_card(meta: dict, n: int) -> str:
    return (
        "---\n"
        f"language:\n  - {_lang_tag(meta.get('source_lang') or 'en')}\n"
        f"  - {_lang_tag(meta.get('target_lang') or 'xx')}\n"
        "task_categories:\n  - translation\n"
        "---\n\n"
        f"# {meta.get('project') or 'Setu export'}\n\n"
        f"{n} verified parallel pairs from {meta.get('board') or 'an Indian school board'}"
        f" class {meta.get('class') or '?'} {meta.get('subject') or ''} textbooks,"
        " annotated in Tulana Setu.\n\n"
        "Each record's `translation` field holds the two texts as an annotator "
        "approved them. Rows with an empty side are excluded from this export.\n\n"
        f"Exported {time.strftime('%Y-%m-%d')}.\n")


#: ISO 639-1 where one exists, so the files a translation tool opens are named
#: the way that tool expects. Data, not code: a new language is one line.
LANG_TAGS = {
    "english": "en", "hindi": "hi", "marathi": "mr", "gujarati": "gu",
    "kannada": "kn", "telugu": "te", "tamil": "ta", "malayalam": "ml",
    "punjabi": "pa", "bengali": "bn", "odia": "or", "assamese": "as",
    "urdu": "ur", "sanskrit": "sa", "nepali": "ne", "konkani": "kok",
    "manipuri": "mni", "bodo": "brx", "santali": "sat", "maithili": "mai",
    "dogri": "doi", "kashmiri": "ks", "sindhi": "sd",
}

_TAG_SAFE = re.compile(r"[^a-z0-9]+")


def _lang_tag(name: Any) -> str:
    key = str(name or "").strip().lower()
    if key in LANG_TAGS:
        return LANG_TAGS[key]
    return _TAG_SAFE.sub("-", key).strip("-")[:12] or "xx"


# ── writing a file ─────────────────────────────────────────────────────────

_SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def safe_stem(stem: str, limit: int = 60) -> str:
    """Reduce a person-supplied name to something safe to put in a path.

    Project names come from people, so this has to survive ``../``, a NUL byte,
    a 2,000-character title and a name that reduces to nothing at all.
    """
    base = unicodedata.normalize("NFKD", str(stem or ""))
    base = _SAFE_NAME.sub("_", base).strip("._-")
    return re.sub(r"_{2,}", "_", base)[:limit].strip("._-") or "setu_export"


def safe_filename(stem: str, ext: str, *, suffix: str = "") -> str:
    """Build ``<name>_<suffix>.<ext>`` with the name truncated, not the suffix.

    The suffix carries the format key and the timestamp, which is what keeps
    two formats sharing an extension — Moses and Hugging Face are both zips —
    from overwriting each other inside a bundle. Truncating the whole string
    at the end would eventually eat the format key and reintroduce exactly that
    collision, so the variable-length part is cut first and the suffix is added
    afterwards.
    """
    name = safe_stem(stem)
    tail = _SAFE_NAME.sub("_", str(suffix or "")).strip("._-")
    clean_ext = _SAFE_NAME.sub("", str(ext or "dat"))[:10] or "dat"
    return f"{name}_{tail}.{clean_ext}" if tail else f"{name}.{clean_ext}"


def export(con, pid: str, fmt_key: Any, *, status: str = "", chapter_no: str = "",
           kind: str = "", only_done: bool = False, include_unpaired: bool = True,
           annotator: str = "") -> dict:
    """Write one export file and record it.

    The file is written to a temporary name and renamed into place, so a reader
    never sees a half-written export, and a crash mid-write leaves no file that
    looks complete.
    """
    fmt = get(fmt_key)
    repo = Repository(con)
    proj = repo.one(
        "SELECT p.*, sb.board_name, sb.class AS cls, sb.subject AS subj"
        "  FROM setu_project p JOIN setu_book sb ON sb.book_key = p.src_book"
        " WHERE p.pid = ?", (pid,))
    if not proj:
        raise Invalid(f"no such project: {pid}")

    meta = {
        "tool": "Tulana Setu", "version": "1.0", "project": proj["name"],
        "project_id": pid, "board": proj["board_name"] or proj["board"],
        "class": proj["cls"], "subject": proj["subj"],
        "source_lang": proj["src_language"], "target_lang": proj["tgt_language"],
        "exported_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "filters": json.dumps({"status": status, "chapter_no": chapter_no,
                               "kind": kind, "only_done": only_done,
                               "include_unpaired": include_unpaired},
                              ensure_ascii=False),
    }

    out_dir = Path(config.EXPORT_DIR) / "setu"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    name = safe_filename(proj["name"], fmt.ext, suffix=f"{fmt.key}_{stamp}")
    final = out_dir / name
    tmp = out_dir / (name + ".part")

    rows = records(con, pid, status=status, chapter_no=chapter_no, kind=kind,
                   only_done=only_done, include_unpaired=include_unpaired)
    total_seen = _Counter(rows)
    try:
        if fmt.binary:
            with open(tmp, "wb") as fh:
                written = fmt.writer(total_seen, fh, meta)
        else:
            encoding = "utf-8-sig" if fmt.key == "csv" else "utf-8"
            with open(tmp, "w", encoding=encoding, newline="") as fh:
                written = fmt.writer(total_seen, fh, meta)
        tmp.replace(final)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise

    xid = ids.export_id()
    size = final.stat().st_size
    repo.run(
        "INSERT INTO setu_export(xid, pid, fmt, filename, path, n_rows, n_bytes,"
        " filters, actor, created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
        (xid, pid, fmt.key, name, final.as_posix(), written, size,
         meta["filters"], annotator[:120], time.time()))
    repo.event("export", pid, {"fmt": fmt.key, "rows": written, "bytes": size},
               actor=annotator)

    return {"xid": xid, "path": final, "filename": name, "format": fmt.key,
            "mime": fmt.mime, "rows_written": written,
            "rows_considered": total_seen.count,
            "rows_excluded": total_seen.count - written,
            "pairs_only": fmt.pairs_only, "bytes": size}


class _Counter:
    """Counts what passed through, so an export can report what it left out."""

    def __init__(self, it: Iterable[dict]):
        self._it = it
        self.count = 0

    def __iter__(self) -> Iterator[dict]:
        for item in self._it:
            self.count += 1
            yield item


def bundle(con, pid: str, keys: Iterable[str] | None = None, **filters) -> dict:
    """Every available format at once, in one zip.

    Names inside the archive carry the format key, because several formats
    share an extension — ``json`` and ``parquet`` do not, but ``moses``,
    ``huggingface`` and any future zip-based format all end in ``.zip``, and an
    archive where one file silently overwrites another is worse than useless.
    """
    chosen = [k for k in (keys or REGISTRY) if k in REGISTRY and REGISTRY[k].available]
    if not chosen:
        raise Invalid("no available export formats were selected")
    proj_name = Repository(con).scalar(
        "SELECT name FROM setu_project WHERE pid = ?", (pid,), default="setu") or "setu"
    out_dir = Path(config.EXPORT_DIR) / "setu"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    name = safe_filename(proj_name, "zip", suffix=f"bundle_{stamp}")
    final = out_dir / name
    tmp = out_dir / (name + ".part")

    written: dict[str, int] = {}
    skipped: dict[str, str] = {}
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for key in chosen:
                try:
                    one = export(con, pid, key, **filters)
                except Exception as exc:
                    skipped[key] = f"{type(exc).__name__}: {exc}"
                    continue
                z.write(one["path"], arcname=f"{key}/{one['filename']}")
                written[key] = one["rows_written"]
        tmp.replace(final)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
    return {"path": final, "filename": name, "formats": written,
            "skipped": skipped, "bytes": final.stat().st_size}
