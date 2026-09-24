"""Two textbooks, browsed independently, side by side.

Why this exists
---------------
Setu's workspace judges one aligned *pair* at a time, and the reading view that
preceded this one drew those same pairs as two long columns. Both assume the
two editions march together. Measured against this corpus, they do not:

    Karnataka   class 10  Kannada   chapter page offsets  -3, 0, +3, +6, +7, +8
    Punjab      class 10  Punjabi                          0, +10, +23, +26
    Gujarat     class 10  Gujarati                      -114, -112, -111, -107
    NCERT       class 11  Hindi      no chapter matched by page at all
    Tamil Nadu  class 10  Tamil      no chapter matched by page at all

and the chapter counts differ outright — Karnataka 13 against 16, Punjab 43
against 48, Gujarat 27 against 20, Kerala 11 against 8. An interface built on
"row *n* on the left is row *n* on the right" cannot express any of that, so an
annotator who noticed that English page 4 answers Gujarati page 2 had nowhere
to go with the observation.

So this module does not use pairs at all. It reads the two books straight out
of ``setu_segment`` — each with its own chapter list, its own page number, its
own scrollbar — and lets the annotator drive them apart, then back together.
The pair rows are consulted only to colour a block by how it has been judged
and to show the edited text where there is one, never to decide what is shown
opposite what.

Where the ideas come from
-------------------------
*POTATO* (davidjurgens/potato) puts a position box, ``done/total`` and
jump-to-next-unjudged in a fixed bar, so the annotator always knows where they
are; its ``show_outline`` builds a table of contents out of heading spans.
Both are here, per side.

*PAWLS* (allenai/pawls) is instructive by omission: it has no way to move
around inside a document, which is survivable for a two-page paper and not for
a 250-page textbook. Its per-document ``finished``/``junk`` status is the idea
behind the status tally in each side's bar.

*CMULAB* (neulab/cmulab) marks every span ``correct | incorrect | generated |
unknown`` rather than done/not-done, and its OCR post-corrector takes the
parallel text as a second source. Setu's seven statuses are the same instinct;
they are shown on the block here so a page's state is visible at a glance.

*DocLayNet* (DS4SD/DocLayNet) labels layout with eleven classes and — the part
that matters — carries no reading order, which is exactly why the page, not the
block index, is the unit an annotator can trust across two editions. Setu's own
23 ``KINDS`` are shown on each block in that spirit.

Safety
------
Read-only throughout, over ``setu_segment``, ``setu_row`` and ``setu_text``.
The one thing written is the remembered page-link, and it goes into
``setu_meta`` — a key/value table Setu already owns — under a key derived from
the project id. Tulana's own eight tables are never touched, no user text ever
reaches a filesystem path, and every number arriving from the browser is
clamped to the book's real page range before it reaches SQL.
"""
from __future__ import annotations

import html
import json
import logging
from typing import Any

from ..core import corpus, store, workspace
from ..core.models import KIND_BY_KEY, STATUS_BY_KEY
from . import session

log = logging.getLogger("annotation.ui.browse")

#: Blocks drawn for one page. A textbook page runs to perhaps forty; the cap is
#: a guard against a parse that produced thousands, not a working limit.
PAGE_BLOCKS = 400

#: Blocks drawn when a whole chapter is shown at once.
CHAPTER_BLOCKS = 1200

#: Structural furniture. Hidden by default in the browser for the same reason
#: it is excluded from pairs: running heads and page numbers are not the text.
NOISE_KINDS = ("header", "footer", "page_number", "figure")


def blank() -> dict:
    """Fresh per-session browser state. Copied, never shared."""
    return {"pid": "", "src_book": "", "tgt_book": "",
            "src_page": 0, "tgt_page": 0,
            "src_chapter": "", "tgt_chapter": "",
            "src_lo": 0, "src_hi": 0, "tgt_lo": 0, "tgt_hi": 0,
            "whole_chapter": False, "hide_noise": True,
            "linked": False, "offset": 0}


def ensure(bs: Any) -> dict:
    """Repair whatever Gradio handed back into a usable browser state."""
    out = blank()
    if isinstance(bs, dict):
        for key, value in bs.items():
            if key in out:
                out[key] = value
    for key in ("src_page", "tgt_page", "src_lo", "src_hi", "tgt_lo", "tgt_hi",
                "offset"):
        out[key] = _int(out[key], 0)
    for key in ("whole_chapter", "hide_noise", "linked"):
        out[key] = bool(out[key])
    return out


