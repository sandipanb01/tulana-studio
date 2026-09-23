"""Setu — the HTTP surface.

A FastAPI router, included by ``app.py`` under ``/api/setu``.

This is **not** the annotation interface — that is the Gradio workspace in
``annotation.ui``, started by ``launch_annotation.py``. This is a second front
end over the same services: useful for scripting an export, checking the health
of an instance, or driving the corpus from a notebook. It also keeps the
services honest, because anything it cannot do without reaching into the
interface would be a layering mistake.

Nothing in here contains business logic: every endpoint validates its input,
calls one service function, and shapes the result. That is what keeps the
services testable without a web server and the router readable without the
services.

Errors come back in one shape, always::

    {"error": "<kind>", "message": "<something a person can act on>"}

with a status code that matches the kind: 400 for input the caller can fix, 404
for something that is not there, 409 for a save that lost a race — which the
interface handles specially, because a 409 is the one error that is nobody's
mistake.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, Query, Request, Response
from fastapi.responses import FileResponse, JSONResponse

import config
import db as legacy_db

from . import __version__
from .core import annotate, corpus, exporters, ids, search, store, workspace
from .core.models import KINDS, STATUSES, normalise
from .core.store import Conflict, Invalid, NotFound

log = logging.getLogger("setu.api")

router = APIRouter(prefix="/api/setu", tags=["setu"])

HERE = Path(__file__).parent.resolve()
DOCS = HERE / "docs"


# ── error handling ─────────────────────────────────────────────────────────

def _fail(kind: str, message: str, code: int, **extra) -> JSONResponse:
    return JSONResponse({"error": kind, "message": message, **extra}, status_code=code)


def guard(fn):
    """Turn the service layer's exceptions into the one error shape.

    An unexpected exception is logged with its traceback and reported as a
    generic failure. The traceback stays in the log: an annotator does not need
    a stack trace, and an error page is not the place to publish file paths.
    """
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Conflict as exc:
            return JSONResponse(exc.payload(), status_code=409)
        except NotFound as exc:
            return _fail("not_found", str(exc), 404)
        except (Invalid, ValueError) as exc:
            return _fail("invalid", str(exc), 400)
        except PermissionError as exc:           # pragma: no cover - fs-specific
            return _fail("forbidden", str(exc), 403)
        except Exception:
            log.exception("unhandled error in %s", fn.__name__)
            return _fail("server_error",
                         "Something went wrong at our end. Your work is saved; "
                         "reload the page and try again.", 500)
    return wrapper


def _actor(request: Request, annotator: str = "") -> tuple[str, str]:
    """Who is acting, and from which tab.

    Both arrive from the client and are treated as labels, never as authority:
    Setu has no accounts, so an annotator name is how work is attributed in the
    audit log, not how anything is permitted. They are length-capped here so a
    long one cannot bloat every row it touches.
    """
    name = normalise(annotator or request.headers.get("x-setu-annotator", ""))[:120]
    sess = normalise(request.headers.get("x-setu-session", ""))[:64]
    return name.strip(), sess.strip()


# ── metadata and vocabulary ────────────────────────────────────────────────

@router.get("/meta")
@guard
def meta() -> dict:
    """Everything the interface needs before it can draw anything."""
    with store.ro() as con:
        c = corpus.CorpusRepo(con)
        counts = c.counts()
        built = counts["books"] > 0
        return {
            "version": __version__,
            "name": "Setu",
            "built": built,
            "corpus": counts,
            "statuses": [
                {"key": s.key, "label": s.label, "help": s.help, "color": s.color,
                 "shortcut": s.shortcut, "counts_as_done": s.counts_as_done}
                for s in STATUSES],
            "kinds": [{"key": k.key, "label": k.label, "icon": k.icon,
                       "annotatable": k.annotatable} for k in KINDS],
            "formats": exporters.formats(),
            "search": "fts" if store.fts_ready(con) else "like",
        }


@router.post("/build")
@guard
def build_source(request: Request, payload: dict = Body(default={})) -> dict:
    """Derive the source layer from the parsed-layout corpus.

    Safe to call repeatedly: books already built are skipped. ``rebuild`` forces
    a re-segmentation, which is what to do after re-importing a corpus.
    """
    actor, _ = _actor(request, str(payload.get("annotator", "")))
    rebuild = bool(payload.get("rebuild"))
    with store.connect() as con:
        report = corpus.build(con, rebuild=rebuild)
    log.info("source layer built by %s: %s", actor or "anonymous", report)
    return report


@router.get("/report")
@guard
def report() -> dict:
    with store.ro() as con:
        return corpus.ingest_report(con)


# ── the metadata cascade ───────────────────────────────────────────────────

@router.get("/boards")
@guard
def boards() -> dict:
    with store.ro() as con:
        return {"boards": corpus.CorpusRepo(con).boards()}


@router.get("/classes")
@guard
def classes(board: str = Query(...)) -> dict:
    with store.ro() as con:
        return {"classes": corpus.CorpusRepo(con).classes(board)}


@router.get("/subjects")
@guard
def subjects(board: str = Query(...), cls: str = Query("", alias="class")) -> dict:
    with store.ro() as con:
        return {"subjects": corpus.CorpusRepo(con).subjects(board, cls)}


@router.get("/languages")
@guard
def languages(board: str = Query(...), cls: str = Query("", alias="class"),
              subject: str = Query("Mathematics")) -> dict:
    with store.ro() as con:
        return {"languages": corpus.CorpusRepo(con).languages(board, cls, subject)}


@router.get("/books")
@guard
def books(board: str = "", cls: str = Query("", alias="class"), subject: str = "",
          language: str = "", exclude: str = "") -> dict:
    with store.ro() as con:
        return {"books": corpus.CorpusRepo(con).books(
            board=board, cls=cls or None, subject=subject, language=language,
            exclude=exclude)}


@router.get("/book/{book_key}")
@guard
def book(book_key: str) -> dict:
    with store.ro() as con:
        c = corpus.CorpusRepo(con)
        b = c.book(book_key)
        b["aliases"] = c.aliases(book_key)
        b["outline"] = c.outline(book_key)
        return b


# ── projects ───────────────────────────────────────────────────────────────

@router.get("/projects")
@guard
def projects(limit: int = 50, offset: int = 0, annotator: str = "") -> dict:
    with store.ro() as con:
        return {"projects": workspace.WorkspaceRepo(con).projects(
            annotator=annotator, limit=limit, offset=offset)}


@router.post("/projects")
@guard
def create_project(request: Request, payload: dict = Body(...)) -> dict:
    actor, _ = _actor(request, str(payload.get("annotator", "")))
    src = str(payload.get("src_book") or "")
    tgt = str(payload.get("tgt_book") or "")
    if not ids.is_id(src, "bk") or not ids.is_id(tgt, "bk"):
        raise Invalid("src_book and tgt_book must both be book identifiers")
    with store.connect() as con:
        con.execute("BEGIN IMMEDIATE")
        try:
            proj = workspace.create_project(
                con, src_book=src, tgt_book=tgt,
                name=str(payload.get("name") or "")[:200], annotator=actor,
                include_noise=bool(payload.get("include_noise")))
            con.execute("COMMIT")
        except Exception:
            con.execute("ROLLBACK")
            raise
    return proj


@router.get("/projects/{pid}")
@guard
def project(pid: str) -> dict:
    with store.ro() as con:
        return workspace.WorkspaceRepo(con).project(pid)


@router.post("/projects/{pid}/rebuild")
@guard
def rebuild(request: Request, pid: str, payload: dict = Body(default={})) -> dict:
    actor, _ = _actor(request, str(payload.get("annotator", "")))
    with store.tx() as con:
        return workspace.build_rows(
            con, pid, annotator=actor, force=bool(payload.get("force")),
            include_noise=bool(payload.get("include_noise")))


@router.delete("/projects/{pid}")
@guard
def remove_project(request: Request, pid: str) -> dict:
    actor, _ = _actor(request)
    with store.tx() as con:
        return workspace.delete_project(con, pid, annotator=actor)


@router.get("/projects/{pid}/chapters")
@guard
def chapters(pid: str) -> dict:
    with store.ro() as con:
        return {"chapters": workspace.WorkspaceRepo(con).chapters(pid)}


@router.get("/projects/{pid}/progress")
@guard
def progress(pid: str) -> dict:
    with store.ro() as con:
        return workspace.WorkspaceRepo(con).progress(pid)


@router.get("/projects/{pid}/rows")
@guard
def rows(pid: str, limit: int = 50, offset: int = 0, status: str = "",
         chapter_no: str = "", kind: str = "", edited: str = "",
         order: str = "seq") -> dict:
    flag = None if edited == "" else edited.lower() in {"1", "true", "yes"}
    with store.ro() as con:
        return workspace.WorkspaceRepo(con).rows(
            pid, limit=limit, offset=offset, status=status,
            chapter_no=chapter_no, kind=kind, edited=flag, order=order)


@router.get("/projects/{pid}/search")
@guard
def do_search(pid: str, q: str = "", limit: int = 40, offset: int = 0,
              status: str = "", chapter_no: str = "", kind: str = "",
              side: str = "both") -> dict:
    with store.ro() as con:
        return search.SearchRepo(con).find(
            pid, q, limit=limit, offset=offset, status=status,
            chapter_no=chapter_no, kind=kind, side=side)


@router.get("/projects/{pid}/next")
@guard
def next_row(pid: str, seq: int = 0, direction: int = 1, status: str = "") -> dict:
    with store.ro() as con:
        found = workspace.WorkspaceRepo(con).neighbour(pid, seq, direction, status)
    return {"row": found}


@router.get("/projects/{pid}/segments")
@guard
def project_segments(pid: str, side: str = "src", q: str = "", page: str = "",
                     limit: int = 40, offset: int = 0) -> dict:
    """Segments of one side's book, for the "choose a different partner" picker."""
    with store.ro() as con:
        w = workspace.WorkspaceRepo(con)
        proj = w.project(pid)
        book_key = proj["src_book"] if side == "src" else proj["tgt_book"]
        c = corpus.CorpusRepo(con)
        if q:
            found = search.SearchRepo(con)._matching_sids(
                q, "fts" if store.fts_ready(con) else "like")
            if not found:
                return {"segments": [], "total": 0}
            marks = ",".join("?" * len(found[:900]))
            lim, off = store.paginate(limit, offset, default=40, cap=100)
            segs = c.all(
                f"SELECT * FROM setu_segment WHERE book_key = ? AND sid IN ({marks})"
                f" ORDER BY seq LIMIT ? OFFSET ?",
                [book_key] + found[:900] + [lim, off])
            return {"segments": segs, "total": len(segs)}
        return {"segments": c.segments(
            book_key, limit=limit, offset=offset,
            page=int(page) if str(page).strip().isdigit() else None)}


