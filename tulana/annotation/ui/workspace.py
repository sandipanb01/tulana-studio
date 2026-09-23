"""The bilingual annotation workspace.

This is the screen an annotator spends the day in: English on the left, the
Indian-language edition on the right, both editable, a status underneath, and
Previous/Next.

Three decisions shape the whole module.

**Nothing is held between events.** Every callback takes the session dict, the
two texts and the controls as inputs, and returns a new session dict. There is
no module-level cache of "the current row" and no open connection kept around.
That is what makes the shared link safe: Gradio gives each session its own
state, and if the interface kept anything of its own, two annotators would see
each other's textbook.

**Saving is explicit about what it is based on.** Every save carries the
revision the editor was showing. The service layer refuses a save that would
land on top of somebody else's, and this module turns that refusal into a panel
offering both versions rather than a traceback.

**Navigation saves first.** Previous, Next, jump and search all run the same
save path before they move. An annotator who types and immediately presses Next
must not lose the edit, and relying on a timer to have fired in time is not a
design, it is a hope.
"""
from __future__ import annotations

import logging
import time
from typing import Any

import gradio as gr

from ..core import annotate, corpus, search, sources, store, workspace
from ..core.models import STATUSES, STATUS_BY_KEY
from ..core.store import Conflict, Invalid, NotFound
from . import render, session

log = logging.getLogger("annotation.ui.workspace")

#: RTL scripts, by the script name the corpus records. Data, not code: a new
#: right-to-left language is an entry here, and nothing else changes.
RTL_SCRIPTS = frozenset({"Perso-Arabic", "Arabic", "Urdu", "Nastaliq", "Hebrew"})

STATUS_CHOICES = [(s.label, s.key) for s in STATUSES]
STATUS_HELP = "  ·  ".join(f"{s.shortcut} {s.label}" for s in STATUSES if s.key != "pending")


# ── data access ────────────────────────────────────────────────────────────
#
# Every one of these opens a connection, does its work and closes it. SQLite in
# WAL mode makes that cheap, and it means no connection is ever shared between
# two annotators' events — which is where the concurrency bugs live.

def _read(fn, *args, **kwargs):
    with store.ro() as con:
        return fn(con, *args, **kwargs)


def _write(fn, *args, **kwargs):
    with store.tx() as con:
        return fn(con, *args, **kwargs)


def _row(rid: str) -> dict:
    with store.ro() as con:
        return workspace.WorkspaceRepo(con).row(rid)


def _progress(pid: str) -> dict:
    with store.ro() as con:
        return workspace.WorkspaceRepo(con).progress(pid)


# ── the metadata cascade ───────────────────────────────────────────────────
#
# Every list is a query over what the database actually holds, so a combination
# that does not exist cannot be offered. Nothing here enumerates boards,
# classes or languages; adding a textbook to the corpus makes it appear.

def boards() -> list:
    """Boards for the first dropdown, each saying how much it offers.

    A board with one language cannot be annotated — there is nothing to read
    beside the text. Saying so on the row is the difference between an
    annotator choosing a different board and an annotator concluding the tool
    is broken.
    """
    with store.ro() as con:
        rows = corpus.CorpusRepo(con).boards()
    out = []
    for b in rows:
        try:
            n = int(b["n_languages"])
        except (KeyError, IndexError, TypeError, ValueError):
            n = 0
        if n >= 2:
            label = f"{b['name']}  ({b['n_books']} books · {n} languages)"
        else:
            label = (f"{b['name']}  ({b['n_books']} books · one language only — "
                     f"cannot be paired)")
        out.append((label, b["code"]))
    return out


def first_board() -> str:
    """The board the workspace opens on: the first pairable one."""
    choices = boards()
    return choices[0][1] if choices else None


def on_board(board: str):
    if not board:
        return (gr.update(choices=[], value=None, interactive=False),) + _clear_from_subject()
    with store.ro() as con:
        rows = corpus.CorpusRepo(con).classes(board)
    choices = [(f"Class {r['value']}", str(r["value"])) for r in rows]
    value = choices[0][1] if len(choices) == 1 else None
    out = gr.update(choices=choices, value=value, interactive=True)
    if value:
        return (out,) + on_class(board, value)
    return (out,) + _clear_from_subject()


