"""Assembling the Gradio Blocks interface.

This module lays out components and wires events. It contains no annotation
logic at all — every handler lives in :mod:`workspace` or :mod:`panels`, which
in turn call the service layer. The split is what makes the logic testable
without a browser and the layout changeable without touching the logic.

Two Gradio facts this file is built around, both of which change between major
versions and both of which fail *silently* when wrong:

* ``css``, ``js`` and ``head`` belong to :meth:`Blocks.launch`, not to the
  ``Blocks`` constructor — they moved in Gradio 6. Passed to the constructor
  they are ignored with a warning, and the workspace comes up with collapsed
  editor panes and no keyboard shortcuts. :func:`assets` returns them and
  :func:`launch_kwargs` puts them where they belong.
* ``gr.State`` is per session. Everything an annotator's tab knows lives in one
  of those, and nothing lives at module level. That is the whole of the
  concurrency design, and it only works if it is never broken.
"""
from __future__ import annotations

import logging
from pathlib import Path

import gradio as gr

import config

from ..core import store
from . import panels, render, session
from . import workspace as ws

log = logging.getLogger("annotation.ui.app")

#: Populated while the layout is built; wired to `demo.load` once the Blocks
#: context is open. A list rather than a direct call because the components do
#: not exist yet at the point the handler is known.
_ON_LOAD: list = []

STATIC = Path(__file__).resolve().parent / "static"

#: The pair-changed output list, in the order every such handler returns.
#: Declared once, used by all of them, so a handler cannot put the target text
#: into the English pane by returning its values in the wrong order.
_PAIR_OUT_NAMES = ("state src tgt status note pairhead savestate progress "
                   "chapter_filter conflict source_img source_msg").split()


def assets() -> dict:
    """CSS, JS and head markup, read from disk at launch.

    Read rather than embedded so the stylesheet can be edited and the app
    restarted, and so a missing file is an obvious error at start-up rather
    than a subtly unstyled page.
    """
    css = (STATIC / "annotation.css").read_text(encoding="utf-8")
    js = (STATIC / "annotation.js").read_text(encoding="utf-8")
    return {"css": css, "head": f"<script>\n{js}\n</script>"}


def build() -> gr.Blocks:
    """Construct the whole interface. Returns an unlaunched Blocks."""
    # Gradio's default theme is built on an ORANGE primary ramp (#f97316,
    # #ea580c, #fb923c …) which colours every primary button, focus ring and
    # selected tab. No amount of editing annotation.css removes it, because it
    # arrives in Gradio's own theme.css. Setting the hues here is the only
    # place it can be changed. Teal matches Tulana; slate keeps the chrome
    # quiet so the two texts are what the eye lands on.
    theme = gr.themes.Soft(
        primary_hue=gr.themes.colors.teal,
        secondary_hue=gr.themes.colors.slate,
        neutral_hue=gr.themes.colors.slate,
    )

    with gr.Blocks(title="Setu — Tulana Studio", fill_width=True,
                   theme=theme) as demo:
        state = gr.State(session.blank())

        gr.Markdown(
            "## सेतु  Setu — parallel textbook annotation\n"
            "English on the left, the Indian-language edition on the right. "
            "Correct either side, say whether they match, and move on. "
            "Everything is saved as you go.")

        with gr.Tabs():
            with gr.Tab("Annotate", id="tab_annotate"):
                pair = _annotate_tab(state)
            with gr.Tab("Saved work", id="tab_review"):
                _review_tab(state, pair)
            with gr.Tab("Download", id="tab_export"):
                _export_tab(state)
            with gr.Tab("Help", id="tab_help"):
                _help_tab()

        for fn, inputs, outputs in _ON_LOAD:
            demo.load(fn, inputs, outputs)
        _ON_LOAD.clear()

    return demo


# ── the annotation tab ─────────────────────────────────────────────────────

