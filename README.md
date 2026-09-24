# Tulana Studio

A workspace for building **parallel corpora from Indian school textbooks**. The
English edition and its translation open side by side with the blocks a document
parser has already found on each page. You check that the two sides say the same
thing, correct the text where it is wrong, and export the result in whichever
format the next tool needs.

Board-, class-, subject-, language- and script-agnostic. Adding a state board or
a regional language is a row of data, never a code change.

The project ships **two workspaces over one database**:

| | | for |
|---|---|---|
| **सेतु Setu** | `/work/` | reading and correcting the two texts side by side — the annotator's daily tool |
| **the studio** | `/studio/` | the page image with its blocks overlaid, and cutting parallel crops from the PDFs |

They are the same corpus, the same `state/` folder and the same export machinery
seen from two angles. Setu is where the text is judged; the studio is where the
page is looked at. Most annotators only ever need Setu.

> **About the figures in this document.** Numbers describing the *shipped
> registries and the studio* are the project's own long-standing figures.
> Numbers describing *the ingested Setu corpus and the test suites* were
> re-measured on 25 September 2026 against `state/studio.db` and by running each
> suite; they are marked **(measured)** and the measuring conditions are stated.
> Where the two disagree, both are shown rather than one quietly overwriting the
> other.

---

## Before anything else

```bash
git clone https://github.com/sandipanb01/tulana-studio.git
cd tulana-studio
git lfs install && git lfs pull      # the PDFs are LFS objects — see below
cd tulana
python3 -m pip install -r requirements.txt
python3 check_install.py             # says exactly what, if anything, is wrong
```

Then start **one** of the two, or both at once:

```bash
python3 launch_annotation.py         # both: Setu at /work/, the studio at /studio/
python3 app.py                       # the studio alone — http://localhost:7862
```

`check_install.py` is the first thing to run after any clone, pull or push. It
reports missing modules, an interface that does not match its backend, PDFs that
are really Git LFS pointers, and a layout corpus it cannot find — each with the
command that fixes it. **24 checks (measured.)**

`git lfs install` has **no `-q` flag.** Writing `git lfs install -q` fails with
`unknown shorthand flag: 'q' in -q`, and in an `&&` chain that failure silently
skips the `git lfs pull` that follows — so every PDF stays a pointer, no page
renders, and the crop tool reports nothing to cut. One wrong flag, five symptoms.

### The PDFs are Git LFS objects, and this bites

`board_pdfs/` holds 150 PDFs, about 600 MB, stored through Git LFS. A clone
**without** `git lfs pull` leaves a 132-byte text pointer where each PDF should
be:

```
version https://git-lfs.github.com/spec/v1
oid sha256:798d2f27d45d2ccda3694005c2ed60bc0b413b8b299f3a5d4ade7c5867094896
size 6254823
```

Right name, right extension, so `find … | wc -l` still counts 150 and everything
*looks* present. The pages then render blank with no obvious cause.

```bash
find board_pdfs -name '*.pdf' | while read f; do
  head -c 5 "$f" | grep -q '%PDF-' || echo "POINTER: $f"
done
```

GitHub's free LFS allowance is 1 GB of storage and 1 GB of bandwidth a month.
**Two full clones exhaust it**, after which every clone silently receives
pointers again. If more than a couple of people will clone this, the PDFs belong
on shared storage rather than in Git.

**What still works without the PDFs.** Setu's text view, all editing, every
answer, the database and all eleven exports need only the parsed layout — which
is ordinary JSON in Git, not LFS. Only the page image, the block overlay and the
cropped images need the PDFs. That is why Setu opens on text and treats the page
picture as the optional second view: the tool has to be useful on a checkout
where the LFS budget ran out.

---

## Repository structure

