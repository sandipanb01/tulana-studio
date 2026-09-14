# Export

The same pairs, shaped for whatever comes next. Choose what to include, then
pick a format.

Drafts are never exported. Pairs marked *excluded* are left out unless you ask
for them.

## The formats

**JSON Lines** — one pair per line. What a training pipeline reads.

**JSON** — a single document with a header describing the corpus.

**CSV** — opens in Excel, Sheets or pandas.

**TSV** — tab separated. Safer than CSV when the text contains commas, which
textbook prose does constantly. Tabs and newlines inside a cell are replaced so
the format cannot break.

**Plain text** — source and target line by line, a blank line between pairs. For
reading, or for a quick eyeball check.

**TMX** — translation memory. Opens in OmegaT, memoQ and Trados. Use this if a
human translator will work with the corpus.

**XLIFF** — the interchange format most CAT tools accept.

**Markdown** — a readable table, for a paper or a review thread.

**Moses / fairseq** — two files aligned line by line, `corpus.english` and
`corpus.marathi`, where line *n* of one translates line *n* of the other. The
classic MT training input. Newlines within a pair become spaces, because the
format is one segment per line; use JSONL if you need the paragraph breaks.

**COCO** — the blocks with their boxes, for training a layout model.

**Hugging Face datasets** — JSONL in the `translation` shape, ready to push.

**Cropped images** — the parallel PNGs, one folder per pair, with a
`manifest.jsonl` giving each file its pair, side, language, page, the fraction
of the page it covers, and the text the parser read there. Every other format
names the same files in `source_images` and `target_images`, so a JSONL row and
its pictures can be matched without guessing the convention.

## The full bundle

**Download the full bundle** gives every format at once, **the cropped images**,
plus a **dataset card**
— what the corpus is, how many pairs in which languages, how a pair was made,
and what the text is and is not. Attach it when you share the corpus; a
recipient who reads only the card should still use the data correctly.

## What the text is

`source_text` and `target_text` are what the **parser** read inside the selected
blocks, joined in reading order. They are not a human transcription.

Say this plainly to anyone you give the corpus to: **the alignment is a human
judgement and the characters are machine-read.** Treat the pairing as reliable
and the text as needing review before the corpus is used as a reference. The
dataset card says so too.
