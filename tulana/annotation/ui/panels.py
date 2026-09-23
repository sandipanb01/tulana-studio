"""The panels beside the workspace: saved work, export, and the manuals.

None of these hold state. Each is a set of callbacks that take the session dict
and return values for their own components, so a person browsing their saved
work in one tab cannot disturb what another annotator is editing.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

import gradio as gr

from ..core import exporters, store, workspace
from ..core.models import STATUS_BY_KEY, STATUSES
from ..core.store import Invalid, NotFound
from . import session

log = logging.getLogger("annotation.ui.panels")

DOCS = Path(__file__).resolve().parent.parent / "docs"


# ── saved work / review ────────────────────────────────────────────────────

REVIEW_COLUMNS = ["Pair", "Answer", "Chapter", "English", "Target language",
                  "Changed", "By"]

REVIEW_FILTERS = [("Everything", "")] + [(s.label, s.key) for s in STATUSES] + [
    ("Only pairs I have edited", "__edited")]


def review(state: Any, show: str, order: str, page: int):
    """A page of this workspace's pairs, filtered the way a reviewer wants."""
    st = session.ensure(state)
    if not session.has_project(st):
        return [], "Open a textbook first.", 1

    try:
        page = max(1, int(page or 1))
    except (TypeError, ValueError):
        page = 1
    per = 40
    kwargs: dict[str, Any] = {"limit": per, "offset": (page - 1) * per,
                              "order": "recent" if order == "Most recently changed"
                                       else "seq"}
    if show == "__edited":
        kwargs["edited"] = True
    elif show:
        kwargs["status"] = show

    try:
        with store.ro() as con:
            data = workspace.WorkspaceRepo(con).rows(st["pid"], **kwargs)
    except NotFound:
        return [], "That workspace is no longer available.", page
    except Exception:
        log.exception("review listing failed")
        return [], "The list could not be loaded.", page

    rows = []
    for r in data["rows"]:
        rows.append([
            r["seq"],
            STATUS_BY_KEY.get(r["status"], STATUSES[0]).label,
            (r["chapter_no"] + " " if r["chapter_no"] else "") + (r["chapter"] or ""),
            _snip(r["src"]["text"]),
            _snip(r["tgt"]["text"]),
            time.strftime("%d %b %H:%M", time.localtime(r["updated_at"]))
            if r["updated_at"] else "",
            r["updated_by"] or "",
        ])

    last = max(1, -(-data["total"] // per))
    note = (f"{data['total']:,} pair{'' if data['total'] == 1 else 's'} · "
            f"page {page} of {last}")
    return rows, note, page


def open_from_review(state: Any, src: str, tgt: str, status: str, note: str,
                     evt: gr.SelectData):
    """Open a pair picked from the review table, in the workspace."""
    from . import workspace as ws
    return ws.open_search_hit(state, src, tgt, status, note, evt)


def _snip(text: str, n: int = 70) -> str:
    one = " ".join((text or "").split())
    return one[:n] + ("…" if len(one) > n else "")


# ── export ─────────────────────────────────────────────────────────────────

def format_choices() -> list:
    """Every registered exporter, with the unavailable ones honestly labelled."""
    out = []
    for f in exporters.formats():
        label = f"{f['label']} (.{f['ext']})"
        if f["pairs_only"]:
            label += " — pairs with both sides only"
        if not f["available"]:
            label += f" — needs {f.get('install', 'an extra package')}"
        out.append((label, f["key"]))
    return out


EXPORT_SCOPES = [
    ("Everything in this workspace", "all"),
    ("Everything I have checked", "done"),
    ("Only “Exact”", "exact"),
    ("“Exact” and “Needs correction”", "exact,needs_correction"),
    ("Only this chapter", "chapter"),
]


def export(state: Any, fmt: str, scope: str, paired_only: bool):
    """Write one export file and hand it to the browser."""
    st = session.ensure(state)
    if not session.has_project(st):
        return None, "Open a textbook first."
    if not fmt:
        return None, "Choose a download format first."

    kwargs: dict[str, Any] = {"include_unpaired": not paired_only}
    if scope == "done":
        kwargs["only_done"] = True
    elif scope == "chapter":
        kwargs["chapter_no"] = st["filters"].get("chapter_no") or ""
        if not kwargs["chapter_no"]:
            return None, "No chapter is selected. Pick one in the workspace first."
    elif scope and scope != "all":
        kwargs["status"] = scope

    try:
        with store.tx() as con:
            out = exporters.export(con, st["pid"], fmt, annotator=st["annotator"],
                                   **kwargs)
    except Invalid as exc:
        return None, str(exc)
    except Exception:
        log.exception("export failed")
        return None, ("The download could not be created. Your annotations are "
                      "unaffected; the details are in the server log.")

    note = (f"{out['rows_written']:,} pair"
            f"{'' if out['rows_written'] == 1 else 's'} written to "
            f"{out['filename']}")
    if out["rows_excluded"]:
        note += (f". {out['rows_excluded']:,} pair"
                 f"{'' if out['rows_excluded'] == 1 else 's'} left out because this "
                 f"format can only hold pairs with text on both sides — including "
                 f"them would shift every later line out of alignment.")
    return str(out["path"]), note


def export_all(state: Any, scope: str, paired_only: bool):
    """Every available format at once, in one zip."""
    st = session.ensure(state)
    if not session.has_project(st):
        return None, "Open a textbook first."
    kwargs: dict[str, Any] = {"include_unpaired": not paired_only}
    if scope == "done":
        kwargs["only_done"] = True
    elif scope == "chapter":
        kwargs["chapter_no"] = st["filters"].get("chapter_no") or ""
    elif scope and scope != "all":
        kwargs["status"] = scope
    try:
        with store.tx() as con:
            out = exporters.bundle(con, st["pid"], annotator=st["annotator"], **kwargs)
    except Exception:
        log.exception("bundle failed")
        return None, "The download could not be created."
    note = f"{len(out['formats'])} formats in {out['filename']}"
    if out["skipped"]:
        note += f" · skipped: {', '.join(out['skipped'])}"
    return str(out["path"]), note


def export_history(state: Any):
    """What has been downloaded from this workspace before."""
    st = session.ensure(state)
    if not session.has_project(st):
        return []
    with store.ro() as con:
        rows = store.Repository(con).all(
            "SELECT fmt, filename, n_rows, n_bytes, actor, created_at"
            "  FROM setu_export WHERE pid = ? ORDER BY created_at DESC LIMIT 25",
            (st["pid"],))
    return [[time.strftime("%d %b %H:%M", time.localtime(r["created_at"])),
             r["fmt"], r["filename"], f"{r['n_rows']:,}",
             f"{r['n_bytes'] / 1024:,.0f} KB", r["actor"] or ""]
            for r in rows]


# ── the manuals ────────────────────────────────────────────────────────────

def doc_choices() -> list:
    out = []
    for p in sorted(DOCS.glob("*.md")):
        title = p.stem.split("_", 1)[-1].replace("_", " ").title()
        try:
            first = p.read_text(encoding="utf-8").lstrip().split("\n", 1)[0]
            if first.startswith("#"):
                title = first.lstrip("# ").strip()
        except OSError:                          # pragma: no cover - fs-specific
            pass
        out.append((title, p.name))
    return out


def read_doc(name: str) -> str:
    """Serve one manual page.

    The name is resolved inside the docs folder and checked afterwards, so
    `../../config.py` and its encoded variants land outside and are refused
    rather than read.
    """
    if not name:
        return ""
    candidate = (DOCS / str(name)).resolve()
    if not candidate.is_relative_to(DOCS.resolve()) or candidate.suffix != ".md" \
            or not candidate.is_file():
        log.warning("refused document request: %r", name)
        return "That page could not be found."
    return candidate.read_text(encoding="utf-8")
