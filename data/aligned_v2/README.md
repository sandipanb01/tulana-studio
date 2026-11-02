# Aligned data v2

This is `data/aligned` with two changes. Everything else, including the file format, is as described in the
v1 README below. The full list of changes is in `changelog.jsonl`; a summary with counts is in `CHANGELOG.md`.

1. **Misaligned pages dropped** (window-mode books only: Karnataka, Punjab, Tamil Nadu, Gujarat, NCERT).
   An English page is dropped when most of its matched content was found on a different translation page
   than the page map said, when its alignment failed, or when nothing on it matched. The page stays in the
   file with its boxes, but:
   - page `align_status` is `dropped_page_mismatch`, with `drop_reason` (`map_wrong`, `alignment_failed`,
     `unparseable`, `nothing_matched`), `drop_detail` (mapped page and where the matches were) and
     `align_status_v1`;
   - every unit with an English part on that page loses its `align_id` on **both** sides;
   - those blocks, and the page's other text blocks, have `align_state: "page_dropped"` and an `align_note`
     (`page_dropped` or `counterpart_page_dropped`).
   `align_summary` and `alignment.summary` count these under `page_dropped`.

2. **Markup restored on the translation side.** Where the English text has HTML (tables, `<br>`), LaTeX
   (`$...$`) or Markdown (`**bold**`, list markers) and the translation OCR wrote the same content as plain
   text, Gemini proposed the markup and code accepted it only if no letter, digit or symbol of the
   translation was added, removed or reordered, and the markup still renders (balanced `$`, `**`, table tags).
   Changed blocks have `markup_restored: true`; `changelog.jsonl` has the text before and after.


---

# Aligned + corrected Maths textbooks (English ↔ Indian languages)

This package contains school Maths textbooks in English and in their official Indian-language
editions. Each English page is **aligned to its translation**, **OCR mistakes are corrected**, and the OCR
blocks that form one **paragraph-level segment** are **merged into a single block with one bounding box**.
The merge is applied to both languages together, so the two sides always stay paired.
It is the input for building a **document-level parallel test set**, and for a viewer app that shows
each page with its boxes and the text below.

The JSON format is the same as the original OCR delivery (`raw/output`), with a few fields added.
Nothing is renamed or removed, so existing readers keep working.

| | |
|---|---|
| Book pairs | 62: 21 state-board book pairs + 41 NCERT chapters |
| Languages | English ↔ Gujarati, Hindi, Kannada, Malayalam, Marathi, Punjabi, Tamil, Telugu |
| English pages aligned | 4,769 (4,653 aligned, 116 failed) |
| Aligned segments | 30,192 paragraph-level segments (merged from 42,309 model units) |
| Model | `gemini-3.5-flash`, thinking `minimal`, prompt v4 (Oct 2026) |
| Human checks so far | spot check only (see "What has been checked") |

---

## 1. Contents

```
aligned/
├── README.md                 this file
├── export_summary.json       every pair: its files, unit count, page status counts
├── failed_pages.tsv          the 116 English pages whose alignment failed (see section 7)
└── <pair_id>/<same relative path as in raw/output>
      e.g. MH10_1_en-mr/CLASS-10/MH_EN_10_1.json          English side
           MH10_1_en-mr/CLASS-10/MH_MR_10_1.json          Marathi side
           AP10_sem1_en-te/CLASS-10/AP_EN-TEL_10_SEM1.json  bilingual book: both sides in one file
           NCERT_1001_en-hi/dataset/input/eng/10/1001.json  NCERT: one pair per chapter
           NCERT_1001_en-hi/dataset/input/hin/10/1001.json
```

There is **one folder per pair** because an English book is merged differently for each target
language. For example, `MH_EN_10_1` is paired with 5 languages, so it appears in 5 folders, each with
different merged blocks and links.

### Book pairs

`pair_id` = `<board><class>_<part>_en-<lang>`.

Boards:
- MH = Maharashtra
- KER = Kerala
- AP = Andhra Pradesh
- KT = Karnataka
- PUN = Punjab
- TM = Tamil Nadu
- GUJ = Gujarat
- NCERT = national (NCERT) books

