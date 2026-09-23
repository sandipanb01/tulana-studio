"""Setu — the vocabulary of the workspace.

Statuses, segment kinds, text normalisation and the dataclasses the services
pass around. Everything an annotator sees a word for is defined once, here, so
that adding a status means editing one tuple rather than hunting through the
interface, the exporters and the progress counters.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field, asdict
from typing import Any

# ── annotation status ──────────────────────────────────────────────────────
#
# Written for someone who has never annotated before. Each status answers one
# question — "what is wrong with this pair, if anything?" — in words that need
# no glossary. `key` goes in the database and the exports; `label` is what the
# screen says; `help` is the one line shown under it in the interface.


@dataclass(frozen=True)
class Status:
    key: str
    label: str
    help: str
    color: str
    shortcut: str
    counts_as_done: bool


STATUSES: tuple[Status, ...] = (
    Status("pending", "Not checked yet",
           "Nobody has looked at this pair yet.",
           "#94a3b8", "0", False),
    Status("exact", "Exact",
           "The two sides say the same thing. Nothing needs changing.",
           "#15803d", "1", True),
    Status("needs_correction", "Needs correction",
           "They mostly match, but something in the text is wrong — a typo, a "
           "wrong number, a garbled formula.",
           "#b45309", "2", True),
    Status("incomplete", "Missing or incomplete",
           "Part of the text is missing on one side, or one side is empty.",
           "#c2410c", "3", True),
    Status("structural_mismatch", "Structural mismatch",
           "Both sides have text, but they are not the same piece of the book — "
           "or one side splits what the other keeps together.",
           "#7c3aed", "4", True),
    Status("unclear", "Unclear",
           "You cannot tell. Leave it for a reviewer.",
           "#0369a1", "5", True),
    Status("not_applicable", "Not applicable",
           "This does not need annotating — a page header, a picture caption, "
           "a decoration.",
           "#64748b", "6", True),
)

STATUS_BY_KEY: dict[str, Status] = {s.key: s for s in STATUSES}
DEFAULT_STATUS = "pending"
DONE_STATUSES = tuple(s.key for s in STATUSES if s.counts_as_done)


def valid_status(value: Any) -> str:
    """Return a known status key, or raise.

    Refusing an unknown status at the edge is what stops a typo in a script
    from quietly creating a seventh category that no progress counter knows
    about.
    """
    key = str(value or "").strip().lower()
    if key not in STATUS_BY_KEY:
        raise ValueError(
            f"unknown status {value!r}; expected one of "
            + ", ".join(STATUS_BY_KEY)
        )
    return key


# ── segment kinds ──────────────────────────────────────────────────────────
#
# The document hierarchy, expressed as the kinds of thing a segment can be.
# The mapping from the parser's own labels lives in `KIND_FROM_LABEL`; adding a
# new parser label is a one-line data change here, not a code change anywhere.


@dataclass(frozen=True)
class Kind:
    key: str
    label: str
    heading: bool          # does this open a new section of the document?
    annotatable: bool      # is it worth an annotator's time by default?
    icon: str


KINDS: tuple[Kind, ...] = (
    Kind("chapter", "Chapter title", True, True, "▣"),
    Kind("section", "Section title", True, True, "▤"),
    Kind("subsection", "Subsection title", True, True, "▥"),
    Kind("paragraph", "Paragraph", False, True, "¶"),
    Kind("example", "Worked example", False, True, "✎"),
    Kind("exercise", "Exercise", False, True, "✐"),
    Kind("question", "Question", False, True, "?"),
    Kind("mcq", "Multiple choice", False, True, "☰"),
    Kind("answer", "Answer", False, True, "✓"),
    Kind("theorem", "Theorem", False, True, "∴"),
    Kind("definition", "Definition", False, True, "≝"),
    Kind("proof", "Proof", False, True, "⊢"),
    Kind("equation", "Equation", False, True, "∑"),
    Kind("list", "List", False, True, "•"),
    Kind("table", "Table", False, True, "⊞"),
    Kind("caption", "Caption", False, True, "❝"),
    Kind("infobox", "Box / aside", False, True, "❏"),
    Kind("footnote", "Footnote", False, True, "†"),
    Kind("figure", "Figure", False, False, "▢"),
    Kind("header", "Running header", False, False, "▔"),
    Kind("footer", "Running footer", False, False, "▁"),
    Kind("page_number", "Page number", False, False, "#"),
    Kind("other", "Other", False, True, "·"),
)

KIND_BY_KEY: dict[str, Kind] = {k.key: k for k in KINDS}

#: Parser label → Setu kind. Every label present in the corpus is mapped; an
#: unmapped label falls back to ``other`` and is reported by
#: :func:`setu.corpus.ingest_report` so it can be added deliberately.
KIND_FROM_LABEL: dict[str, str] = {
    "chapter-title": "chapter",
    "section-title": "section",
    "sub-section-title": "subsection",
    "table-of-contents": "section",
    "paragraph": "paragraph",
    "solved-example": "example",
    "question": "question",
    "mcq": "mcq",
    "answer": "answer",
    "equation": "equation",
    "expression": "equation",
    "list": "list",
    "table": "table",
    "table-caption": "caption",
    "image-caption": "caption",
    "infobox": "infobox",
    "footnote": "footnote",
    "diagram": "figure",
    "image": "figure",
    "chart": "figure",
    "header": "header",
    "footer": "footer",
    "folio": "page_number",
    "page-number": "page_number",
    "placeholder-text": "other",
    "contact-info": "other",
    "dateline": "other",
    "advertisement": "other",
    "website-link": "other",
}

#: Words that mark a paragraph as something more specific than a paragraph, in
#: each language the corpus actually contains. Data, not code: a new language is
#: a new list, and nothing else changes. Matched at the start of the text only,
#: so a mention of "theorem" mid-sentence does not reclassify a paragraph.
KIND_CUES: dict[str, tuple[str, ...]] = {
    "theorem": ("theorem", "प्रमेय", "सिद्धांत", "प्रमेयः", "પ્રમેય", "ಪ್ರಮೇಯ",
                "సిద్ధాంతం", "സിദ്ധാന്തം", "தேற்றம்", "ਪ੍ਰਮੇਯ"),
    "definition": ("definition", "परिभाषा", "व्याख्या", "વ્યાખ્યા", "ವ್ಯಾಖ್ಯೆ",
                   "నిర్వచనం", "നിർവചനം", "வரையறை", "ਪਰਿਭਾਸ਼ਾ"),
    "proof": ("proof", "उपपत्ति", "सिद्धता", "सिद्ध", "સાબિતી", "ಸಾಧನೆ",
              "నిరూపణ", "തെളിവ്", "நிரூபணம்", "ਸਬੂਤ"),
    "example": ("example", "ex.", "ex ", "उदा", "उदाहरण", "ઉદા", "ಉದಾ",
                "ఉదా", "ഉദാ", "எ.கா", "ਉਦਾ"),
    "exercise": ("exercise", "practice set", "सराव", "सरावसंच", "प्रश्नावली",
                 "अभ्यास", "સ્વાધ્યાય", "ಅಭ್ಯಾಸ", "అభ్యాసం", "അഭ്യാസം",
                 "பயிற்சி", "ਅਭਿਆਸ"),
}


def kind_for(label: str, text: str = "") -> str:
    """Classify a block into the document hierarchy.

    The parser's label decides first because it comes from layout analysis and
    is language-blind. Textual cues only ever *refine* a paragraph or a section
    title into something more specific; they never override a heading label.

    *text* is expected to be already normalised — callers segment in bulk and
    normalising twice for 130,000 blocks is half a second of nothing.
    """
    base = KIND_FROM_LABEL.get(str(label or "").strip().lower(), "other")
    if base in {"paragraph", "other", "section", "subsection", "list", "question"}:
        head = (text or "").lstrip()[:40].lower()
        for kind, cues in KIND_CUES.items():
            for cue in cues:
                if head.startswith(cue):
                    # A heading that says "Practice set 1.2" is an exercise
                    # heading, not a generic section title.
                    if base in {"section", "subsection"} and kind not in {"exercise", "example"}:
                        continue
                    return kind
    return base


# ── text handling ──────────────────────────────────────────────────────────
#
# Mathematics, tables and Indic text all arrive in the same string, so
# normalisation has to be conservative: it may fix encoding, and it may not
# touch anything an author wrote.

_LINE_BREAKS = re.compile("\r\n|[\r\u2028\u2029\x0b\x0c]")
_TRAILING_WS = re.compile(r"[ \t]+(?=\n)")
_CONTROL = re.compile(r"[\x00-\x08\x0e-\x1f\x7f]")


def normalise(text: Any) -> str:
    """Canonicalise text without changing what it says.

    * Unicode NFC, so the same Devanagari word compares equal however it was
      typed or extracted.
    * Every Unicode line break becomes ``\\n``. This is not cosmetic: line-based
      exports such as Moses split on all of them, so a stray ``U+2028`` in one
      file and not the other silently misaligns a whole corpus.
    * Control characters that no textbook contains are dropped; ``\\t`` and
      ``\\n`` are kept because tables and stanzas use them.

    What it deliberately does *not* do: collapse spaces, strip, change dashes or
    quotes, or touch anything between ``$``. Mathematics is content.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    text = _LINE_BREAKS.sub("\n", text)
    text = _CONTROL.sub("", text)
    text = unicodedata.normalize("NFC", text)
    return _TRAILING_WS.sub("", text)