def on_class(board: str, cls: str):
    if not (board and cls):
        return _clear_from_subject()
    with store.ro() as con:
        rows = corpus.CorpusRepo(con).subjects(board, cls)
    # Say on the label how many languages a subject holds. One language cannot
    # be annotated against anything, and finding that out only after choosing
    # it — from a right-hand list that offers the same single entry as the
    # left — reads as a broken interface rather than a fact about the corpus.
    choices = []
    for r in rows:
        # Works whether the row arrives as a dict or a sqlite3.Row; a silent
        # zero here would mislabel every subject as having no language.
        try:
            n = int(r["n_languages"])
        except (KeyError, IndexError, TypeError, ValueError):
            n = 0
        if n >= 2:
            label = f"{r['value']}  ({n} languages)"
        elif n == 1:
            label = f"{r['value']}  (1 language only — nothing to compare)"
        else:
            label = f"{r['value']}  (no language recorded)"
        choices.append((label, r["value"]))
    value = choices[0][1] if len(choices) == 1 else None
    out = gr.update(choices=choices, value=value, interactive=True)
    if value:
        return (out,) + on_subject(board, cls, value)
    return (out,) + _clear_from_langs()


def _target_update(board: str, cls: str, subject: str, source_language: str):
    """The right-hand language list: everything except what the left holds.

    Annotating means reading one language beside another, so the language
    already chosen on the left has no business in this list. When removing it
    empties the list, the control says why on its own label instead of sitting
    there empty — the corpus simply has nothing to compare against for this
    board, class and subject.
    """
    with store.ro() as con:
        rest = corpus.CorpusRepo(con).languages(board, cls, subject,
                                                exclude=source_language or "")
    if rest:
        return gr.update(choices=[(l["value"], l["value"]) for l in rest],
                         value=rest[0]["value"] if len(rest) == 1 else None,
                         interactive=True,
                         label="Language")
    return gr.update(
        choices=[], value=None, interactive=False,
        label=("Language — this selection has only one language, "
               "so there is nothing to compare it against"))


def on_subject(board: str, cls: str, subject: str):
    if not (board and cls and subject):
        return _clear_from_langs()
    with store.ro() as con:
        langs = corpus.CorpusRepo(con).languages(board, cls, subject)
    choices = [(f"{l['value']}", l["value"]) for l in langs]
    src_default = "English" if any(l["value"] == "English" for l in langs) else None
    if src_default is None and len(langs) == 1:
        # A corpus without an English edition here — West Bengal's single
        # Bengali textbook, for instance. Select it rather than leaving the
        # left side blank for no visible reason.
        src_default = langs[0]["value"]
    src = gr.update(choices=choices, value=src_default, interactive=True,
                    label="Language")
    tgt = _target_update(board, cls, subject, src_default)
    if src_default:
        books = _books(board, cls, subject, src_default)
        return (src, tgt,
                gr.update(choices=books, value=books[0][1] if len(books) == 1 else None,
                          interactive=True),
                gr.update(choices=[], value=None, interactive=False))
    return (src, tgt,
            gr.update(choices=[], value=None, interactive=False),
            gr.update(choices=[], value=None, interactive=False))


def on_source_language(board: str, cls: str, subject: str, language: str,
                       other_book: str):
    """The left language changed: refresh its books AND the right-hand list.

    Without the second half of this, choosing Marathi on the left left Marathi
    still offered on the right.
    """
    books = on_language(board, cls, subject, language, other_book)
    if not (board and cls and subject):
        return books, gr.update(choices=[], value=None, interactive=False)
    return books, _target_update(board, cls, subject, language)


def on_language(board: str, cls: str, subject: str, language: str, other_book: str):
    """Books for one side, excluding whatever the other side already holds."""
    if not (board and cls and subject and language):
        return gr.update(choices=[], value=None, interactive=False)
    books = _books(board, cls, subject, language, exclude=other_book)
    return gr.update(choices=books,
                     value=books[0][1] if len(books) == 1 else None,
                     interactive=bool(books))


def _books(board, cls, subject, language, exclude: str = "") -> list:
    with store.ro() as con:
        rows = corpus.CorpusRepo(con).books(board=board, cls=cls, subject=subject,
                                            language=language, exclude=exclude or "")
    out = []
    for b in rows:
        name = b["title"] or b["book"]
        extra = f"{b['num_pages']} pages · {b['n_segments']:,} pieces of text"
        out.append((f"{name} — {extra}", b["book_key"]))
    return out


def _clear_from_subject():
    return (gr.update(choices=[], value=None, interactive=False),) + _clear_from_langs()