# ── one row ────────────────────────────────────────────────────────────────

@router.get("/rows/{rid}")
@guard
def row(rid: str) -> dict:
    with store.ro() as con:
        return workspace.WorkspaceRepo(con).row(rid)


@router.patch("/rows/{rid}")
@guard
def save_row(request: Request, rid: str, payload: dict = Body(...)) -> dict:
    """The autosave endpoint.

    Accepts either side's text, the status and the note in one call, and applies
    them in one transaction. ``src_rev`` and ``tgt_rev`` are the revisions the
    editor was showing; a mismatch comes back as 409 with both texts rather than
    overwriting somebody.
    """
    actor, sess = _actor(request, str(payload.get("annotator", "")))
    with store.tx() as con:
        result = annotate.save_many(
            con, rid,
            src=payload.get("src"), tgt=payload.get("tgt"),
            src_rev=payload.get("src_rev"), tgt_rev=payload.get("tgt_rev"),
            status=payload.get("status"), note=payload.get("note"),
            annotator=actor, session=sess,
            reason=str(payload.get("reason") or "edit")[:32])
        if sess:
            workspace.WorkspaceRepo(con).touch_session(sess, actor)
    return result


@router.post("/rows/{rid}/status")
@guard
def row_status(request: Request, rid: str, payload: dict = Body(...)) -> dict:
    actor, sess = _actor(request, str(payload.get("annotator", "")))
    with store.tx() as con:
        out = annotate.set_status(con, rid, payload.get("status"),
                                  note=payload.get("note"), annotator=actor,
                                  session=sess)
        out["row"] = workspace.WorkspaceRepo(con).row(rid)
    return out


