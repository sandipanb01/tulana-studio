"""The annotator's workspace: two textbooks, block by block, side by side.

This is the whole of Setu's annotation surface. There is no separate "open a
pair and judge it" screen any more, because that screen asked the annotator to
hold two things in their head at once — where they were in the book, and which
pair they were judging — and the two disagreed constantly.

Here the page *is* the workspace. Each side shows the blocks the layout parser
found on the page you are looking at, in reading order, as text. Turn on
"Let me correct the text" and every block becomes editable in place. The answer
for a pair sits under the English block it belongs to. Nothing is opened and
nothing is closed.

Three facts about the data drive the whole design.

**Pages are stored counting from zero.** ``setu_segment.page`` comes straight
from the layout JSON, whose first page is 0, and PyMuPDF indexes the same way,
so the two agree and the crop renderer is correct. What was *not* correct was
showing that number to a person: an annotator reading "page 57" and turning to
page 57 of the printed book was looking one page too early, on all 121 books.
Every number this module shows goes through :func:`to_display`, and every
number it accepts comes back through :func:`from_display`. The conversion
happens nowhere else.

**Boxes are fractions of the page.** ``fx0..fy1`` give a block's position as a
fraction of the parser's raster, so they survive any DPI and any rescale —
which is what lets the printed page be rendered at one resolution and a crop at
another without either knowing about the other. This is Tulana's own rule, kept.

**The two editions do not march together.** Chapter-start offsets between an
English edition and its counterpart run from 0 to 114 pages across this corpus,
and two board pairs share no chapter page at all. So each side carries its own
chapter list, its own page and its own scrollbar, and the two are joined only
when an annotator says they are joined.

What came from where
--------------------
*Tulana's own Blocks tab* is the parent of this design: progressive disclosure,
one primary button per state, plain words, blocks positioned as fractions, a
dashed blank page of the right proportions when the PDF is absent, and autosave
that says so in words rather than going quiet.

*POTATO* (davidjurgens/potato): the ``done/total`` counter, the go-to-page box,
and the ``text_edit`` lesson — the visible editor is never the record. Here the
textarea is a view; ``setu_text`` is the record, and a save carries the
revision it was based on.

*PAWLS* (allenai/pawls): a comment saves on blur rather than on every keystroke.

*CMULAB* (neulab/cmulab): every annotation says whether it was *generated* by a
model or confirmed by a person. A block nobody has touched is labelled as the
parser's reading, not as a fact.

*DocLayNet* (DS4SD/DocLayNet): this corpus was parsed by a DocLayNet-trained
model and its classes arrive in ``setu_segment.kind``. They are shown on every
block, because "this one is a caption" is often the whole explanation for why
two sides look different.
"""
from __future__ import annotations

import html
import json
import logging
from typing import Any

from ..core import corpus, store, workspace
from ..core.models import KIND_BY_KEY, STATUS_BY_KEY, STATUSES
from ..core.store import Conflict, Invalid, NotFound
from . import session

log = logging.getLogger("annotation.ui.browse")

#: Blocks drawn for one page. A textbook page runs to perhaps forty; the cap
#: guards against a parse that produced thousands, not against normal use.
PAGE_BLOCKS = 120

#: Structural furniture, hidden by default: running heads and page numbers are
#: not the text, and an annotator asked to check them wastes their afternoon.
NOISE_KINDS = ("header", "footer", "page_number", "figure")


# ── the one conversion ─────────────────────────────────────────────────────
#
# Storage counts pages from zero. People count from one. Everything shown goes
# through to_display; everything accepted comes back through from_display.
# Nowhere else in this file is a page number adjusted.

def to_display(page: Any) -> int:
    """Stored page number → the number printed on the page."""
    return _int(page, 0) + 1


def from_display(page: Any, default_stored: int = 0) -> int:
    """What a person typed → the stored page number."""
    return _int(page, default_stored + 1) - 1


