"""Per-session state for the annotation workspace.

Everything an annotator's browser tab knows lives in one dictionary held in a
``gr.State``. Gradio gives every session its own copy, which is what makes the
shared link safe: one person's current pair, filters, unsaved text and name are
invisible to everyone else.

The rule this module exists to enforce is that **there are no module-level
mutable globals anywhere in the interface**. Not a cache of the current row,
not a "last opened project", not a convenience handle to the current
connection. Every one of those becomes cross-session contamination the moment
two people use the link at once, and the failure is silent — person A simply
starts seeing person B's textbook. A test asserts the absence.

The state is a plain dict rather than a dataclass because Gradio serialises it
between the server and the browser on every event; a dict survives that without
a custom encoder, and staying boring here is worth more than the type checking.
"""
from __future__ import annotations

import copy
import time
from typing import Any

#: A fresh session. Copied, never shared — returning this object itself would
#: hand every session the same dictionary.
BLANK: dict[str, Any] = {
    "annotator": "",
    "pid": "",
    "project": {},           # name, languages, scripts, book keys
    "seq": -1,               # position of the open pair, -1 = nothing open
    "rid": "",
    "src_rev": 0,
    "tgt_rev": 0,
    # What the server last confirmed. Comparing against these is how "is there
    # anything to save?" is answered without asking the database.
    "saved": {"src": "", "tgt": "", "status": "pending", "note": ""},
    # Immutable originals, kept so "restore what the machine read" needs no
    # round trip and cannot be confused with the last save.
    "original": {"src": "", "tgt": ""},
    "present": {"src": False, "tgt": False},
    "filters": {"status": "", "chapter_no": "", "kind": ""},
    "last_error": "",
    "conflict": None,        # set when a save lost a race, cleared on resolve
    "opened_at": 0.0,
}


def blank() -> dict:
    return copy.deepcopy(BLANK)


def ensure(state: Any) -> dict:
    """Accept whatever Gradio handed back and return a usable session.

    Gradio will pass ``None`` on the very first event of a session, and a
    half-populated dict if the state schema changed while a tab was open. Both
    are repaired here rather than crashing the first click of the day.
    """
    if not isinstance(state, dict):
        return blank()
    out = blank()
    for key, value in state.items():
        if key in out:
            out[key] = value
    # Nested dicts must not be left partial: a missing "src" key in `saved`
    # would raise deep inside a save handler where the message is useless.
    for key in ("saved", "original", "present", "filters"):
        merged = copy.deepcopy(BLANK[key])
        if isinstance(state.get(key), dict):
            merged.update(state[key])
        out[key] = merged
    return out


def has_project(state: dict) -> bool:
    return bool(state.get("pid"))


def has_row(state: dict) -> bool:
    return bool(state.get("rid"))


def dirty(state: dict, src: Any, tgt: Any, status: Any, note: Any) -> bool:
    """Is anything on screen different from what the server confirmed?

    Answered locally, so the autosave tick costs nothing when an annotator is
    reading rather than typing — which is most of the time.
    """
    saved = state.get("saved") or {}
    return (_s(src) != _s(saved.get("src"))
            or _s(tgt) != _s(saved.get("tgt"))
            or _s(status) != _s(saved.get("status"))
            or _s(note) != _s(saved.get("note")))


def mark_saved(state: dict, src: Any, tgt: Any, status: Any, note: Any,
               src_rev: Any = None, tgt_rev: Any = None) -> dict:
    state["saved"] = {"src": _s(src), "tgt": _s(tgt),
                      "status": _s(status) or "pending", "note": _s(note)}
    if src_rev is not None:
        state["src_rev"] = int(src_rev)
    if tgt_rev is not None:
        state["tgt_rev"] = int(tgt_rev)
    state["last_error"] = ""
    return state


def load_row(state: dict, row: dict) -> dict:
    """Point the session at a pair and record everything needed to save it."""
    state["rid"] = row["rid"]
    state["seq"] = int(row["seq"])
    state["src_rev"] = int(row["src"].get("rev") or 0)
    state["tgt_rev"] = int(row["tgt"].get("rev") or 0)
    state["present"] = {"src": bool(row["src"].get("present")),
                        "tgt": bool(row["tgt"].get("present"))}
    state["original"] = {"src": row["src"].get("source") or "",
                         "tgt": row["tgt"].get("source") or ""}
    state["conflict"] = None
    state["opened_at"] = time.time()
    return mark_saved(state, row["src"].get("text"), row["tgt"].get("text"),
                      row.get("status"), row.get("note"))


def _s(v: Any) -> str:
    return "" if v is None else str(v)
