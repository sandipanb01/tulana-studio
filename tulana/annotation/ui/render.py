"""Small HTML fragments for the workspace.

Gradio draws components; these draw the handful of things a component cannot —
the pair header, the progress bar, the save indicator, the view toolbar. They
are the only place in the interface that emits markup, and every value that
reaches them goes through :func:`esc` first.

That matters more than it sounds. Chapter titles, notes and segment text all
come from OCR of scanned books and from annotators typing free text; a stray
``<`` in a Marathi chapter title would otherwise break the page, and a
deliberate one would be an injection. Escaping in one module means there is one
place to check rather than a dozen f-strings to audit.
"""
from __future__ import annotations

import html
from typing import Any

from ..core.models import KIND_BY_KEY, STATUS_BY_KEY, STATUSES

ORIGIN_LABEL = {
    "suggested": ("suggested", "Setu found strong evidence these two belong together."),
    "derived": ("in order", "Placed by position between two stronger matches. Less certain."),
    "unpaired": ("one side only", "No partner was found for this text."),
    "manual": ("yours", "You chose this pairing."),
    "imported": ("imported", "Brought in from existing data."),
}


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


# ── the save indicator ─────────────────────────────────────────────────────

_SAVE_WORDS = {
    "saved": "All changes saved",
    "saving": "Saving…",
    "dirty": "Unsaved changes",
    "error": "Could not save — will retry",
    "conflict": "Someone else changed this pair",
    "idle": "Nothing open",
}


def save_state(kind: str, detail: str = "") -> str:
    """The one line that tells an annotator whether their work is safe."""
    words = _SAVE_WORDS.get(kind, kind)
    if detail:
        words = f"{words} — {esc(detail)}"
    else:
        words = esc(words)
    return f'<div class="setu-save" data-state="{esc(kind)}">{words}</div>'


# ── the pair header ────────────────────────────────────────────────────────

def pair_header(row: dict | None, position: dict | None = None) -> str:
    """Where this pair sits in the book, and where it came from."""
    if not row:
        return ('<div class="setu-head"><span class="setu-loc">'
                'Choose two textbooks above, then press “Open these two books”.'
                '</span></div>')

    status = STATUS_BY_KEY.get(row.get("status", ""), STATUSES[0])
    kind = KIND_BY_KEY.get(row.get("kind", ""))
    label, why = ORIGIN_LABEL.get(row.get("origin", ""), (row.get("origin", ""), ""))

    where = " · ".join(p for p in (
        (f"{row.get('chapter_no')}." if row.get("chapter_no") else "") + " "
        + (row.get("chapter") or ""),
        row.get("section") or "",
    ) if p.strip())

    pos = ""
    if position and position.get("total"):
        pos = (f'<span class="setu-loc">pair {position["index"]:,} '
               f'of {position["total"]:,}</span>')

    conf = ""
    if row.get("origin") == "suggested" and row.get("confidence"):
        conf = " ({}% sure)".format(round(float(row["confidence"]) * 100))

    return (
        '<div class="setu-head">'
        f'<span class="setu-dot" style="background:{esc(status.color)}" '
        f'title="{esc(status.label)}"></span>'
        f'<span class="setu-seq">#{esc(row.get("seq"))}</span>'
        f'{pos}'
        f'<span class="setu-badge" title="{esc(why)}">{esc(label)}{esc(conf)}</span>'
        + (f'<span class="setu-badge">{esc(kind.icon)} {esc(kind.label)}</span>'
           if kind else "")
        + (f'<span class="setu-loc">{esc(where)}</span>' if where else "")
        + '</div>'
    )