def blank() -> dict:
    """Fresh per-session state. Copied, never shared."""
    return {"pid": "", "src_book": "", "tgt_book": "",
            "src_page": 0, "tgt_page": 0,
            "src_chapter": "", "tgt_chapter": "",
            "src_lo": 0, "src_hi": 0, "tgt_lo": 0, "tgt_hi": 0,
            "editing": False, "show_page": False, "hide_noise": True,
            "linked": False, "offset": 0,
            "src_title": "", "tgt_title": "",
            "src_lang": "", "tgt_lang": ""}


def ensure(bs: Any) -> dict:
    out = blank()
    if isinstance(bs, dict):
        for key, value in bs.items():
            if key in out:
                out[key] = value
    for key in ("src_page", "tgt_page", "src_lo", "src_hi",
                "tgt_lo", "tgt_hi", "offset"):
        out[key] = _int(out[key], 0)
    for key in ("editing", "show_page", "hide_noise", "linked"):
        out[key] = bool(out[key])
    return out


def _int(value: Any, default: int = 0) -> int:
    """Whatever the browser sent, as an int — or the default, never an error.

    ``gr.Number`` sends a float even with ``precision=0``, so "page 3" arrives
    as ``3.0`` and ``int("3.0")`` raises. It sends ``None`` for an empty box.
    Both land here, because this value reaches a SQL parameter.
    """
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return default if value != value or value in (
            float("inf"), float("-inf")) else int(value)
    try:
        text = str(value).strip()
    except Exception:                            # pragma: no cover
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
    return lo if hi < lo else max(lo, min(hi, page))


# ── reading one side ───────────────────────────────────────────────────────

def page_range(con, book_key: str) -> tuple[int, int]:
    """First and last **stored** page that carries text.

    ``setu_book.num_pages`` is the PDF's page count, which for several books is
    larger than the range the parser produced segments for. Stepping onto a
    page with nothing on it looks like a fault, so the bounds come from the
    segments themselves.
    """
    row = store.Repository(con).one(
        "SELECT MIN(page) AS lo, MAX(page) AS hi FROM setu_segment"
        "  WHERE book_key = ? AND page IS NOT NULL", (book_key,))
    lo = _int(row["lo"] if row else 0, 0)
    hi = _int(row["hi"] if row else 0, 0)
    return lo, max(lo, hi)


def blocks(con, *, pid: str, book_key: str, side: str, page: Any = None,
           hide_noise: bool = True, limit: int = PAGE_BLOCKS) -> list[dict]:
    """Every block of one book on one page, in reading order.

    Left-joined onto the pair rows on purpose: a block the aligner never paired
    still has to be visible, because finding those is most of the job.
    """
    if side not in ("src", "tgt"):
        raise ValueError("side must be 'src' or 'tgt'")
    col = "src_sid" if side == "src" else "tgt_sid"

    sql = [
        "SELECT s.sid, s.seq, s.page, s.kind, s.label, s.source_text,"
        "       s.fx0, s.fy0, s.fx1, s.fy1, s.has_math, s.has_table,"
        "       s.chapter_no, s.chapter,"
        "       r.rid, r.seq AS row_seq, r.status, r.note, r.edited,"
        "       t.text AS edited_text, t.rev AS rev"
        "  FROM setu_segment s"
        f"  LEFT JOIN setu_row  r ON r.{col} = s.sid AND r.pid = ?"
        "  LEFT JOIN setu_text t ON t.rid = r.rid AND t.side = ?"
        " WHERE s.book_key = ?"]
    args: list[Any] = [pid, side, book_key]
    if page is not None:
        sql.append(" AND s.page = ?")
        args.append(int(page))
    if hide_noise:
        sql.append(f" AND s.kind NOT IN ({','.join('?' * len(NOISE_KINDS))})")
        args.extend(NOISE_KINDS)
    sql.append(" ORDER BY s.seq LIMIT ?")
    args.append(max(1, min(int(limit), PAGE_BLOCKS)))

    out = []
    for r in store.Repository(con).all("".join(sql), args):
        b = dict(r)
        b["display_page"] = to_display(b["page"])
        b["current"] = b["edited_text"] if b["edited_text"] is not None \
            else (b["source_text"] or "")
        b["rev"] = _int(b["rev"], 0)
        out.append(b)
    return out


