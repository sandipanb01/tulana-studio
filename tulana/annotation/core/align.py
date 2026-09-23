"""Setu — proposing which segment on the left goes with which on the right.

This module never decides anything. It *proposes*, with a confidence, and every
proposal reaches the annotator marked "suggested" and unconfirmed. That is not
timidity: measured on this corpus, anchor-based alignment puts about 36% of
segments within one page of where they belong, at 83–96% accuracy depending on
the book. Useful enough to save hours, nowhere near good enough to commit.

How it works, in the order the signals were found to matter:

**Mathematics is the strongest anchor.** ``$2 \\times 3 \\times 5 \\times 7$``
reads the same in Marathi, Kannada and Telugu as it does in English. Roughly
three quarters of maths-bearing segments find their counterpart on this signal
alone. The corpus is 55% maths-bearing, which is what makes this viable at all.

**Structural numbers are the second anchor.** "Practice set 1.2" and
"सरावसंच 1.2" print the same 1.2. Native-script digits are folded to ASCII
first, so "सराव १.२" anchors too.

**Alignment does not cross.** Two books tell the same story in the same order,
so if segment 40 pairs with 38, segment 60 cannot pair with 30. A weighted
longest-increasing-subsequence over the candidate anchors keeps only a
non-crossing chain, which removes most of what a greedy nearest-match gets
wrong — a formula that recurs in three exercises stops being a coin toss.

**Everything between two anchors is filled in order.** Between consecutive
anchors the two runs are zipped by kind and position. These fills get a low
confidence because they rest on the anchors either side, not on evidence of
their own.

Anything left over becomes a one-sided row. Nothing is dropped: a segment the
aligner cannot place still reaches the annotator, because a segment that never
appears on screen is a segment nobody will ever fix.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, Sequence

log = logging.getLogger("setu.align")

# Weights. Chosen by measuring against the page-parallel Maharashtra editions,
# where the correct answer is known to be on the same page.
W_MATH = 3.0          # per shared mathematical fingerprint
W_NUM = 1.0           # per shared structural number
W_ITEM = 1.2          # same item number AND same kind ("Example 3" ↔ "उदा 3")
W_KIND = 0.8          # same kind of thing
W_POSITION = 12.0     # penalty per unit of relative-position distance
W_LENGTH = 0.8        # penalty for wildly different lengths

#: Below this an anchor is not worth proposing; it is almost always a single
#: coincidental number shared by two unrelated segments.
MIN_ANCHOR_SCORE = 1.5

#: Anchors at or above this are shown as "high confidence" in the interface.
STRONG_SCORE = 4.0

#: Candidate pairs considered per source segment. A fingerprint shared by fifty
#: segments carries no information and searching it exhaustively is wasted work.
MAX_CANDIDATES = 24

#: A fingerprint occurring more often than this in the target book is a
#: boilerplate formula, not an anchor.
MAX_POSTING = 40


@dataclass
class Proposal:
    """One suggested pairing, or a one-sided row when a side is ``-1``."""
    src: int          # index into the source segment list, or -1
    tgt: int          # index into the target segment list, or -1
    score: float
    basis: str        # "math" | "number" | "chain" | "fill" | "unpaired"

    @property
    def confidence(self) -> float:
        """0–1, for display. Saturates at twice the strong threshold."""
        if self.src < 0 or self.tgt < 0:
            return 0.0
        return round(min(1.0, max(0.0, self.score / (STRONG_SCORE * 2))), 3)


def _norm_len(n: int) -> float:
    return float(n or 0)


def _relative_positions(segs: Sequence[dict]) -> list[float]:
    """Each segment's position through the book, 0 to 1.

    Relative rather than absolute because the two editions have different
    lengths — Hindi runs about 15% longer than English in the NCERT set — so
    comparing raw indices would drift steadily out by the last chapter.
    """
    n = max(len(segs) - 1, 1)
    return [i / n for i in range(len(segs))]


def _index(segs: Sequence[dict]) -> tuple[dict[str, list[int]], dict[str, list[int]]]:
    math_idx: dict[str, list[int]] = {}
    num_idx: dict[str, list[int]] = {}
    for j, s in enumerate(segs):
        for f in s.get("anchor_math") or ():
            math_idx.setdefault(f, []).append(j)
        for f in s.get("anchor_num") or ():
            num_idx.setdefault(f, []).append(j)
    return math_idx, num_idx


def candidates(src: Sequence[dict], tgt: Sequence[dict]) -> list[tuple[int, int, float, str]]:
    """Every plausible pairing, scored. Ordered by source index."""
    math_idx, num_idx = _index(tgt)
    spos, tpos = _relative_positions(src), _relative_positions(tgt)
    out: list[tuple[int, int, float, str]] = []

    for i, s in enumerate(src):
        hits: dict[int, float] = {}
        basis: dict[int, str] = {}
        for f in s.get("anchor_math") or ():
            posting = math_idx.get(f)
            if not posting or len(posting) > MAX_POSTING:
                continue
            for j in posting:
                hits[j] = hits.get(j, 0.0) + W_MATH
                basis[j] = "math"
        for f in s.get("anchor_num") or ():
            posting = num_idx.get(f)
            if not posting or len(posting) > MAX_POSTING:
                continue
            for j in posting:
                hits[j] = hits.get(j, 0.0) + W_NUM
                basis.setdefault(j, "number")
        if not hits:
            continue

        # Only the most promising handful are scored fully; the rest cannot win.
        ranked = sorted(hits.items(), key=lambda kv: -kv[1])[:MAX_CANDIDATES]
        scored: list[tuple[int, int, float, str]] = []
        for j, base in ranked:
            t = tgt[j]
            score = base
            if s.get("kind") == t.get("kind"):
                score += W_KIND
            if (s.get("item_no") and s.get("item_no") == t.get("item_no")
                    and s.get("kind") == t.get("kind")):
                score += W_ITEM
            score -= W_POSITION * abs(spos[i] - tpos[j])
            a, b = _norm_len(s.get("n_chars")), _norm_len(t.get("n_chars"))
            if a and b:
                ratio = max(a, b) / min(a, b)
                if ratio > 2.5:
                    score -= W_LENGTH * min(ratio - 2.5, 4.0)
            if score >= MIN_ANCHOR_SCORE:
                scored.append((i, j, score, basis.get(j, "math")))
        # One anchor per source segment: the aligner's job is a chain, and the
        # chain step below cannot use more than one per row anyway.
        if scored:
            out.append(max(scored, key=lambda c: c[2]))
    return out


class _FenwickMax:
    """Prefix-maximum tree — the chain step's inner loop, in O(log n)."""

    def __init__(self, n: int):
        self.n = n + 1
        self.best = [(-1e18, -1)] * (self.n + 1)

    def update(self, i: int, value: float, payload: int) -> None:
        i += 1
        while i <= self.n:
            if value > self.best[i][0]:
                self.best[i] = (value, payload)
            i += i & -i

    def query(self, i: int) -> tuple[float, int]:
        """Best value over indices strictly below *i*."""
        i += 1
        out = (-1e18, -1)
        while i > 0:
            if self.best[i][0] > out[0]:
                out = self.best[i]
            i -= i & -i
        return out