_MATH_SPAN = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$|\\\[(.+?)\\\]|\\\((.+?)\\\)", re.S)
_TEX_CMD = re.compile(r"\\[a-zA-Z]{2,}")
_HTML_TABLE = re.compile(r"<table\b", re.I)


def has_math(text: str) -> bool:
    return bool(_MATH_SPAN.search(text or "") or _TEX_CMD.search(text or ""))


def has_table(text: str) -> bool:
    return bool(_HTML_TABLE.search(text or ""))


def math_spans(text: str) -> list[str]:
    """Every mathematical span in *text*, in order, with delimiters stripped."""
    out = []
    for m in _MATH_SPAN.finditer(text or ""):
        body = next((g for g in m.groups() if g is not None), "")
        if body.strip():
            out.append(body.strip())
    return out


def math_fingerprints(text: str, min_len: int = 6) -> list[str]:
    """Whitespace-free forms of the mathematics in *text*.

    Used for alignment. Mathematics survives translation essentially unchanged —
    ``$2 \\times 3 \\times 5$`` reads the same in Marathi as in English — which
    makes it by far the strongest cross-language anchor this corpus offers.
    Measured on the corpus: about 75% of maths-bearing segments find their
    counterpart this way.
    """
    seen, out = set(), []
    for span in math_spans(text):
        flat = re.sub(r"\s+", "", span)
        if len(flat) >= min_len and flat not in seen:
            seen.add(flat)
            out.append(flat)
    return out