Pairing modes:
- **page**: the two books are page-aligned, so English page *n* ↔ target page *n*.
- **facing**: one bilingual book. English is on page *n* and the Telugu translation on page *n*+1.
- **window**: the pages drift. Each English page was sent with the 3 target pages around its mapped page.

| pair_id | English book | Target book | Language | Mode | EN pages | Segments | Aligned | Failed |
|---|---|---|---|---|---|---|---|---|
| MH9_1_en-gu | MH_EN_9_1 | MH_GU_9_1 | Gujarati | page | 148 | 1,127 | 148 | 0 |
| MH9_1_en-hi | MH_EN_9_1 | MH_HI_9_1 | Hindi | page | 148 | 1,145 | 148 | 0 |
| MH9_1_en-ka | MH_EN_9_1 | MH_KA_9_1 | Kannada | page | 148 | 1,122 | 148 | 0 |
| MH9_1_en-mr | MH_EN_9_1 | MH_MR_9_1 | Marathi | page | 148 | 1,134 | 147 | 1 |
| MH9_1_en-te | MH_EN_9_1 | MH_TE_9_1 | Telugu | page | 148 | 1,140 | 148 | 0 |
| MH10_1_en-gu | MH_EN_10_1 | MH_GU_10_1 | Gujarati | page | 188 | 1,284 | 188 | 0 |
| MH10_1_en-hi | MH_EN_10_1 | MH_HI_10_1 | Hindi | page | 188 | 1,281 | 188 | 0 |
| MH10_1_en-ka | MH_EN_10_1 | MH_KA_10_1 | Kannada | page | 188 | 1,279 | 188 | 0 |
| MH10_1_en-mr | MH_EN_10_1 | MH_MR_10_1 | Marathi | page | 188 | 1,293 | 188 | 0 |
| MH10_1_en-te | MH_EN_10_1 | MH_TE_10_1 | Telugu | page | 188 | 1,294 | 188 | 0 |
| MH10_2_en-mr | MH_EN_10_2 | MH_MR_10_2 | Marathi | page | 180 | 1,309 | 180 | 0 |
| KER10_1_en-ml | KER_EN_10_1 | KER_ML_10_1 | Malayalam | page | 152 | 781 | 152 | 0 |
| KER10_2_en-ml | KER_EN_10_2 | KER_ML_10_2 | Malayalam | page | 144 | 753 | 144 | 0 |
| AP10_sem1_en-te | AP_EN-TEL_10_SEM1 | (same book) | Telugu | facing | 142 | 967 | 142 | 0 |
| AP10_sem2_en-te | AP_EN-TEL_10_SEM2 | (same book) | Telugu | facing | 122 | 800 | 122 | 0 |
| KT10_1_en-kn | KT_EN_10_1 | KT_Ka_10_1 | Kannada | window | 152 | 852 | 145 | 7 |
| KT10_2_en-kn | KT_EN_10_2 | KT_Ka_10_2 | Kannada | window | 128 | 724 | 122 | 6 |
| PUN10_en-pa | PUN_EN_10 | PUN_PU_10 | Punjabi | window | 368 | 2,289 | 354 | 14 |
| PUN12_1_en-pa | PUN_EN_12_1 | PUN_PU_12_1 | Punjabi | window | 249 | 994 | 237 | 12 |
| TM10_en-ta | TM_EN_10 | TM_Ta_10 | Tamil | window | 352 | 2,592 | 334 | 18 |
| GUJ10_en-gu | GUJ_EN_10 | GUJ_GJ_10 | Gujarati | window | 170 | 1,008 | 159 | 11 |
| NCERT_\<ch\>_en-hi (41 chapters, classes 10–12) | eng/\<class\>/\<ch\> | hin/\<class\>/\<ch\> | Hindi | window | 930 | 5,024 | 883 | 47 |

"EN pages" counts the English pages that were sent for alignment. The files contain every page of the
book; pages not sent are marked `not_processed`.

### Not included

- **Kerala class 11 (EN–ML).** Its Malayalam book is the board's own text on the same syllabus, not a
  translation. Only 41% of English blocks found a counterpart in a pilot.
