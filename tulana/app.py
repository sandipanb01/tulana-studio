"""Tulana Studio — parallel chunk clipping across two textbook editions.

The annotator reads the English edition and its translation side by side,
marks the region on each page that says the same thing, and saves the two as a
parallel pair. The studio's job is to make that fast, keep every clipping
identifiable afterwards, and hand the result over in whatever format the next
stage needs.

Design notes worth knowing:

* A clipping is stored as **page + rectangle in PDF points**, not as a picture
  of what was on screen. The image is re-rendered from the source PDF at print
  resolution when it is saved and again at export, so a clipping never degrades
  and stays correct if the viewer changes.
* Text under the rectangle is extracted at the same time. Where the PDF has a
  readable text layer this gives a parallel *text* corpus for free, alongside
  the images.
* Excluded topics (geometry, conics and the rest) are detected from the page
  text and flagged, so an annotator is warned rather than silently allowed to
  build pairs the project does not want.
"""
import io
import json
import os
import re
import time
import zipfile
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException, Header, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import config
import db
import blocks
import layout
import pairs as bpairs
import library
from pdflib import fitz

app = FastAPI(title="Tulana Studio", version="2.0.0")

_DOC_CACHE: dict = {}
_DOC_ORDER: list = []
_DOC_MAX = 6


def open_doc(rel_path: str):
    """Reuse open documents — opening a textbook costs more than drawing a page."""
    if fitz is None:
        raise HTTPException(500, "PyMuPDF is not installed on the server")
    key = str(rel_path)
    if key in _DOC_CACHE:
        return _DOC_CACHE[key]
    full = (config.DATA_DIR / Path(*str(rel_path).replace("\\", "/").split("/")))
    if not full.exists():
        found = next((p for p in config.DATA_DIR.rglob(Path(rel_path).name)), None)
        if found is None:
            raise HTTPException(404, f"Textbook file not found: {Path(rel_path).name}")
        full = found
    doc = fitz.open(str(full))
    _DOC_CACHE[key] = doc
    _DOC_ORDER.append(key)
    while len(_DOC_ORDER) > _DOC_MAX:
        old = _DOC_ORDER.pop(0)
        try:
            _DOC_CACHE.pop(old).close()
        except Exception:
            pass
    return doc


def resolve_path(rel_path: str) -> Path:
    """The real file for a stored relative path.

    Mirrors open_doc's fallback: if the recorded path no longer resolves —
    the corpus moved, or auto-discovery picked a different folder — the file is
    looked up by name before giving up."""
    full = (config.DATA_DIR / Path(*str(rel_path).replace("\\", "/").split("/")))
    if full.exists():
        return full
    found = next((p for p in config.DATA_DIR.rglob(Path(rel_path).name)), None)
    if found is None:
        raise HTTPException(404, f"Textbook file not found: {Path(rel_path).name}")
    return found


def doc_row(con, doc_id: int):
    r = con.execute("SELECT * FROM documents WHERE id=?", (doc_id,)).fetchone()
    if not r:
        raise HTTPException(404, "Unknown textbook")
    return r


# ---------------------------------------------------------------- library ---
def _scan_log(message: str):
    """Print only what an operator needs to see from a scan."""
    text = (message or "").strip()
    if any(k in text for k in ("[warn]", "[skip]", "[error]")):
        print(f"[studio] {text}")


@app.on_event("startup")
def _index_on_startup():
    initialise()



def interface_matches_backend() -> dict:
    """Is the interface as new as the code serving it?

    A half-deployed update is silent and confusing: `layout.py` ships, the
    endpoints answer, and the annotator sees no Layout tab because
    `static/index.html` was not copied. Nothing errors — the feature simply
    appears not to exist. This compares what the backend can do with what the
    interface offers, and says so out loud."""
    static = Path(__file__).parent / "static"
    report = {"ok": True, "missing": [], "static_dir": str(static)}
    try:
        html = (static / "index.html").read_text(encoding="utf-8")
        js = (static / "app.js").read_text(encoding="utf-8")
    except OSError as e:
        report["ok"] = False
        report["missing"].append(f"static files unreadable: {e}")
        return report

    # each entry: the backend feature, and the marker the interface must carry
    for feature, marker, where in (
            ("layout annotation", 'data-page="Layout"', "static/index.html"),
            ("layout annotation", "loadLayout", "static/app.js"),
            ("missing-textbook diagnosis", "library/diagnose", "static/app.js")):
        blob = html if where.endswith("index.html") else js
        if marker not in blob:
            report["ok"] = False
            report["missing"].append(
                f"{feature}: the backend has it, but {where} does not "
                f"(looked for {marker!r})")
    return report


def initialise():
    """Index the textbook folder however the application was launched.

    Deliberately a plain function as well as a startup hook. FastAPI does not
    fire startup events for a sub-application mounted onto a server that is
    already running, which is exactly what share_gradio.py does — so relying on
    the hook alone brought the studio up with an empty dropdown and no
    explanation. Idempotent, so calling it twice is harmless.

    Doing this only in the __main__ block meant that running under `uvicorn
    app:app` — which is how it is deployed and tested — started the studio with
    an empty library and no explanation."""
    # Two separate concerns, so a failure in one cannot silently take the other
    # down with it. Wrapping both in a single try meant that any error while
    # unpacking archives — including a missing optional module — skipped the
    # indexing entirely, and the studio came up with an empty dropdown.
    try:
        import sources as srcmod
        if config.DATA_DIR.is_dir() and not any(config.DATA_DIR.rglob("*.pdf")):
            # Nothing to work with yet: unpack whatever archives are here.
            # Downloading is left to an explicit request so startup is never
            # blocked on a slow link.
            srcmod.extract_all(config.DATA_DIR, log=lambda m: print("[studio]", m))
    except Exception as e:
        print(f"[studio] could not unpack archives in {config.DATA_DIR}: {e}")

    # Locate the corpus before scanning. Depending on a symlink the operator
    # has to create by hand — and which .gitignore excludes — made an empty
    # dropdown the default outcome of a fresh clone.
    try:
        found, note = config.discover_data_dir()
        if note:
            print(f"[studio] {note}")
        config.DATA_DIR = found
    except Exception as e:
        print(f"[studio] could not locate the textbook folder: {e}")

    try:
        with db.tx() as con:
            # Suppress the routine per-file chatter but never the warnings:
            # silencing the scan entirely hid the one line that explains an
            # empty dropdown ("these files are Git LFS pointers").
            n = library.scan(con, config.DATA_DIR, log=_scan_log)
        print(f"[studio] {n} textbook PDF(s) available from {config.DATA_DIR}")
        try:
            with db.tx() as bcon:
                r = blocks.ingest(bcon, data_dir=config.DATA_DIR, log=lambda m: None)
            if r["books"]:
                print(f"[studio] parsed layout: {r['books']} books, "
                      f"{r['blocks']} blocks from {r['corpus']}")
                for p in r["problems"]:
                    print(f"[studio]   {p}")
            else:
                print("[studio] no parsed-layout corpus found — the Blocks tab "
                      "will be empty until one is placed beside the data folder")
        except Exception as e:
            print(f"[studio] could not load the parsed layout: {e}")

        iface = interface_matches_backend()
        if not iface["ok"]:
            print("[studio] the interface is older than the code serving it — "
                  "copy the static/ files as well as the Python ones:")
            for m in iface["missing"]:
                print(f"[studio]   {m}")
        if n == 0:
            print(f"[studio] nothing indexed. Checked {config.DATA_DIR} — set "
                  f"TULANA_DATA_DIR to the folder holding your PDFs, or run "
                  f"`git lfs pull` if the files are LFS pointers.")
    except Exception as e:                      # never block startup
        print(f"[studio] could not index {config.DATA_DIR}: {e}")