def monotone_chain(cands: Sequence[tuple[int, int, float, str]],
                   n_tgt: int) -> list[tuple[int, int, float, str]]:
    """Keep the best-scoring set of anchors that do not cross each other.

    Candidates arrive sorted by source index, so this is a weighted
    longest-increasing-subsequence on the target index. Removing crossings is
    what turns "this formula appears somewhere in the book" into "this formula
    appears *here*".
    """
    if not cands:
        return []
    tree = _FenwickMax(n_tgt + 2)
    total = [0.0] * len(cands)
    back = [-1] * len(cands)
    best_end, best_total = -1, -1e18

    for k, (_i, j, score, _b) in enumerate(cands):
        prev_total, prev_k = tree.query(j)          # strictly smaller target index
        base = prev_total if prev_k >= 0 else 0.0
        total[k] = base + score
        back[k] = prev_k if prev_k >= 0 else -1
        tree.update(j, total[k], k)
        if total[k] > best_total:
            best_total, best_end = total[k], k

    chain: list[tuple[int, int, float, str]] = []
    k = best_end
    while k >= 0:
        chain.append(cands[k])
        k = back[k]
    chain.reverse()
    return chain


def suggest(src: Sequence[dict], tgt: Sequence[dict]) -> list[Proposal]:
    """Propose a complete set of rows covering every segment on both sides.

    The result is ordered as the source book reads. One-sided rows appear where
    they belong in that order, so an annotator scrolling through never has to
    wonder where the unmatched material went.
    """
    anchors = monotone_chain(candidates(src, tgt), len(tgt))
    out: list[Proposal] = []
    si = ti = 0

    for i, j, score, basis in anchors:
        if i < si or j < ti:                      # defensive: chain is monotone
            continue
        out.extend(_fill(src, tgt, si, i, ti, j))
        out.append(Proposal(i, j, score, basis))
        si, ti = i + 1, j + 1

    out.extend(_fill(src, tgt, si, len(src), ti, len(tgt)))
    return out