- **West Bengal *Ganit Prakash*.** Bengali only; no English counterpart was delivered.
- **Gujarat English chapters 1–6** (108 pages). The Gujarati book delivered starts at chapter 7. These
  pages are present but `not_processed`.
- **Punjab class 12, 13 English pages** with no counterpart in the Punjabi book. Present, `not_processed`.

---

## 2. File format

```jsonc
{
  "book": "MH_MR_10_1", "relpath": "CLASS-10/MH_MR_10_1.pdf", "num_pages": 188,     // as in raw
  "alignment": { "pair_id": "MH10_1_en-mr", "lang": "mr", "language": "Marathi",
                 "other_book": "MH_EN_10_1", "model": "gemini-3.5-flash",
                 "prompt_version": "v4", "thinking_level": "minimal",
                 "summary": { "text_blocks": 2113, "aligned": 2091, "unpaired": 22,
                              "page_failed": 0, "not_processed": 0, "aligned_pct": 98.96 } },  // added
  "pages": [{
    "image": "0044_p0122.png", "width": 1650, "height": 2200, "page": 122,             // as in raw
    "align_status": "ok",                                                               // added
    "align_summary": { "text_blocks": 13, "aligned": 13, "unpaired": 0,
                       "page_failed": 0, "not_processed": 0 },                         // added
    "blocks": [{
      "order": 3, "label": "List", "type": "Text", "conf": 0.959,                       // as in raw
      "bbox_xyxy": [396.6, 557.9, 1289.6, 679.7],   // union of the member boxes, pixels on `image`
      "text": "• संभाव्यता : ओळख\n• …",               // corrected text; members joined by a blank line
      "aligned": true,                              // true = has a counterpart in the other language
      "align_state": "aligned",                     // aligned / unpaired / page_failed / not_processed / no_text
      "align_id": "MH10_1_en-mr/p122/u3",           // shared with the counterpart block; null = not aligned
      "align_relation": "equivalent",               // or "partial": one side has extra material
      "align_confidence": "high",                   // model's own rating: high / medium / low
      "members": [ {"order": 3, "label": "List", "bbox_xyxy": [...]} ],   // original OCR blocks merged here
      "merged_units": ["…/u5", "…/u6"],            // only if several model units were joined into this paragraph
      "part": "1/2",                                // only when a unit continues on another page
      "align_note": "no_counterpart",               // only on unaligned blocks: why (no_counterpart / junk / page_furniture)
      "flags": ["[translation_divergence] …"]       // only when a reviewer should look at this block
    }]
  }]
}
```

### Field reference

| Level | Field | Meaning |
|---|---|---|
| file | `alignment` | which pair this file belongs to, its language, the other book, and the model settings |
| file | `alignment.summary` | counts of the book's OCR text blocks in each `align_state`, and `aligned_pct` |
| page | `align_status` | see table below |
| page | `align_summary` | counts of the page's OCR text blocks in each `align_state` |
| block | `order`, `label`, `type`, `conf` | from the first member (`conf` is the lowest across members) |
| block | `bbox_xyxy` | `[x0, y0, x1, y1]` in pixels on the page image; the union of `members` |
| block | `text` | corrected text (section 4); filler loops of 20+ repeats were cut to 5 |
| block | `aligned` | `true` if the block has a counterpart in the other language, else `false` |
| block | `align_state` | why it is or is not aligned; see table below |
| block | `align_id` | `<pair_id>/p<English page>/u<n>`. Every non-null id appears on **both** language sides |
| block | `members` | the original OCR blocks (with their original boxes) merged into this one |
| block | `merged_units` | the model's smaller units joined into this paragraph segment (only when more than one) |
| block | `part` | `k/n` when a unit spans pages: one block per page, same `align_id` |
| block | `flags` | suggestions **not** applied, for human review (section 4) |

### Page `align_status`

| value | meaning |
|---|---|
| `ok` | aligned and corrected on the first pass |
| `retried_ok` | the first attempt failed the checks; a retry passed |
| `alignment_failed` | still fails the alignment checks after 2 retries: blocks unmerged, no `align_id`, no edits applied |
| `unparseable` | the model returned no usable output: blocks unmerged, original text |
| `not_processed` | page not sent for alignment (front or back matter outside the pair, and the exclusions above) |

