# Tulana Studio — Phase I

A workspace for building **parallel corpora from textbooks**: the English
edition and its translation, side by side, where a linguist marks the passages
that correspond and clips both.

This is a rebuild against the Phase I brief, not an extension of the earlier
verification workbench. It does one thing thoroughly.

## What an annotator does

1. Picks a board, class and target language.
2. Reads both editions in scrollable panes, side by side (stacked on a phone).
3. Drags a rectangle around a passage in English, then around the same passage
   in the target language.
4. Presses **Save pair**.

Everything else — cutting the images, naming them, keeping them identifiable,
packaging them — happens for them.

## What comes out

```
NCERT_class9_math/
    eng_ncert_math_1.png  .jpg  .pdf     the same passage,
    hin_ncert_math_1.png  .jpg  .pdf     in two languages
    …
    manifest.json    pages, rectangles, extracted text, annotator, timestamps
    pairs.jsonl      one chunk per line, for data pipelines
    pairs.csv        the same, for a spreadsheet
    parallel.tsv     just the two texts, tab separated
    README.md        a readable summary
```

The name carries everything: `eng_ncert_math_7` and `hin_ncert_math_7` are the
same passage, chunk 7, from the NCERT mathematics textbook. Every clipping is
written as PNG, JPG and a one-page PDF, each cut from the source at 300 DPI.

## Categories, in the doccano manner

Each project carries a label set — Definition, Theorem, Example, Exercise,
Activity, Table, Figure caption, Summary — every one with a colour and a
single-key shortcut, so categorising a chunk is a keystroke. Labels are stored
relationally rather than as free text, travel into every export format, and are
summarised per project alongside coverage and per-annotator counts.

## A public link

```bash
pip install gradio
python3 share_gradio.py        # prints an https://….gradio.live address
```

Annotators need nothing installed — the link works on a laptop, an Android
phone or an iPad. Clippings are written to this machine's `state/` folder, so a
new link after a restart never loses work.

## Where the textbooks come from

`sources.json` declares the corpus archives and their Drive links. The Export
tab shows what is present and offers two actions: unpack the archives already in
the data folder, or unpack and download only what is genuinely missing. Nothing
you already have is downloaded again.

## Running it

```bash
pip install -r requirements.txt
TULANA_DATA_DIR=/path/to/textbook/pdfs python3 app.py     # http://localhost:7862
```

Any folder layout works. Board, class, language and volume are inferred from
each file's own path, so `MH_MR_10_1.pdf` and `input/hin/10/1001.pdf` are both
understood. A board and class is offered once it has an English edition **and**
at least one other language.

## Design decisions worth knowing

**A clipping is a rectangle, not a screenshot.** What is stored is the page plus
the rectangle in PDF points. The PNG is cut from the source at 300 DPI when the
pair is saved. So a clipping never depends on the annotator's screen, zoom level
or device, and the whole corpus can be re-cut at a different resolution later
without anyone re-doing the work.

**Text comes along free where it exists.** The text under each rectangle is
extracted and stored beside the image. Where a PDF has a readable text layer
this yields a parallel *text* corpus at no extra effort. Where the PDF is a scan
or uses an unmapped font encoding, the field is empty — the images are still
correct, and the images are what the corpus is built from.

**Geometry is excluded, visibly.** Geometry, conics and related chapters are out
of scope. Pages that look like them are marked in the interface, the annotator
is warned, and a pair saved anyway is recorded as *excluded* rather than
silently included. Exports leave excluded pairs out unless asked otherwise.

**It works on a phone.** Pointer events throughout, so a finger behaves exactly
like a mouse; the two editions stack vertically below 900 px and the controls
move behind a menu button.

**Built to be extended.** A pair is a group of clippings joined by `pair_id`, so
a third language does not need a migration. `clips.text` already carries the
text, so a text-level export needs no re-annotation. A machine-proposed
rectangle would be a `clips` row an annotator confirms — nothing about the
storage changes.

## Documentation

Also served inside the application, under **Guide**:

- `docs/01_annotator_guide.md` — for linguists; no technical knowledge assumed
- `docs/02_admin_manual.md` — installing, adding textbooks, backups, auditing
- `docs/03_developer_manual.md` — architecture, schema, API, extension points
- `docs/04_faq.md` — troubleshooting for both audiences, and stated limits

## Checking the sources

```bash
python3 check_sources.py
```

Reports, for each configured archive, whether it is already on disk or whether
its link genuinely returns a file — following Drive's confirmation step for
large files. Run it on the host machine; that is where the answer counts.

## Testing

```bash
python3 selftest.py
```

64 checks against the real textbooks: indexing, pairing, page rendering and
caching, clipping (including that a clipping really is the requested rectangle
at print resolution and not a whole page), rejection of bad input, the excluded
path, export contents, deletion, in-app documentation and the interface itself.