def chapter_choices(con, book_key: str) -> list[tuple[str, str]]:
    """One book's chapters, in the book's own order and its own language.

    The label carries the chapter's first page — as printed, not as stored —
    because that is the number the annotator is about to type into the other
    side's box when the two editions disagree.
    """
    out: list[tuple[str, str]] = [("Whole book", "")]
    try:
        chapters = corpus.CorpusRepo(con).outline(book_key)
    except Exception:                            # pragma: no cover
        log.exception("outline failed for %s", book_key)
        return out
    for ch in chapters:
        number = (ch.get("chapter_no") or "").strip()
        title = " ".join((ch.get("chapter") or "").split())[:70]
        # The parser usually leaves the number at the front of the title too,
        # so joining them blindly gives "3 3 Arithmetic Progression".
        label = title if (number and title.startswith(number)) \
            else f"{number} {title}".strip()
        label = label or "Front matter"
        first = ch.get("first_page")
        if first is not None:
            label += f"  ·  from page {to_display(first)}"
        out.append((label, number or title))
    return out


def chapter_first_page(con, book_key: str, chapter_no: str):
    """The **stored** first page of a chapter, matched by number or title."""
    if not chapter_no:
        return None
    row = store.Repository(con).one(
        "SELECT MIN(page) AS p FROM setu_segment"
        "  WHERE book_key = ? AND (chapter_no = ? OR chapter = ?)"
        "    AND page IS NOT NULL", (book_key, chapter_no, chapter_no))
    if not row or row["p"] is None:
        return None
    return _int(row["p"], 0)


def tally(rows: list[dict]) -> str:
    """POTATO's done/total, for one page rather than one document."""
    total = len(rows)
    if not total:
        return "nothing on this page"
    paired = sum(1 for b in rows if b.get("rid"))
    done = sum(1 for b in rows
               if b.get("rid") and (b.get("status") or "pending") != "pending")
    out = f"{total} block{'' if total == 1 else 's'}"
    if paired < total:
        out += f" · {total - paired} with no counterpart"
    if paired:
        out += f" · {done} of {paired} checked"
    return out


# ── the remembered page link ───────────────────────────────────────────────
#
# When an annotator works out that English page 4 answers the other edition's
# page 2, that is a finding about the two books, not about their afternoon. It
# is kept in setu_meta — a key/value table Setu already owns — under a key
# built from the project id, so nothing typed into the interface can influence
# where it is written.

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
    con.execute(
        "INSERT INTO setu_meta(key, value) VALUES(?, ?)"
        " ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (_link_key(pid), json.dumps({"offset": int(offset),
                                     "src_page": int(src_page),
                                     "tgt_page": int(tgt_page),
                                     "by": (actor or "")[:80]})))


def clear_link(con, pid: str) -> None:
    if pid:
        con.execute("DELETE FROM setu_meta WHERE key = ?", (_link_key(pid),))


# ── loading a page of work ─────────────────────────────────────────────────

def load(bs: Any) -> dict:
    """Everything the screen needs for the two pages currently chosen.

    One call, one connection, both sides — so the two columns can never be
    drawn from two different moments.
    """
    bs = ensure(bs)
    out: dict[str, Any] = {"src": [], "tgt": [], "src_tally": "",
                           "tgt_tally": "", "error": ""}
    if not bs.get("pid"):
        return out
    try:
        with store.ro() as con:
            for side in ("src", "tgt"):
                rows = blocks(con, pid=bs["pid"], book_key=bs[f"{side}_book"],
                              side=side, page=bs[f"{side}_page"],
                              hide_noise=bs["hide_noise"])
                out[side] = rows
                out[f"{side}_tally"] = tally(rows)
    except Exception:
        log.exception("could not load the page")
        out["error"] = ("This page could not be loaded. Your saved work is "
                        "unaffected.")
    return out