```text
tulana-studio/
├── board_pdfs/                  the original textbook PDFs (Git LFS)
│   ├── Boardwise_PDF_class10_Maths/CLASS-9/MH_EN_9_1.pdf
│   ├── CLASS-10/KER_ML_10_1.pdf
│   └── dataset/input/eng/10/1001.pdf
│
├── board_outputs/output/        the parsed layout, one JSON per book
│   ├── Boardwise_PDF_class10_Maths/CLASS-9/MH_EN_9_1.json
│   └── CLASS-10/KER_ML_10_1.json
│
└── tulana/                      the application
    ├── app.py                   the studio (FastAPI, port 7862)
    ├── launch_annotation.py     both workspaces on one port, with a share link
    ├── config.py  db.py  library.py  pdflib.py  sources.py
    ├── blocks.py                the parsed-layout corpus
    ├── pairs.py                 saved pairs and export (studio)
    ├── layout.py                layout annotation (API only)
    ├── shelf.py                 register a newly added PDF
    ├── check_install.py         is this checkout complete?
    ├── test_*.py  windows_check.py  selftest.py
    ├── share_gradio.py
    ├── docs/                    the studio's six manuals
    ├── static/                  the studio's front end
    │
    └── annotation/              सेतु Setu
        ├── api.py               47 routes under /api/setu (measured)
        ├── core/
        │   ├── corpus.py        books, chapters, segments
        │   ├── store.py         schema, revisions, pagination
        │   ├── models.py        the seven statuses
        │   ├── align.py         pairing the two editions
        │   ├── annotate.py      answers and history
        │   ├── exporters.py     eleven formats + the bundle
        │   ├── sources.py       page images and crops from the PDFs
        │   └── search.py  ids.py  workspace.py
        ├── ui/
        │   ├── app.py           the Gradio fallback interface
        │   ├── browse.py        the two-document model
        │   ├── workspace.py  panels.py  render.py  session.py
        │   └── static/work/     the workspace served at /work/
        │       └── index.html  app.js  style.css
        └── docs/                01_manual.md  02_faq.md  03_for_developers.md
```

**The two data folders are joined by `relpath`.** Each layout JSON names the PDF
it was parsed from, and that path matches `board_pdfs/` exactly. 152 books of
layout; 144 of them map onto a PDF that is present.

Both workspaces find both folders themselves — including `board_outputs/output/`
nested a level deeper — and ignore the `__MACOSX/._*.json` resource forks a macOS
zip leaves behind. `tulana/data` is optional; set `TULANA_DATA_DIR` if you keep
the PDFs somewhere else.

**A note on five similarly-named files.** `tulana/app.py` is the studio;
`tulana/annotation/ui/app.py` is Setu's interface. `annotation/core/workspace.py`
holds logic and imports no Gradio; `annotation/ui/workspace.py` holds the
handlers and does. `tulana/static/` is the studio's front end;
`tulana/annotation/ui/static/` is Setu's. Copying one over the other is the
single easiest way to break this checkout, and `check_install.py` is written to
notice when it has happened.

---

## सेतु Setu — the parallel workspace

```bash
python3 launch_annotation.py
```

Open `http://localhost:7862/`. It redirects to `/work/`. Four tabs: **Annotate ·
Saved work · Download · Guide**.

Setu is **text first**. Two editions of the same textbook open as two columns of
readable, scrollable text — not two page images. That is the view an annotator
spends the day in, it works when the PDFs are pointers, and it is the view in
which a translation can actually be compared sentence by sentence.

### Annotate

Pick a board, a class, a subject, then the language and edition on each side, and
press **Open side by side**. The left column is usually English; the right is the
language being checked.

**The two sides are independent.** This is the heart of the design, and it comes
from measurement rather than taste. Translated text is longer, editions are
typeset differently, and chapters do not begin on the same page:

| textbook | chapter-start drift, English → translation | chapters |
|---|---|---|
| Karnataka 10 Kannada | −3, 0, +3, +6, +7, +8 | 13 vs 16 |
| Punjab 10 Punjabi | 0, +10, +23, +26 | 43 vs 48 |
| Gujarat 10 Gujarati | −114, −112, −111, −107 | 27 vs 20 |
| Kerala 10 Malayalam | — | 11 vs 8 |
| NCERT 11 Hindi | no chapter starts on the same page at all | |
| Tamil Nadu 10 Tamil | no chapter starts on the same page at all | |

*(measured across the ingested corpus)*

