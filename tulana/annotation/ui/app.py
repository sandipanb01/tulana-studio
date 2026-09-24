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
from . import browse, panels, session
from . import workspace as ws

log = logging.getLogger("annotation.ui.app")

#: Populated while the layout is built; wired to `demo.load` once the Blocks
#: context is open. A list rather than a direct call because the components do
#: not exist yet at the point the handler is known.
_ON_LOAD: list = []

STATIC = Path(__file__).resolve().parent / "static"

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
        # Soft ships Montserrat, a geometric display face meant for posters.
        # It carries no Devanagari, Gujarati, Kannada, Tamil or Malayalam
        # glyphs, so every Indian-language pane fell back to whatever the
        # browser chose — different on each machine, and heavier than the
        # English beside it. The system stack renders both sides with the
        # fonts the operating system already ships for those scripts, which
        # is what an annotator reading Marathi all day needs.
        font=("system-ui", "-apple-system", "Segoe UI", "Roboto",
              "Noto Sans", "Arial", "sans-serif"),
        font_mono=("ui-monospace", "SFMono-Regular", "Consolas",
                   "Liberation Mono", "monospace"),
    )

    with gr.Blocks(title="Setu — Tulana Studio", fill_width=True,
                   theme=theme) as demo:
        state = gr.State(session.blank())

        gr.Markdown(
            "## सेतु  Setu — parallel textbook annotation\n"
            "English on the left, the Indian-language edition on the right, "
            "page by page. Correct what the machine misread, say whether the "
            "two sides match, and turn the page. Everything is saved as you "
            "go.")

        with gr.Tabs():
            with gr.Tab("Annotate", id="tab_annotate"):
                shop = _workspace_tab(state)
            with gr.Tab("Saved work", id="tab_review"):
                _review_tab(state, shop)
            with gr.Tab("Download", id="tab_export"):
                _export_tab(state)
            with gr.Tab("Help", id="tab_help"):
                _help_tab()

        for fn, inputs, outputs in _ON_LOAD:
            demo.load(fn, inputs, outputs)
        _ON_LOAD.clear()

        # There is one interface, and it is the workspace at /work/. This page
        # is what a bare share link lands on, so it forwards there rather than
        # offering a second, different-looking tool — two interfaces for one
        # job is the confusion this whole rebuild exists to end.
        #
        # Kept reachable at ?stay=1 so there is a way back if the workspace
        # ever fails to load, and skipped when /work/ is not installed, which
        # launch_annotation.py reports separately.
        demo.load(None, None, None, js="""
            () => {
              try {
                if (new URLSearchParams(location.search).has('stay')) return;
                const base = location.pathname.replace(/\\/+$/, '');
                fetch(base + '/work/', {method: 'HEAD'})
                  .then(r => { if (r.ok) location.replace(base + '/work/'); })
                  .catch(() => {});
              } catch (e) {}
            }
        """)

    return demo


# ── the workspace: two textbooks, page by page ─────────────────────────────