def _annotate_tab(state: gr.State) -> dict:
    with gr.Accordion("Choose a textbook", open=True) as chooser:
        with gr.Row():
            annotator = gr.Textbox(
                label="Your name", placeholder="so your work can be attributed",
                scale=1, max_lines=1, elem_id="setu_annotator")
            # Opens on the first pairable board rather than empty, so the
            # cascade below fills in and the annotator lands on two books.
            board = gr.Dropdown(label="State board", choices=ws.boards(),
                                value=ws.first_board(), scale=2)
            klass = gr.Dropdown(label="Class", choices=[], interactive=False, scale=1)
            subject = gr.Dropdown(label="Subject", choices=[], interactive=False, scale=1)
        with gr.Row():
            with gr.Column():
                gr.Markdown("**Left — the source, usually English**")
                src_lang = gr.Dropdown(label="Language", choices=[], interactive=False)
                src_book = gr.Dropdown(label="Textbook", choices=[], interactive=False)
            with gr.Column():
                gr.Markdown("**Right — the language you are checking**")
                tgt_lang = gr.Dropdown(label="Language", choices=[], interactive=False)
                tgt_book = gr.Dropdown(label="Textbook", choices=[], interactive=False)
        open_btn = gr.Button("Open these two books", variant="primary",
                             elem_id="setu_open")

    view_bar = gr.HTML(render.VIEW_BAR, elem_id="setu_viewbar")
    pair_head = gr.HTML(render.pair_header(None), elem_id="setu_pairhead")

    with gr.Row():
        with gr.Column(scale=5):
            with gr.Row():
                src = gr.Textbox(label="English", lines=18, max_lines=18,
                                 elem_id="setu_src", buttons=["copy"],
                                 interactive=True, autoscroll=False)
            with gr.Row(elem_classes=["setu-secondary"]):
                src_orig = gr.Button("Restore the original", size="sm")
                src_check = gr.Button("Check the printed page", size="sm")
        with gr.Column(scale=5):
            with gr.Row():
                tgt = gr.Textbox(label="Target language", lines=18, max_lines=18,
                                 elem_id="setu_tgt", buttons=["copy"],
                                 interactive=True, autoscroll=False)
            with gr.Row(elem_classes=["setu-secondary"]):
                tgt_orig = gr.Button("Restore the original", size="sm")
                tgt_check = gr.Button("Check the printed page", size="sm")

    with gr.Row():
        status = gr.Radio(choices=ws.STATUS_CHOICES, value="pending",
                          label="Are these the same text?", elem_id="setu_status",
                          info=ws.STATUS_HELP)
    with gr.Row():
        note = gr.Textbox(label="Note (optional)", max_lines=2, scale=4,
                          placeholder="Why did you choose that answer?")
        save_state = gr.HTML(render.save_state("idle"), elem_id="setu_savestate")

    with gr.Row():
        prev_btn = gr.Button("← Previous", elem_id="setu_prev")
        next_btn = gr.Button("Next →", variant="primary", elem_id="setu_next")
        pending_btn = gr.Button("Next unchecked", elem_id="setu_next_pending")
        save_btn = gr.Button("Save changes", elem_id="setu_save")

    conflict = gr.HTML("", elem_id="setu_conflict")
    with gr.Row(elem_classes=["setu-secondary"]):
        keep_mine = gr.Button("Keep what I typed", size="sm")
        keep_theirs = gr.Button("Keep the saved version", size="sm")

    with gr.Row(elem_classes=["setu-secondary"]):
        with gr.Column(scale=2, elem_id="setu_sidebar"):
            chapter = gr.Dropdown(label="Jump to a chapter", choices=[("Everything", "")],
                                  value="", interactive=True)
            show = gr.Dropdown(label="Only show",
                               choices=[("Everything", ""),
                                        ("Not checked yet", "pending"),
                                        ("Needs correction", "needs_correction"),
                                        ("Unclear", "unclear")],
                               value="", interactive=True)
            progress = gr.HTML(render.progress(None), elem_id="setu_progress")
        with gr.Column(scale=5):
            search_box = gr.Textbox(label="Search this textbook", max_lines=1,
                                    placeholder="a word, or: page 42 · chapter 3 · #450")
            search_note = gr.Markdown("")
            results = gr.Dataframe(
                headers=["Pair", "Answer", "Chapter", "English", "Target language"],
                datatype=["number", "str", "str", "str", "str"],
                interactive=False, wrap=True, row_count=(0, "dynamic"),
                label="Click a row to open it")

    with gr.Accordion("The printed page", open=False,
                      elem_classes=["setu-secondary"]) as source_acc:
        source_msg = gr.Markdown("Use “Check the printed page” under either side.")
        source_img = gr.Image(label=None, show_label=False, elem_id="setu_sourceimg",
                              interactive=False, height=520)

    with gr.Accordion("What changed on this pair", open=False,
                      elem_classes=["setu-secondary"]):
        hist_btn = gr.Button("Show the history", size="sm")
        hist_table = gr.Dataframe(
            headers=["When", "What", "Version", "Who", "Why", "Size"],
            interactive=False, wrap=True, row_count=(0, "dynamic"))
        hist_diff = gr.Markdown("")

    pair = {"state": state, "src": src, "tgt": tgt, "status": status, "note": note,
            "pairhead": pair_head, "savestate": save_state, "progress": progress,
            "chapter_filter": chapter, "conflict": conflict,
            "source_img": source_img, "source_msg": source_msg}
    pair_out = [pair[k] for k in _PAIR_OUT_NAMES]
    edit_in = [state, src, tgt, status, note]

    # ── cascade ──
    board.change(ws.on_board, [board], [klass, subject, src_lang, tgt_lang,
                                        src_book, tgt_book])
    klass.change(ws.on_class, [board, klass], [subject, src_lang, tgt_lang,
                                               src_book, tgt_book])
    subject.change(ws.on_subject, [board, klass, subject],
                   [src_lang, tgt_lang, src_book, tgt_book])
    # The left language also re-filters the right-hand language list, so the
    # language being read on one side is never offered on the other.
    src_lang.change(ws.on_source_language,
                    [board, klass, subject, src_lang, tgt_book],
                    [src_book, tgt_lang])
    tgt_lang.change(ws.on_language, [board, klass, subject, tgt_lang, src_book],
                    [tgt_book])

    open_btn.click(ws.open_books, [state, annotator, src_book, tgt_book], pair_out) \
            .then(lambda: gr.update(open=False), None, [chooser])

    # ── saving ──
    #
    # Four routes, one implementation. Blur catches the common case the instant
    # an annotator looks away; the timer catches someone who types for minutes
    # without leaving the box; navigation saves before it moves; and the button
    # is there for people who want to press it.
    save_out = [state, save_state, conflict]
    # Progress is part of the answer to "did that register?", so a status
    # change refreshes it rather than waiting for the next navigation.
    status_out = save_out + [progress]
    save_btn.click(lambda *a: ws.save(*a, reason="manual"), edit_in, save_out)
    src.blur(lambda *a: ws.save(*a, reason="blur"), edit_in, save_out)
    tgt.blur(lambda *a: ws.save(*a, reason="blur"), edit_in, save_out)
    note.blur(lambda *a: ws.save(*a, reason="blur"), edit_in, save_out)
    status.change(lambda *a: ws.save_and_count(*a, reason="status"), edit_in, status_out)

    gr.Timer(3.0).tick(ws.autosave_tick, edit_in, save_out, show_progress="hidden")

    # ── navigation ──
    prev_btn.click(lambda *a: ws.move(*a, direction=-1), edit_in, pair_out)
    next_btn.click(lambda *a: ws.move(*a, direction=1), edit_in, pair_out)
    pending_btn.click(lambda *a: ws.move(*a, direction=1, only_pending=True),
                      edit_in, pair_out)
    chapter.input(ws.jump_to_chapter, edit_in + [chapter], pair_out)
    show.input(ws.filter_status, edit_in + [show], pair_out)

    # ── search ──
    search_box.submit(ws.do_search, [state, search_box], [results, search_note])
    results.select(ws.open_search_hit, edit_in, pair_out)

    # ── conflicts ──
    keep_mine.click(lambda s: ws.resolve_conflict(s, True), [state], pair_out)
    keep_theirs.click(lambda s: ws.resolve_conflict(s, False), [state], pair_out)

    # ── originals and source ──
    src_orig.click(lambda s: ws.restore_original(s, "src"), [state], pair_out)
    tgt_orig.click(lambda s: ws.restore_original(s, "tgt"), [state], pair_out)
    src_check.click(lambda s: ws.show_source(s, "src"), [state],
                    [source_img, source_msg]) \
             .then(lambda: gr.update(open=True), None, [source_acc])
    tgt_check.click(lambda s: ws.show_source(s, "tgt"), [state],
                    [source_img, source_msg]) \
             .then(lambda: gr.update(open=True), None, [source_acc])

    hist_btn.click(ws.history, [state], [hist_table, hist_diff])

    # Gradio selects the first choice of a Dropdown by default, but selecting
    # it does not fire `change`. Without this the workspace opens showing a
    # board with an empty Class list beside it, and the only way forward is to
    # pick a different board and pick back. Running the cascade once on load
    # makes the first paint consistent with what is selected.
    demo_load_targets = [klass, subject, src_lang, tgt_lang, src_book, tgt_book]
    _ON_LOAD.append((ws.on_board, [board], demo_load_targets))

    return pair