@router.get("/rows/{rid}/history")
@guard
def history(rid: str, side: str = "", limit: int = 50, offset: int = 0) -> dict:
    with store.ro() as con:
        repo = annotate.AnnotateRepo(con)
        return {"text": repo.history(rid, side, limit, offset),
                "status": repo.status_history(rid)}


@router.get("/rows/{rid}/diff")
@guard
def row_diff(rid: str, side: str = "src", a: str = "0", b: str = "current") -> dict:
    with store.ro() as con:
        return annotate.diff(con, rid, side, a=a, b=b)


@router.post("/rows/{rid}/restore")
@guard
def row_restore(request: Request, rid: str, payload: dict = Body(...)) -> dict:
    actor, sess = _actor(request, str(payload.get("annotator", "")))
    with store.tx() as con:
        out = annotate.restore(con, rid, str(payload.get("side") or "src"),
                               rev=payload.get("rev"), annotator=actor, session=sess)
        out["row"] = workspace.WorkspaceRepo(con).row(rid)
    return out


@router.post("/rows/{rid}/attach")
@guard
def row_attach(request: Request, rid: str, payload: dict = Body(...)) -> dict:
    actor, sess = _actor(request, str(payload.get("annotator", "")))
    with store.tx() as con:
        return annotate.attach(con, rid, str(payload.get("side") or "tgt"),
                               payload.get("sid"), annotator=actor, session=sess)