def _clear_from_langs():
    off = gr.update(choices=[], value=None, interactive=False)
    return (off, off, off, off)


# ── opening a workspace ────────────────────────────────────────────────────

def open_books(state: Any, annotator: str, src_book: str, tgt_book: str):
    """Create or reopen the workspace for two books, and show its first pair."""
    st = session.ensure(state)
    st["annotator"] = (annotator or "").strip()[:120]

    if not src_book or not tgt_book:
        return _no_change(st, "Choose a book on each side first.")
    if src_book == tgt_book:
        return _no_change(st, "The two sides must be different books.")

    try:
        proj = _write(workspace.create_project, src_book=src_book, tgt_book=tgt_book,
                      annotator=st["annotator"])
    except (Invalid, NotFound) as exc:
        return _no_change(st, str(exc))
    except Exception:
        log.exception("could not open %s / %s", src_book, tgt_book)
        return _no_change(st, "That pair of books could not be opened. "
                              "The details are in the server log.")

    st["pid"] = proj["pid"]
    st["project"] = {
        "name": proj["name"],
        "src_lang": proj.get("src_lang") or "", "tgt_lang": proj.get("tgt_lang") or "",
        "src_script": proj.get("src_script") or "", "tgt_script": proj.get("tgt_script") or "",
    }
    st["filters"] = {"status": "", "chapter_no": "", "kind": ""}
    return _goto_first(st)


def _goto_first(st: dict):
    with store.ro() as con:
        first = workspace.WorkspaceRepo(con).first(st["pid"], **st["filters"])
    if not first:
        return _no_change(st, "This workspace has no pairs matching the current filters.")
    return _load(st, first["rid"])


# ── loading a pair ─────────────────────────────────────────────────────────

def _load(st: dict, rid: str, note: str = ""):
    """Put a pair on screen. The single place that does so."""
    try:
        row = _row(rid)
    except NotFound:
        return _no_change(st, "That pair no longer exists.")
    st = session.load_row(st, row)

    with store.ro() as con:
        repo = workspace.WorkspaceRepo(con)
        pos = repo.position(st["pid"], row["seq"], **st["filters"])
        prog = repo.progress(st["pid"])
        chapters = repo.chapters(st["pid"])

    proj = st["project"]
    return (
        st,
        gr.update(value=row["src"]["text"],
                  label=render.pane_label("src", row, proj.get("src_lang")),
                  interactive=bool(row["src"]["present"]),
                  rtl=is_rtl(proj.get("src_script")),
                  elem_classes=_pane_classes("src", row)),
        gr.update(value=row["tgt"]["text"],
                  label=render.pane_label("tgt", row, proj.get("tgt_lang")),
                  interactive=bool(row["tgt"]["present"]),
                  rtl=is_rtl(proj.get("tgt_script")),
                  elem_classes=_pane_classes("tgt", row)),
        gr.update(value=row["status"]),
        gr.update(value=row["note"]),
        render.pair_header(row, pos),
        render.save_state("saved" if not note else "saved", note),
        render.progress(prog),
        gr.update(choices=_chapter_choices(chapters),
                  value=st["filters"]["chapter_no"] or ""),
        "",                                   # conflict panel: cleared
        gr.update(value=None),                # source image: cleared
        "",                                   # source message: cleared
    )


def is_rtl(script: Any) -> bool:
    """Is this script written right to left?

    Decided by the script the book records, never by a hard-coded language
    list, so adding Urdu is a row of data. Gradio's Textbox takes `rtl`
    natively, which sets the direction *and* moves the cursor and the text
    alignment with it — better than styling the box and leaving the caret
    behaving as if the text were English.
    """
    return str(script or "") in RTL_SCRIPTS


def _pane_classes(side: str, row: dict) -> list:
    return [] if row[side].get("present") else ["setu-empty"]


def _chapter_choices(chapters: list) -> list:
    out = [("Everything", "")]
    for ch in chapters:
        label = (f"{ch['chapter_no']}. " if ch["chapter_no"] else "") + (ch["chapter"] or "—")
        out.append((f"{label}  ({ch['done']}/{ch['n']})", ch["chapter_no"] or label))
    return out


def _no_change(st: dict, message: str):
    """Report something without disturbing what is on screen.

    Every component keeps its value; only the message line changes. An error
    that blanked the editor would lose the annotator's unsaved text, which is
    a far worse outcome than whatever caused the error.
    """
    keep = gr.update()
    return (st, keep, keep, keep, keep, keep,
            render.save_state("error", message), keep, keep, "", keep, "")