A single page counter cannot express any of that. So each side gets its own
chapter dropdown, its own page box with **‹** and **›**, and its own scrollbar —
and there are **common controls** for moving both together when they do happen to
agree. A checkbox, *Turn both pages together*, locks them at whatever offset they
currently have; a live indicator shows what that offset is. **⇄ These two pages
match** records the offset for the project, so the next session opens where this
one left off.

Because two editions rarely have the same chapter list, Setu never assumes they
do. It offers both lists, separately, and lets the annotator decide which chapter
on the left belongs against which chapter on the right.

**Two views.** *Text* is the default. *Page + blocks* shows the scanned page with
the parser's blocks overlaid, labelled and coloured by type — the studio's view,
inside Setu, for when the text alone is not enough to judge a table or a formula.
The switch is one button and the selection survives it.

**Two modes.** *Read* is the default, and nothing typed can change the text.
*Correct it* makes each block editable in place. Type the correction, click away,
and it saves — the row is outlined, marked *saved*, and tagged `corrected`
immediately. There is no save button to forget.

The editor is never the record. What is displayed is a view of the row; the row
itself carries a revision number, and a save that arrives against a stale
revision is rejected rather than silently overwriting someone else's correction.
This is a lesson borrowed at some cost from other annotation tools, where making
the visible textarea the canonical input has lost people their work.

**Two tools, in the *Page + blocks* view.** *Click a block* takes what the parser
found and brings its text with it. *Drag to crop* takes what **you** decide: draw
a rectangle over the passage, drag inside it to move, the corner to resize, **×**
to remove. A figure with its caption may be one passage to a reader and three
blocks to the parser — and a hand-drawn diagram or a margin note was never a
block at all, so no amount of clicking would reach it.

**Seven answers**, bound to the number keys:

| key | answer | means |
|---|---|---|
| `1` | Exact | the two sides say the same thing; nothing needs changing |
| `2` | Needs correction | they mostly match, but the text is wrong somewhere — a typo, a wrong number, a garbled formula |
| `3` | Missing or incomplete | part of the text is missing on one side, or one side is empty |
| `4` | Structural mismatch | both have text, but they are not the same piece of the book |
| `5` | Unclear | you cannot tell; leave it for a reviewer |
| `6` | Not applicable | a page header, a caption, a decoration |
| | Not checked yet | the state every row starts in |

Zoom per pane, a draggable split, a filter by block type, an optional *Dim the
rest*, and a legend built from the corpus itself. `n` jumps to the next block
nobody has answered; `e` swaps Read and Correct it; `c` swaps Click and Crop;
`←` and `→` turn both pages, `Alt` with them turns only the left and `Shift`
only the right; `Ctrl` held down hides the block labels; `?` lists every
shortcut. Every shortcut is suppressed while you are typing, so a `1` inside a
correction is a digit and not an answer.

### Saved work

Everything answered, filterable by status, refreshable, and showing what was
actually stored rather than what the interface believes it sent. The point is
that a correction is verifiable within seconds of making it.

### Download

Eleven formats from the same rows **(measured — the registry in
`annotation/core/exporters.py`)**:

**JSONL** · **JSON** · **CSV** · **TSV** · **XML** · **plain text** ·
**TMX** (OmegaT, memoQ, Trados) · **Moses/fairseq** · **Excel `.xlsx`** ·
**Parquet** · **Hugging Face dataset**

Plus **every format at once as a zip**, with a dataset card describing what the
corpus is, how a row was made, and what the text is and is not. Scope the export
to everything, to what has been answered, or to a single status.

Export filenames are built from a sanitised stem, never from raw project text,
and the written path is asserted to resolve inside `state/exports` — a project
named `../../../../tmp/evil` exports to a file in the exports folder with a safe
name, and there is a test that says so.

### Guide

The manual and the FAQ, served from `annotation/docs/`, with a navigation pane.
Written for someone who has never annotated anything: what the four tabs do, what
each of the seven answers means, what to do when the two sides plainly do not
correspond, and why the page numbers on screen are one higher than the ones in
the database.

### What is saved, and when

Every answer, every correction and every page link goes to SQLite as it happens.
There is no in-memory draft that a closed tab loses.