def _int(value: Any, default: int = 0) -> int:
    """Whatever the browser sent, as an int — or the default, never an error.

    ``gr.Number`` sends a float even with ``precision=0``, so "page 3" arrives
    as ``3.0`` and ``int("3.0")`` raises. It also sends ``None`` for an empty
    box. Both go through here, as does anything else a hand-crafted request
    might carry, because this value ends up in a SQL parameter.
    """
    if isinstance(value, bool):                  # bool is an int; not a page
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return default if value != value or value in (float("inf"), float("-inf")) \
            else int(value)
    try:
        text = str(value).strip()
    except Exception:                            # pragma: no cover - exotic repr
        return default
    if not text:
        return default
    try:
        return int(text)
    except ValueError:
        pass
    try:
        number = float(text)
    except (TypeError, ValueError):
        return default
    if number != number or number in (float("inf"), float("-inf")):
        return default
    return int(number)


def _clamp(page: int, lo: int, hi: int) -> int:
    if hi < lo:
        return lo
    return max(lo, min(hi, page))


# ── reading one side out of the corpus ─────────────────────────────────────

def _page_range(con, book_key: str) -> tuple[int, int]:
    """The first and last page that actually carry text.

    ``setu_book.num_pages`` is the PDF's page count, which for several books in
    this corpus is larger than the range the parser produced segments for.
    Stepping to a page with nothing on it looks like a bug, so the bounds come
    from the segments themselves.
    """
    row = store.Repository(con).one(
        "SELECT MIN(page) AS lo, MAX(page) AS hi FROM setu_segment"
        "  WHERE book_key = ? AND page IS NOT NULL", (book_key,))
    lo = _int(row["lo"] if row else 0, 0) or 1
    hi = _int(row["hi"] if row else 0, 0) or lo
    return lo, hi


def blocks(con, *, pid: str, book_key: str, side: str, page: Any = None,
           chapter_no: str = "", hide_noise: bool = True,
           limit: int = PAGE_BLOCKS) -> list[dict]:
    """Every block of one book on one page (or in one chapter), in order.

    The join onto ``setu_row``/``setu_text`` is a left join on purpose: a
    segment that the aligner never managed to pair still has to be visible,
    because finding those is most of what this view is for.
    """
    if side not in ("src", "tgt"):
        raise ValueError("side must be 'src' or 'tgt'")
    col = "src_sid" if side == "src" else "tgt_sid"

    sql = [
        "SELECT s.sid, s.seq, s.page, s.kind, s.label,"
        "       s.chapter_no, s.chapter, s.section_no, s.section,"
        "       s.source_text, s.has_math, s.has_table,"
        "       r.rid, r.seq AS row_seq, r.status, r.edited,"
        "       t.text AS edited_text"
        "  FROM setu_segment s"
        f"  LEFT JOIN setu_row  r ON r.{col} = s.sid AND r.pid = ?"
        "  LEFT JOIN setu_text t ON t.rid = r.rid AND t.side = ?"
        " WHERE s.book_key = ?"]
    args: list[Any] = [pid, side, book_key]

    if chapter_no:
        sql.append(" AND s.chapter_no = ?")
        args.append(chapter_no)
    if page is not None:
        sql.append(" AND s.page = ?")
        args.append(int(page))
    if hide_noise:
        sql.append(f" AND s.kind NOT IN ({','.join('?' * len(NOISE_KINDS))})")
        args.extend(NOISE_KINDS)

    sql.append(" ORDER BY s.seq LIMIT ?")
    args.append(max(1, min(int(limit), CHAPTER_BLOCKS)))
    return [dict(r) for r in store.Repository(con).all("".join(sql), args)]


def chapter_choices(con, book_key: str) -> list[tuple[str, str]]:
    """Dropdown choices for one book's chapters, in the book's own order.

    Built from ``CorpusRepo.outline``, so the label carries the chapter's first
    page — which is the number the annotator is about to type into the other
    side's page box when the two editions disagree.
    """
    out: list[tuple[str, str]] = [("Whole book", "")]
    try:
        chapters = corpus.CorpusRepo(con).outline(book_key)
    except Exception:                                # pragma: no cover
        log.exception("outline failed for %s", book_key)
        return out
    for ch in chapters:
        number = (ch.get("chapter_no") or "").strip()
        title = " ".join((ch.get("chapter") or "").split())[:70]
        # The parser usually leaves the number at the front of the title too,
        # so joining them blindly gives "3 3 Arithmetic Progression".
        if number and title.startswith(number):
            label = title
        else:
            label = f"{number} {title}".strip()
        first = ch.get("first_page")
        label = label or "Front matter"
        if first:
            label += f"  ·  from p{first}"
        out.append((label, number or title))
    return out