#: What every "the pair changed" callback returns, in order. Declared once so
#: a handler cannot quietly return them in the wrong order — which produces a
#: workspace that shows the Marathi text in the English pane.
PAIR_OUTPUTS_DOC = (
    "state, src, tgt, status, note, pair_header, save_state, progress, "
    "chapter_filter, conflict_panel, source_image, source_message")


# ── saving ─────────────────────────────────────────────────────────────────

def save(state: Any, src: str, tgt: str, status: str, note: str,
         reason: str = "edit"):
    """Persist whatever is on screen. Returns (state, save-indicator, conflict)."""
    st = session.ensure(state)
    if not session.has_row(st):
        return st, render.save_state("idle"), ""
    if not session.dirty(st, src, tgt, status, note):
        return st, render.save_state("saved"), ""

    payload: dict[str, Any] = {}
    saved = st["saved"]
    if st["present"]["src"] and src != saved["src"]:
        payload["src"] = src
        payload["src_rev"] = st["src_rev"]
    if st["present"]["tgt"] and tgt != saved["tgt"]:
        payload["tgt"] = tgt
        payload["tgt_rev"] = st["tgt_rev"]
    if status != saved["status"]:
        payload["status"] = status
    if note != saved["note"]:
        payload["note"] = note
    if not payload:
        return st, render.save_state("saved"), ""

    try:
        with store.tx() as con:
            result = annotate.save_many(
                con, st["rid"], annotator=st["annotator"], session=_session_key(st),
                reason=reason, **payload)
    except Conflict as exc:
        side = "src" if "src" in payload else "tgt"
        st["conflict"] = {"side": side, "mine": payload.get(side, ""),
                          "theirs": exc.current, "rev": exc.rev}
        log.info("save conflict on %s (%s)", st["rid"], side)
        return st, render.save_state("conflict"), render.conflict_panel(st["conflict"])
    except Invalid as exc:
        st["last_error"] = str(exc)
        return st, render.save_state("error", str(exc)), ""
    except Exception:
        log.exception("save failed for %s", st.get("rid"))
        return (st, render.save_state(
            "error", "We could not save just now. Your last saved version is "
                     "still safe. It will be retried."), "")

    row = result.get("row") or {}
    st = session.mark_saved(st, src, tgt, status, note,
                            src_rev=(row.get("src") or {}).get("rev"),
                            tgt_rev=(row.get("tgt") or {}).get("rev"))
    st["conflict"] = None
    return st, render.save_state("saved"), ""


def save_and_count(state: Any, src: str, tgt: str, status: str, note: str,
                   reason: str = "status"):
    """Save, and refresh the progress panel with it.

    Setting an answer is the moment an annotator wants to see the count move.
    Leaving it until the next navigation makes the tool feel as though it did
    not hear them.
    """
    st, indicator, conflict = save(state, src, tgt, status, note, reason=reason)
    prog = gr.update()
    if session.has_project(st):
        try:
            prog = render.progress(_progress(st["pid"]))
        except Exception:                        # never fail a save over a counter
            log.debug("progress refresh failed", exc_info=True)
    return st, indicator, conflict, prog


def autosave_tick(state: Any, src: str, tgt: str, status: str, note: str):
    """The periodic autosave.

    Deliberately cheap when there is nothing to do: it compares the four values
    against what the session already knows was saved and returns without
    touching the database. An annotator reading a long passage generates one
    dictionary comparison every couple of seconds, not a write.
    """
    st = session.ensure(state)
    if not session.has_row(st) or not session.dirty(st, src, tgt, status, note):
        return st, gr.update(), gr.update()
    return save(st, src, tgt, status, note, reason="autosave")


def _session_key(st: dict) -> str:
    """A stable-ish id for this tab, for the audit trail.

    Gradio does not expose its session hash to a handler, so this is derived
    from the annotator and when their workspace was opened. Two tabs of one
    person opening at different moments get different keys, which is enough for
    the log; the revision check, not this, is what protects the data.
    """
    return f"{st.get('annotator') or 'anon'}@{int(st.get('opened_at') or 0)}"


# ── navigation ─────────────────────────────────────────────────────────────