@app.get("/api/version")
def version_info():
    """What this deployment can actually do, and whether its interface agrees."""
    with db.tx() as con:
        try:
            layout.ensure_schema(con)
            has_layout = True
        except Exception:
            has_layout = False
    return {"backend": {"layout_annotation": has_layout,
                        "layout_metrics_version": layout.METRICS_VERSION,
                        "library_diagnose": True},
            "interface": interface_matches_backend()}


@app.get("/api/health")
def health():
    with db.tx() as con:
        n = con.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        p = con.execute("SELECT COUNT(*) FROM pairs").fetchone()[0]
    from pdflib import available, version
    return {"ok": True, "documents": n, "pairs": p,
            "data_dir": str(config.DATA_DIR), "pymupdf": version(),
            "pdf_ready": available()}


@app.get("/api/library/diagnose")
def library_diagnose():
    """Every PDF found, and for anything not in the dropdown, the reason why."""
    with db.tx() as con:
        return library.diagnose(con, config.DATA_DIR)


@app.get("/api/library")
def get_library():
    """Boards, classes and the language editions available for each."""
    with db.tx() as con:
        combos = library.pairable(con)
        out = []
        for c in combos:
            docs = con.execute(
                """SELECT id, language, title, pages, volume, path FROM documents
                   WHERE board=? AND class=? AND subject=? ORDER BY language, volume""",
                (c["board"], c["class"], c["subject"])).fetchall()
            # Same existence filter as pairable(): an edition whose file was
            # removed by a pull must not be offered, or opening it 404s.
            docs = [d for d in docs if library.present(config.DATA_DIR, d["path"])]
            english = [dict(d) for d in docs if d["language"] == "English"]
            targets = [dict(d) for d in docs if d["language"] != "English"]
            langs = sorted({d["language"] for d in targets})
            out.append({
                "board": c["board"], "board_name": config.board_name(c["board"]),
                "class": c["class"], "class_name": f"Class {c['class']}",
                "subject": c["subject"],
                "target_languages": langs,
                "english_editions": english, "target_editions": targets,
                "label": f"{config.board_name(c['board'])} · Class {c['class']} · {c['subject']}",
            })
    return out


@app.get("/api/doc/{doc_id}")
def get_doc(doc_id: int):
    with db.tx() as con:
        r = doc_row(con, doc_id)
    d = dict(r)
    doc = open_doc(r["path"])
    d["page_sizes"] = [{"w": round(doc[i].rect.width, 1),
                        "h": round(doc[i].rect.height, 1)}
                       for i in range(min(doc.page_count, 2))]
    return d


@app.get("/api/doc/{doc_id}/page/{page}.png")
def doc_page(doc_id: int, page: int, dpi: int | None = Query(None, ge=40, le=400)):
    """A rendered page, cached on disk so scrolling back is instant."""
    # Query() carries a default only when FastAPI resolves it; calling this
    # function directly (tests, tooling) would otherwise pass the marker object
    # straight into the renderer.
    dpi = config.VIEW_DPI if not isinstance(dpi, int) else max(40, min(400, dpi))
    with db.tx() as con:
        r = doc_row(con, doc_id)
    cache = config.PAGE_CACHE / f"d{doc_id}_p{page}_{dpi}.png"
    if not cache.exists():
        doc = open_doc(r["path"])
        if page < 1 or page > doc.page_count:
            raise HTTPException(404, f"Page out of range (1..{doc.page_count})")
        pix = doc[page - 1].get_pixmap(dpi=dpi)
        # PyMuPDF picks the encoder from the file extension, so the temporary
        # name has to stay a .png; the pid keeps concurrent renders apart and
        # the rename is atomic, so a reader never sees a partial file.
        tmp = cache.with_name(cache.stem + f".{os.getpid()}.part.png")
        pix.save(tmp)
        tmp.replace(cache)
    return FileResponse(cache, media_type="image/png",
                        headers={"Cache-Control": "public, max-age=31536000, immutable"})


@app.get("/api/doc/{doc_id}/page/{page}/text")
def doc_page_text(doc_id: int, page: int):
    """Page text plus an excluded-topic check, used to warn the annotator."""
    with db.tx() as con:
        r = doc_row(con, doc_id)
    doc = open_doc(r["path"])
    if page < 1 or page > doc.page_count:
        raise HTTPException(404, "Page out of range")
    text = doc[page - 1].get_text()
    excluded, term = library.is_excluded(text)
    return {"page": page, "chars": len(text.strip()),
            "excluded_topic": excluded, "matched_term": term,
            "text": text[:4000]}


@app.get("/api/doc/{doc_id}/outline")
def doc_outline(doc_id: int):
    """Chapter bookmarks, so an annotator can jump rather than scroll."""
    with db.tx() as con:
        r = doc_row(con, doc_id)
    doc = open_doc(r["path"])
    items = []
    try:
        for lvl, title, page in (doc.get_toc() or [])[:400]:
            excluded, term = library.is_excluded(title)
            items.append({"level": lvl, "title": title, "page": page,
                          "excluded_topic": excluded, "matched_term": term})
    except Exception:
        pass
    return {"pages": doc.page_count, "outline": items}


# --------------------------------------------------------------- projects ---
class ProjectIn(BaseModel):
    board: str
    cls: int
    subject: str = "Mathematics"
    src_doc: int
    tgt_doc: int
    name: str = ""