def pane_label(side: str, row: dict | None, language: str) -> str:
    """The caption above one editor pane: language, page, and what it contains."""
    name = language or ("English" if side == "src" else "Target language")
    if not row:
        return name
    data = row.get(side) or {}
    bits = [name]
    if data.get("page") is not None:
        bits.append(f"page {int(data['page']) + 1}")
    if data.get("has_math"):
        bits.append("has mathematics")
    if data.get("has_table"):
        bits.append("has a table")
    if data.get("edited"):
        bits.append("edited")
    if not data.get("present"):
        bits.append("nothing on this side")
    return "  ·  ".join(bits)


# ── progress ───────────────────────────────────────────────────────────────

def progress(prog: dict | None) -> str:
    """How much of the book is done, and how the answers break down."""
    if not prog or not prog.get("total"):
        return '<div class="setu-prog">No textbook open.</div>'

    done, total = prog["done"], prog["total"]
    pct = prog.get("percent", 0.0)
    rows = []
    for s in STATUSES:
        n = (prog.get("by_status") or {}).get(s.key, 0)
        if not n and s.key == "pending":
            continue
        rows.append(
            f'<tr><td><span class="setu-dot" style="background:{esc(s.color)}">'
            f'</span></td><td>{esc(s.label)}</td>'
            f'<td style="text-align:right">{n:,}</td></tr>')

    return (
        '<div class="setu-prog">'
        f'<b>{done:,}</b> of <b>{total:,}</b> pairs checked'
        f'<div class="setu-track"><div class="setu-fill" style="width:{pct}%"></div></div>'
        f'<table>{"".join(rows)}</table>'
        '</div>'
    )


# ── the view toolbar ───────────────────────────────────────────────────────
#
# Plain HTML, wired entirely by annotation.js. None of these buttons touches
# annotation data or the server, so routing them through Gradio events would
# add a network round trip to something that should be instantaneous — and
# would put view preferences into session state, where they do not belong.

VIEW_BAR = """
<div class="setu-bar">
  <button type="button" id="setu_sync_btn" data-act="sync" data-on="1"
          title="Both sides scroll together.">Scrolling: linked</button>
  <button type="button" data-act="zoom-out" title="Smaller text (Ctrl and minus)">A&minus;</button>
  <span class="setu-hint" id="setu_zoom_label">16px</span>
  <button type="button" data-act="zoom-in" title="Larger text (Ctrl and plus)">A+</button>
  <button type="button" data-act="zoom-reset" title="Back to the default view (Ctrl and 0)">Reset</button>
  <button type="button" data-act="shorter" title="Shorter text boxes">&minus; Height</button>
  <button type="button" data-act="taller" title="Taller text boxes">+ Height</button>
  <button type="button" data-act="compact" title="Hide everything except the two texts">Compact</button>
  <button type="button" data-act="focus" title="Hide the side panel as well">Focus</button>
  <span class="setu-sep"></span>
  <span class="setu-hint">1&ndash;6 set the answer &nbsp;·&nbsp; Alt+&larr;/&rarr; move &nbsp;·&nbsp; Ctrl+S saves</span>
</div>
"""


# ── errors ─────────────────────────────────────────────────────────────────

def conflict_panel(conflict: dict | None) -> str:
    """Both versions, side by side, when two people saved the same pair."""
    if not conflict:
        return ""
    side = "English" if conflict.get("side") == "src" else "the target language"
    return (
        '<div style="border:1px solid #7c3aed;border-radius:8px;padding:10px">'
        f'<b>Someone else changed {esc(side)} while you were editing it.</b>'
        '<p style="margin:.4em 0">Nothing has been lost. Both versions are below. '
        'Choose which one to keep.</p>'
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">'
        '<div><b>Now saved (them)</b>'
        f'<pre style="white-space:pre-wrap;font-family:var(--setu-indic);'
        f'max-height:220px;overflow:auto">{esc(conflict.get("theirs"))}</pre></div>'
        '<div><b>What you typed</b>'
        f'<pre style="white-space:pre-wrap;font-family:var(--setu-indic);'
        f'max-height:220px;overflow:auto">{esc(conflict.get("mine"))}</pre></div>'
        '</div></div>'
    )