def move(state: Any, src: str, tgt: str, status: str, note: str, direction: int,
         only_pending: bool = False):
    """Save, then step to the next or previous pair under the current filters."""
    st = session.ensure(state)
    if not session.has_project(st):
        return _no_change(st, "Open a textbook first.")

    st, _indicator, conflict = save(st, src, tgt, status, note, reason="navigate")
    if conflict:
        # Do not move away from an unresolved conflict; the annotator would
        # have to find the pair again to deal with it.
        return _stay_with_conflict(st, conflict)

    filters = dict(st["filters"])
    if only_pending:
        filters["status"] = "pending"
    with store.ro() as con:
        found = workspace.WorkspaceRepo(con).neighbour(
            st["pid"], st["seq"], direction, **filters)
    if not found:
        where = "unchecked pairs" if only_pending else "pairs"
        edge = "after" if direction >= 0 else "before"
        return _no_change(st, f"No more {where} {edge} this one.")
    return _load(st, found["rid"])


def jump_to_chapter(state: Any, src: str, tgt: str, status: str, note: str,
                    chapter_no: str):
    """Filter to one chapter and open its first pair."""
    st = session.ensure(state)
    if not session.has_project(st):
        return _no_change(st, "Open a textbook first.")
    st, _i, conflict = save(st, src, tgt, status, note, reason="navigate")
    if conflict:
        return _stay_with_conflict(st, conflict)
    st["filters"]["chapter_no"] = chapter_no or ""
    return _goto_first(st)


def filter_status(state: Any, src: str, tgt: str, status: str, note: str,
                  show: str):
    """Restrict navigation to one answer — usually 'not checked yet'."""
    st = session.ensure(state)
    if not session.has_project(st):
        return _no_change(st, "Open a textbook first.")
    st, _i, conflict = save(st, src, tgt, status, note, reason="navigate")
    if conflict:
        return _stay_with_conflict(st, conflict)
    st["filters"]["status"] = show or ""
    return _goto_first(st)


def do_search(state: Any, query: str):
    """Find pairs. Returns rows for the results table, not a navigation."""
    st = session.ensure(state)
    if not session.has_project(st):
        return [], "Open a textbook first."
    q = (query or "").strip()
    if not q:
        return [], ""
    try:
        with store.ro() as con:
            found = search.SearchRepo(con).find(st["pid"], q, limit=50)
    except NotFound:
        return [], "That workspace is no longer available."
    except Exception:
        log.exception("search failed")
        return [], "The search could not be completed."

    rows = [[r["seq"],
             STATUS_BY_KEY.get(r["status"], STATUSES[0]).label,
             (r["chapter_no"] + " " if r["chapter_no"] else "") + (r["chapter"] or ""),
             _snip(r["src"]["text"]), _snip(r["tgt"]["text"])]
            for r in found["rows"]]
    how = {"fts": "", "like": " (slower search — this SQLite has no full-text index)",
           "page": " — by page", "row": " — by pair number",
           "location": " — by chapter or section", "id": " — by identifier"}
    note = (f"{found['total']:,} match"
            f"{'' if found['total'] == 1 else 'es'}{how.get(found['mode'], '')}")
    if found["total"] > len(rows):
        note += f", showing the first {len(rows)}"
    return rows, note


def open_search_hit(state: Any, src: str, tgt: str, status: str, note: str,
                    evt: gr.SelectData):
    """Open the pair a search result points at."""
    st = session.ensure(state)
    if not session.has_project(st) or evt is None:
        return _no_change(st, "Open a textbook first.")
    st, _i, conflict = save(st, src, tgt, status, note, reason="navigate")
    if conflict:
        return _stay_with_conflict(st, conflict)
    try:
        seq = int(evt.row_value[0])
    except (TypeError, ValueError, IndexError):
        return _no_change(st, "That result could not be opened.")
    with store.ro() as con:
        found = workspace.WorkspaceRepo(con).at_seq(st["pid"], seq)
    if not found:
        return _no_change(st, "That pair could not be found.")
    return _load(st, found["rid"])


def _snip(text: str, n: int = 90) -> str:
    one = " ".join((text or "").split())
    return one[:n] + ("…" if len(one) > n else "")


def _stay_with_conflict(st: dict, conflict_html: str):
    keep = gr.update()
    return (st, keep, keep, keep, keep, keep,
            render.save_state("conflict"), keep, keep, conflict_html, keep, "")


# ── conflict resolution ────────────────────────────────────────────────────