@router.post("/rows/{rid}/split")
@guard
def row_split(request: Request, rid: str) -> dict:
    actor, sess = _actor(request)
    with store.tx() as con:
        return annotate.split_row(con, rid, annotator=actor, session=sess)


@router.post("/rows/{rid}/merge")
@guard
def row_merge(request: Request, rid: str, payload: dict = Body(...)) -> dict:
    actor, sess = _actor(request)
    other = str(payload.get("other") or "")
    with store.tx() as con:
        return annotate.merge_rows(con, rid, other, annotator=actor, session=sess)


# ── sessions and presence ──────────────────────────────────────────────────

@router.post("/session")
@guard
def session(request: Request, payload: dict = Body(default={})) -> dict:
    """Register or refresh this tab.

    The client mints its own session id per tab and sends it on every request.
    That is what makes two tabs of one person distinguishable, which in turn is
    what makes "you have this row open in another tab" possible to say.
    """
    actor, sess = _actor(request, str(payload.get("annotator", "")))
    sess = sess or ids.session_id()
    agent = request.headers.get("user-agent", "")[:200]
    with store.tx() as con:
        w = workspace.WorkspaceRepo(con)
        row = w.touch_session(sess, actor, str(payload.get("pid") or ""), agent)
        others = [s for s in w.active_sessions(str(payload.get("pid") or ""))
                  if s["sess"] != sess]
    return {"session": sess, "annotator": row.get("annotator", ""),
            "others": [{"annotator": s["annotator"] or "someone",
                        "seen_at": s["seen_at"]} for s in others][:12]}


@router.post("/rows/{rid}/claim")
@guard
def claim(request: Request, rid: str, payload: dict = Body(default={})) -> dict:
    actor, sess = _actor(request, str(payload.get("annotator", "")))
    if not sess:
        raise Invalid("this request has no session; reload the page")
    with store.tx() as con:
        return workspace.WorkspaceRepo(con).claim(rid, sess, actor)


@router.post("/rows/{rid}/release")
@guard
def release(request: Request, rid: str) -> dict:
    _, sess = _actor(request)
    with store.tx() as con:
        workspace.WorkspaceRepo(con).release(rid, sess)
    return {"released": rid}


# ── export ─────────────────────────────────────────────────────────────────

@router.get("/formats")
@guard
def formats() -> dict:
    return {"formats": exporters.formats()}


@router.get("/projects/{pid}/export.{fmt}")
@guard
def export(request: Request, pid: str, fmt: str, status: str = "",
           chapter_no: str = "", kind: str = "", only_done: str = "",
           include_unpaired: str = "1"):
    actor, _ = _actor(request)
    with store.tx() as con:
        out = exporters.export(
            con, pid, fmt, status=status, chapter_no=chapter_no, kind=kind,
            only_done=only_done.lower() in {"1", "true", "yes"},
            include_unpaired=include_unpaired.lower() in {"1", "true", "yes"},
            annotator=actor)
    return FileResponse(
        out["path"], media_type=out["mime"], filename=out["filename"],
        headers={"X-Setu-Rows": str(out["rows_written"]),
                 "X-Setu-Excluded": str(out["rows_excluded"])})


@router.get("/projects/{pid}/export-bundle.zip")
@guard
def export_bundle(request: Request, pid: str, status: str = "",
                  chapter_no: str = "", only_done: str = ""):
    actor, _ = _actor(request)
    with store.tx() as con:
        out = exporters.bundle(
            con, pid, status=status, chapter_no=chapter_no,
            only_done=only_done.lower() in {"1", "true", "yes"}, annotator=actor)
    return FileResponse(out["path"], media_type="application/zip",
                        filename=out["filename"])