@app.post("/api/projects")
def create_project(body: ProjectIn, x_annotator: str = Header("")):
    with db.tx() as con:
        s, t = doc_row(con, body.src_doc), doc_row(con, body.tgt_doc)
        name = body.name.strip() or (
            f"{body.board}_class_{body.cls}_"
            f"{body.subject.split()[0].lower()}")
        existing = con.execute(
            "SELECT * FROM projects WHERE src_doc=? AND tgt_doc=?",
            (body.src_doc, body.tgt_doc)).fetchone()
        if existing:
            return dict(existing)
        cur = con.execute(
            """INSERT INTO projects(name, board, class, subject, src_doc, tgt_doc,
               src_language, tgt_language, created_at)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            (name, body.board, body.cls, body.subject, body.src_doc, body.tgt_doc,
             s["language"], t["language"], time.time()))
        db.log(con, x_annotator, "project_create", name,
               {"src": s["title"], "tgt": t["title"]})
        seed_labels(con, cur.lastrowid)
        row = con.execute("SELECT * FROM projects WHERE id=?", (cur.lastrowid,)).fetchone()
    return dict(row)


@app.get("/api/projects")
def list_projects():
    with db.tx() as con:
        rows = con.execute("""
            SELECT p.*, ds.title AS src_title, dt.title AS tgt_title,
                   ds.pages AS src_pages, dt.pages AS tgt_pages,
                   (SELECT COUNT(*) FROM pairs WHERE project_id=p.id) AS n_pairs
            FROM projects p
            JOIN documents ds ON ds.id=p.src_doc
            JOIN documents dt ON dt.id=p.tgt_doc
            ORDER BY p.created_at DESC""").fetchall()
    return [dict(r) for r in rows]


@app.get("/api/projects/{pid}")
def get_project(pid: int):
    with db.tx() as con:
        r = con.execute("""
            SELECT p.*, ds.title AS src_title, dt.title AS tgt_title,
                   ds.pages AS src_pages, dt.pages AS tgt_pages,
                   ds.language AS src_lang, dt.language AS tgt_lang
            FROM projects p JOIN documents ds ON ds.id=p.src_doc
            JOIN documents dt ON dt.id=p.tgt_doc WHERE p.id=?""", (pid,)).fetchone()
    if not r:
        raise HTTPException(404, "Unknown project")
    return dict(r)


# ----------------------------------------------------------------- labels ---
# Categories an annotator applies to a chunk, in the doccano manner: a named
# set per project, each with a colour and a single-key shortcut, so labelling is
# a keystroke rather than a menu.
DEFAULT_LABELS = [
    ("Definition", "#0e7a72", "1"),
    ("Theorem", "#3b6fc4", "2"),
    ("Example", "#c98a1b", "3"),
    ("Exercise", "#7a4fc0", "4"),
    ("Activity", "#158a4a", "5"),
    ("Table", "#a8552f", "6"),
    ("Figure caption", "#607089", "7"),
    ("Summary", "#c2503f", "8"),
]


def seed_labels(con, project_id: int):
    have = con.execute("SELECT COUNT(*) FROM labels WHERE project_id=?",
                       (project_id,)).fetchone()[0]
    if have:
        return
    for i, (name, color, key) in enumerate(DEFAULT_LABELS):
        con.execute("""INSERT OR IGNORE INTO labels(project_id, name, color, shortcut, ord)
                       VALUES(?,?,?,?,?)""", (project_id, name, color, key, i))


class LabelIn(BaseModel):
    name: str
    color: str = "#0e7a72"
    shortcut: str = ""


@app.get("/api/projects/{pid}/labels")
def list_labels(pid: int):
    with db.tx() as con:
        seed_labels(con, pid)
        rows = con.execute("""SELECT l.*, (SELECT COUNT(*) FROM pair_labels pl
                              WHERE pl.label_id=l.id) AS uses
                              FROM labels l WHERE project_id=? ORDER BY ord, id""",
                           (pid,)).fetchall()
    return [dict(r) for r in rows]


@app.post("/api/projects/{pid}/labels")
def add_label(pid: int, body: LabelIn, x_annotator: str = Header("")):
    name = body.name.strip()
    if not name:
        raise HTTPException(400, "A label needs a name")
    with db.tx() as con:
        if not con.execute("SELECT 1 FROM projects WHERE id=?", (pid,)).fetchone():
            raise HTTPException(404, "Unknown project")
        n = con.execute("SELECT COALESCE(MAX(ord),0)+1 FROM labels WHERE project_id=?",
                        (pid,)).fetchone()[0]
        try:
            cur = con.execute("""INSERT INTO labels(project_id, name, color, shortcut, ord)
                                 VALUES(?,?,?,?,?)""",
                              (pid, name, body.color, body.shortcut.strip()[:1], n))
        except Exception:
            raise HTTPException(409, f"A label called {name} already exists")
        db.log(con, x_annotator, "label_add", name)
        return dict(con.execute("SELECT * FROM labels WHERE id=?",
                                (cur.lastrowid,)).fetchone())


@app.delete("/api/labels/{label_id}")
def delete_label(label_id: int, x_annotator: str = Header("")):
    with db.tx() as con:
        con.execute("DELETE FROM pair_labels WHERE label_id=?", (label_id,))
        con.execute("DELETE FROM labels WHERE id=?", (label_id,))
        db.log(con, x_annotator, "label_delete", label_id)
    return {"deleted": label_id}


class PairLabels(BaseModel):
    label_ids: list[int] = []


@app.put("/api/pairs/{pair_id}/labels")
def set_pair_labels(pair_id: int, body: PairLabels, x_annotator: str = Header("")):
    with db.tx() as con:
        if not con.execute("SELECT 1 FROM pairs WHERE id=?", (pair_id,)).fetchone():
            raise HTTPException(404, "Unknown pair")
        con.execute("DELETE FROM pair_labels WHERE pair_id=?", (pair_id,))
        for lid in body.label_ids:
            con.execute("INSERT OR IGNORE INTO pair_labels(pair_id, label_id)"
                        " VALUES(?,?)", (pair_id, lid))
        db.log(con, x_annotator, "pair_labels", pair_id, {"labels": body.label_ids})
        rows = con.execute("""SELECT l.* FROM labels l JOIN pair_labels pl
                              ON pl.label_id=l.id WHERE pl.pair_id=? ORDER BY l.ord""",
                           (pair_id,)).fetchall()
    return [dict(r) for r in rows]


@app.get("/api/projects/{pid}/progress")
def project_progress(pid: int):
    """Counts an annotator and a project lead both want at a glance."""
    with db.tx() as con:
        proj = con.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
        if not proj:
            raise HTTPException(404, "Unknown project")
        total = con.execute("SELECT COUNT(*) FROM pairs WHERE project_id=?",
                            (pid,)).fetchone()[0]
        excluded = con.execute("SELECT COUNT(*) FROM pairs WHERE project_id=? AND excluded=1",
                               (pid,)).fetchone()[0]
        per_label = [dict(r) for r in con.execute("""
            SELECT l.name, l.color, COUNT(pl.pair_id) AS n FROM labels l
            LEFT JOIN pair_labels pl ON pl.label_id=l.id
            WHERE l.project_id=? GROUP BY l.id ORDER BY l.ord""", (pid,))]
        per_person = [dict(r) for r in con.execute("""
            SELECT COALESCE(NULLIF(annotator,''),'(unnamed)') AS who, COUNT(*) n
            FROM pairs WHERE project_id=? GROUP BY who ORDER BY n DESC""", (pid,))]
        pages = con.execute("""SELECT COUNT(DISTINCT page) FROM clips
                               WHERE project_id=? AND side='src'""", (pid,)).fetchone()[0]
        src_pages = con.execute("SELECT pages FROM documents WHERE id=?",
                                (proj["src_doc"],)).fetchone()[0] or 0
    return {"pairs": total, "included": total - excluded, "excluded": excluded,
            "pages_covered": pages, "source_pages": src_pages,
            "coverage_pct": round(pages * 100 / src_pages, 1) if src_pages else 0,
            "by_label": per_label, "by_annotator": per_person}


# ------------------------------------------------------------------ pairs ---
class Region(BaseModel):
    page: int
    x0: float
    y0: float
    x1: float
    y1: float


class PairIn(BaseModel):
    project_id: int
    src: Region
    tgt: Region
    label: str = ""
    note: str = ""


def render_clip(doc_row_, region: Region, out_path: Path) -> dict:
    """Re-render the marked rectangle from the source PDF at print resolution."""
    doc = open_doc(doc_row_["path"])
    if region.page < 1 or region.page > doc.page_count:
        raise HTTPException(400, f"Page {region.page} is outside this textbook")
    page = doc[region.page - 1]
    rect = fitz.Rect(min(region.x0, region.x1), min(region.y0, region.y1),
                     max(region.x0, region.x1), max(region.y0, region.y1))
    rect = rect & page.rect
    if rect.is_empty or rect.width < 4 or rect.height < 4:
        raise HTTPException(400, "That selection is too small to clip")
    pix = page.get_pixmap(clip=rect, dpi=config.CROP_DPI)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path)
    text = page.get_textbox(rect) or ""
    excluded, term = library.is_excluded(page.get_text())
    return {"text": text.strip(), "excluded": excluded, "term": term,
            "width": pix.width, "height": pix.height}


@app.post("/api/pairs")
def create_pair(body: PairIn, x_annotator: str = Header("")):
    """Save one parallel pair: the English region and its counterpart."""
    with db.tx() as con:
        proj = con.execute("SELECT * FROM projects WHERE id=?",
                           (body.project_id,)).fetchone()
        if not proj:
            raise HTTPException(404, "Unknown project")
        seq = (con.execute("SELECT COALESCE(MAX(seq),0)+1 FROM pairs WHERE project_id=?",
                           (body.project_id,)).fetchone()[0])
        cur = con.execute(
            """INSERT INTO pairs(project_id, seq, label, note, annotator, created_at)
               VALUES(?,?,?,?,?,?)""",
            (body.project_id, seq, body.label, body.note, x_annotator, time.time()))
        pair_id = cur.lastrowid
        info = {}
        for side, region, doc_id in (("src", body.src, proj["src_doc"]),
                                     ("tgt", body.tgt, proj["tgt_doc"])):
            drow = doc_row(con, doc_id)
            folder = config.project_folder(proj["board"], proj["class"], proj["subject"])
            rel = f"{folder}/" + config.clip_name(
                drow["language"], proj["board"], proj["subject"], seq)
            meta = render_clip(drow, region, config.CROP_DIR / rel)
            con.execute(
                """INSERT INTO clips(project_id, pair_id, side, doc_id, page,
                   x0, y0, x1, y1, image_path, text, label, excluded, annotator, created_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (body.project_id, pair_id, side, doc_id, region.page,
                 region.x0, region.y0, region.x1, region.y1, rel,
                 meta["text"], body.label, 1 if meta["excluded"] else 0,
                 x_annotator, time.time()))
            info[side] = {"image": rel, "chars": len(meta["text"]),
                          "excluded_topic": meta["excluded"], "term": meta["term"]}
        if info["src"]["excluded_topic"] or info["tgt"]["excluded_topic"]:
            term = info["src"]["term"] or info["tgt"]["term"]
            con.execute("UPDATE pairs SET excluded=1, reason=? WHERE id=?",
                        (f"page mentions an excluded topic: {term}", pair_id))
        db.log(con, x_annotator, "pair_create", f"{proj['name']}#{seq}", info)
    return {"pair_id": pair_id, "seq": seq, "sides": info,
            "excluded": bool(info["src"]["excluded_topic"] or info["tgt"]["excluded_topic"])}


@app.get("/api/projects/{pid}/pairs")
def list_pairs(pid: int, include_excluded: bool = True):
    with db.tx() as con:
        rows = con.execute("""SELECT * FROM pairs WHERE project_id=?
                              ORDER BY seq""", (pid,)).fetchall()
        out = []
        for p in rows:
            if not include_excluded and p["excluded"]:
                continue
            clips = con.execute(
                "SELECT * FROM clips WHERE pair_id=? ORDER BY side DESC", (p["id"],)).fetchall()
            d = dict(p)
            d["clips"] = {c["side"]: dict(c) for c in clips}
            d["labels"] = [dict(r) for r in con.execute(
                """SELECT l.id, l.name, l.color FROM labels l
                   JOIN pair_labels pl ON pl.label_id=l.id
                   WHERE pl.pair_id=? ORDER BY l.ord""", (p["id"],))]
            out.append(d)
    return out


@app.delete("/api/pairs/{pair_id}")
def delete_pair(pair_id: int, x_annotator: str = Header("")):
    with db.tx() as con:
        clips = con.execute("SELECT image_path FROM clips WHERE pair_id=?",
                            (pair_id,)).fetchall()
        for c in clips:
            (config.CROP_DIR / c["image_path"]).unlink(missing_ok=True)
        con.execute("DELETE FROM clips WHERE pair_id=?", (pair_id,))
        con.execute("DELETE FROM pairs WHERE id=?", (pair_id,))
        db.log(con, x_annotator, "pair_delete", pair_id)
    return {"deleted": pair_id}


class PairPatch(BaseModel):
    label: str | None = None
    note: str | None = None
    excluded: bool | None = None
    reason: str | None = None


@app.patch("/api/pairs/{pair_id}")
def patch_pair(pair_id: int, body: PairPatch, x_annotator: str = Header("")):
    with db.tx() as con:
        row = con.execute("SELECT * FROM pairs WHERE id=?", (pair_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Unknown pair")
        for field in ("label", "note", "reason"):
            v = getattr(body, field)
            if v is not None:
                con.execute(f"UPDATE pairs SET {field}=? WHERE id=?", (v, pair_id))
        if body.excluded is not None:
            con.execute("UPDATE pairs SET excluded=? WHERE id=?",
                        (1 if body.excluded else 0, pair_id))
        db.log(con, x_annotator, "pair_update", pair_id, body.model_dump())
        return dict(con.execute("SELECT * FROM pairs WHERE id=?", (pair_id,)).fetchone())


@app.get("/api/clip/{clip_id}.png")
def clip_image(clip_id: int):
    with db.tx() as con:
        r = con.execute("SELECT image_path FROM clips WHERE id=?", (clip_id,)).fetchone()
    if not r:
        raise HTTPException(404, "Unknown clipping")
    p = config.CROP_DIR / r["image_path"]
    if not p.exists():
        raise HTTPException(404, "Clipping image is missing from the store")
    return FileResponse(p, media_type="image/png",
                        headers={"Cache-Control": "public, max-age=86400"})


# ----------------------------------------------------------------- export ---
def _manifest(proj, pairs, folder="") -> list:
    out = []
    for p in pairs:
        src = p["clips"].get("src", {})
        tgt = p["clips"].get("tgt", {})
        out.append({
            "seq": p["seq"], "label": p["label"], "note": p["note"],
            "board": proj["board"], "class": proj["class"],
            "subject": proj["subject"],
            "src_language": proj["src_language"], "tgt_language": proj["tgt_language"],
            "src_image": config.clip_name(proj["src_language"], proj["board"],
                                          proj["subject"], p["seq"]),
            "tgt_image": config.clip_name(proj["tgt_language"], proj["board"],
                                          proj["subject"], p["seq"]),
            "folder": folder,
            "src_page": src.get("page"), "tgt_page": tgt.get("page"),
            "src_bbox": [src.get("x0"), src.get("y0"), src.get("x1"), src.get("y1")],
            "tgt_bbox": [tgt.get("x0"), tgt.get("y0"), tgt.get("x1"), tgt.get("y1")],
            "src_text": src.get("text", ""), "tgt_text": tgt.get("text", ""),
            "labels": [l["name"] for l in p.get("labels", [])],
            "excluded": bool(p["excluded"]), "reason": p["reason"],
            "annotator": p["annotator"], "created_at": p["created_at"],
        })
    return out


@app.get("/api/projects/{pid}/export.zip")
def export_zip(pid: int, include_excluded: bool = False,
               formats: str = "png,jpg,pdf",
               x_annotator: str = Header("")):
    """The deliverable.

    Each clipping is written in every requested image format — PNG for
    fidelity, JPG for size, PDF for anything that expects a document — all cut
    from the source at print resolution rather than converted from a screen
    grab. Alongside them go the manifests: JSON, JSONL, CSV, Markdown and a
    plain-text parallel corpus.
    """
    want = {f.strip().lower() for f in formats.split(",") if f.strip()}
    want &= {"png", "jpg", "jpeg", "pdf"}
    if not want:
        want = {"png"}
    proj = get_project(pid)
    pairs = [p for p in list_pairs(pid) if include_excluded or not p["excluded"]]
    folder = config.project_folder(proj["board"], proj["class"], proj["subject"])
    manifest = _manifest(proj, pairs, folder)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for p in pairs:
            for side, lang in (("src", proj["src_language"]), ("tgt", proj["tgt_language"])):
                clip = p["clips"].get(side)
                if not clip:
                    continue
                png = config.CROP_DIR / clip["image_path"]
                if not png.exists():
                    continue
                stem = config.clip_name(lang, proj["board"], proj["subject"],
                                        p["seq"], "png").rsplit(".", 1)[0]
                if "png" in want:
                    z.write(png, f"{folder}/{stem}.png")
                if want & {"jpg", "jpeg"}:
                    z.writestr(f"{folder}/{stem}.jpg", _as_jpeg(png))
                if "pdf" in want:
                    z.writestr(f"{folder}/{stem}.pdf", _as_pdf(png))
        z.writestr(f"{folder}/manifest.json",
                   json.dumps({"project": {k: proj[k] for k in
                                           ("name", "board", "class", "subject",
                                            "src_language", "tgt_language")},
                               "folder": folder,
                               "pairs": manifest}, ensure_ascii=False, indent=1))
        z.writestr(f"{folder}/pairs.jsonl",
                   "\n".join(json.dumps(m, ensure_ascii=False) for m in manifest))
        z.writestr(f"{folder}/pairs.csv", _csv(manifest))
        z.writestr(f"{folder}/parallel.tsv", _tsv(manifest))
        z.writestr(f"{folder}/README.md", _readme(proj, manifest, folder, sorted(want)))

    data = buf.getvalue()
    out = config.EXPORT_DIR / f"{folder}_{int(time.time())}.zip"
    out.write_bytes(data)
    with db.tx() as con:
        con.execute("""INSERT INTO exports(project_id, name, path, n_pairs,
                       formats, created_at) VALUES(?,?,?,?,?,?)""",
                    (pid, folder, str(out), len(manifest),
                     ",".join(sorted(want)) + ",json,jsonl,csv,tsv,md", time.time()))
        db.log(con, x_annotator, "export", folder, {"pairs": len(manifest)})
    return Response(data, media_type="application/zip",
                    headers={"Content-Disposition": f'attachment; filename="{folder}.zip"'})


def _as_jpeg(png_path: Path, quality: int = 92) -> bytes:
    """JPEG on a white background — clippings have no transparency to lose.

    Falls back to the PNG bytes if Pillow is unavailable: an export should never
    fail over one format."""
    try:
        from PIL import Image
        with Image.open(png_path) as im:
            rgb = Image.new("RGB", im.size, "white")
            rgb.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
            b = io.BytesIO()
            rgb.save(b, "JPEG", quality=quality, optimize=True)
            return b.getvalue()
    except Exception:
        return png_path.read_bytes()          # never fail an export over a format


def _as_pdf(png_path: Path) -> bytes:
    """A one-page PDF sized exactly to the clipping."""
    try:
        doc = fitz.open()
        pix = fitz.Pixmap(str(png_path))
        page = doc.new_page(width=pix.width * 72 / config.CROP_DPI,
                            height=pix.height * 72 / config.CROP_DPI)
        page.insert_image(page.rect, filename=str(png_path))
        data = doc.tobytes()
        doc.close()
        return data
    except Exception:
        return b""


def _readme(proj, manifest, folder, formats) -> str:
    src, tgt = proj["src_language"], proj["tgt_language"]
    lines = [f"# {folder}", "",
             f"{config.board_name(proj['board'])} · Class {proj['class']} · "
             f"{proj['subject']}", "",
             f"{len(manifest)} parallel chunks · {src} ↔ {tgt}", "",
             "## How the files are named", "",
             "```",
             f"{config.clip_name(src, proj['board'], proj['subject'], 1)}"
             f"    {src}, chunk 1",
             f"{config.clip_name(tgt, proj['board'], proj['subject'], 1)}"
             f"    {tgt}, chunk 1  (the same passage)",
             "```", "",
             f"Formats included: {', '.join(formats)} per clipping, plus "
             f"manifest.json, pairs.jsonl, pairs.csv, parallel.tsv.", ""]
    for m in manifest:
        lines += [f"## Chunk {m['seq']}" + (f" — {m['label']}" if m["label"] else ""),
                  f"- {src}: `{m['src_image']}` (page {m['src_page']})",
                  f"- {tgt}: `{m['tgt_image']}` (page {m['tgt_page']})"]
        if m["src_text"]:
            lines += ["", f"**{src}**", "", m["src_text"]]
        if m["tgt_text"]:
            lines += ["", f"**{tgt}**", "", m["tgt_text"]]
        lines.append("")
    return "\n".join(lines)


def _tsv(manifest) -> str:
    """A plain parallel-text file, for anything that just wants the sentences."""
    rows = ["source\ttarget"]
    for m in manifest:
        s = (m["src_text"] or "").replace("\t", " ").replace("\n", " ").strip()
        t = (m["tgt_text"] or "").replace("\t", " ").replace("\n", " ").strip()
        if s or t:
            rows.append(f"{s}\t{t}")
    return "\n".join(rows)


def _csv(manifest) -> str:
    import csv
    buf = io.StringIO()
    cols = ["seq", "label", "labels", "src_image", "tgt_image", "src_page",
            "tgt_page", "src_text", "tgt_text", "excluded", "annotator"]
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for m in manifest:
        row = dict(m)
        row["labels"] = "; ".join(row.get("labels") or [])
        w.writerow(row)
    return buf.getvalue()


@app.get("/api/exports")
def export_history():
    with db.tx() as con:
        rows = con.execute("SELECT * FROM exports ORDER BY created_at DESC LIMIT 100").fetchall()
    return [dict(r) for r in rows]


# -------------------------------------------------------------------- docs ---
@app.get("/api/docs")
def docs_list():
    d = Path(__file__).parent / "docs"
    out = []
    for f in sorted(d.glob("*.md")):
        title = f.stem.replace("_", " ").title()
        try:
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
        except OSError:
            pass
        out.append({"name": f.stem, "title": title})
    return out


@app.get("/api/docs/{name}")
def docs_get(name: str):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise HTTPException(400, "bad document name")
    f = Path(__file__).parent / "docs" / f"{name}.md"
    if not f.exists():
        raise HTTPException(404, "No such document")
    return Response(f.read_text(encoding="utf-8"), media_type="text/plain; charset=utf-8")


@app.get("/api/sources")
def sources_status():
    """Where the textbooks come from and what is present."""
    import sources as srcmod
    return srcmod.status(config.DATA_DIR)


@app.post("/api/sources/acquire")
def sources_acquire(download: bool = True):
    """Unpack archives already here, and fetch only what is missing."""
    import sources as srcmod
    steps = []
    res = srcmod.acquire(config.DATA_DIR, log=lambda m: steps.append(m.strip()),
                         allow_download=download)
    with db.tx() as con:
        n = library.scan(con, config.DATA_DIR, log=lambda m: steps.append(m.strip()))
    return {**res, "documents": n, "steps": steps}


@app.post("/api/rescan")
def rescan():
    with db.tx() as con:
        n = library.scan(con, config.DATA_DIR, log=lambda m: None)
    return {"documents": n}



# ── layout annotation ──────────────────────────────────────────────────────
# Additive throughout: `layout.ensure_schema()` only ever runs
# CREATE TABLE IF NOT EXISTS, and nothing here writes to documents, projects,
# clips, pairs, labels, pair_labels, exports or audit.

@app.get("/api/layout/types")
def layout_types():
    with db.tx() as con:
        return layout.region_types(con)


class RegionTypeIn(BaseModel):
    code: str
    name: str
    color: str = "#1f4e79"
    shortcut: str = ""


@app.post("/api/layout/types")
def layout_add_type(body: RegionTypeIn, x_annotator: str = Header("")):
    code = re.sub(r"[^a-z0-9-]", "-", body.code.strip().lower()).strip("-")
    if not code:
        raise HTTPException(400, "A region type needs a code")
    with db.tx() as con:
        layout.ensure_schema(con)
        n = con.execute("SELECT COALESCE(MAX(ord),0)+1 FROM layout_region_types"
                        ).fetchone()[0]
        con.execute("""INSERT INTO layout_region_types(code, name, color, shortcut, ord)
                       VALUES(?,?,?,?,?) ON CONFLICT(code) DO UPDATE SET
                       name=excluded.name, color=excluded.color,
                       shortcut=excluded.shortcut""",
                    (code, body.name.strip() or code, body.color,
                     body.shortcut.strip()[:1], n))
        db.log(con, x_annotator, "layout_type_add", code)
        return dict(con.execute("SELECT * FROM layout_region_types WHERE code=?",
                                (code,)).fetchone())


@app.get("/api/layout/page/{doc_id}/{page}")
def layout_get_page(doc_id: int, page: int):
    """The regions on one page, with the page's true size in PDF points."""
    with db.tx() as con:
        d = doc_row(con, doc_id)
        path = resolve_path(d["path"])
        try:
            out = layout.get_page(con, doc_id, page, path)
        except ValueError as e:
            raise HTTPException(404, str(e))
        out["document"] = dict(d)
        return out


class LayoutRegionIn(BaseModel):
    type_code: str
    x0: float
    y0: float
    x1: float
    y1: float
    seq: int | None = None
    note: str = ""


class LayoutSaveIn(BaseModel):
    doc_id: int
    page: int
    regions: list[LayoutRegionIn] = []
    status: str = "in_progress"
    note: str = ""


@app.put("/api/layout/page")
def layout_save_page(body: LayoutSaveIn, x_annotator: str = Header("")):
    with db.tx() as con:
        d = doc_row(con, body.doc_id)
        path = resolve_path(d["path"])
        regions = [r.model_dump() for r in body.regions]
        for i, r in enumerate(regions):
            if r.get("seq") is None:
                r["seq"] = i
        try:
            res = layout.save_page(con, body.doc_id, body.page, path, regions,
                                   body.status, (x_annotator or "").strip(),
                                   body.note)
        except ValueError as e:
            raise HTTPException(400, str(e))
        db.log(con, x_annotator, "layout_save", f"doc{body.doc_id}p{body.page}",
               {"regions": res["regions"], "status": body.status})
        return res


class LayoutCompareIn(BaseModel):
    src_doc: int
    src_page: int
    tgt_doc: int
    tgt_page: int


@app.post("/api/layout/compare")
def layout_compare(body: LayoutCompareIn, x_annotator: str = Header("")):
    """How far does the target page preserve the source page's layout?"""
    with db.tx() as con:
        sp = resolve_path(doc_row(con, body.src_doc)["path"])
        tp = resolve_path(doc_row(con, body.tgt_doc)["path"])
        try:
            m = layout.compare_pages(con, body.src_doc, body.src_page, sp,
                                     body.tgt_doc, body.tgt_page, tp,
                                     (x_annotator or "").strip())
        except ValueError as e:
            raise HTTPException(400, str(e))
        db.log(con, x_annotator, "layout_compare",
               f"{body.src_doc}p{body.src_page}->{body.tgt_doc}p{body.tgt_page}")
        return m


@app.get("/api/layout/progress")
def layout_progress(doc_id: int = None):
    with db.tx() as con:
        return layout.progress(con, doc_id)


@app.get("/api/layout/export.zip")
def layout_export(doc_id: int = None, only_done: bool = False,
                  x_annotator: str = Header("")):
    """Layout annotations as COCO, JSONL and CSV.

    COCO because DocLayNet, PubLayNet and DocBank all use it, so this corpus
    can be trained on or merged with them rather than being a private format.
    Boxes are emitted as [x, y, width, height] with a top-left origin, in PDF
    points — independent of any rendering resolution.
    """
    import csv as _csv
    with db.tx() as con:
        layout.ensure_schema(con)
        where = ["1=1"]
        args = []
        if doc_id:
            where.append("lp.doc_id=?"); args.append(doc_id)
        if only_done:
            where.append("lp.status='done'")
        pages = con.execute(f"""SELECT lp.*, d.title, d.path, d.board, d.class,
            d.subject, d.language, d.script FROM layout_pages lp
            JOIN documents d ON d.id=lp.doc_id WHERE {' AND '.join(where)}
            ORDER BY lp.doc_id, lp.page""", args).fetchall()
        if not pages:
            raise HTTPException(400, "No layout annotations match that selection")
        types = [dict(t) for t in con.execute(
            "SELECT * FROM layout_region_types ORDER BY ord, id")]
        regions = {p["id"]: [dict(r) for r in con.execute(
            "SELECT * FROM layout_regions WHERE layout_page_id=? ORDER BY seq, id",
            (p["id"],))] for p in pages}
        comps = [dict(c) for c in con.execute("SELECT * FROM layout_comparisons")]

    cat = {t["code"]: i + 1 for i, t in enumerate(types)}
    coco = {"info": {"description": "Tulana Lipi layout annotations",
                     "version": layout.METRICS_VERSION,
                     "date_created": time.strftime("%Y-%m-%d"),
                     "coordinate_units": "pdf_points_top_left_origin"},
            "categories": [{"id": cat[t["code"]], "name": t["code"],
                            "supercategory": "layout"} for t in types],
            "images": [], "annotations": []}
    rows, ann_id = [], 1
    for img_id, p in enumerate(pages, 1):
        coco["images"].append({
            "id": img_id, "file_name": f"{Path(p['path']).stem}_p{p['page']:04d}.png",
            "width": round(p["width"] or 0, 2), "height": round(p["height"] or 0, 2),
            "document": p["title"], "page": p["page"], "board": p["board"],
            "class": p["class"], "subject": p["subject"],
            "language": p["language"], "script": p["script"]})
        for r in regions[p["id"]]:
            w, h = r["x1"] - r["x0"], r["y1"] - r["y0"]
            typo = json.loads(r["typography"] or "{}")
            space = json.loads(r["spacing"] or "{}")
            coco["annotations"].append({
                "id": ann_id, "image_id": img_id,
                "category_id": cat.get(r["type_code"], 0),
                "bbox": [round(r["x0"], 2), round(r["y0"], 2), round(w, 2), round(h, 2)],
                "area": round(w * h, 2), "iscrowd": 0,
                "reading_order": r["seq"], "text": r["text"],
                "typography": typo, "spacing": space,
                "annotator": r["annotator"]})
            rows.append({"document": p["title"], "page": p["page"],
                         "board": p["board"], "class": p["class"],
                         "language": p["language"], "script": p["script"],
                         "region_type": r["type_code"], "reading_order": r["seq"],
                         "x0": round(r["x0"], 2), "y0": round(r["y0"], 2),
                         "x1": round(r["x1"], 2), "y1": round(r["y1"], 2),
                         "font": typo.get("dominant_font"),
                         "size": typo.get("dominant_size"),
                         "bold": typo.get("bold"), "italic": typo.get("italic"),
                         "line_height": space.get("line_height"),
                         "indent": space.get("first_line_indent"),
                         "gap_above": space.get("gap_above"),
                         "text": (r["text"] or "").replace("\n", " ")[:2000],
                         "annotator": r["annotator"]})
            ann_id += 1

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("layout/coco.json", json.dumps(coco, ensure_ascii=False, indent=1))
        z.writestr("layout/regions.jsonl",
                   "\n".join(json.dumps(r, ensure_ascii=False) for r in rows))
        sio = io.StringIO()
        cols = ["document", "page", "board", "class", "language", "script",
                "region_type", "reading_order", "x0", "y0", "x1", "y1", "font",
                "size", "bold", "italic", "line_height", "indent", "gap_above",
                "text", "annotator"]
        w2 = _csv.DictWriter(sio, fieldnames=cols, extrasaction="ignore")
        w2.writeheader()
        for r in rows:
            w2.writerow(r)
        z.writestr("layout/regions.csv", sio.getvalue())
        if comps:
            z.writestr("layout/comparisons.jsonl", "\n".join(
                json.dumps({**{k: c[k] for k in ("src_page_id", "tgt_page_id",
                                                 "metrics_version", "created_by")},
                            "metrics": json.loads(c["metrics"] or "{}")},
                           ensure_ascii=False) for c in comps))
        z.writestr("layout/README.md", _layout_readme(pages, rows, comps))
    return Response(buf.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition":
                             'attachment; filename="tulana_layout.zip"'})


def _layout_readme(pages, rows, comps) -> str:
    from collections import Counter
    counts = Counter(r["region_type"] for r in rows)
    langs = sorted({p["language"] for p in pages if p["language"]})
    boards = sorted({p["board"] for p in pages if p["board"]})
    lines = [
        "# Layout annotations — Tulana Lipi", "",
        f"{len(rows)} regions across {len(pages)} pages.", "",
        f"- boards: {', '.join(boards) or '—'}",
        f"- languages: {', '.join(langs) or '—'}",
        f"- cross-language comparisons: {len(comps)}", "",
        "## Region counts", "", "| type | regions |", "|---|---|",
        *[f"| {code} | {n} |" for code, n in counts.most_common()], "",
        "## Coordinates", "",
        "Boxes are in **PDF points** with a top-left origin — the page's own",
        "units — so they are independent of any rendering resolution. Rasterise",
        "a page at any DPI and multiply by `dpi / 72` to get pixels.", "",
        "`coco.json` follows the COCO detection layout with `bbox` as",
        "`[x, y, width, height]`, so this corpus can be trained on or merged",
        "with DocLayNet and PubLayNet. Four fields extend COCO: `reading_order`,",
        "`text` (what was under the box where the PDF had a readable layer),",
        "`typography` (font, size, weight from the PDF's own text layer) and",
        "`spacing` (line height, indent, gap above, in points).", "",
        "## Limitations, stated", "",
        "- Typography and spacing come from the PDF text layer. A scanned page",
        "  has none, and those fields are then empty — that means *not",
        "  recoverable*, not *no formatting*.",
        "- Reading order on a multi-column or sidebar-heavy page is one",
        "  annotator's judgement and is genuinely ambiguous.",
        "- Layout comparison scores over fewer than three regions a side are",
        "  unstable and should not be quoted.", "",
    ]
    return "\n".join(lines)



# ── parsed layout corpus ───────────────────────────────────────────────────
# The blocks, reading order and extracted text produced by the document
# parser. Additive: three new tables, nothing existing written to.

@app.get("/api/blocks/mapping")
def blocks_mapping():
    """Which layout books map onto an original PDF, and which do not."""
    with db.tx() as con:
        return blocks.mapping_report(con, config.DATA_DIR)


@app.get("/api/blocks/stats")
def blocks_stats():
    with db.tx() as con:
        return blocks.stats(con)


@app.post("/api/blocks/ingest")
def blocks_ingest(path: str = None, x_annotator: str = Header("")):
    """Load the parsed-layout corpus. Idempotent; safe to re-run."""
    with db.tx() as con:
        res = blocks.ingest(con, corpus=Path(path) if path else None,
                            data_dir=config.DATA_DIR, log=lambda m: None)
        db.log(con, x_annotator, "blocks_ingest", res.get("corpus") or "-",
               {"books": res["books"], "blocks": res["blocks"]})
    return res


@app.get("/api/blocks/library")
def blocks_library():
    """Board/class/subject groups with an English and a target edition."""
    with db.tx() as con:
        out = []
        for c in blocks.pairable(con):
            eng = blocks.editions(con, c["board"], c["class"], c["subject"], "English")
            tgt = [e for e in blocks.editions(con, c["board"], c["class"], c["subject"])
                   if e["language"] != "English"]
            out.append({**c, "english_editions": eng, "target_editions": tgt})
        return out


@app.get("/api/blocks/page/{book_id}/{page}")
def blocks_page(book_id: int, page: int):
    """Blocks on one page, with fractional geometry so any zoom lines up."""
    with db.tx() as con:
        try:
            return blocks.page_blocks(con, book_id, page)
        except ValueError as e:
            raise HTTPException(404, str(e))


@app.get("/api/blocks/page-image/{book_id}/{page}.png")
def blocks_page_image(book_id: int, page: int,
                      dpi: int | None = Query(None, ge=40, le=300)):
    """The rendered PDF page behind a set of blocks.

    404 when the PDF is not on disk — the parsed layout is still served, so the
    interface falls back to drawing the blocks on a blank page of the right
    proportions rather than showing nothing."""
    dpi = 110 if not isinstance(dpi, int) else max(40, min(300, dpi))
    with db.tx() as con:
        b = blocks.book(con, book_id)
    pdf = blocks._find_pdf(config.DATA_DIR, b["relpath"])
    if not pdf:
        raise HTTPException(404, f"The PDF for {b['book']} is not in "
                                 f"{config.DATA_DIR}")
    cache = config.PAGE_CACHE / f"pl{book_id}_{page}_{dpi}.png"
    if not cache.exists():
        with fitz.open(pdf) as doc:
            if page < 0 or page >= doc.page_count:
                raise HTTPException(404, f"Page out of range (0..{doc.page_count-1})")
            pix = doc[page].get_pixmap(dpi=dpi)
            cache.parent.mkdir(parents=True, exist_ok=True)
            tmp = cache.with_name(cache.stem + f".{os.getpid()}.part.png")
            pix.save(tmp)
            tmp.replace(cache)
    return FileResponse(cache, media_type="image/png",
                        headers={"Cache-Control": "public, max-age=86400"})


class SelectionIn(BaseModel):
    block_ids: list[int] = []


@app.post("/api/blocks/selection")
def blocks_selection(body: SelectionIn):
    """The text of the chosen blocks, assembled in reading order."""
    with db.tx() as con:
        return blocks.selection_text(con, body.block_ids[:2000])


class PairSelectionIn(BaseModel):
    src_block_ids: list[int] = []
    tgt_block_ids: list[int] = []


@app.post("/api/blocks/selection/pair")
def blocks_selection_pair(body: PairSelectionIn):
    """Both sides at once — what an annotator comparing editions actually wants."""
    with db.tx() as con:
        s = blocks.selection_text(con, body.src_block_ids[:2000])
        t = blocks.selection_text(con, body.tgt_block_ids[:2000])
    return {"source": s, "target": t,
            "comparable": bool(s["n_blocks"] and t["n_blocks"]),
            "label_match": sorted(s.get("labels") or []) == sorted(t.get("labels") or [])}


@app.get("/api/blocks/export.zip")
def blocks_export(board: str = None, cls: int = None, language: str = None,
                  label: str = None, limit: int = 50000):
    """The parsed layout as JSONL and CSV, filtered however you like."""
    import csv as _csv
    where, args = ["1=1"], []
    for col, val in (("k.board", board), ("k.class", cls),
                     ("k.language", language), ("b.label", label)):
        if val not in (None, ""):
            where.append(f"{col}=?")
            args.append(val)
    with db.tx() as con:
        blocks.ensure_schema(con)
        rows = [dict(r) for r in con.execute(f"""
            SELECT k.book, k.relpath, k.board, k.class, k.subject, k.language,
                   k.script, p.page, p.width, p.height, b.ord, b.label, b.type,
                   b.x0, b.y0, b.x1, b.y1, b.fx0, b.fy0, b.fx1, b.fy1, b.conf, b.text
            FROM pl_blocks b JOIN pl_pages p ON p.id=b.page_id
            JOIN pl_books k ON k.id=p.book_id
            WHERE {' AND '.join(where)}
            ORDER BY k.book, p.page, b.ord LIMIT ?""", args + [min(limit, 200000)])]
    if not rows:
        raise HTTPException(400, "Nothing matches that selection")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("layout/blocks.jsonl",
                   "\n".join(json.dumps(r, ensure_ascii=False) for r in rows))
        sio = io.StringIO()
        cols = [c for c in rows[0] if c != "text"] + ["text"]
        w = _csv.DictWriter(sio, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "text": (r["text"] or "").replace("\n", " ")[:2000]})
        z.writestr("layout/blocks.csv", sio.getvalue())
        z.writestr("layout/README.md", (
            "# Parsed layout blocks\n\n"
            f"{len(rows)} blocks.\n\n"
            "## Coordinates\n\n"
            "`x0,y0,x1,y1` are in the pixel space of the raster the parser measured\n"
            "against, whose size is given per page as `width` and `height`. Those\n"
            "rasters are not shipped, so `fx0,fy0,fx1,fy1` — the same boxes as\n"
            "fractions of the page — are the portable form: multiply by whatever\n"
            "size you render at.\n\n"
            "## Text\n\n"
            "`text` is what the parser read inside the box. About one block in ten\n"
            "has none: diagrams and images legitimately carry no text, and a page\n"
            "without a usable text layer yields none either. Empty means *not\n"
            "recovered*, not *empty on the page*.\n"))
    return Response(buf.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition":
                             'attachment; filename="tulana_blocks.zip"'})