def _workspace_tab(state: gr.State) -> dict:
    """Everything an annotator does, on one screen.

    This replaces the two tabs that came before it — a pair editor and a
    reading view — because keeping them apart made the annotator hold two
    positions in their head at once: where they were in the book, and which
    pair was open. The two disagreed constantly.

    The page is now the unit. Each side shows the blocks the parser found on
    the page you are looking at, in reading order. Tick *Let me correct the
    text* and every block becomes editable where it stands; the answer for a
    pair sits under the English block it belongs to. Nothing opens, nothing
    closes.

    The layout follows Tulana's own Blocks tab, which annotators already use
    without being taught: four dropdowns and one button on the first screen,
    everything else revealed once two books are open.
    """
    bstate = gr.State(browse.blank())

    # ── step 1: which two books ──────────────────────────────────────────
    with gr.Accordion("Step 1 — choose two textbooks", open=True) as chooser:
        with gr.Row():
            annotator = gr.Textbox(
                label="Your name", placeholder="so your work can be attributed",
                scale=1, max_lines=1, elem_id="setu_annotator")
            # Opens on the first pairable board rather than empty, so the
            # cascade below fills in and the annotator lands on two books.
            board = gr.Dropdown(label="State board", choices=ws.boards(),
                                value=ws.first_board(), scale=2)
            klass = gr.Dropdown(label="Class", choices=[], interactive=False,
                                scale=1)
            subject = gr.Dropdown(label="Subject", choices=[],
                                  interactive=False, scale=1)
        with gr.Row():
            with gr.Column():
                gr.Markdown("**Left — the source, usually English**")
                src_lang = gr.Dropdown(label="Language", choices=[],
                                       interactive=False)
                src_book = gr.Dropdown(label="Textbook", choices=[],
                                       interactive=False)
            with gr.Column():
                gr.Markdown("**Right — the language you are checking**")
                tgt_lang = gr.Dropdown(label="Language", choices=[],
                                       interactive=False)
                tgt_book = gr.Dropdown(label="Textbook", choices=[],
                                       interactive=False)
        open_btn = gr.Button("Open these two books", variant="primary",
                             elem_id="setu_open")

    # ── step 2: the work ─────────────────────────────────────────────────
    with gr.Row(elem_id="setu_modebar"):
        editing = gr.Checkbox(label="Let me correct the text", value=False,
                              elem_id="setu_editing")
        show_page = gr.Checkbox(label="Show me the printed page", value=False,
                                elem_id="setu_showpage")
        hide_noise = gr.Checkbox(
            label="Hide running heads, footers and page numbers", value=True)

    saved = gr.Markdown("", elem_id="setu_savestate")

    with gr.Row(elem_id="setu_navbar"):
        with gr.Column(scale=6):
            with gr.Row():
                src_chapter = gr.Dropdown(
                    label="Left — chapter", choices=[("Whole book", "")],
                    value="", interactive=True, scale=4,
                    elem_id="setu_src_chapter")
                src_page = gr.Number(label="Page", value=1, precision=0,
                                     minimum=1, step=1, scale=1,
                                     elem_id="setu_src_page")
            with gr.Row():
                src_prev = gr.Button("◀ Previous page", size="sm")
                src_next = gr.Button("Next page ▶", size="sm")
            src_tally = gr.Markdown("", elem_id="setu_src_tally")
        with gr.Column(scale=6):
            with gr.Row():
                tgt_chapter = gr.Dropdown(
                    label="Right — chapter", choices=[("Whole book", "")],
                    value="", interactive=True, scale=4,
                    elem_id="setu_tgt_chapter")
                tgt_page = gr.Number(label="Page", value=1, precision=0,
                                     minimum=1, step=1, scale=1,
                                     elem_id="setu_tgt_page")
            with gr.Row():
                tgt_prev = gr.Button("◀ Previous page", size="sm")
                tgt_next = gr.Button("Next page ▶", size="sm")
            tgt_tally = gr.Markdown("", elem_id="setu_tgt_tally")

    with gr.Row(elem_id="setu_bothbar"):
        both_prev = gr.Button("◀◀ Both back", size="sm", scale=1)
        both_next = gr.Button("Both forward ▶▶", size="sm", scale=1)
        link_btn = gr.Button("⇄ These two pages match", variant="primary",
                             size="sm", scale=2, elem_id="setu_link")
        unlink_btn = gr.Button("Unlink", size="sm", scale=1)

    offset_note = gr.Markdown("", elem_id="setu_offset")

    # ── the two columns of blocks ────────────────────────────────────────
    #
    # Drawn with gr.render rather than as a fixed set of components, because
    # a page carries however many blocks it carries — five on a chapter
    # opening, forty in the middle of an exercise — and an interface built
    # from a fixed number of boxes has to either cut the page short or
    # show empty ones. Both sides are drawn in one pass so they can never come
    # from two different moments.

    @gr.render(inputs=[bstate, editing, show_page], show_progress="minimal")
    def _columns(bs, is_editing, wants_page):
        bs = browse.ensure(bs)
        if not bs.get("pid"):
            gr.Markdown("Choose two textbooks above and press "
                        "**Open these two books**.",
                        elem_classes=["setu-doc-empty"])
            return

        data = browse.load(bs)
        if data["error"]:
            gr.Markdown(data["error"])
            return

        with gr.Row():
            for side in ("src", "tgt"):
                heading = (f"**{bs[f'{side}_lang'] or ('Left' if side == 'src' else 'Right')}**"
                           f"  ·  {bs[f'{side}_title']}"
                           f"  ·  page {browse.to_display(bs[f'{side}_page'])}"
                           f" of {browse.to_display(bs[f'{side}_hi'])}")
                with gr.Column(scale=5,
                               elem_id=f"setu_col_{side}",
                               elem_classes=["setu-doc", f"setu-doc-{side}"]):
                    gr.Markdown(heading, elem_classes=["setu-doc-head"])

                    if wants_page:
                        path, message = browse.printed_page(bs, side)
                        if path:
                            gr.Image(value=path, show_label=False,
                                     show_download_button=False,
                                     elem_classes=["setu-printed"])
                        else:
                            # A missing PDF is the normal case on a Git LFS
                            # checkout. Say so in a sentence and carry on —
                            # the text does not depend on it.
                            gr.Markdown(message,
                                        elem_classes=["setu-doc-empty"])

                    rows = data[side]
                    if not rows:
                        gr.Markdown(
                            f"Page {browse.to_display(bs[f'{side}_page'])} has "
                            f"no text in this edition — it may be a full-page "
                            f"illustration. Step to the next page.",
                            elem_classes=["setu-doc-empty"])
                        continue

                    for b in rows:
                        _block(state, bs, b, side, is_editing, saved)

    # ── wiring ───────────────────────────────────────────────────────────

    nav_out = [bstate, src_page, tgt_page, src_tally, tgt_tally, offset_note]

    def _after(bs):
        """Everything the bar above the columns shows, from one state."""
        data = browse.load(bs)
        return (bs,
                gr.update(value=browse.to_display(bs["src_page"]),
                          minimum=browse.to_display(bs["src_lo"]),
                          maximum=browse.to_display(bs["src_hi"])),
                gr.update(value=browse.to_display(bs["tgt_page"]),
                          minimum=browse.to_display(bs["tgt_lo"]),
                          maximum=browse.to_display(bs["tgt_hi"])),
                data["src_tally"], data["tgt_tally"], browse.offset_note(bs))

    def _open(st, bs):
        bs = browse.open_books(st, bs)
        if not bs.get("pid"):
            return (*_after(bs), gr.update(), gr.update())
        with store.ro() as con:
            src_ch = browse.chapter_choices(con, bs["src_book"])
            tgt_ch = browse.chapter_choices(con, bs["tgt_book"])
        return (*_after(bs),
                gr.update(choices=src_ch, value=bs["src_chapter"]),
                gr.update(choices=tgt_ch, value=bs["tgt_chapter"]))

    open_out = nav_out + [src_chapter, tgt_chapter]

    def _open_project(st, who, sb, tb):
        """ws.open_books returns the old pair-editor's whole output tuple; this
        workspace needs only the session it produced."""
        return ws.open_books(st, who, sb, tb)[0]

    open_btn.click(_open_project, [state, annotator, src_book, tgt_book],
                   [state]) \
            .then(_open, [state, bstate], open_out) \
            .then(lambda: gr.update(open=False), None, [chooser])
    _ON_LOAD.append((_open, [state, bstate], open_out))

    src_chapter.change(lambda b, c: _after(browse.jump_chapter(b, "src", c)),
                       [bstate, src_chapter], nav_out)
    tgt_chapter.change(lambda b, c: _after(browse.jump_chapter(b, "tgt", c)),
                       [bstate, tgt_chapter], nav_out)
    src_page.submit(lambda b, v: _after(browse.goto(b, "src", v)),
                    [bstate, src_page], nav_out)
    tgt_page.submit(lambda b, v: _after(browse.goto(b, "tgt", v)),
                    [bstate, tgt_page], nav_out)

    src_prev.click(lambda b: _after(browse.step(b, "src", -1)), [bstate], nav_out)
    src_next.click(lambda b: _after(browse.step(b, "src", 1)), [bstate], nav_out)
    tgt_prev.click(lambda b: _after(browse.step(b, "tgt", -1)), [bstate], nav_out)
    tgt_next.click(lambda b: _after(browse.step(b, "tgt", 1)), [bstate], nav_out)
    both_prev.click(lambda b: _after(browse.step_both(b, -1)), [bstate], nav_out)
    both_next.click(lambda b: _after(browse.step_both(b, 1)), [bstate], nav_out)

    def _link(st, bs):
        bs, message = browse.link_pages(st, bs)
        return (*_after(bs), message)

    link_btn.click(_link, [state, bstate], nav_out + [saved])
    unlink_btn.click(lambda b: _after(browse.unlink_pages(b)), [bstate], nav_out)

    def _set_noise(bs, hide):
        bs = browse.ensure(bs)
        bs["hide_noise"] = bool(hide)
        return _after(bs)

    hide_noise.change(_set_noise, [bstate, hide_noise], nav_out)

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

    # Gradio selects the first choice of a Dropdown by default, but selecting
    # it does not fire `change`. Without this the workspace opens showing a
    # board with an empty Class list beside it, and the only way forward is to
    # pick a different board and pick back. Running the cascade once on load
    # makes the first paint consistent with what is selected.
    _ON_LOAD.append((ws.on_board, [board],
                     [klass, subject, src_lang, tgt_lang, src_book, tgt_book]))

    return {"bstate": bstate, "nav_out": nav_out, "after": _after,
            "saved": saved}