def _chapter_page(con, book_key: str, chapter_no: str) -> int:
    """The first page of a chapter, matched by number or by title."""
    if not chapter_no:
        return 0
    row = store.Repository(con).one(
        "SELECT MIN(page) AS p FROM setu_segment"
        "  WHERE book_key = ? AND (chapter_no = ? OR chapter = ?)"
        "    AND page IS NOT NULL", (book_key, chapter_no, chapter_no))
    return _int(row["p"] if row else 0, 0)


# ── drawing one side ───────────────────────────────────────────────────────

def _block_html(b: dict) -> str:
    """One block of text, with where it sits and how it has been judged."""
    text = b.get("edited_text")
    if text is None:
        text = b.get("source_text") or ""
    body = html.escape(text).replace("\n", "<br>")
    if not text.strip():
        body = '<span class="setu-b-empty">(no text in this block)</span>'

    kind = KIND_BY_KEY.get(b.get("kind") or "")
    bits = []
    if kind:
        bits.append(f'<span class="setu-b-kind">{html.escape(kind.icon)} '
                    f'{html.escape(kind.label)}</span>')
    if b.get("page"):
        bits.append(f'p{int(b["page"])}')

    if b.get("rid"):
        key = b.get("status") or "pending"
        # "Not checked yet" on every block of every page is noise that hides
        # the two or three that *have* been judged. Absence means pending; the
        # tally above the column says how many that is.
        if key != "pending":
            status = STATUS_BY_KEY.get(key)
            bits.append(f'<span class="setu-b-status setu-st-{html.escape(key)}">'
                        f'{html.escape(status.label if status else key)}</span>')
        if b.get("edited"):
            bits.append('<span class="setu-b-edited">edited</span>')
        bits.append(f'<span class="setu-b-pair">pair #{int(b["row_seq"])}</span>')
    else:
        # Not in any pair: the aligner found nothing opposite it. This is the
        # 26% the old view could not show at all.
        bits.append('<span class="setu-b-unpaired">not paired</span>')

    classes = "setu-b"
    if not b.get("rid"):
        classes += " setu-b-lonely"
    return (f'<div class="{classes}" data-sid="{html.escape(str(b["sid"]))}"'
            f' data-seq="{int(b["seq"])}"'
            f' data-rid="{html.escape(str(b.get("rid") or ""))}">'
            f'<div class="setu-b-meta">{" · ".join(bits)}</div>'
            f'<div class="setu-b-text">{body}</div></div>')


def _side_html(rows: list[dict], *, side: str, title: str, language: str,
               page: int, lo: int, hi: int, whole_chapter: bool,
               empty_hint: str) -> str:
    """One scrolling column: a heading strip, then the blocks.

    The scroll container is a div written here rather than the Gradio
    component's own wrapper. When the wrapper carried the scrolling, whether it
    actually scrolled depended on which of Gradio's rules won on specificity —
    and on one side it lost, which is the "English side does not scroll" bug.
    A container in Setu's own markup cannot lose that argument.
    """
    if not rows:
        inner = f'<div class="setu-doc-empty">{html.escape(empty_hint)}</div>'
    else:
        parts: list[str] = []
        seen_page: int | None = None
        for b in rows:
            p = b.get("page")
            if whole_chapter and p and p != seen_page:
                seen_page = p
                parts.append(f'<div class="setu-pagemark" data-page="{int(p)}">'
                             f'page {int(p)}</div>')
            parts.append(_block_html(b))
        inner = "\n".join(parts)

    where = (f"whole chapter · pages {lo}–{hi}" if whole_chapter
             else f"page {page} · this edition runs {lo}–{hi}")
    heading = (f'<div class="setu-doc-head">'
               f'<span class="setu-doc-lang">{html.escape(language or "—")}</span>'
               f'<span class="setu-doc-title">{html.escape(title or "")}</span>'
               f'<span class="setu-doc-where">{html.escape(where)}</span>'
               f'</div>')
    return (f'<div class="setu-doc setu-doc-{html.escape(side)}">{heading}'
            f'<div class="setu-doc-scroll" id="setu_scroll_{html.escape(side)}"'
            f' tabindex="0">{inner}</div></div>')