@router.get("/exports")
@guard
def export_history(pid: str = "", limit: int = 30) -> dict:
    lim, _ = store.paginate(limit, 0, default=30, cap=100)
    with store.ro() as con:
        repo = store.Repository(con)
        if pid:
            return {"exports": repo.all(
                "SELECT xid, pid, fmt, filename, n_rows, n_bytes, actor, created_at"
                "  FROM setu_export WHERE pid = ? ORDER BY created_at DESC LIMIT ?",
                (pid, lim))}
        return {"exports": repo.all(
            "SELECT xid, pid, fmt, filename, n_rows, n_bytes, actor, created_at"
            "  FROM setu_export ORDER BY created_at DESC LIMIT ?", (lim,))}


@router.get("/exports/{xid}/download")
@guard
def download_export(xid: str):
    """Re-download a previous export.

    The path comes from the database, never from the request, and is checked to
    be inside the export directory before it is opened. A row whose path points
    outside — which would mean the database itself had been tampered with — is
    refused rather than served.
    """
    with store.ro() as con:
        rec = store.Repository(con).one(
            "SELECT * FROM setu_export WHERE xid = ?", (xid,))
    if not rec:
        raise NotFound(f"no such export: {xid}")
    root = Path(config.EXPORT_DIR).resolve()
    target = Path(rec["path"]).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise NotFound("that export file is no longer available")
    fmt = exporters.REGISTRY.get(rec["fmt"])
    return FileResponse(target, filename=rec["filename"],
                        media_type=fmt.mime if fmt else "application/octet-stream")


# ── observability ──────────────────────────────────────────────────────────

@router.get("/health")
@guard
def health() -> dict:
    """Is Setu working, and is its data where it should be?

    Deliberately does a real read rather than returning a constant: a health
    check that cannot fail tells you nothing.
    """
    started = time.time()
    with store.ro() as con:
        c = corpus.CorpusRepo(con).counts()
        projects_n = store.Repository(con).scalar(
            "SELECT COUNT(*) FROM setu_project", default=0)
        rows_n = store.Repository(con).scalar(
            "SELECT COUNT(*) FROM setu_row", default=0)
        journal = con.execute("PRAGMA journal_mode").fetchone()[0]
        sync = con.execute("PRAGMA synchronous").fetchone()[0]
    return {"ok": True, "version": __version__, "corpus": c,
            "projects": projects_n, "rows": rows_n,
            "durability": {"journal_mode": journal, "synchronous": int(sync),
                           "synchronous_name": {0: "OFF", 1: "NORMAL", 2: "FULL",
                                                3: "EXTRA"}.get(int(sync), "?")},
            "db": Path(config.DB_PATH).name,
            "took_ms": round((time.time() - started) * 1000, 1)}


@router.get("/events")
@guard
def events(target: str = "", limit: int = 50) -> dict:
    lim, _ = store.paginate(limit, 0, default=50, cap=200)
    with store.ro() as con:
        repo = store.Repository(con)
        if target:
            return {"events": repo.all(
                "SELECT * FROM setu_event WHERE target = ? ORDER BY ts DESC LIMIT ?",
                (target, lim))}
        return {"events": repo.all(
            "SELECT * FROM setu_event ORDER BY ts DESC LIMIT ?", (lim,))}


# ── documentation ──────────────────────────────────────────────────────────

@router.get("/docs")
@guard
def doc_index() -> dict:
    out = []
    for p in sorted(DOCS.glob("*.md")):
        title = p.stem.split("_", 1)[-1].replace("_", " ").title()
        try:
            first = p.read_text(encoding="utf-8").lstrip().split("\n", 1)[0]
            if first.startswith("#"):
                title = first.lstrip("# ").strip()
        except OSError:                          # pragma: no cover - fs-specific
            pass
        out.append({"name": p.name, "title": title, "bytes": p.stat().st_size})
    return {"docs": out}


@router.get("/docs/{name}")
@guard
def doc(name: str) -> Response:
    """Serve one manual page.

    The filename is resolved inside the docs directory and checked afterwards,
    so ``../../etc/passwd`` and its encoded variants resolve to something
    outside and are refused.
    """
    candidate = (DOCS / name).resolve()
    if not candidate.is_relative_to(DOCS) or candidate.suffix != ".md" \
            or not candidate.is_file():
        raise NotFound(f"no such document: {name}")
    return Response(candidate.read_text(encoding="utf-8"),
                    media_type="text/markdown; charset=utf-8")