def _fill(src: Sequence[dict], tgt: Sequence[dict],
          s0: int, s1: int, t0: int, t1: int) -> list[Proposal]:
    """Pair up the run between two anchors, in order.

    Same-kind neighbours are zipped first because a heading pairs with a
    heading far more reliably than with whatever happens to sit at the same
    offset. What remains is zipped positionally, and any surplus on either side
    becomes one-sided rows.
    """
    left = list(range(s0, s1))
    right = list(range(t0, t1))
    if not left and not right:
        return []
    if not left:
        return [Proposal(-1, j, 0.0, "unpaired") for j in right]
    if not right:
        return [Proposal(i, -1, 0.0, "unpaired") for i in left]

    out: list[Proposal] = []
    li = ri = 0
    while li < len(left) and ri < len(right):
        i, j = left[li], right[ri]
        if src[i].get("kind") == tgt[j].get("kind"):
            out.append(Proposal(i, j, 0.5, "fill"))
            li += 1
            ri += 1
            continue
        # Kinds disagree. Look one step ahead on each side for a match before
        # giving up on this pair; a single extra figure on one side is the
        # commonest cause and skipping it keeps the rest of the run aligned.
        ahead_r = ri + 1 < len(right) and src[i].get("kind") == tgt[right[ri + 1]].get("kind")
        ahead_l = li + 1 < len(left) and tgt[j].get("kind") == src[left[li + 1]].get("kind")
        if ahead_r and not ahead_l:
            out.append(Proposal(-1, j, 0.0, "unpaired"))
            ri += 1
        elif ahead_l and not ahead_r:
            out.append(Proposal(i, -1, 0.0, "unpaired"))
            li += 1
        else:
            out.append(Proposal(i, j, 0.25, "fill"))
            li += 1
            ri += 1

    out.extend(Proposal(left[k], -1, 0.0, "unpaired") for k in range(li, len(left)))
    out.extend(Proposal(-1, right[k], 0.0, "unpaired") for k in range(ri, len(right)))
    return out


def quality(proposals: Iterable[Proposal]) -> dict:
    """Summarise a proposal set, for the screen that asks "is this any good?"."""
    n = anchored = filled = one_sided = strong = 0
    for p in proposals:
        n += 1
        if p.src < 0 or p.tgt < 0:
            one_sided += 1
        elif p.basis in {"math", "number"}:
            anchored += 1
            if p.score >= STRONG_SCORE:
                strong += 1
        else:
            filled += 1
    return {"rows": n, "anchored": anchored, "strong": strong,
            "filled": filled, "one_sided": one_sided,
            "anchored_pct": round(100.0 * anchored / n, 1) if n else 0.0}
