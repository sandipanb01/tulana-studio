"""Stable identifiers for Setu.

An identifier must survive an annotator rewriting the text it points at. So no
identifier here is ever derived from the *current* text of anything. Segment
identity comes from where the segment sits in the parsed source — book, page,
reading-order span — because that is a fact about the document, not about what
somebody typed into a box this afternoon.

Two consequences worth stating plainly:

* Re-ingesting the same corpus produces the same segment identifiers, so
  annotations survive a reparse of an unchanged book.
* If a book is genuinely re-parsed into a different block layout, the
  identifiers change. That is correct — they now denote different spans — and
  :func:`setu.corpus.remap_segments` handles the carry-over explicitly rather
  than pretending the old identifiers still mean something.

Identifiers are short, opaque, URL-safe, and carry a two-letter prefix so a
stray identifier in a log or an export says what kind of thing it names.
"""
from __future__ import annotations

import hashlib
import os
import re
import time

# Crockford base32 without I, L, O, U: no character pair that a human can
# confuse when reading an id off a screen and typing it into the search box.
_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

_VALID = re.compile(r"^[a-z]{2}_[0-9A-HJKMNP-TV-Z]{6,26}$")


def _b32(raw: bytes, length: int) -> str:
    n = int.from_bytes(raw, "big")
    out = []
    for _ in range(length):
        out.append(_ALPHABET[n & 31])
        n >>= 5
    return "".join(reversed(out))


def derive(prefix: str, *parts: object, length: int = 14) -> str:
    """A deterministic identifier for a thing defined by *parts*.

    The same parts always give the same id, on any machine, in any process, in
    any Python version — the digest is over a NUL-joined UTF-8 encoding, not
    over ``hash()`` or ``repr()``, both of which vary.
    """
    joined = "\x00".join("" if p is None else str(p) for p in parts)
    digest = hashlib.sha256(joined.encode("utf-8")).digest()
    return f"{prefix}_{_b32(digest, length)}"


def mint(prefix: str) -> str:
    """A fresh identifier for a thing that has no natural definition.

    Time-ordered so ids sort roughly by creation, with enough randomness that
    two processes minting in the same millisecond do not collide.
    """
    stamp = int(time.time() * 1000) & ((1 << 45) - 1)
    rand = int.from_bytes(os.urandom(8), "big") & ((1 << 35) - 1)
    return f"{prefix}_{_b32(((stamp << 35) | rand).to_bytes(10, 'big'), 16)}"


def is_id(value: object, prefix: str = "") -> bool:
    """True if *value* looks like an identifier this module could have made.

    Used at the edge of the API so a malformed id is rejected with a clear
    message instead of reaching SQL and coming back as an empty result that
    looks like missing data.
    """
    if not isinstance(value, str) or not _VALID.match(value):
        return False
    return not prefix or value.startswith(prefix + "_")


# ── the identifier kinds ───────────────────────────────────────────────────

def book_key(relpath: str) -> str:
    """Identity of a parsed book.

    Keyed on the *relative path* the parser recorded, normalised to forward
    slashes and lowercased, so the same book does not acquire two identities by
    being read on Windows and then on Linux.
    """
    norm = str(relpath or "").replace("\\", "/").strip("/").lower()
    return derive("bk", norm, length=12)


def dedup_key(book: str, num_pages: int, n_blocks: int) -> str:
    """Identity of a book's *content*, for collapsing duplicate parses.

    The corpus ships several books twice under different folders. Those copies
    differ only in the folder they sit in and the raster filenames, so keying on
    the book name plus its page and block counts groups them without any
    risk of merging two genuinely different books: two different textbooks
    sharing a name, a page count and a block count to the unit does not happen.
    """
    return derive("dk", str(book).strip().lower(), int(num_pages), int(n_blocks),
                  length=12)


def segment_id(book_key_: str, page: int, ord_start: int, ord_end: int) -> str:
    """Identity of a segment — position only, never text."""
    return derive("sg", book_key_, int(page), int(ord_start), int(ord_end))


def project_id(name: str, src_book: str, tgt_book: str) -> str:
    return derive("pj", str(name).strip().lower(), src_book, tgt_book, length=12)


def row_id(project: str, seq: int) -> str:
    return derive("rw", project, int(seq))


def session_id() -> str:
    return mint("ss")


def export_id() -> str:
    return mint("xp")