_STRUCT_NUM = re.compile(r"(?<![\d.])(\d{1,2}(?:\.\d{1,3}){1,3})(?![\d.])")
_ITEM_NUM = re.compile(r"^[^\d\n]{0,24}?(?<!\d)(\d{1,3})(?!\d)")

#: Devanagari, Bengali, Gurmukhi, Gujarati, Odia, Tamil, Telugu, Kannada,
#: Malayalam and Perso-Arabic digits, folded to ASCII so that "सराव १.२" and
#: "Practice set 1.2" anchor to each other.
_NATIVE_DIGITS = {}
for _base in (0x0966, 0x09E6, 0x0A66, 0x0AE6, 0x0B66, 0x0BE6, 0x0C66,
              0x0CE6, 0x0D66, 0x0660, 0x06F0):
    for _d in range(10):
        _NATIVE_DIGITS[chr(_base + _d)] = str(_d)
_DIGIT_TABLE = str.maketrans(_NATIVE_DIGITS)


def fold_digits(text: str) -> str:
    """Rewrite native-script digits as ASCII, leaving everything else alone."""
    return (text or "").translate(_DIGIT_TABLE)


def structural_numbers(text: str) -> list[str]:
    """Dotted numbers such as ``1.2`` or ``3.4.1`` found in *text*.

    These are section, exercise and theorem numbers. They are printed in the
    same digits in almost every edition, which makes them a second independent
    anchor after the mathematics.
    """
    folded = fold_digits(text or "")[:400]
    seen, out = set(), []
    for m in _STRUCT_NUM.finditer(folded):
        v = m.group(1)
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def item_number(text: str) -> str:
    """The leading item number of ``Example 3`` / ``उदा (3)``, if there is one."""
    m = _ITEM_NUM.match(fold_digits(text or "").lstrip())
    return m.group(1) if m else ""


# ── dataclasses ────────────────────────────────────────────────────────────

@dataclass
class Segment:
    """One immutable unit of a parsed book."""
    sid: str
    book_key: str
    seq: int
    page: int
    ord_start: int
    ord_end: int
    kind: str
    label: str = ""
    block_type: str = ""
    chapter: str = ""
    chapter_no: str = ""
    section: str = ""
    section_no: str = ""
    item_no: str = ""
    depth: int = 0
    source_text: str = ""
    n_chars: int = 0
    has_math: int = 0
    has_table: int = 0
    block_ids: list[int] = field(default_factory=list)
    fx0: float = 0.0
    fy0: float = 0.0
    fx1: float = 0.0
    fy1: float = 0.0
    anchor_math: list[str] = field(default_factory=list)
    anchor_num: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class RowView:
    """A bilingual row as the interface needs it: both texts, both origins."""
    rid: str
    pid: str
    seq: int
    status: str
    origin: str
    confidence: float
    note: str
    kind: str
    chapter: str
    chapter_no: str
    section: str
    section_no: str
    src: dict
    tgt: dict
    edited: bool
    updated_at: float | None
    updated_by: str

    def as_dict(self) -> dict:
        return asdict(self)


def side_of(value: Any) -> str:
    s = str(value or "").strip().lower()
    if s not in {"src", "tgt"}:
        raise ValueError(f"side must be 'src' or 'tgt', got {value!r}")
    return s