**Corrections never destroy the original.** `setu_segment.source_text` is what
the parser read, and the annotation path never writes to it. A correction is a
row in `setu_text` with its own revision, and `setu_rev` keeps the history. *Put
back what the parser read* restores the original because the original was never
gone. Provenance survives the annotator, which is the only way a corpus stays
auditable.

---

## The studio — four tabs

```bash
python3 app.py            # or /studio/ under launch_annotation.py
```

### Blocks

Choose a board and class, then the target language, then the two editions. Both
pages open side by side with their blocks overlaid, each labelled and coloured
by type, numbered in reading order.

**Two tools, because they answer different questions.**

*Click blocks* takes what the parser found and brings its text with it.
Shift-click takes a range in reading order. *Drag to crop* takes what **you**
decide: draw a rectangle over the passage, drag inside it to move, the corner to
resize, **×** to remove.

Both work across pages, both are kept automatically, both are cut as parallel
images, and both can be used in the same pair. The extracted text of the
selected blocks appears underneath, both languages at once.

**Your selection survives turning the page.** Translated text is longer, so a
passage that fits one English page often runs onto the next in Marathi — a
selection confined to a single page could not express that alignment at all. The
panel tells you when blocks are selected on pages you are not looking at, so
nothing is ever silently included.

Zoom per pane, a draggable split, a filter by block type. 30 block types come
from the corpus itself.

**The parallel images are cut as you go.** Every rectangle you draw, and the
region around the blocks you clicked, is rendered from the original PDFs at
300 DPI. One image per page a side touches — a single image cannot span a
page break, and one that silently showed only the first page would be worse than
two honest ones.

**Nothing is lost if you stop.** The selection *and its images* are written to
the server about a second and a half after you stop clicking, and again as the
tab closes. It says *Kept automatically* — and says so plainly if it could not.
A draft already has its pictures; nothing waits for a manual save.

### Saved pairs

Everything you have saved, **with the cropped images shown side by side**. That
is the point: reading Devanagari against English in two columns of plain text
tells you little, while the two passages as they appear in the books tell you
immediately whether the alignment is right.

Filter by textbook, language or status, or search the text in either language.
Rename, approve, exclude, delete. Where a PDF was missing when a pair was saved,
**Try again** cuts the images once it arrives.

**Open in Blocks** puts the selection back on the pages it came from, so a
correction is an adjustment rather than starting again.

A pair keeps its own copy of the text, not just a reference to the blocks.
Re-running the parser renumbers every block; a pair you approved must not
quietly change what it says because the corpus was reloaded underneath it. It
also keeps each block's page and reading position, and uses those to re-resolve
a pair whose ids no longer exist.

### Export

Twelve formats from the same rows:

**JSONL** · **JSON** · **CSV** · **TSV** · **plain text** · **TMX** (OmegaT,
memoQ, Trados) · **XLIFF** · **Markdown** · **Moses/fairseq** · **COCO** ·
**Hugging Face datasets** · **Cropped images**

The images export is one folder per pair with a `manifest.jsonl` giving each
file its pair, side, language, page, the fraction of the page it covers and the
text found there. Every other format names the same files in `source_images`
and `target_images`, so a JSONL row and its pictures match up without guessing
the convention.

Plus the full bundle — every format at once, the images, and a dataset card
describing what the corpus is, how a pair was made, and what the text is and is
not.

Drafts are never exported. Pairs marked excluded are left out unless you ask.

### Guide

Six manuals, served from `tulana/docs/`.

**Why two export lists.** The studio exports *pairs of cropped regions* — so it
has COCO and an images folder, which only mean something when there are pictures.
Setu exports *rows of judged text* — so it has Parquet and `.xlsx`, which only
mean something when there are columns. Neither list is a subset of the other, and
merging them would produce formats that are empty half the time.

---

## What the text is

`source_text` is what the **parser** read inside a block, joined in reading
order. It is not a human transcription.

Say this plainly to anyone you give the corpus to: **the alignment is a human
judgement and the characters are machine-read.** Treat the pairing as reliable
and the text as needing review before the corpus is used as a reference. The
dataset card says the same.

