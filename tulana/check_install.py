#!/usr/bin/env python3
"""Is this checkout complete and consistent?

Run this first, after any pull or push. A partial deployment is the hardest
kind of problem to see from the outside: nothing errors, the server starts, and
a feature is simply absent — or the interface offers a tab the backend cannot
answer. This says which, and what to copy.

    python3 check_install.py

Exit code is the number of problems.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
problems, notes = [], []


def ok(msg):
    notes.append(msg)


def bad(msg, fix=""):
    problems.append((msg, fix))


REQUIRED = {
    "app.py": "the API",
    "config.py": "boards, languages, scripts, ports",
    "db.py": "the database (never modified by this work)",
    "library.py": "textbook naming and discovery",
    "pdflib.py": "the PyMuPDF shim",
    "blocks.py": "the parsed-layout corpus — the Blocks tab",
    "layout.py": "human layout annotation",
    "share_gradio.py": "the shareable link",
}
OPTIONAL = {
    "test_stress.py": "138 edge-case and database-safety checks",
    "test_blocks.py": "645 corpus-wide checks",
    "test_naming.py": "265 naming checks",
    "windows_check.py": "cross-platform audit",
    "sources.py": "archive unpacking",
}
for name, what in REQUIRED.items():
    if (HERE / name).exists():
        ok(f"{name} present — {what}")
    else:
        bad(f"{name} is MISSING — {what}", f"copy {name} into {HERE}")
for name, what in OPTIONAL.items():
    if (HERE / name).exists():
        ok(f"{name} present — {what}")
    else:
        notes.append(f"{name} absent (optional) — {what}")

static = HERE / "static"
read = lambda p: p.read_text(encoding="utf-8") if p.exists() else ""
html, js, api = read(static / "index.html"), read(static / "app.js"), read(HERE / "app.py")

# Both directions matter. Pushing only the Python leaves a tab invisible;
# pushing only the interface leaves a tab that appears and then fails.
FEATURES = [
    ("Blocks (the parsed layout)", "/api/blocks", 'data-page="Blocks"', "loadBlocks"),
    ("Layout annotation", "/api/layout/page", 'data-page="Layout"', "loadLayout"),
    ("Missing-textbook diagnosis", "/api/library/diagnose", None, "library/diagnose"),
]
for label, backend, html_marker, js_marker in FEATURES:
    in_backend = backend in api
    in_ui = ((html_marker in html) if html_marker else True) and \
            ((js_marker in js) if js_marker else True)
    if in_backend and in_ui:
        ok(f"{label}: backend and interface agree")
    elif in_backend:
        bad(f"{label}: the backend has it but the interface does not",
            "copy static/index.html, static/app.js and static/style.css")
    elif in_ui:
        bad(f"{label}: the interface offers it but the backend cannot answer",
            "copy app.py, and blocks.py for the Blocks tab")
    else:
        notes.append(f"{label}: not installed on either side")

try:
    sys.path.insert(0, str(HERE))
    import config
    data = (config.discover_data_dir()[0]
            if hasattr(config, "discover_data_dir") else config.DATA_DIR)
    pdfs = list(Path(data).rglob("*.pdf")) if Path(data).is_dir() else []
    if pdfs:
        ok(f"{len(pdfs)} PDF(s) found in {data}")
        pointers = 0
        for p in pdfs[:400]:
            try:
                if open(p, "rb").read(5) != b"%PDF-":
                    pointers += 1
            except OSError:
                pointers += 1
        if pointers:
            bad(f"{pointers} of the PDFs checked are not real PDFs — Git LFS "
                f"pointers, most likely",
                "run `git lfs install && git lfs pull`, then restart")
        else:
            ok("every PDF checked begins with %PDF- — none are LFS pointers")
    else:
        bad(f"no PDFs found — looked in {data}",
            "point TULANA_DATA_DIR at the folder holding the textbooks")
except Exception as e:
    bad(f"could not inspect the data folder: {e}")

# A vendored asset referenced by the HTML but absent produces a 404 on every
# page load. Harmless here — the Guide falls back to plain text — but it looks
# like a fault to whoever opens the developer tools.
for asset in ("vendor/marked.min.js",):
    if asset in html and not (static / asset).exists():
        bad(f"static/{asset} is referenced but absent — every page load 404s",
            f"copy static/{asset}; the Guide still works without it, but the "
            f"console error is misleading")

if not (HERE / "blocks.py").exists():
    bad("the parsed-layout corpus cannot be checked, because blocks.py is absent",
        "copy blocks.py, then run this again")
try:
    import blocks as _b
    corpus = _b.find_corpus()
    if corpus:
        allj = list(Path(corpus).rglob("*.json"))
        n = len([f for f in allj
                 if not _b._is_junk(f.relative_to(corpus))])
        junk = len(allj) - n
        if junk:
            notes.append(f"{junk} archive-litter file(s) in the corpus are ignored "
                         f"(macOS __MACOSX resource forks)")
        ok(f"parsed-layout corpus found at {corpus} — {n} JSON file(s)")
        if n < 5:
            notes.append("that is very few books; check the whole corpus was copied")
    else:
        bad("no parsed-layout corpus found — the Blocks tab will be empty",
            "unpack the parser output as `output/` beside the PDFs, or as a "
            "sibling of the data folder")
except ImportError:
    pass
except Exception as e:
    bad(f"could not inspect the layout corpus: {e}")

# A module present but unreferenced is the other half of a partial push, and it
# fails quietly: the file is there, nothing imports it, the tab never appears.
if (HERE / "blocks.py").exists() and "/api/blocks" not in api:
    bad("blocks.py is present but app.py does not use it",
        "copy the newer app.py — the module is installed but unreachable")
if (HERE / "layout.py").exists() and "/api/layout" not in api:
    bad("layout.py is present but app.py does not use it", "copy the newer app.py")

print("TULANA — INSTALLATION CHECK")
print(f"  {HERE}\n")
for n in notes:
    print(f"  ok     {n}")
if problems:
    print()
    for msg, fix in problems:
        print(f"  PROBLEM  {msg}")
        if fix:
            print(f"           → {fix}")
print(f"\n  {len(notes)} ok, {len(problems)} problem(s)")
sys.exit(len(problems))
