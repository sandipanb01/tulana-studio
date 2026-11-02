# Aligned pages UI

The Gradio viewer for the aligned textbook data: pick a book pair and an English page, see the English page
and its translation page(s) with the OCR bounding boxes drawn from their coordinates, and the paired text
in a table below. Each translation unit has one colour on both pages and one row in the table.

**Current served data: `data/aligned_v2/`.** The viewer opens it by default. `data/aligned/` (v1) is kept
for comparison.

## How the data was made

```
 raw OCR books (data/raw/output, not in this repo)
 62 English <-> Indian-language book pairs, OCR blocks with boxes and text
        |
        |  pair pages:  page n <-> n  |  bilingual facing pages  |  3-page window around a page map
        |  Gemini 3.5 Flash (prompt v4): align blocks into translation units + minimal OCR /
        |  translation correction; guards in code reject damaging edits
        |  export: merge each unit's OCR blocks (union box), merge paragraph splits
        v
 data/aligned   (v1)
 4,769 English pages, 30,192 aligned segments, 94.7% of OCR text blocks aligned
        |
        |  1. drop English pages whose page map was wrong (most matches on another page),
        |     whose alignment failed, or where nothing matched: 359 pages, window books only
        |  2. Gemini 3.5 Flash (prompt markup_restore_v1, thinking low): put the English markup
        |     (tables, $...$ math, **bold**, lists, <br>) back on the translation; a code guard
        |     accepts an edit only if no letter, digit or symbol changed and the markup renders
        |  3. change log of every change
        v
 data/aligned_v2   (v2, served)
 28,817 aligned segments, 96.1% of OCR text blocks aligned on kept pages,
 markup restored on 3,302 translation blocks
```

## v1 -> v2

| | v1 `data/aligned` | v2 `data/aligned_v2` |
|---|---|---|
| English pages sent for alignment | 4,769 | 4,769, of which 359 dropped |
| Dropped pages by reason | - | map wrong 225, alignment failed 113, nothing matched 19, unparseable 2 |
| Aligned segments | 30,192 | 28,817 (1,375 units unlinked on both sides) |
| OCR text blocks aligned (kept pages) | 94.7% | 96.1% |
| Segments where the translation lacks the English markup | 9,070 (30.0%) | 6,645 (23.1%) |
| Translation blocks with markup restored | - | 3,302 |
| English text | - | unchanged |

Markup restored, by type (blocks that gained it; a block can gain several):

| Markup | Blocks |
|---|---|
| LaTeX `$...$` | 1,736 |
| Bold `**...**` | 1,285 |
| LaTeX commands (`\angle`, `\cup`, ...) | 816 |
| Other HTML (`<br>`, `<sup>`) | 67 |
| List markers | 25 |
| Tables | 17 |

By book family:

| Family | Pairing | English pages dropped | Units unlinked | Blocks with markup restored |
|---|---|---|---|---|
| Maharashtra | page n <-> n | 0 | 0 | 1,277 |
| Kerala 10 | page n <-> n | 0 | 0 | 189 |
| Andhra Pradesh (bilingual) | facing pages | 0 | 0 | 251 |
| Karnataka | window | 59 | 223 | 190 |
| Punjab (10 + 12) | window | 104 | 433 | 350 |
| Tamil Nadu | window | 51 | 248 | 227 |
| Gujarat | window | 24 | 68 | 155 |
| NCERT | window | 121 | 403 | 663 |
| **Total** | | **359** | **1,375** | **3,302** |

Pages were dropped only in the window books (Karnataka, Punjab, Tamil Nadu, Gujarat, NCERT), where the
page numbers of the two books drift. Every change is listed in `data/aligned_v2/changelog.jsonl`
(text before and after for markup changes); `data/aligned_v2/CHANGELOG.md` has the counts per pair, and
`data/aligned_v2/README.md` describes the new fields (`dropped_page_mismatch`, `page_dropped`,
`markup_restored`) above the full field reference.

## Why not all markup was restored

The markup pass looked at 10,074 translation blocks (on 3,790 English pages) whose English counterpart has
markup the block lacks or has less of. A code guard accepted an edit only if every letter, digit and symbol
of the translation stayed the same and in order, and the markup still renders:

| Outcome of the 10,074 blocks | Blocks |
|---|---|
| Accepted and applied | 3,302 |
| Rejected by the guard (the edit also changed content; original kept) | 4,407 |
| No change proposed | 2,365 |

Separately, 2,012 proposed edits could not be placed because their text did not occur exactly once.

After v2, 6,645 aligned segments (23.1%) still have less markup than their English. Why:

| What happened to these segments in the markup pass | Segments | Share |
|---|---|---|
| Edit rejected by the guard: it also changed content, mostly by copying English words or the English math into the translation | 3,899 | 59% |
| No change proposed (often nothing to fix) | 1,195 | 18% |
| Accepted, partial fix: applied in v2, but some markup is still missing (967 the model restored only part; 189 units split over pages where one part was not fixed) | 1,156 | 17% |
| Edit could not be placed (its text did not occur exactly once) | 395 | 6% |

Most of the remainder is not lost markup. In 4,335 of the 6,645 segments (65%) the translation already uses
the missing kind of markup, just less often than the English, which usually reflects how the translation is
written: two math spans merged into one (`$f=\{...\}, \mathbf{Z}$`), a different expression
(`$\frac{BP}{PA}$` for English `$\frac{AP}{PB}$`), or a word instead of math (`21 वाँ` for
`$21^{\text{st}}$`). The likely real gaps are segments whose translation has none of that markup at all:

| Missing markup | Translation has none | Translation has fewer |
|---|---|---|
| LaTeX `$...$` | 904 | 3,320 |
| LaTeX commands | 1,022 | 2,811 |
| Bold | 837 | 113 |
| Lists | 168 | 70 |
| Other HTML | 69 | 122 |
| Tables | 22 | 61 |

(A segment can miss more than one type.)

## Run

```bash
pip install -r requirements.txt            # gradio 5.49.1
python aligned_viewer.py --port 7864                                          # serves data/aligned_v2
python aligned_viewer.py --aligned data/aligned --port 7864                   # v1, for comparison
python aligned_viewer.py --aligned /path/to/aligned --host 0.0.0.0 --port 7864
python aligned_viewer.py --port 7864 --share                                  # temporary public gradio.live link
```

## Data

Both folders have the same layout: one folder per book pair (`<pair_id>/<book>.json`, the raw OCR format
plus alignment fields), `export_summary.json`, `failed_pages.tsv` and a `README.md` that describes every
field. 62 pairs. The files have the OCR bounding boxes and text but not the page images.

Reports saved from the viewer ("Report a problem") go to `<data folder>/viewer_reports.jsonl`, which is
git-ignored.

## What the viewer does

- **Book pair / English page**, with ◀ Prev / Next ▶. The pair list shows each pair's aligned %
  (in v2, blocks on dropped pages count as not aligned). "Only pages with not-aligned text" narrows the
  page list and Prev/Next to those pages.
- **Pages.** English page and translation page(s) as boxes on blank pages (the scans are not in the data).
  Same colour = same unit; dashed grey inside = the original OCR blocks that were merged; dashed red =
  text with no counterpart; grey = figures, empty blocks, pages not processed and, in v2, dropped pages.
  Hover a box for its text.
- **Header** with the page status (`dropped_page_mismatch` for dropped pages), the translation pages
  shown, the unit count, and OCR text block counts per page.
- **Table.** One row per unit: English | translation, math typeset with KaTeX. A unit that crosses a page
  break lists all its parts on both sides, each marked `[pN]`. Reviewer flags (⚑) appear with the unit;
  text with no counterpart is listed with the reason.
- **Find text.** Searches English and translated text in all pairs, ignoring LaTeX commands, braces, `$`
  and spaces, and jumps to the matching page.
- **Report a problem.** Saves name, pair, page, unit(s) and the description as one JSON line.

`aligned_viewer.py` is `scripts/aligned_viewer.py` from the main `doc-mt-iitr-collaboration` folder with
one change: the default `--aligned` is `data/aligned_v2`. KaTeX is loaded from cdn.jsdelivr.net, so the
browser needs internet access to typeset math.