### Block `aligned` / `align_state`

| `align_state` | `aligned` | meaning |
|---|---|---|
| `aligned` | true | has an `align_id`; the counterpart block in the other file has the same id |
| `unpaired` | false | the page was aligned, but the model found no counterpart for this block (`align_note` says why: `no_counterpart`, `junk` or `page_furniture`) |
| `page_failed` | false | the page's `align_status` is `alignment_failed` or `unparseable` |
| `not_processed` | false | the page was not sent for alignment |
| `no_text` | false | the OCR block has no text (figure, diagram, empty header) |

A target page that is `not_processed` or failed as its own page can still hold `aligned` blocks: in
window mode a target page is also seen by the neighbouring English pages' tasks. So test `aligned` on the
block, not the page status.

Counts in `align_summary` and `alignment.summary` are in original OCR blocks (`members`), not merged
blocks. Across the whole delivery: 101,725 OCR text blocks on pages that were sent for alignment;
96,367 aligned (94.7%), 3,113 unpaired (3.1%), 2,245 on failed pages (2.2%).

Figures, diagrams, page headers and footers were never transcribed by the OCR. They appear as blocks with
empty `text` and `align_id: null`, so the full page layout can still be drawn.

---

## 3. How it was produced

1. **OCR (by the data provider).** Each PDF page was split into layout blocks with a label, a box and
   text. Math is in LaTeX and tables are in HTML.
2. **Page pairing.**
   - Page-aligned books were paired page by page.
   - AP bilingual books were paired as English odd page ↔ next Telugu page, from page 13.
   - For books whose pages drift, each English page was mapped to a target page using shared numbers and
     LaTeX, with an order-preserving path through both books. On books where the true mapping is known,
     this mapper was 96–99% exact and 98–100% within ±1 page; chapter starts land within ±1 (22/22).
     Each English page was then sent with target pages *m*−1 … *m*+1.
3. **Align + correct (one request per English page).** Gemini returns:
   - **units**: English block IDs ↔ target block IDs, 1-1, 1-many or many-many, never forced;
   - **unaligned blocks**, with a reason;
   - **minimal edits**: exact find → replace on one block;
   - **flags** for the reviewer.

   The model never rewrites whole text. It returns IDs and small edits, and the text is rebuilt in code.
4. **Code guards** (not the model) decide which edits are applied (section 4).
5. **Retries.** Pages failing the alignment checks were re-run twice: 269 → 153 → 116 still failing.
6. **Paragraph merge.** The model often pairs the pieces of a paragraph that the OCR split (a sentence
   and the equation that completes it, a list and its intro, a paragraph continuing overleaf) as
   separate units. Consecutive units are joined into one segment when they belong to one paragraph,
   judged on the English side:
   - Never join across headings or into a new example, question or numbered item.
   - Displayed equations join the text before them.
   - Units are joined when the sentence has not ended (`… as`, `… -`) or the next piece continues it
     (`∴ …`, `where …`, a lowercase start).
   - The join is applied to both languages at once.
   This reduced 42,309 model units to 30,192 segments. The finer unit-level version is kept
   separately (`aligned_unit_level`).
7. **Export.** For every segment, its blocks on each side are merged into one block per page.
   - In window mode a target block can appear in up to 3 requests. It keeps the unit from the request
     where its page was the mapped page (759 such overlaps resolved).
   - Target text comes from that same request.

Prompt, scripts and the per-page results are kept in the project repository (`prompts/align_correct_v4.txt`,
`scripts/align_correct.py`, `scripts/export_aligned.py`).

---

## 4. What "corrected" means

`text` contains only the edits that passed the automatic checks. Edits applied:

| Edit type | Applied | What it is |
|---|---|---|
| `ocr_text` | 3,077 | OCR slips in prose: `eqully` → `equally`, `यमुना` → `नमुना`, run-together words |
| `ocr_math` | 2,102 | wrong or stray symbols and digits in LaTeX, broken brackets |
| `structure` | 2,476 | target layout made to follow the English (list markers, line breaks, `$`/`$$`, bold). Layout only |
| `ocr_repetition` | 241 | filler or looping repetition removed |
| `ocr_hallucination` | 95 | text invented by the OCR (e.g. "[Image of …]") removed |
| `translation_fix` | 105 | a number or symbol substituted, where the English confirms the new value (e.g. an answer key `2/9` → `4/9`) |