# ── saved pairs, built from parsed blocks ──────────────────────────────────

class RegionIn(BaseModel):
    page: int
    x0: float
    y0: float
    x1: float
    y1: float
    note: str = ""


class PairIn(BaseModel):
    src_book_id: int
    tgt_book_id: int
    src_block_ids: list[int] = []
    tgt_block_ids: list[int] = []
    src_regions: list[RegionIn] = []
    tgt_regions: list[RegionIn] = []
    label: str = ""
    note: str = ""
    status: str = "saved"
    pair_id: int | None = None


@app.post("/api/pairs/block")
def pairs_save(body: PairIn, x_annotator: str = Header("")):
    """Save an aligned selection. Either side may span several pages."""
    with db.tx() as con:
        try:
            p = bpairs.save_pair(con, body.src_book_id, body.tgt_book_id,
                                 body.src_block_ids, body.tgt_block_ids,
                                 body.label, body.note, body.status,
                                 (x_annotator or "").strip(), body.pair_id,
                                 [r.model_dump() for r in body.src_regions],
                                 [r.model_dump() for r in body.tgt_regions])
        except ValueError as e:
            raise HTTPException(400, str(e))
        db.log(con, x_annotator, "pair_save", str(p["id"]),
               {"src": len(body.src_block_ids), "tgt": len(body.tgt_block_ids)})
        return p


