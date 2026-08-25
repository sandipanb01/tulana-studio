#!/usr/bin/env python3
"""shelf.py — make a newly added textbook PDF visible in Tulana Studio.

Put this file either in the repository root or in the `tulana/` folder — it
finds the studio's own config/db/library modules on its own, so it always
agrees with the running application about where the data folder is and how a
document row is shaped.

    python shelf.py doctor                 # why is my PDF not in the dropdown?
    python shelf.py doctor --template      # write shelf_overrides.json to fill in
    python shelf.py apply                  # register everything in that file
    python shelf.py add FILE --board WB --class 10 --lang Bengali
    python shelf.py add FILE ... --replace # same path, new file: also drop stale cache

SAFETY CONTRACT — this tool:
  * writes to the `documents` table only;
  * only ever INSERTs a new row or UPDATEs the metadata columns of a row it
    matched by path — an existing document keeps its `id`, so no clip, pair or
    project can be orphaned;
  * never issues DELETE or DROP, and never touches clips/pairs/projects/labels;
  * takes a consistent .backup of the database before its first write.

WHY THE METADATA STICKS: library.scan() skips any row whose path and checksum
still match what is on disk. Because this tool stores the same checksum
library.sha256() would compute, a hand-set board/class/language survives every
restart and every rescan. No studio source file needs to be edited.
"""
import argparse
import json
import os
import shutil
import sqlite3
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent.resolve()


def _find_studio():
    """Locate the folder holding config.py / db.py / library.py.

    The file gets dropped either next to app.py or at the repository root, and
    it is run from whichever directory the person happens to be standing in.
    Rather than insist on one layout, look in the obvious places.
    """
    seen, cands = set(), []
    for base in (HERE, Path.cwd().resolve(), *HERE.parents):
        for c in (base, base / "tulana"):
            if c not in seen:
                seen.add(c)
                cands.append(c)
    for c in cands:
        if all((c / f).is_file() for f in ("config.py", "db.py", "library.py")):
            return c
    return None


_STUDIO = _find_studio()
if _STUDIO is None:
    sys.exit("Could not find the studio modules (config.py, db.py, library.py).\n"
             "Put shelf.py in the repository root or in the tulana/ folder, "
             "and run it from inside the repository.")
sys.path.insert(0, str(_STUDIO))

try:
    import config
    import db
    import library
    from pdflib import fitz
except ImportError as e:
    sys.exit(f"Found {_STUDIO} but could not import from it: {e}")

OVERRIDES = _STUDIO / "shelf_overrides.json"
LFS_MAGIC = b"version https://git-lfs.github.com"

C = {"ok": "\033[32m", "bad": "\033[31m", "warn": "\033[33m",
     "dim": "\033[2m", "b": "\033[1m", "_": "\033[0m"}
if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
    C = {k: "" for k in C}


# ------------------------------------------------------------------ helpers --
def backup_db():
    """A consistent copy, taken through SQLite so WAL content is included."""
    if not Path(config.DB_PATH).exists():
        return None
    dest = Path(config.DB_PATH).with_name(
        f"studio.backup-{time.strftime('%Y%m%d-%H%M%S')}.db")
    src = sqlite3.connect(str(config.DB_PATH))
    dst = sqlite3.connect(str(dest))
    with dst:
        src.backup(dst)
    src.close(); dst.close()
    old = sorted(dest.parent.glob("studio.backup-*.db"))[:-10]
    for p in old:                      # keep the ten most recent
        p.unlink(missing_ok=True)
    return dest


def read_state(path: Path):
    """Everything that decides whether this file can become a document row."""
    st = {"path": path, "size": path.stat().st_size, "pages": None,
          "problem": None, "hint": None}
    if path.suffix != ".pdf":
        st["problem"] = f"extension is '{path.suffix}', not lowercase '.pdf'"
        st["hint"] = ("library.scan uses rglob('*.pdf'), which is case-sensitive "
                      "on Linux. Rename the file to lowercase .pdf")
        return st
    try:
        head = path.open("rb").read(64)
    except OSError as e:
        st["problem"] = f"cannot be read: {e}"
        return st
    if head.startswith(LFS_MAGIC):
        st["problem"] = "this is a Git LFS pointer, not a PDF"
        st["hint"] = "git lfs install && git lfs pull   (then re-run doctor)"
        return st
    if fitz is None:
        st["problem"] = "PyMuPDF is not installed, so no PDF can be opened"
        return st
    try:
        with fitz.open(path) as d:
            st["pages"] = d.page_count
        if not st["pages"]:
            st["problem"] = "opens but has zero pages"
    except Exception as e:
        st["problem"] = f"not a readable PDF: {str(e)[:90]}"
        st["hint"] = "re-download or re-export it; a truncated upload looks like this"
    return st