A block over a diagram carries no text, and a page without a usable text layer
yields none. Empty means *not recovered*, not *empty on the page*.

Setu adds a second layer on top of that: where an annotator has corrected a row,
the export carries **both** — the machine-read original and the human-corrected
text, with the revision that produced it. A consumer can take whichever it
trusts, and can tell them apart, which is not true of a corpus that overwrites.

---

## The data model

Three conventions run through both workspaces. Getting any of them wrong
produces errors that look like something else entirely, so they are stated here.

**A box travels as a fraction of the page.** `fx0, fy0, fx1, fy1` are in 0–1.
Pixels exist only at the two endpoints: the parser measured against one raster
(commonly 1654 × 2339, A4 at 200 DPI), the browser draws the page at whatever
width the pane happens to be, and a crop is cut at 300 DPI. None of the three
needs to know about the others. On screen the overlay is positioned against the
image's **measured** `clientWidth`, never an assumed one, which is why it stays
correct at any zoom and in any window.

**Pages are stored 0-indexed and displayed 1-indexed.** `setu_segment.page`
matches PyMuPDF's `doc[page]`, so page one of the book is `0`. This was verified
across the whole corpus — `max(page) == num_pages - 1` for all 121 books, none of
them 1-indexed. People count from one, so the conversion happens in exactly one
place per interface: `to_display()` / `from_display()` in `browse.py`, `shown()` /
`stored()` in `app.js`. `test_browse.py` contains eight tests whose only purpose
is this off-by-one.

**Blocks are typed twice.** `kind` is the coarse type used for colour and
filtering — 23 values in the ingested corpus. `label` is the richer one the
parser emits — 29 values, including *Solved-example*, *Sub-section-title* and
*Question*. The underlying model is DocLayNet-trained; its official eleven
classes (`Caption, Footnote, Formula, List-item, Page-footer, Page-header,
Picture, Section-header, Table, Text, Title`) are visible underneath. DocLayNet's
`precedence` field is the redundant-annotator index, **not** reading order —
DocLayNet provides no reading order, so reading order here is synthesised from
geometry and should be treated as a strong hint rather than ground truth.

**The ingested corpus, measured 25 September 2026:**

| | |
|---|---|
| books | 121 |
| segments | 132,678 |
| pages | 11,573 (11,553 carry at least one segment) |
| boards | 9 — AP, GJ, KA, KL, MH, NCERT, PB, TN, WB |
| languages | 10 — Bengali, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Punjabi, Tamil, Telugu |
| classes | 9, 10, 11, 12 |
| scripts | 9 |
| block kinds | 23 · block labels 29 |
| Setu tables | 14, plus an FTS5 index over segment text |

That is what has been *ingested*. What the code *supports* is the shipped
registry below — 32 boards and 23 languages — and nothing in the code names any
of them.

**One measured alignment, for calibration.** Maharashtra class 10,
English ⇄ Gujarati, 2,304 rows: 1,641 two-sided (71.2%), 663 one-sided (28.8%),
and of the paired rows 1,514 on the same page (92.3%). Median segment, 89
characters. The one-sided quarter is structural, not a bug — this tool's job is
to *surface* those rows for a human, not to silently invent a partner for them.

---

## A shareable link

```bash
python3 launch_annotation.py        # Setu and the studio, with a public link
python3 share_gradio.py             # the studio alone
```

Either prints an `https://….gradio.live` address. **That bare address is the one
to share** — it opens the annotator's workspace directly, with no path to append
and nothing to explain. `/studio/` and `/work/` are reachable beneath it for
anyone who wants the other tool, and `/?stay=1` opens the Gradio interface
instead of redirecting, which is the fallback when a browser or a corporate proxy
will not serve the static workspace.

Annotators need nothing installed. The link is a tunnel — the database and images
stay on the host, so a restart never loses work, only the address changes. Gradio
links last about a week; for a permanent address, put the studio behind nginx.

Both `/studio` and `/studio/` work, assets are fingerprinted so a deployed change
cannot be served stale, and the port walks forward if 7862 is busy.

### Running it on Colab

A Colab cell ships with the repository. Three things in it are not obvious, and
each was a real failure before it was a line of code:

- **Never `git pull`.** It fails on a dirty tree and on a detached HEAD, which is
  exactly the state a stopped-and-restarted notebook is in.
  `git fetch -q origin main && git checkout -q -f -B main origin/main` recovers
  from a dirty tree, a deleted file, a detached HEAD and no clone at all — and it
  is *not* `git clean`, so an untracked `state/` full of annotations survives.
- **Never `pkill -f`.** The pattern matches its own command line and the
  invoking shell's, so it kills the cell that ran it. Stale servers are stopped
  by walking `/proc/*/cmdline`, building the ancestor set from `PPid:`, and never
  signalling an ancestor.
- **The database stays local and is copied to Drive.** Drive's FUSE layer does
  not provide the file locking SQLite needs, and WAL mode on it can corrupt.
  `sqlite3.Connection.backup()` runs against a live database, so a copy is taken
  every couple of minutes without stopping anyone's work.

The cell scans the corpus once and caches the result to Drive behind a content
hash, so a re-run does not re-fetch the LFS objects. (`git lfs ls-files -s` sums
to **1,497 MB** — more than GitHub's whole monthly free allowance. One pull
spends the month.)

---

## Adding a board, class, subject, language or script

Nothing in the code names one. **32 boards, 23 languages and 12 scripts** ship as
seed data; more are added with `POST /api/registry` or a row in `config.py`.

Name a file so the studio can place it. All of these work:

```
KER_ML_10.pdf                       BOARD_LANG_CLASS
Kerala_Class10_Malayalam_Maths.pdf  written out
kerala-class-9-malayalam.pdf        hyphenated
SCERT_Kerala_Std10_Malayalam.pdf    Std, Grade, Class
Kerala_Class_X_Malayalam.pdf        roman numerals
Kerala/Class 10/Malayalam/maths.pdf folders instead of a long name
```

Board and language codes overlap — `guj` names both Gujarat and Gujarati, `pun`
both Punjab and Punjabi — and that is handled: the board token is identified and
consumed before languages are read.

Where a name says nothing, the parser's own text is used as evidence. The script
is measured from the characters, and for a script shared by several languages,
orthographic markers decide between them — `आहे` appears throughout Marathi and
never in Hindi; `ৰ` is Assamese where Bengali writes `র`. Validated against every
book whose language the file name already gives: **124 correct, 28 abstained,
0 wrong.** Anything undecidable is left unset rather than guessed.

Registering a PDF by hand:

```bash
python3 shelf.py doctor
python3 shelf.py add FILE --board WB --class 10 --lang Bengali
```

A newly added board needs no migration on the Setu side either: `setu_book` keys
a book by a derived `book_key`, a project is a pair of book keys, and every
dropdown is a `SELECT DISTINCT` over what is present. A board added tomorrow
appears in the interface the moment its PDF is registered and its layout ingested.
`test_stress.py` invents an Odisha Class 8 Odia book to prove exactly this
resolves end to end.

---

## Tests

```bash
python3 check_install.py     is this checkout complete and consistent
python3 test_pairs.py        cross-page selection, cropping, autosave, every format
python3 test_stress.py       edge cases, malformed input, database safety
python3 test_blocks.py       every book in the layout corpus
python3 test_naming.py       32 boards × 23 languages × naming styles
python3 windows_check.py     cross-platform audit
python3 -m unittest test_annotation test_browse test_workspace   # Setu
```

| suite | project baseline | measured 25 Sep 2026 | |
|---|---|---|---|
| `check_install.py` | 22 | **24** | grew with Setu |
| `test_pairs.py` | 113 | **95** | fewer: crop checks need real PDFs |
| `test_stress.py` | 138 | **121** | fewer: seeded-pair check needs real PDFs |
| `test_blocks.py` | 645 | **645** | identical |
| `test_naming.py` | 265 | **265** | identical |
| `windows_check.py` | 8 | **8** | |
| `test_annotation.py` | — | **123** | Setu core and API |
| `test_browse.py` | — | **46** | the two-document model |
| `test_workspace.py` | — | **19** | page geometry, proved against a real PDF |
| | **1,191** | | the baseline, on a checkout with its PDFs |