@app.post("/api/pairs/block/draft")
def pairs_draft(body: PairIn, x_annotator: str = Header("")):
    """Keep the in-progress selection without being asked.

    Called as the annotator works, so a closed tab costs nothing."""
    with db.tx() as con:
        try:
            return bpairs.save_draft(con, body.src_book_id, body.tgt_book_id,
                                     body.src_block_ids, body.tgt_block_ids,
                                     (x_annotator or "").strip(),
                                     [r.model_dump() for r in body.src_regions],
                                     [r.model_dump() for r in body.tgt_regions])
        except ValueError as e:
            raise HTTPException(400, str(e))


@app.get("/api/pairs/block")
def pairs_list(src_book_id: int = None, tgt_book_id: int = None,
               status: str = None, board: str = None, language: str = None,
               search: str = None, include_drafts: bool = False,
               limit: int = 500, offset: int = 0):
    with db.tx() as con:
        return bpairs.list_pairs(con, src_book_id, tgt_book_id, status, board,
                                 language, search, include_drafts, limit, offset)


@app.get("/api/pairs/block/stats")
def pairs_stats():
    with db.tx() as con:
        return bpairs.stats(con)


@app.get("/api/pairs/block/{pair_id}")
def pairs_get(pair_id: int):
    with db.tx() as con:
        try:
            return bpairs.get_pair(con, pair_id)
        except ValueError as e:
            raise HTTPException(404, str(e))