# ── the other tabs ─────────────────────────────────────────────────────────

def _review_tab(state: gr.State, pair: dict) -> None:
    gr.Markdown("Everything in the open workspace. Click a row to open it in "
                "**Annotate**.")
    with gr.Row():
        show = gr.Dropdown(label="Show", choices=panels.REVIEW_FILTERS, value="",
                           scale=2)
        order = gr.Dropdown(label="Order", value="In book order",
                            choices=["In book order", "Most recently changed"], scale=2)
        page = gr.Number(label="Page", value=1, precision=0, minimum=1, scale=1)
        refresh = gr.Button("Refresh", scale=1)
    note = gr.Markdown("")
    table = gr.Dataframe(headers=panels.REVIEW_COLUMNS, interactive=False, wrap=True,
                         row_count=(0, "dynamic"),
                         datatype=["number", "str", "str", "str", "str", "str", "str"])

    inputs = [state, show, order, page]
    outputs = [table, note, page]
    for control in (show, order):
        control.input(lambda s, sh, o, _p: panels.review(s, sh, o, 1), inputs, outputs)
    page.change(panels.review, inputs, outputs)
    refresh.click(panels.review, inputs, outputs)

    pair_out = [pair[k] for k in _PAIR_OUT_NAMES]
    table.select(panels.open_from_review,
                 [state, pair["src"], pair["tgt"], pair["status"], pair["note"]],
                 pair_out)