The checks that protect the reference text:
- **OCR fixes must look like OCR slips.** Each changed word must stay similar, character by character, to
  the original.
- **No copying the other language.** An edit that only adds or removes a symbol so that one language
  matches the other is not applied, because it may be a real difference between the two books.
- **Structure edits change layout only.** Letters, digits, math and punctuation must be identical before
  and after; this is checked in code.
- **Translation fixes are applied only when checkable.** That means a number or symbol substitution
  confirmed by the English. **Word-level translation fixes are never applied**; they become flags with the
  suggested correction.
- **Pages whose alignment failed apply no edits at all.**

Everything not applied is kept in `flags` (3,615 block-level notes) for a human reviewer, together with
any translation differences the model noticed.

---

## 5. What has been checked

**Automatic checks, all files, all passed:**
- every raw OCR block appears exactly once per page;
- member boxes are identical to the raw boxes;
- each `bbox_xyxy` is the union of its members;
- every `align_id` exists on both language sides.

**Visual spot check:** one page pair of each mode was drawn as boxes and looked correct. Paragraph
merging was checked on sample pages, e.g. MH9 p51 ("Method II" and its 6 pieces become one segment)
and MH10 p11 ("… from equation (II) as" joined with its equation).

**Human check: limited so far.** An annotator reviewed the alignment of 16 pages (MH class 10, ch. 5,
EN–MR) and reported it correct. **The applied edits and the flags have not been human-verified at scale.**
Treat this package as pre-annotation for human verification, not as a final reference.

---

## 6. Using it

### Reading aligned pairs (Python)

```python
import json
pair = "MH10_1_en-mr"
en = json.load(open(f"aligned/{pair}/CLASS-10/MH_EN_10_1.json"))
mr = json.load(open(f"aligned/{pair}/CLASS-10/MH_MR_10_1.json"))

def by_id(book):
    out = {}
    for page in book["pages"]:
        for b in page["blocks"]:
            if b.get("align_id"):
                out.setdefault(b["align_id"], []).append((page["page"], b))   # >1 entry if the unit spans pages
    return out

E, M = by_id(en), by_id(mr)
for aid in E.keys() & M.keys():
    en_text = "\n\n".join(b["text"] for _, b in E[aid])
    mr_text = "\n\n".join(b["text"] for _, b in M[aid])
```

For the bilingual AP books, both sides are in one file. English blocks are on odd pages from 13 on, and
Telugu blocks are on the following even page.

### Drawing a page

Draw `bbox_xyxy` on the page image named in `image`; coordinates are pixels at `width` × `height`. To show
the original OCR boxes inside a merged block, draw `members[*].bbox_xyxy`. Blocks with the same
`align_id` in the two files are translations of each other, so give them the same colour.

---

## 7. Known limitations

- **Page images are not included.** The images named in `image`, and the source PDFs, were not part of
  the OCR delivery. A viewer needs them from the data provider.
- **116 English pages failed alignment** after two retries: 114 `alignment_failed` and 2 `unparseable`,
  mostly in window-mode books. They are listed in `failed_pages.tsv`, with the check that failed (usually
  "a target block used in two units"). Their blocks are unmerged and their text uncorrected, so they need
  manual alignment.
- **Window-mode books** (KT, PUN, TM, GUJ, NCERT) have coarser, slightly less reliable alignment than
  page-aligned books. A unit near a page edge can be missed when its counterpart falls outside the 3-page
  window.
- **NCERT Hindi** may come from a slightly different edition than the English. Hindi chapters run 0–4
  pages longer, and one chapter (1213) has an extra section.
- **Figures and diagrams are not transcribed.** Text references to figures have no figure content.
- **The model labels its own confidence** (`align_confidence`). This is useful for prioritising review,
  but it is not a calibrated probability.
