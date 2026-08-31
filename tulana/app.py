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

from fastapi import Body, FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import config
import db
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
        if n == 0:
            print(f"[studio] nothing indexed. Checked {config.DATA_DIR} — set "
                  f"TULANA_DATA_DIR to the folder holding your PDFs, or run "
                  f"`git lfs pull` if the files are LFS pointers.")
    except Exception as e:                      # never block startup
        print(f"[studio] could not index {config.DATA_DIR}: {e}")


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


app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    return (Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)