def _block(state: gr.State, bs: dict, b: dict, side: str,
           is_editing: bool, saved: gr.Markdown) -> None:
    """One block of text, as the annotator meets it.

    In reading mode it is a paragraph with a grey line above it saying what
    kind of thing it is, which page it is on, and how it stands. In correcting
    mode the paragraph becomes a box.

    The box is a *view*. The record is ``setu_text``, and the save carries the
    revision the box was showing — POTATO's ``text_edit`` widget learned that
    keeping the editor and the record as one thing loses edits, and this keeps
    them apart.
    """
    rid = b.get("rid") or ""
    if not is_editing or not rid:
        gr.HTML(browse.read_only_html(b))
        if not rid:
            return
    else:
        gr.Markdown(browse.block_heading(b),
                    elem_classes=["setu-b-meta"])
        # interactive=True is not optional here. A component built inside
        # gr.render is not inferred to be an input, so without it every
        # correcting box renders disabled and the annotator cannot type.
        box = gr.Textbox(value=b.get("current") or "", show_label=False,
                         lines=2, max_lines=16, autoscroll=False,
                         interactive=True, elem_classes=["setu-b-edit"])
        rev = gr.State(b.get("rev") or 0)
        rid_s = gr.State(rid)
        side_s = gr.State(side)
        # Saving on blur catches the common case the instant the annotator
        # looks away, which is what makes "everything is saved as you go"
        # true rather than aspirational.
        box.blur(browse.save_text, [state, rid_s, side_s, box, rev], [saved])

        if b.get("edited"):
            undo = gr.Button("Put back what the parser read", size="sm",
                             elem_classes=["setu-secondary"])
            undo.click(browse.restore_original, [state, rid_s, side_s], [saved])

    # The judgement belongs to the pair, and the English side is the reference,
    # so it is asked once, on the left, rather than twice in two places that
    # could disagree on screen.
    if side == "src" and rid:
        rid_a = gr.State(rid)
        answer = gr.Dropdown(choices=browse.ANSWERS,
                             value=b.get("status") or "pending",
                             label="Do these two say the same thing?",
                             interactive=True, elem_classes=["setu-answer"])
        answer.change(browse.set_answer, [state, rid_a, answer], [saved])


def _review_tab(state: gr.State, shop: dict) -> None:
    gr.Markdown("Everything in the open workspace. Click a row to go to that "
                "page in **Annotate**.")
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

    # Clicking a row moves the workspace to the page that row sits on, rather
    # than opening a separate editor: there is only one place to work now.
    table.select(panels.goto_from_review, [state, shop["bstate"], table],
                 [shop["bstate"]]) \
         .then(shop["after"], [shop["bstate"]], shop["nav_out"])


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