def resolve_conflict(state: Any, keep_mine: bool):
    """Settle a save that lost a race, without losing either version."""
    st = session.ensure(state)
    conflict = st.get("conflict")
    if not conflict:
        return _no_change(st, "There is nothing to resolve.")
    side = conflict["side"]
    try:
        if keep_mine:
            with store.tx() as con:
                annotate.save_text(con, st["rid"], side, conflict["mine"],
                                   base_rev=conflict["rev"], annotator=st["annotator"],
                                   session=_session_key(st), reason="conflict-keep-mine")
        st["conflict"] = None
        return _load(st, st["rid"],
                     note="your version was kept" if keep_mine
                          else "the other version was kept")
    except Conflict:
        return _no_change(st, "It changed again while you were deciding. "
                              "The pair has been reloaded; please look again.")
    except Exception:
        log.exception("conflict resolution failed for %s", st.get("rid"))
        return _no_change(st, "That could not be applied. Nothing was lost.")


# ── restoring the parser's original ────────────────────────────────────────

def restore_original(state: Any, side: str):
    """Put back exactly what the machine read from the page."""
    st = session.ensure(state)
    if not session.has_row(st):
        return _no_change(st, "Open a pair first.")
    if not st["present"].get(side):
        return _no_change(st, "There is nothing on that side to restore.")
    try:
        with store.tx() as con:
            annotate.restore(con, st["rid"], side, rev=0, annotator=st["annotator"],
                             session=_session_key(st))
    except Exception:
        log.exception("restore failed for %s/%s", st.get("rid"), side)
        return _no_change(st, "The original could not be restored just now.")
    return _load(st, st["rid"], note="the original text was put back")


# ── history ────────────────────────────────────────────────────────────────

def history(state: Any):
    """Every version of this pair, newest first, plus what changed."""
    st = session.ensure(state)
    if not session.has_row(st):
        return [], "Open a pair first."
    with store.ro() as con:
        repo = annotate.AnnotateRepo(con)
        text = repo.history(st["rid"], limit=60)
        statuses = repo.status_history(st["rid"], limit=40)
        diffs = {side: annotate.diff(con, st["rid"], side, a=0, b="current")
                 for side in ("src", "tgt") if st["present"].get(side)}

    rows = []
    for h in text:
        rows.append([time.strftime("%d %b %Y, %H:%M", time.localtime(h["ts"])),
                     "English" if h["side"] == "src" else "Target",
                     f"version {h['rev']}", h["actor"] or "someone",
                     h["reason"], f"{h['n_chars']:,} characters"])
    for h in statuses:
        rows.append([time.strftime("%d %b %Y, %H:%M", time.localtime(h["ts"])),
                     "Answer", STATUS_BY_KEY.get(h["status"], STATUSES[0]).label,
                     h["actor"] or "someone", "status", h["note"] or ""])
    rows.sort(key=lambda r: r[0], reverse=True)

    parts = []
    for side, d in diffs.items():
        name = "English" if side == "src" else "Target language"
        if d["identical"]:
            parts.append(f"**{name}** — unchanged from what the machine read.")
        else:
            body = "\n".join(d["diff"][:60]) or "(no line differences)"
            parts.append(f"**{name}** — changed "
                         f"({round(d['similarity'] * 100)}% of the original kept)\n"
                         f"```diff\n{body}\n```")
    return rows, "\n\n".join(parts) if parts else "Nothing open."


# ── source verification ────────────────────────────────────────────────────

def show_source(state: Any, side: str):
    """Render the region of the printed page this text came from.

    Deliberately a separate event that touches neither editor pane: checking
    the original must never cost an annotator the sentence they were part way
    through typing.
    """
    st = session.ensure(state)
    if not session.has_row(st):
        return None, "Open a pair first."
    if not st["present"].get(side):
        return None, "There is nothing on that side to check."
    try:
        with store.ro() as con:
            row = workspace.WorkspaceRepo(con).row(st["rid"])
            sid = (row.get(side) or {}).get("sid")
            if not sid:
                return None, "There is nothing on that side to check."
            view = sources.for_segment(con, sid)
    except Exception:
        log.exception("source view failed for %s/%s", st.get("rid"), side)
        return None, "The original page could not be loaded."
    if not view.ok:
        return None, view.message
    which = "English" if side == "src" else "target-language"
    return str(view.path), (f"The {which} text as printed — “{view.book}”, "
                            f"page {view.page + 1}.")