def offset_note(bs: Any) -> str:
    """The sentence under the controls. Always says where the two sides sit."""
    bs = ensure(bs)
    if not bs.get("pid"):
        return ""
    live = bs["src_page"] - bs["tgt_page"]
    s, t = to_display(bs["src_page"]), to_display(bs["tgt_page"])
    if bs["linked"]:
        held = bs["offset"]
        if held == 0:
            body = ("**Linked.** The two editions are level, and both sides "
                    "move together.")
        else:
            word = "ahead of" if held > 0 else "behind"
            body = (f"**Linked.** The English edition runs {abs(held)} page"
                    f"{'' if abs(held) == 1 else 's'} {word} the other one, "
                    f"and both sides move together.")
        if live != held:
            body += (f" You have moved them {live - held:+d} further apart — "
                     f"press **These two pages match** again to keep the new "
                     f"distance.")
        return body
    if live:
        return (f"English page {s} is sitting beside page {t}. If those two "
                f"pages really do say the same thing, press **These two pages "
                f"match** and both sides will move together from now on.")
    return (f"Both sides are on page {s}. Move either one on its own, or press "
            f"**These two pages match** once you find two pages that say the "
            f"same thing.")


# ── handlers: choosing where to be ─────────────────────────────────────────

def open_books(state: Any, bs: Any) -> dict:
    """Load the two books of the open project. Returns the browser state."""
    st = session.ensure(state)
    bs = ensure(bs)
    if not session.has_project(st):
        return blank()

    try:
        with store.ro() as con:
            proj = workspace.WorkspaceRepo(con).project(st["pid"])
            src_book, tgt_book = proj["src_book"], proj["tgt_book"]
            src_lo, src_hi = page_range(con, src_book)
            tgt_lo, tgt_hi = page_range(con, tgt_book)
            remembered = load_link(con, st["pid"])
    except Exception:
        log.exception("could not open the two books")
        return blank()

    changed = bs.get("pid") != st["pid"]
    new = blank() if changed else ensure(bs)
    new.update({
        "pid": st["pid"], "src_book": src_book, "tgt_book": tgt_book,
        "src_lo": src_lo, "src_hi": src_hi,
        "tgt_lo": tgt_lo, "tgt_hi": tgt_hi,
        "src_title": proj.get("src_title") or proj.get("src_book_name") or "",
        "tgt_title": proj.get("tgt_title") or proj.get("tgt_book_name") or "",
        "src_lang": proj.get("src_language") or proj.get("src_lang") or "",
        "tgt_lang": proj.get("tgt_language") or proj.get("tgt_lang") or "",
    })
    if changed:
        # Reopen where the last annotator left the link, so a finding about
        # these two editions survives the session that produced it.
        new["src_page"] = _clamp(_int(remembered.get("src_page"), src_lo),
                                 src_lo, src_hi)
        new["tgt_page"] = _clamp(_int(remembered.get("tgt_page"), tgt_lo),
                                 tgt_lo, tgt_hi)
        if "offset" in remembered:
            new["offset"] = _int(remembered.get("offset"), 0)
            new["linked"] = True
    else:
        new["src_page"] = _clamp(new["src_page"], src_lo, src_hi)
        new["tgt_page"] = _clamp(new["tgt_page"], tgt_lo, tgt_hi)
    return new


def _follow(bs: dict, moved: str) -> dict:
    """Move the other side to preserve the linked distance."""
    other = "tgt" if moved == "src" else "src"
    want = (bs["src_page"] - bs["offset"]) if moved == "src" \
        else (bs["tgt_page"] + bs["offset"])
    bs[f"{other}_page"] = _clamp(want, bs[f"{other}_lo"], bs[f"{other}_hi"])
    return bs


def goto(bs: Any, side: str, shown_page: Any) -> dict:
    """A page number typed into one side's box. Arrives as printed, 1-based."""
    bs = ensure(bs)
    if not bs.get("pid"):
        return bs
    want = _clamp(from_display(shown_page, bs[f"{side}_page"]),
                  bs[f"{side}_lo"], bs[f"{side}_hi"])
    if want != bs[f"{side}_page"]:
        bs[f"{side}_page"] = want
        if bs["linked"]:
            bs = _follow(bs, side)
    return bs