class PairMetaIn(BaseModel):
    label: str | None = None
    note: str | None = None
    status: str | None = None


@app.patch("/api/pairs/block/{pair_id}")
def pairs_patch(pair_id: int, body: PairMetaIn, x_annotator: str = Header("")):
    with db.tx() as con:
        try:
            if body.label is not None or body.note is not None:
                bpairs.update_meta(con, pair_id, body.label, body.note)
            if body.status is not None:
                bpairs.set_status(con, pair_id, body.status,
                                  (x_annotator or "").strip())
            db.log(con, x_annotator, "pair_update", str(pair_id))
            return bpairs.get_pair(con, pair_id)
        except ValueError as e:
            raise HTTPException(400, str(e))


@app.delete("/api/pairs/block/{pair_id}")
def pairs_delete(pair_id: int, x_annotator: str = Header("")):
    with db.tx() as con:
        db.log(con, x_annotator, "pair_delete", str(pair_id))
        return bpairs.delete_pair(con, pair_id)


@app.get("/api/pairs/block/{pair_id}/crop/{crop_id}.png")
def pairs_crop(pair_id: int, crop_id: int):
    """One cropped parallel image."""
    with db.tx() as con:
        try:
            data, fn = bpairs.crop_bytes(con, crop_id)
        except ValueError as e:
            raise HTTPException(404, str(e))
    return Response(data, media_type="image/png",
                    headers={"Cache-Control": "public, max-age=31536000",
                             "Content-Disposition": f'inline; filename="{fn}"'})