The baseline suites are run twice interleaved to prove they do not depend on
order.

**The two failures in the measured column are both the LFS pointers**, on the
sandbox this was measured in: `check_install.py` reports *150 of the PDFs checked
are not real PDFs*, so `test_pairs.py` cannot cut an image and `test_stress.py`
cannot seed a pair against a document that was never registered. The check that
matters for data safety — *every pre-existing table is byte-identical after a
full run* — passes. On a checkout where `git lfs pull` has succeeded, both suites
run their full set.

`windows_check.py` reports **5 passed, 3 issues** today. All three are the
auditor matching deliberate attack strings inside the security tests
(`"../../../../tmp/evil"` is a payload, not a path the code uses) and the
presence of `run.sh`. They are left visible rather than silenced: an auditor
tuned until it is quiet has stopped being an auditor.

`test_stress.py` feeds in malformed JSON, zero-size pages, inverted boxes,
non-numeric coordinates, null bytes and emoji; asks for pages beyond the end of
a book and negative pages; selects 5000 blocks at once; and checks box placement
at 72 and 150 dpi.

`test_workspace.py` builds a real three-page A4 PDF with marks at known
fractions of the page and asserts that asking for a fraction cuts the region it
names — all four quadrants exact, unchanged at 150% zoom, and the three pages
hashing differently so a page-number slip cannot pass. `test_browse.py` keeps
eight tests whose only job is the 0-indexed/1-indexed boundary, including one
that feeds the page box a float, because `gr.Number` sends `3.0` even with
`precision=0` and `int("3.0")` raises.

---

## The annotation database is protected

`blocks.py`, `pairs.py` and `layout.py` create their own tables with
`CREATE TABLE IF NOT EXISTS` and never write to `documents`, `projects`,
`clips`, `pairs`, `labels`, `pair_labels`, `exports` or `audit`. No `ALTER`, no
`DROP`.

This is proved two ways rather than asserted: the tests read each module's source
for writes to those tables, and they seed a project and a pair, run everything,
and hash all eight tables before and after. If a future change ever writes to one
of them, the test fails.

**Setu is held to the same rule and tested the same way.** Every table it owns is
prefixed `setu_`; `test_browse.py` and a source scan in `test_annotation.py`
assert that no destructive DDL exists anywhere in the `annotation` package. The
two families of tables share a file and never share a row.

`shelf.py` is the deliberate exception — registering a document is its whole
purpose — and it only inserts a row or updates the metadata columns of one it
matched by path, so an existing document keeps its `id` and no saved work can be
orphaned.

**Earlier work is not deleted.** PDF clipping and hand-drawn layout annotation
were removed from the *interface*, not from the database. Everything they saved
is untouched and still reachable through the API.

**User text never becomes a filesystem path.** Export names are sanitised and the
resolved path is asserted to stay inside `state/exports`. The page-link key is
derived from the project id, never from anything typed. Page and crop requests
take numbers, clamp them to the book, and resolve into the page cache or fail
with a sentence — never with a traceback and never outside the cache directory.

---

## Windows, Linux, macOS

Python 3.10 or newer. **No PowerShell, no bash, no Node, no build step, no
database server, no external binaries.** `.zip` and `.7z` are both read in pure
Python.

The interpreter is `py` (or `python`) on Windows and `python3` on Linux and
macOS — Debian and Ubuntu ship no `python` command at all. That naming is the
only difference; the files are identical.

`windows_check.py` audits what works on Linux and fails on Windows: hard-coded
POSIX paths, text files opened without an explicit encoding (Windows defaults to
cp1252, which cannot read Devanagari), shell invocation, filenames that are
illegal on Windows, and any OS-specific separator reaching the database.

---

## Configuration

| variable | meaning | default |
|---|---|---|
| `TULANA_DATA_DIR` | where the PDFs live | discovered |
| `TULANA_STATE_DIR` | database, page cache, exports | `./state` |
| `TULANA_DB` | the database file | `state/studio.db` |
| `TULANA_CROPS` | the cropped images | `state/crops` |
| `TULANA_EXPORTS` | written exports | `state/exports` |
| `TULANA_PAGES` | rendered page cache | `state/pages` |
| `TULANA_HOST` | bind address | `0.0.0.0` |
| `TULANA_PORT` | preferred port | `7862` |
| `TULANA_VIEW_DPI` | on-screen page resolution | `110` |
| `TULANA_CROP_DPI` | resolution the parallel images are cut at | `300` |