def _tally(rows: list[dict]) -> str:
    """POTATO's done/total, per page rather than per document."""
    total = len(rows)
    if not total:
        return "nothing here"
    paired = sum(1 for b in rows if b.get("rid"))
    done = sum(1 for b in rows
               if b.get("rid") and (b.get("status") or "pending") != "pending")
    out = f"{total} block{'' if total == 1 else 's'}"
    if paired < total:
        out += f" · {total - paired} not paired"
    if paired:
        out += f" · {done}/{paired} judged"
    return out


# ── the remembered page-link ───────────────────────────────────────────────
#
# When an annotator works out that English p4 answers Gujarati p2, that is a
# finding about the two editions, not about their afternoon. It is kept in
# setu_meta, which Setu already owns, under a key built from the project id —
# so the key can never be influenced by anything typed into the interface.

def _link_key(pid: str) -> str:
    return f"browse.link:{pid}"


def load_link(con, pid: str) -> dict:
    if not pid:
        return {}
    row = store.Repository(con).one(
        "SELECT value FROM setu_meta WHERE key = ?", (_link_key(pid),))
    if not row:
        return {}
    try:
        data = json.loads(row["value"])
    except (ValueError, TypeError):
        return {}
    return data if isinstance(data, dict) else {}


def save_link(con, pid: str, *, offset: int, src_page: int, tgt_page: int,
              actor: str = "") -> None:
    if not pid:
        return
    value = json.dumps({"offset": int(offset), "src_page": int(src_page),
                        "tgt_page": int(tgt_page), "by": (actor or "")[:80]})
    con.execute("INSERT INTO setu_meta(key, value) VALUES(?, ?)"
                " ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (_link_key(pid), value))


def clear_link(con, pid: str) -> None:
    if pid:
        con.execute("DELETE FROM setu_meta WHERE key = ?", (_link_key(pid),))


# ── the one function every control goes through ────────────────────────────

EMPTY = ('<div class="setu-doc"><div class="setu-doc-scroll">'
          '<div class="setu-doc-empty">Open two textbooks in the Annotate tab '
          'first.</div></div></div>')


def _render(bs: dict, *, note: str = "") -> tuple:
    """Draw both sides from the browser state. Every handler ends here."""
    import gradio as gr

    if not bs.get("pid"):
        return (bs, EMPTY, EMPTY, gr.update(), gr.update(), "", "",
                note or "Open two textbooks in the Annotate tab first.")

    try:
        with store.ro() as con:
            proj = workspace.WorkspaceRepo(con).project(bs["pid"])
            out: dict[str, Any] = {}
            for side, book, page, chapter in (
                    ("src", bs["src_book"], bs["src_page"], bs["src_chapter"]),
                    ("tgt", bs["tgt_book"], bs["tgt_page"], bs["tgt_chapter"])):
                whole = bs["whole_chapter"] and bool(chapter)
                rows = blocks(con, pid=bs["pid"], book_key=book, side=side,
                              page=None if whole else page,
                              chapter_no=chapter if whole else "",
                              hide_noise=bs["hide_noise"],
                              limit=CHAPTER_BLOCKS if whole else PAGE_BLOCKS)
                out[side] = rows
    except Exception:
        log.exception("browse render failed")
        return (bs, EMPTY, EMPTY, gr.update(), gr.update(), "", "",
                "The text could not be loaded. Your annotations are unaffected.")

    panes = {}
    for side, key in (("src", "src"), ("tgt", "tgt")):
        rows = out[side]
        whole = bs["whole_chapter"] and bool(bs[f"{side}_chapter"])
        # In whole-chapter mode the strip should report the chapter's own page
        # span, not the book's, or it reads as though nothing moved.
        pages = [int(b["page"]) for b in rows if b.get("page")]
        lo = min(pages) if (whole and pages) else bs[f"{side}_lo"]
        hi = max(pages) if (whole and pages) else bs[f"{side}_hi"]
        panes[key] = _side_html(
            rows, side=side, title=proj.get(f"{side}_title") or "",
            language=proj.get(f"{side}_language") or proj.get(f"{side}_lang") or "",
            page=bs[f"{side}_page"], lo=lo, hi=hi, whole_chapter=whole,
            empty_hint=(f"Nothing in this chapter on this side."
                        if whole else
                        f"Page {bs[f'{side}_page']} has no text in this edition — "
                        f"it may be a full-page illustration. Step to the next page."))
    left, right = panes["src"], panes["tgt"]

    if not note:
        note = _offset_note(bs)
    return (bs, left, right,
            gr.update(value=bs["src_page"], minimum=bs["src_lo"], maximum=bs["src_hi"]),
            gr.update(value=bs["tgt_page"], minimum=bs["tgt_lo"], maximum=bs["tgt_hi"]),
            _tally(out["src"]), _tally(out["tgt"]), note)


def _offset_note(bs: dict) -> str:
    live = bs["src_page"] - bs["tgt_page"]
    if bs["linked"]:
        held = bs["offset"]
        word = ("ahead of" if held > 0 else "behind" if held < 0 else "level with")
        state = (f"**Linked.** English is {abs(held)} page"
                 f"{'' if abs(held) == 1 else 's'} {word} the other edition, and "
                 f"both sides move together." if held
                 else "**Linked.** The two editions are level, and both sides "
                      "move together.")
        if live != held:
            state += (f" You have since moved them {live - held:+d} apart — "
                      f"press *Link these two pages* again to keep the new "
                      f"offset.")
        return state
    if live:
        return (f"Not linked. English p{bs['src_page']} is sitting beside "
                f"p{bs['tgt_page']} — an offset of {live:+d}. If those two pages "
                f"do answer each other, press **Link these two pages** and both "
                f"sides will move together from now on.")
    return ("Not linked. Move each side on its own, or press **Link these two "
            "pages** once you find two pages that answer each other.")


# ── handlers ───────────────────────────────────────────────────────────────

def open_books(state: Any, bs: Any):
    """Called when the tab is opened or refreshed: load both books afresh."""
    import gradio as gr

    st = session.ensure(state)
    bs = ensure(bs)
    if not session.has_project(st):
        fresh = blank()
        return (fresh, EMPTY, EMPTY, gr.update(), gr.update(), "", "",
                "Open two textbooks in the Annotate tab first, then come back.",
                gr.update(choices=[("Whole book", "")], value=""),
                gr.update(choices=[("Whole book", "")], value=""))

    try:
        with store.ro() as con:
            proj = workspace.WorkspaceRepo(con).project(st["pid"])
            src_book, tgt_book = proj["src_book"], proj["tgt_book"]
            src_lo, src_hi = _page_range(con, src_book)
            tgt_lo, tgt_hi = _page_range(con, tgt_book)
            src_choices = chapter_choices(con, src_book)
            tgt_choices = chapter_choices(con, tgt_book)
            remembered = load_link(con, st["pid"])
    except Exception:
        log.exception("browse open failed")
        fresh = blank()
        return (fresh, EMPTY, EMPTY, gr.update(), gr.update(), "", "",
                "Those textbooks could not be opened.",
                gr.update(), gr.update())

    changed = bs.get("pid") != st["pid"]
    new = ensure(bs) if not changed else blank()
    new.update({"pid": st["pid"], "src_book": src_book, "tgt_book": tgt_book,
                "src_lo": src_lo, "src_hi": src_hi,
                "tgt_lo": tgt_lo, "tgt_hi": tgt_hi})

    if changed or not new["src_page"]:
        # Reopen where the link was left, so a finding survives the session.
        new["src_page"] = _clamp(_int(remembered.get("src_page"), src_lo) or src_lo,
                                 src_lo, src_hi)
        new["tgt_page"] = _clamp(_int(remembered.get("tgt_page"), tgt_lo) or tgt_lo,
                                 tgt_lo, tgt_hi)
        if "offset" in remembered:
            new["offset"] = _int(remembered.get("offset"), 0)
            new["linked"] = True
    else:
        new["src_page"] = _clamp(new["src_page"], src_lo, src_hi)
        new["tgt_page"] = _clamp(new["tgt_page"], tgt_lo, tgt_hi)

    result = _render(new)
    return result + (gr.update(choices=src_choices, value=new["src_chapter"]),
                     gr.update(choices=tgt_choices, value=new["tgt_chapter"]))


def goto(state: Any, bs: Any, side: str, page: Any):
    """A page number typed into one side's box."""
    bs = ensure(bs)
    if not bs.get("pid"):
        return _render(bs)
    lo, hi = bs[f"{side}_lo"], bs[f"{side}_hi"]
    want = _clamp(_int(page, bs[f"{side}_page"]), lo, hi)
    if want == bs[f"{side}_page"]:
        return _render(bs)
    bs[f"{side}_page"] = want
    if bs["linked"]:
        bs = _follow(bs, side)
    return _render(bs)


def step(state: Any, bs: Any, side: str, delta: int):
    """One page forward or back on one side."""
    bs = ensure(bs)
    if not bs.get("pid"):
        return _render(bs)
    lo, hi = bs[f"{side}_lo"], bs[f"{side}_hi"]
    before = bs[f"{side}_page"]
    bs[f"{side}_page"] = _clamp(before + int(delta), lo, hi)
    if bs[f"{side}_page"] == before:
        edge = "first" if delta < 0 else "last"
        return _render(bs, note=f"That is already the {edge} page of this edition.")
    if bs["linked"]:
        bs = _follow(bs, side)
    return _render(bs)


def step_both(state: Any, bs: Any, delta: int):
    """Both sides at once, keeping whatever gap they are sitting at.

    This is the "common next button": the annotator has already positioned the
    two sides against each other, and from here the pair of pages advances as
    one, whether or not the offset was formally linked.
    """
    bs = ensure(bs)
    if not bs.get("pid"):
        return _render(bs)
    moved = False
    for side in ("src", "tgt"):
        lo, hi = bs[f"{side}_lo"], bs[f"{side}_hi"]
        before = bs[f"{side}_page"]
        bs[f"{side}_page"] = _clamp(before + int(delta), lo, hi)
        moved = moved or bs[f"{side}_page"] != before
    if not moved:
        edge = "first" if delta < 0 else "last"
        return _render(bs, note=f"Both editions are already at their {edge} page.")
    return _render(bs)


def _follow(bs: dict, moved: str) -> dict:
    """Move the other side to preserve the linked offset."""
    other = "tgt" if moved == "src" else "src"
    if moved == "src":
        want = bs["src_page"] - bs["offset"]
    else:
        want = bs["tgt_page"] + bs["offset"]
    bs[f"{other}_page"] = _clamp(want, bs[f"{other}_lo"], bs[f"{other}_hi"])
    return bs


def jump_chapter(state: Any, bs: Any, side: str, chapter_no: str):
    """A chapter chosen on one side — independently of the other.

    This is the freedom the specification asked for: which chapter to work on
    is a decision taken once per side, because the two editions do not agree on
    how many chapters there are, let alone where they start.
    """
    bs = ensure(bs)
    if not bs.get("pid"):
        return _render(bs)
    bs[f"{side}_chapter"] = chapter_no or ""
    if chapter_no:
        try:
            with store.ro() as con:
                first = _chapter_page(con, bs[f"{side}_book"], chapter_no)
        except Exception:
            log.exception("chapter jump failed")
            first = 0
        if first:
            bs[f"{side}_page"] = _clamp(first, bs[f"{side}_lo"], bs[f"{side}_hi"])
            if bs["linked"]:
                bs = _follow(bs, side)
    return _render(bs)


def set_whole_chapter(state: Any, bs: Any, whole: Any):
    bs = ensure(bs)
    bs["whole_chapter"] = bool(whole)
    if bs["whole_chapter"] and not (bs["src_chapter"] or bs["tgt_chapter"]):
        return _render(bs, note="Choose a chapter on a side first — then that "
                                "side shows the whole chapter at once.")
    return _render(bs)


def set_hide_noise(state: Any, bs: Any, hide: Any):
    bs = ensure(bs)
    bs["hide_noise"] = bool(hide)
    return _render(bs)


def link_pages(state: Any, bs: Any):
    """Record that the two pages now on screen answer each other."""
    st = session.ensure(state)
    bs = ensure(bs)
    if not bs.get("pid"):
        return _render(bs)
    bs["offset"] = bs["src_page"] - bs["tgt_page"]
    bs["linked"] = True
    try:
        with store.tx() as con:
            save_link(con, bs["pid"], offset=bs["offset"],
                      src_page=bs["src_page"], tgt_page=bs["tgt_page"],
                      actor=st.get("annotator") or "")
    except Exception:
        log.exception("could not save the page link")
        return _render(bs, note=_offset_note(bs) +
                       "  *(Kept for this session only — it could not be saved.)*")
    return _render(bs, note=_offset_note(bs) + "  Saved for everyone on this "
                            "workspace.")


def unlink_pages(state: Any, bs: Any):
    bs = ensure(bs)
    bs["linked"], bs["offset"] = False, 0
    try:
        with store.tx() as con:
            clear_link(con, bs["pid"])
    except Exception:
        log.exception("could not clear the page link")
    return _render(bs, note="Unlinked. Each side moves on its own again.")