@app.post("/api/pairs/block/{pair_id}/recrop")
def pairs_recrop(pair_id: int, dpi: int = None, x_annotator: str = Header("")):
    """Cut the images again — after a PDF arrives, or at a different DPI."""
    with db.tx() as con:
        res = bpairs.build_crops(con, pair_id, dpi)
        db.log(con, x_annotator, "pair_recrop", str(pair_id), res)
        return {**res, "pair": bpairs.get_pair(con, pair_id)}


@app.post("/api/pairs/crops/prune")
def pairs_prune(apply: bool = False):
    """Delete crop files no pair refers to."""
    with db.tx() as con:
        return bpairs.prune_crops(con, dry_run=not apply)


@app.get("/api/pairs/formats")
def pairs_formats():
    """Every export format, with what each is for."""
    return [{"key": k, "name": n, "extension": e, "description": d}
            for k, (n, _m, e, d) in bpairs.FORMATS.items()]


@app.get("/api/pairs/export.{fmt}")
def pairs_export(fmt: str, board: str = None, language: str = None,
                 cls: int = None, status: str = None,
                 include_excluded: bool = False):
    with db.tx() as con:
        try:
            if fmt == "bundle":
                data, media, fn = bpairs.export_bundle(
                    con, board=board, language=language, cls=cls, status=status,
                    include_excluded=include_excluded)
            else:
                data, media, fn = bpairs.export(
                    con, fmt, board=board, language=language, cls=cls,
                    status=status, include_excluded=include_excluded)
        except ValueError as e:
            raise HTTPException(400, str(e))
    return Response(data, media_type=media,
                    headers={"Content-Disposition": f'attachment; filename="{fn}"'})