def _export_tab(state: gr.State) -> None:
    gr.Markdown("Download the annotations from the open workspace.")
    with gr.Row():
        fmt = gr.Dropdown(label="Format", choices=panels.format_choices(),
                          value="jsonl", scale=3)
        scope = gr.Dropdown(label="Which pairs", choices=panels.EXPORT_SCOPES,
                            value="all", scale=3)
        paired = gr.Checkbox(label="Only pairs with text on both sides", scale=2)
    with gr.Row():
        go = gr.Button("Prepare the download", variant="primary")
        go_all = gr.Button("Every format, as one zip")
    note = gr.Markdown("")
    out = gr.File(label="Your download", interactive=False)
    gr.Markdown("### Downloaded before")
    hist = gr.Dataframe(headers=["When", "Format", "File", "Pairs", "Size", "By"],
                        interactive=False, wrap=True, row_count=(0, "dynamic"))
    refresh = gr.Button("Refresh this list", size="sm")

    go.click(panels.export, [state, fmt, scope, paired], [out, note]) \
      .then(panels.export_history, [state], [hist])
    go_all.click(panels.export_all, [state, scope, paired], [out, note]) \
          .then(panels.export_history, [state], [hist])
    refresh.click(panels.export_history, [state], [hist])


def _help_tab() -> None:
    choices = panels.doc_choices()
    first = choices[0][1] if choices else ""
    with gr.Row():
        picker = gr.Radio(choices=choices, value=first, label="", scale=1)
        body = gr.Markdown(panels.read_doc(first), elem_classes=["setu-doc"],
                           header_links=True)
    picker.change(panels.read_doc, [picker], [body])


# ── launching ──────────────────────────────────────────────────────────────

def launch_kwargs(**overrides) -> dict:
    """Arguments for :meth:`Blocks.launch`, with the assets where they belong.

    Gradio 6 moved ``css``, ``js`` and ``head`` from the ``Blocks`` constructor
    to ``launch``. Putting them here, in one function every launcher uses,
    means the interface cannot come up unstyled because one entry point forgot.

    ``allowed_paths`` matters just as much. Gradio will only serve a file that
    lives under the working directory, the system temp directory or a path it
    has been told about; anything else is refused with a message about the
    cache directory. Both things this interface hands to the browser — the
    rendered page images and the export files — live under ``STATE_DIR``,
    which is configurable and routinely points somewhere else. Without this,
    "Check the printed page" and every download fail on exactly the
    installations that configured their storage deliberately.
    """
    state_dir = str(Path(config.STATE_DIR).resolve())
    kwargs = dict(assets())
    kwargs["allowed_paths"] = [state_dir]
    kwargs.update(overrides)
    # An override may add its own paths; never silently drop the state folder.
    if "allowed_paths" in overrides:
        merged = list(dict.fromkeys([state_dir, *overrides["allowed_paths"]]))
        kwargs["allowed_paths"] = merged
    return kwargs


def ready() -> tuple[bool, str]:
    """Is there anything to annotate yet?

    Checked before launching so an annotator meets a sentence telling them what
    to run, rather than four empty dropdowns.
    """
    try:
        with store.ro() as con:
            from ..core.corpus import CorpusRepo
            counts = CorpusRepo(con).counts()
    except Exception as exc:                     # pragma: no cover - environment
        return False, f"The annotation database could not be opened: {exc}"
    if not counts["books"]:
        return False, (
            "No textbooks have been prepared yet. Run this once:\n"
            "    python3 -c \"import sys; sys.path.insert(0,'.'); "
            "from annotation.core import store, corpus; "
            "con = store.connect(); corpus.build(con, log_fn=print)\"")
    return True, (f"{counts['books']} textbooks · "
                  f"{counts['segments']:,} pieces of text")