def step(bs: Any, side: str, delta: int) -> dict:
    bs = ensure(bs)
    if not bs.get("pid"):
        return bs
    before = bs[f"{side}_page"]
    bs[f"{side}_page"] = _clamp(before + int(delta),
                                bs[f"{side}_lo"], bs[f"{side}_hi"])
    if bs[f"{side}_page"] != before and bs["linked"]:
        bs = _follow(bs, side)
    return bs


def step_both(bs: Any, delta: int) -> dict:
    """Both sides at once, keeping whatever distance they are sitting at."""
    bs = ensure(bs)
    if not bs.get("pid"):
        return bs
    for side in ("src", "tgt"):
        bs[f"{side}_page"] = _clamp(bs[f"{side}_page"] + int(delta),
                                    bs[f"{side}_lo"], bs[f"{side}_hi"])
    return bs


def jump_chapter(bs: Any, side: str, chapter_no: str) -> dict:
    """A chapter chosen on one side, independently of the other."""
    bs = ensure(bs)
    if not bs.get("pid"):
        return bs
    bs[f"{side}_chapter"] = chapter_no or ""
    if chapter_no:
        try:
            with store.ro() as con:
                first = chapter_first_page(con, bs[f"{side}_book"], chapter_no)
        except Exception:
            log.exception("chapter jump failed")
            first = None
        if first is not None:
            bs[f"{side}_page"] = _clamp(first, bs[f"{side}_lo"],
                                        bs[f"{side}_hi"])
            if bs["linked"]:
                bs = _follow(bs, side)
    return bs


def link_pages(state: Any, bs: Any):
    """Record that the two pages now on screen say the same thing."""
    st = session.ensure(state)
    bs = ensure(bs)
    if not bs.get("pid"):
        return bs, ""
    bs["offset"] = bs["src_page"] - bs["tgt_page"]
    bs["linked"] = True
    try:
        with store.tx() as con:
            save_link(con, bs["pid"], offset=bs["offset"],
                      src_page=bs["src_page"], tgt_page=bs["tgt_page"],
                      actor=st.get("annotator") or "")
    except Exception:
        log.exception("could not save the page link")
        return bs, "Kept for this session only — it could not be saved."
    return bs, "Saved for everyone working on these two books."


def unlink_pages(bs: Any) -> dict:
    bs = ensure(bs)
    bs["linked"], bs["offset"] = False, 0
    try:
        with store.tx() as con:
            clear_link(con, bs["pid"])
    except Exception:
        log.exception("could not clear the page link")
    return bs


# ── handlers: doing the work ───────────────────────────────────────────────

def save_text(state: Any, rid: str, side: str, text: Any, base_rev: Any) -> str:
    """Store a correction to one block. Returns a sentence for the annotator.

    The textarea on screen is a view, never the record — POTATO's ``text_edit``
    learned that the hard way, and Setu keeps the same separation: the record
    is ``setu_text``, and the save carries the revision the editor was showing
    so it cannot land on top of somebody else's work.
    """
    from ..core import annotate
    st = session.ensure(state)
    if not rid:
        return ""
    try:
        with store.tx() as con:
            annotate.save_text(con, rid, side, text,
                               base_rev=_int(base_rev, 0),
                               annotator=st.get("annotator") or "",
                               reason="edit")
    except Conflict:
        return ("Somebody else changed this block while you were typing. "
                "Turn the page and back to see their version — nothing of "
                "yours was thrown away, it is in the history.")
    except (Invalid, NotFound) as exc:
        return str(exc)
    except Exception:
        log.exception("save failed for %s/%s", rid, side)
        return "That correction could not be saved. Nothing else is affected."
    return "Saved."


def set_answer(state: Any, rid: str, status: Any, note: Any = None) -> str:
    """Record the judgement for one pair."""
    from ..core import annotate
    st = session.ensure(state)
    if not rid or not status:
        return ""
    try:
        with store.tx() as con:
            annotate.set_status(con, rid, status, note=note,
                                annotator=st.get("annotator") or "")
    except (Invalid, NotFound) as exc:
        return str(exc)
    except Exception:
        log.exception("could not record the answer for %s", rid)
        return "That answer could not be saved."
    return "Saved."