app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Serve the interface with a correct base URL and versioned assets.

    Two faults this fixes, both of which look identical from the outside — the
    page appears not to have changed.

    **The base URL.** The HTML references `static/app.js` relatively. Mounted
    under Gradio at `/studio`, that resolves correctly from `/studio/` but from
    `/studio` (no trailing slash, which is what a pasted link often is) the
    browser resolves it against `/` and gets a 404. The page then loads with no
    script and no stylesheet. Emitting an explicit `<base>` built from the
    mount prefix makes both forms work.

    **Stale assets.** With only an ETag and no `Cache-Control`, browsers apply
    heuristic freshness and can serve a cached `app.js` for hours without
    revalidating — so a deployed change genuinely does not appear. Each asset
    URL now carries a fingerprint of the file, so a changed file is a different
    URL and can never be served from cache."""
    static = Path(__file__).parent / "static"
    html = (static / "index.html").read_text(encoding="utf-8")

    root = (request.scope.get("root_path") or "").rstrip("/")
    base = f"{root}/" if root else "/"
    if "<base " not in html:
        html = html.replace("<head>", f'<head>\n<base href="{base}">', 1)

    for name in ("app.js", "style.css"):
        f = static / name
        if not f.exists():
            continue
        stamp = f"{int(f.stat().st_mtime)}-{f.stat().st_size}"
        html = html.replace(f'"static/{name}"', f'"static/{name}?v={stamp}"')
    return html


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)