def guess(path: Path):
    return library.infer(path, config.DATA_DIR)


def missing_fields(meta):
    return [k for k in ("board", "class", "language") if not meta.get(k)]


def validate(board, cls, lang, subject):
    board = str(board).upper() if board else None
    if board not in config.BOARDS:
        sys.exit(f"--board must be one of: {', '.join(sorted(config.BOARDS))}")
    langs = sorted(set(config.SCRIPTS) | set(config.EXPORT_CODE))
    if lang not in langs:
        sys.exit(f"--lang must be one of: {', '.join(langs)}")
    try:
        cls = int(cls)
    except (TypeError, ValueError):
        sys.exit("--class must be a number, e.g. 10")
    if not 1 <= cls <= 12:
        sys.exit("--class must be between 1 and 12")
    return board, cls, lang, subject or "Mathematics"


def register(con, rel, board, cls, lang, subject, volume, pages, checksum):
    """Insert or metadata-update one row. Returns (doc_id, 'added'|'updated')."""
    meta = {"board": board, "class": cls, "language": lang,
            "subject": subject, "volume": volume}
    title = library.title_for(meta)
    row = con.execute("SELECT id FROM documents WHERE path=?", (rel,)).fetchone()
    if row:
        con.execute(
            """UPDATE documents SET board=?, class=?, subject=?, language=?,
               script=?, volume=?, title=?, pages=?, checksum=? WHERE id=?""",
            (board, cls, subject, lang, config.script_of(lang), volume,
             title, pages, checksum, row["id"]))
        return row["id"], "updated"
    cur = con.execute(
        """INSERT INTO documents(path, board, class, subject, language, script,
           volume, title, pages, checksum, added_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
        (rel, board, cls, subject, lang, config.script_of(lang), volume,
         title, pages, checksum, time.time()))
    return cur.lastrowid, "added"


def clear_page_cache(doc_id):
    n = 0
    for p in Path(config.PAGE_CACHE).glob(f"d{doc_id}_p*"):
        p.unlink(missing_ok=True); n += 1
    return n


def visibility_report(con):
    """Exactly what the board/class dropdown will contain."""
    combos = library.pairable(con)
    groups = {}
    for r in con.execute("""SELECT board, class, subject, language, COUNT(*) n
                            FROM documents GROUP BY board, class, subject, language"""):
        groups.setdefault((r["board"], r["class"], r["subject"]), []).append(
            (r["language"], r["n"]))
    return combos, groups


# ------------------------------------------------------------------- doctor --
def cmd_doctor(args):
    root = Path(config.DATA_DIR)
    print(f"{C['b']}Tulana Studio — library doctor{C['_']}")
    print(f"  data folder : {root}")
    print(f"  database    : {config.DB_PATH}")
    print(f"  page cache  : {config.PAGE_CACHE}")
    if not root.is_dir():
        print(f"\n{C['bad']}The data folder does not exist.{C['_']}")
        print("  The studio only ever looks inside this one folder. Point it at "
              "your PDFs with:\n    export TULANA_DATA_DIR=/absolute/path/to/board_pdfs")
        return 1

    every = sorted(p for p in root.rglob("*")
                   if p.is_file() and p.suffix.lower() == ".pdf"
                   and not any(x.startswith(".") for x in p.parts))
    seen_by_scan = {p.resolve() for p in root.rglob("*.pdf")}
    if not every:
        print(f"\n{C['bad']}No PDF files anywhere under this folder.{C['_']}")
        return 1

    with db.tx() as con:
        rows = {r["path"]: dict(r) for r in con.execute("SELECT * FROM documents")}
        used = {r[0] for r in con.execute("SELECT DISTINCT doc_id FROM clips")}

    ok, broken, basenames = [], [], {}
    for p in every:
        rel = p.relative_to(root).as_posix()
        basenames.setdefault(p.name.lower(), []).append(rel)
        st = read_state(p)
        meta = guess(p)
        row = rows.get(rel)
        # a row already in the database wins: its metadata may have been set here
        eff = {k: (row[k] if row and row.get(k) is not None else meta.get(k))
               for k in ("board", "class", "language", "subject")}
        reasons = []
        if p.resolve() not in seen_by_scan:
            reasons.append("the scanner's glob does not match this filename")
        if st["problem"]:
            reasons.append(st["problem"])
        for f in missing_fields(eff):
            reasons.append(f"{f} could not be worked out from the filename")
        entry = {"rel": rel, "state": st, "eff": eff, "row": row,
                 "reasons": reasons, "guess": meta}
        (broken if reasons else ok).append(entry)

    print(f"\n{C['b']}{len(every)} PDF file(s) on disk, "
          f"{len(rows)} row(s) in the library, "
          f"{len(ok)} file(s) with complete metadata.{C['_']}")

    if broken:
        print(f"\n{C['bad']}{C['b']}Not usable yet — {len(broken)} file(s){C['_']}")
        by_sig = {}
        for e in broken:
            by_sig.setdefault(" + ".join(e["reasons"]), []).append(e)
        for sig, files in sorted(by_sig.items(), key=lambda kv: -len(kv[1])):
            print(f"\n  {C['bad']}·{C['_']} {C['b']}{sig}{C['_']}"
                  f"  {C['dim']}({len(files)} file"
                  f"{'s' if len(files) > 1 else ''}){C['_']}")
            hint = next((f["state"]["hint"] for f in files if f["state"]["hint"]), None)
            if hint:
                print(f"    {C['dim']}→ {hint}{C['_']}")
            elif missing_fields(files[0]["eff"]):
                print(f"    {C['dim']}→ fix each with: python shelf.py add "
                      f"\"<path>\" --board … --class … --lang …{C['_']}")
                print(f"    {C['dim']}→ or all at once: python shelf.py doctor "
                      f"--template{C['_']}")
            limit = len(files) if args.all else 6
            for e in files[:limit]:
                g = e["eff"]
                have = ", ".join(f"{k}={g[k]}" for k in
                                 ("board", "class", "language") if g[k])
                extra = f"   {C['dim']}read: {have}{C['_']}" if (
                    have and missing_fields(g)) else ""
                print(f"      {e['rel']}{extra}")
            if len(files) > limit:
                print(f"      {C['dim']}… and {len(files) - limit} more "
                      f"(--all to list){C['_']}")

    if args.audit and ok:
        print(f"\n{C['b']}What each usable file resolved to{C['_']}")
        print(f"  {C['dim']}Check this column by column — a wrong-but-confident "
              f"reading is invisible otherwise. `tm` reads as Tamil Nadu, so "
              f"telangana-…-tm-… lands under the wrong board.{C['_']}")
        for e in sorted(ok, key=lambda x: (str(x["eff"]["board"]),
                                           str(x["eff"]["class"]))):
            g = e["eff"]
            print(f"    {str(g['board']):6} cls {str(g['class']):3} "
                  f"{str(g['language']):10} {g['subject']:15} {e['rel']}")

    # duplicate basenames matter: open_doc() falls back to a basename search
    dupes = {k: v for k, v in basenames.items() if len(v) > 1}
    if dupes:
        print(f"\n{C['warn']}{C['b']}Duplicate filenames — {len(dupes)}{C['_']}")
        print(f"  {C['dim']}If a path ever goes missing the viewer opens the first"
              f" file with a matching name, which may be the wrong copy.{C['_']}")
        for name, paths in list(dupes.items())[:10]:
            print(f"    {name}: {', '.join(paths)}")

    phantom = [p for p in rows if not (root / p).exists()]
    if phantom:
        print(f"\n{C['warn']}{C['b']}Library rows whose file is gone — "
              f"{len(phantom)}{C['_']}")
        for p in phantom[:10]:
            tag = " (has clips — do not remove)" if rows[p]["id"] in used else ""
            print(f"    {p}{tag}")

    pending = [e for e in ok if not e["row"]]
    if pending:
        print(f"\n{C['warn']}{C['b']}Ready, but not indexed yet — "
              f"{len(pending)} file(s){C['_']}")
        print(f"  {C['dim']}Metadata reads cleanly; the library simply has not "
              f"been rescanned since these appeared.{C['_']}")
        for e in pending[:8]:
            g = e["eff"]
            print(f"      {e['rel']}   {C['dim']}{g['board']} · Class "
                  f"{g['class']} · {g['language']}{C['_']}")
        if len(pending) > 8:
            print(f"      {C['dim']}… and {len(pending) - 8} more{C['_']}")
        print(f"  {C['dim']}→ restart the studio, or: "
              f"curl -X POST http://localhost:{config.PORT}/api/rescan{C['_']}")

    with db.tx() as con:
        combos, groups = visibility_report(con)
    print(f"\n{C['b']}What the dropdown will show right now{C['_']}")
    if combos:
        for c in combos:
            langs = ", ".join(f"{l} ×{n}" for l, n in
                              sorted(groups.get((c["board"], c["class"],
                                                 c["subject"]), [])))
            print(f"  {C['ok']}✓{C['_']} {config.board_name(c['board'])} · "
                  f"Class {c['class']} · {c['subject']}  {C['dim']}[{langs}]{C['_']}")
    else:
        print(f"  {C['bad']}nothing — the dropdown will be empty{C['_']}")

    shown = {(c["board"], c["class"], c["subject"]) for c in combos}
    unpaired = [(k, v) for k, v in groups.items()
                if k[0] and k[1] and k not in shown]
    if unpaired:
        print(f"\n{C['warn']}{C['b']}Indexed but hidden — no English partner{C['_']}")
        print(f"  {C['dim']}A board/class/subject group appears only when it holds "
              f"an English edition and at least one other language.{C['_']}")
        for (b, cl, sub), langs in unpaired[:15]:
            names = ", ".join(l for l, _ in langs)
            need = "add an English edition" if "English" not in dict(langs) \
                else "add a non-English edition"
            print(f"    {config.board_name(b)} · Class {cl} · {sub} "
                  f"[{names}] → {need}")

    if args.template:
        stub = []
        for e in broken:
            if e["state"]["problem"] and "extension" not in str(e["state"]["problem"]):
                continue          # a broken file needs fixing on disk, not here
            g = e["eff"]
            stub.append({"path": e["rel"],
                         "board": g["board"] or "",
                         "class": g["class"] or "",
                         "lang": g["language"] or "",
                         "subject": g["subject"] or "Mathematics",
                         "volume": ""})
        OVERRIDES.write_text(json.dumps(
            {"_boards": sorted(config.BOARDS),
             "_languages": sorted(set(config.SCRIPTS) | set(config.EXPORT_CODE)),
             "documents": stub}, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n{C['ok']}Wrote {OVERRIDES} with {len(stub)} entr(ies).{C['_']}")
        print("  Fill in the blank fields, then run:  python shelf.py apply")
    return 0


# --------------------------------------------------------------------- add ---
def cmd_add(args):
    root = Path(config.DATA_DIR)
    p = Path(args.file)
    if not p.is_absolute():
        p = (root / args.file) if (root / args.file).exists() else Path.cwd() / args.file
    p = p.resolve()
    if not p.exists():
        sys.exit(f"No such file: {p}")
    try:
        rel = p.relative_to(root).as_posix()
    except ValueError:
        sys.exit(f"That file is outside the data folder.\n  data folder: {root}\n"
                 f"  file:        {p}\nCopy it under the data folder first.")

    st = read_state(p)
    if st["problem"] and "extension" not in st["problem"]:
        print(f"{C['bad']}{st['problem']}{C['_']}")
        if st["hint"]:
            print(f"  → {st['hint']}")
        sys.exit(1)

    board, cls, lang, subject = validate(args.board, getattr(args, "class"),
                                         args.lang, args.subject)
    checksum = library.sha256(p)
    bk = backup_db()
    if bk:
        print(f"{C['dim']}database backed up to {bk.name}{C['_']}")
    with db.tx() as con:
        doc_id, what = register(con, rel, board, cls, lang, subject,
                                args.volume or None, st["pages"], checksum)
        combos = library.pairable(con)
    print(f"{C['ok']}{what}{C['_']}  id={doc_id}  {rel}")
    print(f"  {config.board_name(board)} · Class {cls} · {subject} · {lang} "
          f"· {st['pages']} pages")
    if args.replace:
        print(f"  cleared {clear_page_cache(doc_id)} cached page image(s)")
    hit = [c for c in combos if (c["board"], c["class"], c["subject"])
           == (board, cls, subject)]
    if hit:
        print(f"{C['ok']}It will appear in the dropdown.{C['_']} "
              f"Restart the studio, or open Sources → “Unpack what is here”, "
              f"then reload the page.")
    else:
        other = "an English" if lang != "English" else "a non-English"
        print(f"{C['warn']}Registered, but still hidden:{C['_']} this "
              f"board/class/subject needs {other} edition too.")
    return 0


# ------------------------------------------------------------------- apply ---
def cmd_apply(args):
    src = Path(args.file) if args.file else OVERRIDES
    if not src.exists():
        sys.exit(f"{src} not found. Run:  python shelf.py doctor --template")
    data = json.loads(src.read_text(encoding="utf-8"))
    items = data.get("documents", data if isinstance(data, list) else [])
    root = Path(config.DATA_DIR)
    todo, skipped = [], []
    for it in items:
        rel = str(it.get("path", "")).strip()
        if not rel:
            continue
        p = root / rel
        if not p.exists():
            skipped.append((rel, "file not found under the data folder")); continue
        if not all(str(it.get(k, "")).strip() for k in ("board", "class", "lang")):
            skipped.append((rel, "board / class / lang not filled in")); continue
        st = read_state(p)
        if st["problem"] and "extension" not in st["problem"]:
            skipped.append((rel, st["problem"])); continue
        b, c, l, s = validate(it["board"], it["class"], it["lang"],
                              it.get("subject"))
        todo.append((rel, p, b, c, l, s, (it.get("volume") or "").strip() or None,
                     st["pages"]))

    for rel, why in skipped:
        print(f"{C['warn']}skip{C['_']} {rel} — {why}")
    if not todo:
        print("Nothing to apply.")
        return 1
    print(f"\n{len(todo)} document(s) to register:")
    for rel, _, b, c, l, s, v, pg in todo:
        print(f"  {rel}\n    → {config.board_name(b)} · Class {c} · {s} · {l}"
              f"{' · ' + v if v else ''} · {pg} pages")
    if not args.yes and input("\nProceed? [y/N] ").strip().lower() != "y":
        print("Cancelled — nothing was written.")
        return 1

    bk = backup_db()
    if bk:
        print(f"{C['dim']}database backed up to {bk.name}{C['_']}")
    with db.tx() as con:
        for rel, p, b, c, l, s, v, pg in todo:
            doc_id, what = register(con, rel, b, c, l, s, v, pg,
                                    library.sha256(p))
            print(f"  {C['ok']}{what}{C['_']} id={doc_id} {rel}")
        combos = library.pairable(con)
    print(f"\n{C['b']}The dropdown will now show:{C['_']}")
    for c in combos:
        print(f"  ✓ {config.board_name(c['board'])} · Class {c['class']} "
              f"· {c['subject']}")
    print("\nRestart the studio (or Sources → “Unpack what is here”) and reload.")
    return 0


def main():
    ap = argparse.ArgumentParser(
        prog="shelf.py", description="Diagnose and register Tulana textbooks.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("doctor", help="explain why a PDF is not in the dropdown")
    d.add_argument("--template", action="store_true",
                   help="write shelf_overrides.json for the unusable files")
    d.add_argument("--all", action="store_true", help="list every affected file")
    d.add_argument("--audit", action="store_true",
                   help="list what every usable file resolved to")
    d.set_defaults(fn=cmd_doctor)

    a = sub.add_parser("add", help="register one PDF with metadata you supply")
    a.add_argument("file", help="path to the PDF, relative to the data folder")
    a.add_argument("--board", required=True)
    a.add_argument("--class", required=True, dest="class")
    a.add_argument("--lang", required=True)
    a.add_argument("--subject", default="Mathematics")
    a.add_argument("--volume", default="")
    a.add_argument("--replace", action="store_true",
                   help="the file at this path changed: drop its cached pages")
    a.set_defaults(fn=cmd_add)

    p = sub.add_parser("apply", help="register everything in shelf_overrides.json")
    p.add_argument("file", nargs="?")
    p.add_argument("--yes", "-y", action="store_true")
    p.set_defaults(fn=cmd_apply)

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