def restore_original(state: Any, rid: str, side: str) -> str:
    """Put back exactly what the parser read, as a new revision."""
    from ..core import annotate
    st = session.ensure(state)
    if not rid:
        return ""
    try:
        with store.tx() as con:
            annotate.restore(con, rid, side, rev=0,
                             annotator=st.get("annotator") or "")
    except Exception:
        log.exception("restore failed for %s/%s", rid, side)
        return "The original could not be put back."
    return "Put back what the parser read."


# ── the printed page: the PDF↔OCR mapping, made visible ────────────────────

def printed_page(bs: Any, side: str):
    """The region of the real PDF page the blocks on screen came from.

    The same fractional box that places a block is handed to Tulana's own crop
    renderer, so what appears here and what the text says are the same region
    by construction, not by coincidence.

    Returns ``(path or None, sentence)`` and never raises: a missing PDF is the
    normal case on a Git LFS checkout and must not stop the work.
    """
    from ..core import sources
    bs = ensure(bs)
    if not bs.get("pid"):
        return None, ""
    page = bs[f"{side}_page"]
    shown = to_display(page)
    try:
        with store.ro() as con:
            row = store.Repository(con).one(
                "SELECT sid FROM setu_segment WHERE book_key = ? AND page = ?"
                " ORDER BY seq LIMIT 1", (bs[f"{side}_book"], page))
            if not row:
                return None, f"Nothing was parsed from page {shown}."
            view = sources.for_segment(con, row["sid"], context=1.0)
    except Exception:
        log.exception("printed page failed")
        return None, (f"Page {shown} could not be shown. The text is "
                      f"unaffected — carry on.")
    if not view.ok:
        return None, view.message or (
            f"Page {shown} of this book is not on this machine. The text is "
            f"unaffected. If the PDFs are stored with Git LFS, run: "
            f"git lfs pull")
    return str(view.path), f"Page {shown}, as printed."


# ── vocabulary for the screen ──────────────────────────────────────────────

#: The answer list, in the order an annotator meets them.
ANSWERS = [(s.label, s.key) for s in STATUSES]


def kind_label(kind: str) -> str:
    """A block's type, in words, with its glyph.

    These are DocLayNet's classes as this corpus's parser emitted them, mapped
    onto Setu's own vocabulary. Showing them is not decoration: "this one is a
    caption and that one is a paragraph" is frequently the entire reason two
    sides look different.
    """
    k = KIND_BY_KEY.get(kind or "")
    return f"{k.icon} {k.label}" if k else "· Text"


def status_label(status: str) -> str:
    s = STATUS_BY_KEY.get(status or "")
    return s.label if s else "Not checked yet"


def block_heading(b: dict) -> str:
    """The small grey line above a block: where it is, and how it stands."""
    bits = [kind_label(b.get("kind") or ""), f"page {b['display_page']}"]
    if b.get("rid"):
        status = b.get("status") or "pending"
        if status != "pending":
            bits.append(f"**{status_label(status)}**")
        if b.get("edited"):
            bits.append("corrected by hand")
        else:
            # CMULAB's distinction: untouched text is the machine's reading,
            # not yet anybody's judgement.
            bits.append("as the parser read it")
    else:
        bits.append("**no counterpart found**")
    return "&nbsp;·&nbsp; ".join(bits)


def read_only_html(b: dict) -> str:
    """One block, for reading rather than correcting."""
    text = (b.get("current") or "").strip()
    body = html.escape(text).replace("\n", "<br>") if text else \
        '<span class="setu-b-empty">(the parser found no text here)</span>'
    classes = "setu-b" + ("" if b.get("rid") else " setu-b-lonely")
    return (f'<div class="{classes}">'
            f'<div class="setu-b-meta">{block_heading(b)}</div>'
            f'<div class="setu-b-text">{body}</div></div>')