Back up `state/`. That folder is the annotators' work — the database and the
cropped images in `state/crops`; the PDFs and the layout can always be fetched
again.

Crops are named by content hash, so the same passage cropped twice costs one
file. `POST /api/pairs/crops/prune` reports what no pair refers to any more;
add `?apply=true` to delete it.

---

## Troubleshooting

**Everything is blank and no pages render.** The PDFs are probably LFS pointers.
`git lfs install && git lfs pull` — and note there is no `-q` flag on
`git lfs install`; using one breaks the `&&` chain and skips the pull.

**The Blocks tab is empty.** The layout corpus was not found.
`check_install.py` says where it looked.

**A textbook is missing from the dropdown.** `GET /api/blocks/mapping` names
every book as mapped, missing or worth a look. The commonest cause is not the
file name: the **subject must match too** — a Malayalam *Science* book beside an
English *Mathematics* book will never pair.

**A page shows blocks but no image.** The layout covers that page and the PDF
does not — a truncated copy, or a different edition. The blocks and text are
still usable, and Setu's Text view is unaffected.

**A block has no text.** Diagrams carry none, and a page without a text layer
yields none. Select it anyway if it belongs to the passage; its position is
recorded and it still appears in the cropped image.

**A pair has no image.** The PDF was not on disk when it was saved — usually
`git lfs pull` away. Press **Try again** on the pair once it is there.

**A change does not appear after deploying.** Assets are fingerprinted, so this
should not happen. If a whole tab is missing, `check_install.py` says whether the
Python or the interface was the half that did not get copied.

**`address already in use`.** The studio takes the next free port and prints
which one.

**The share link opens Gradio, not the workspace.** The redirect could not reach
`/work/`. Open the link with `/work/` appended; if that 404s, the static folder
did not get copied — `launch_annotation.py` prints a loud notice saying so. A
folder literally named `"   work"` with leading spaces renders identically to
`work` in GitHub's file list and is a different directory; the launcher tolerates
it and tells you to rename it.

**The left and right pages show different chapters.** They are supposed to be
able to. Use the per-side chapter dropdowns, set the two pages so they correspond,
and press **⇄ These two pages match** to remember the offset.

**An edit did not save.** The row flashes green when it does. If it did not, the
revision was stale — someone else edited the same row — so reload and apply the
correction to the current text.

---

## Where things stand

Stated plainly, because a corpus tool that oversells itself costs more than it
saves.

**Solid.** The two-document model and its independent navigation; the 0-indexed
page boundary, verified on all 121 books; in-place editing with the original
preserved and a full revision history; the block overlay's geometry, proved
against a PDF with marks at known fractions; eleven Setu exports and twelve
studio exports; the protection of the eight pre-existing tables, proved two ways;
recovery from a dirty tree, a detached HEAD or a stopped Colab run without losing
`state/`.

**Structural, not fixable by this tool.** About 29% of rows in the measured
project are one-sided. NCERT class 11 Hindi and Tamil Nadu class 10 Tamil share
no chapter start with their English editions at all. Andhra Pradesh's bilingual
single-file PDFs put both languages in one document and cannot be paired by a
two-book model. Reading order is synthesised, because the parser does not supply
one.

**Not yet built.** A navigation pane that genuinely beats doccano's — the current
one is per-side chapter and page, which is better for *this* problem but is not a
general outline tree. The manual and FAQ render in the Guide tab from markdown
rather than being first-class interactive sections. Multi-annotator behaviour on
one shared link has not been load-tested.

**Unverified here.** Every PDF in the environment this was last measured in is an
LFS pointer, so the page overlay and the crop tool have been proved against a
synthetic PDF built for the purpose — not against a real textbook scan. That
check belongs to whoever has the PDFs.

---

## License

MIT.
