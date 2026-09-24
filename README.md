# Tulana Studio

**Parallel corpora from Indian school textbooks.** An English edition and its
Indian-language counterpart, opened side by side, corrected by a human, and
exported in eleven formats.

`Python 3.10+` · `SQLite` · `FastAPI` · `Gradio 6` · `PyMuPDF` · no build step

---

## Contents

1. [What this is](#what-this-is)
2. [Quick start](#quick-start)
3. [Tech stack](#tech-stack)
4. [Architecture](#architecture)
5. [Data model](#data-model)
6. [Setu — the annotation workspace](#setu--the-annotation-workspace)
7. [Browsing two editions that do not line up](#browsing-two-editions-that-do-not-line-up)
8. [Exporting](#exporting)
9. [Adding a board, class, subject, language or script](#adding-a-board-class-subject-language-or-script)
10. [Tests](#tests)
11. [Configuration](#configuration)
12. [Troubleshooting](#troubleshooting)
13. [Known limitations](#known-limitations)
14. [Licence](#licence)

---

## What this is

A school textbook published in English and in Marathi is, in principle, a
sentence-aligned parallel corpus that somebody has already paid to produce. In
practice it is two PDFs that were typeset by different teams, scanned at
different times, and parsed by a layout model that got some of it wrong.

Tulana Studio is the workbench that turns the second thing into the first. It
does three jobs:

| Part | What it is for |
|---|---|
| **Setu** — सेतु, *bridge* | Two editions as **editable text**, side by side. An annotator fixes what the parser misread on either side and says whether the two halves match. This is where nearly all the work happens. |
| **Studio** (`/studio`) | The original block-and-crop workbench: page images with the parser's blocks overlaid, rectangle selection across pages, parallel images cut from the PDFs at 300 DPI. |
| **API** (`/api`) | An HTTP surface over the same services, for pipelines that do not want a browser. |

Board-, class-, subject-, language- and script-agnostic throughout. Adding a
state board or a regional language is a row of data, never a code change.

**What ships in this repository:** 121 canonical parsed books (152 layout files,
31 of them duplicate parses resolved to an alias), **132,678 text segments**
across **11,573 pages**, 9 boards and 10 languages. The registry knows 32 boards,
23 languages and 12 scripts, so the rest is a matter of adding files.

---

## Quick start

### On Google Colab — the fastest route, nothing installed

```python
%cd /content
!git clone https://github.com/sandipanb01/tulana-studio.git || git -C tulana-studio pull
%cd tulana-studio/tulana
!pip install -q -r requirements.txt
!pip install -q "gradio>=6.0" PyMuPDF
!python -u launch_annotation.py --host 0.0.0.0
```

This prints an `https://….gradio.live` link. **Share that link** — annotators
need nothing installed at all. Leave the cell running; stopping it ends the link.

> **Colab discards the machine.** Before you finish for the day, download the
> database — the code is on GitHub, the work is not:
> ```python
> from google.colab import files
> files.download('/content/tulana-studio/tulana/state/studio.db')
> ```

The textbook PDFs are ~600 MB of Git LFS objects and are needed **only** for
*Check the printed page*. Everything else — the text, the alignment, editing,
saving, exporting — works without them. To fetch them:

```python
!apt-get install -y git-lfs -qq && git lfs install && git -C .. lfs pull
```

### Locally — Linux, macOS

```bash
git clone https://github.com/sandipanb01/tulana-studio.git
cd tulana-studio
git lfs install && git lfs pull          # the PDFs; see the LFS note below
cd tulana
python3 -m pip install -r requirements.txt
python3 -m pip install "gradio>=6.0"     # Setu only; the rest runs without it
python3 check_install.py                 # says exactly what, if anything, is wrong
python3 launch_annotation.py             # Setu, plus a link to share
```

### Locally — Windows

Identical files; the interpreter is `py` (or `python`) rather than `python3`,
because Debian and Ubuntu ship no `python` command at all. There is no
PowerShell script to run, no bash, no Node, no build step, no database server
and no external binaries.

```powershell
py -m pip install -r requirements.txt
py -m pip install "gradio>=6.0"
py check_install.py
py launch_annotation.py
```

### Entry points

| Command | What it starts |
|---|---|
| `python3 launch_annotation.py` | **The usual one.** Setu, with the rest of the studio mounted underneath at `/studio`, and a public link. |
| `python3 launch_annotation.py --no-share` | The same, this machine only. |
| `python3 launch_annotation.py --port 7870` | A specific port. The port walks forward if it is busy. |
| `python3 launch_annotation.py --prepare` | Rebuild the text layer before starting. |
| `python3 app.py` | The original studio alone, without Setu. |
| `python3 share_gradio.py` | A thin wrapper that delegates to `launch_annotation.py`. |

The first start prepares the textbook text — about a minute, once.

> ### The PDFs are Git LFS objects, and this bites
>
> A clone **without** `git lfs pull` leaves a 132-byte text pointer where each
> PDF should be. Right name, right extension, so `find … | wc -l` still counts
> 150 and everything *looks* present. Pages then render blank with no obvious
> cause. To check:
>
> ```bash
> find board_pdfs -name '*.pdf' | while read f; do
>   head -c 5 "$f" | grep -q '%PDF-' || echo "POINTER: $f"
> done
> ```
>
> GitHub's free LFS allowance is 1 GB of storage and 1 GB of bandwidth a month.
> **Two full clones exhaust it**, after which every clone silently receives
> pointers again. If more than a couple of people will clone this, the PDFs
> belong on shared storage rather than in Git.

---

## Tech stack

Chosen so that a linguist on a laptop and a researcher on a cluster run the same
code, and so that the only thing needing a backup is one file.

| Layer | Choice | Version | Why this and not the obvious alternative |
|---|---|---|---|
| **Language** | Python | **3.10+** (tested on 3.11) | `match`, PEP 604 union types, `dataclasses`. Nothing newer is required, so a 2022 institutional image still runs it. |
| **Storage** | SQLite | 3.35+ (3.45 tested) | One file. No server to provision, no credentials to distribute, no ops. `RETURNING` and `ON CONFLICT DO UPDATE` need 3.35. Runs in WAL with `synchronous=FULL`, so *saved* means *on disk*. |
| **Full-text search** | SQLite **FTS5** | built in | Searching 132,678 segments in both scripts without a search server. Degrades to `LIKE` if the interpreter was built without FTS5, and says so rather than failing. |
| **Annotation UI** | **Gradio** | **6.28** | Gives a public HTTPS link with one flag, which is the whole deployment story for annotators who cannot install anything. Gradio 6 specifically: `css`/`js`/`head` moved from the `Blocks` constructor to `launch()`, and passing them to the constructor fails *silently*. |
| **HTTP / API** | **FastAPI** + Uvicorn | 0.110+ / 0.29+ | Typed request models, automatic OpenAPI. Gradio mounts onto it, so both surfaces share one process and one port. |
| **Validation** | **Pydantic v2** | 2.6+ | The API boundary. Nothing inside `core/` depends on it. |
| **PDF & rendering** | **PyMuPDF** (`fitz`) | 1.24+ | Page rendering and region cropping at 300 DPI. Pure wheel, no system Poppler, no Ghostscript. |
| **Images** | Pillow | 10+ | JPEG encoding of the cropped parallel regions. |
| **Excel export** | openpyxl | 3.1+ | *Optional.* Absent → the format is shown as unavailable **with the install command**, rather than failing when somebody clicks Download. |
| **Parquet export** | pyarrow | 14+ | *Optional*, same treatment. |
| **Browser tests** | Playwright + Chromium | — | *Optional.* Scrolling, keyboard, session isolation — the things a Gradio upgrade breaks and a Python test cannot see. |
| **Front-end** | Hand-written CSS + vanilla JS | — | Two files, no bundler, no `node_modules`, no build step. The interface must still start in five years on a machine with no network. |

**Deliberately absent:** no Node, no Docker requirement, no message queue, no
Redis, no ORM, no Alembic, no cloud dependency. Every dependency above is a pure
wheel or ships with Python.

```
fastapi>=0.110     uvicorn[standard]>=0.29     pydantic>=2.6
PyMuPDF>=1.24      Pillow>=10.0                requests>=2.31
openpyxl>=3.1      pyarrow>=14.0               gradio>=6.0
```

---

## Architecture

Three layers, one rule: **`core/` imports no UI library.** That is what makes
the logic testable without a browser and the interface replaceable without
touching the logic. A test enforces it.

```
                 ┌──────────────────────────────────────────┐
  annotators ───▶│  annotation/ui/     Gradio Blocks         │
                 │    app.py      layout and event wiring    │
                 │    workspace.py  the annotate tab         │
                 │    browse.py     the two-document browser │
                 │    panels.py     review, export, manuals  │
                 │    session.py    per-session state only   │
                 └────────────────────┬─────────────────────┘
                                      │
  pipelines  ───▶ annotation/api.py ──┤   (same services, over HTTP)
                                      │
                 ┌────────────────────▼─────────────────────┐
                 │  annotation/core/   no UI import, ever    │
                 │    store.py     connections, tx, errors   │
                 │    schema.sql   14 tables, all setu_*     │
                 │    corpus.py    books, segments, outline  │
                 │    align.py     the pairing heuristic     │
                 │    workspace.py projects and rows         │
                 │    annotate.py  edits, statuses, history  │
                 │    search.py    FTS5                      │
                 │    exporters.py 11 formats                │
                 └────────────────────┬─────────────────────┘
                                      │
                 ┌────────────────────▼─────────────────────┐
                 │  SQLite — state/studio.db                 │
                 │  board_outputs/ parsed layout (read-only) │
                 │  board_pdfs/    original PDFs (read-only) │
                 └───────────────────────────────────────────┘
```

### Repository layout

```text
tulana-studio/
├── board_pdfs/                  original textbook PDFs (Git LFS, ~600 MB)
├── board_outputs/output/        parsed layout, one JSON per book
└── tulana/                      the application
    ├── launch_annotation.py     ← start here
    ├── app.py  config.py  db.py  blocks.py  pairs.py  layout.py
    ├── library.py  pdflib.py  shelf.py  sources.py
    ├── check_install.py         is this checkout complete?
    ├── annotation/              Setu
    │   ├── core/                services; imports no UI library
    │   ├── ui/                  the Gradio workspace
    │   │   └── static/annotation.css  annotation.js
    │   ├── api.py               HTTP surface
    │   └── docs/                manual · FAQ · developer guide
    ├── test_annotation.py  test_browse.py  test_pairs.py
    ├── test_stress.py  test_blocks.py  test_naming.py
    └── windows_check.py
```

**The two data folders are joined by `relpath`.** Each layout JSON names the PDF
it was parsed from, and that path matches `board_pdfs/` exactly. The studio finds
both folders itself — including `board_outputs/output/` nested a level deeper —
and ignores the `__MACOSX/._*.json` resource forks a macOS zip leaves behind.

### Concurrency

Every annotator's browser tab has its own `gr.State`. **There is no mutable
module-level state anywhere in the interface** — not a cached current row, not a
"last opened project", not a convenience handle to a connection. Each of those
becomes cross-session contamination the moment two people use the link at once,
and the failure is silent: person A simply starts seeing person B's textbook. A
test asserts the absence by parsing the module for module-level assignments.

---

## Data model

Fourteen tables, every one prefixed `setu_`, in four groups by how often they
change.

```
immutable source        setu_book · setu_book_alias · setu_segment
                        written once when the corpus is prepared, read for ever

workspace               setu_project · setu_row
                        one project = two books; one row = one bilingual pair

editable state          setu_text · setu_status_rev
                        present only once a side has actually been edited —
                        absent means "still exactly what the parser extracted"

history and bookkeeping setu_rev · setu_event · setu_session · setu_lock
                        setu_export · setu_meta · setu_seg_fts
```

Three properties matter more than the schema:

**The parser's original extraction is never modified.** `setu_segment.source_text`
is what the machine read. An annotator's correction goes to `setu_text`, a
different table. That is the whole reason the two are separate. The interface can
therefore offer *restore the original* with no round trip, and provenance is never
lost because somebody fixed a typo.

**Every save carries the revision it was based on.** A save that would land on
top of somebody else's is refused; both versions are shown side by side and the
annotator chooses. Every version is kept in `setu_rev` for ever and nothing is
pruned automatically.

**Tulana's eight original tables are never written to.** `documents`, `projects`,
`clips`, `pairs`, `labels`, `pair_labels`, `exports`, `audit` — no `INSERT`, no
`UPDATE`, no `DELETE`, no `ALTER`, no `DROP`, from anywhere under `annotation/`.
This is proved three ways rather than asserted: the tests parse each module's
string literals for a write to a table not named `setu_*`; they grep the package
for `DROP`, `TRUNCATE` and `ALTER … DROP`; and they seed a document and an audit
row, run every operation Setu has, and hash all eight tables before and after.
Introducing such a write makes the suite fail — which was checked by introducing
one.

---

## Setu — the annotation workspace

Built for people who have never annotated before: plain words on every control,
one obvious action per pair, nothing to configure before starting.

### Five tabs

| Tab | What it is for |
|---|---|
| **Annotate** | One pair at a time. Both sides editable, six answers, a note box. |
| **Browse both books** | The two editions as **two independent documents**. See the next section. |
| **Saved work** | Everything judged so far, filterable, click a row to reopen it. |
| **Download** | Eleven formats, filtered by answer, chapter or completeness. |
| **Help** | The annotator's manual, the FAQ and the developer guide, in-app. |

### Opening two books

Board → class → subject → language → book, **every list generated from what is
actually in the database**, so no combination that does not exist can be chosen.
Boards that cannot be paired at all — only one language present — are ordered
last and labelled as such rather than offered as a dead end. The right-hand
language list excludes whatever is selected on the left, and carries every Indic
language for future-proofing, marking the ones with no textbook yet.

### How the pairs are laid out

Mathematics survives translation unchanged — `$2 \times 3 \times 7$` reads the
same in Marathi as in English — so Setu anchors on shared formulas, then on
shared section numbers, keeping only the set of anchors that do not cross.
Measured against the page-parallel Maharashtra editions, anchored pairs land
within one page **99–100%** of the time and cover about a third of a book; the
rest is filled in reading order and **marked as the weaker guess it is**.

Every pairing arrives as a *suggestion*, never a decision.

### The six answers

`Exact` · `Needs correction` · `Missing or incomplete` · `Structural mismatch` ·
`Unclear` · `Not applicable`

Defined once in `annotation/core/models.py`. Adding a seventh is one entry in one
tuple.

### Saving

On leaving a box, on setting an answer, on moving to another pair, and every
three seconds while typing. `synchronous=FULL`, so *saved* means *on disk*.
Measured: **12 annotators × 58 saves in 0.23 s** — 7 ms median, 67 ms at the 95th
percentile.

### Keyboard

<kbd>1</kbd>–<kbd>6</kbd> set the answer · <kbd>n</kbd> next unchecked ·
<kbd>Alt</kbd>+<kbd>←</kbd>/<kbd>→</kbd> or <kbd>j</kbd>/<kbd>k</kbd> move ·
<kbd>Ctrl</kbd>+<kbd>S</kbd> save now · <kbd>Ctrl</kbd>+<kbd>±</kbd> text size ·
<kbd>Ctrl</kbd>+<kbd>0</kbd> reset the view.

<kbd>Ctrl</kbd>+<kbd>Z</kbd> is left to the browser, whose undo stack is finer
than anything the tool could add.

---

## Browsing two editions that do not line up

**This is the part most people need and do not expect to need.**

The two editions were printed separately. They were typeset separately, they
number their chapters differently, and several carry chapters the other does not
have at all. Measured across this corpus, chapter-start page offsets between the
English edition and its counterpart:

| Board · class · language | Chapter page offsets | Chapters, English vs other |
|---|---|---|
| Karnataka · 10 · Kannada | −3, 0, +3, +6, +7, +8 | 13 vs 16 |
| Punjab · 10 · Punjabi | 0, +10, +23, +26 | 43 vs 48 |
| Gujarat · 10 · Gujarati | −114, −112, −111, −107 | 27 vs 20 |
| Kerala · 10 · Malayalam | — | 11 vs 8 |
| NCERT · 11 · Hindi | **no chapter matched by page at all** | — |
| Tamil Nadu · 10 · Tamil | **no chapter matched by page at all** | — |

None of that is a fault in the books. It is what happens when two editions are
produced by two teams. But it means an interface built on *row n on the left is
row n on the right* is simply wrong for most of this corpus.

**Browse both books** reads the two editions straight out of `setu_segment` as
two separate documents:

- **Each side has its own chapter list**, in that edition's own language and
  numbering — so a chapter that exists on only one side is visible as such.
- **Each side has its own page box** and its own <kbd>◀ Previous page</kbd> /
  <kbd>Next page ▶</kbd>. Moving one side does not move the other.
- **Each side scrolls on its own.**
- <kbd>◀◀ Both back</kbd> and <kbd>Both forward ▶▶</kbd> move the two together,
  keeping whatever gap you have put between them.
- <kbd>⇄ Link these two pages</kbd> records the offset once you find two pages
  that answer each other — *English is 3 pages ahead* — and from then on either
  side moves the other by exactly that much. **The link is saved to the
  workspace**, so the next annotator starts where you left off instead of
  re-deriving it. The live offset is on screen at all times.

Each block carries its kind (one of 23: paragraph, worked example, table, section
title …), its page, and how it has been judged. A block the aligner never managed
to pair is marked **not paired** and shaded — about **29%** of a typical project,
because the two editions break their paragraphs in different places. Those are
not errors to report; they are precisely what you are hunting for when a passage
seems to have gone missing.

Measured on the Maharashtra class 10 English ⇄ Gujarati project, 2,304 rows:

```
both sides have text      1,641   71.2%
one side only               663   28.8%
of paired rows, same page 1,514   92.3%
median segment length        89 characters
```

**Prior art this was built from.** POTATO (`davidjurgens/potato`) for the
position box, the `done/total` tally and the heading-derived outline; PAWLS
(`allenai/pawls`) by omission — it has no intra-document navigation, which is
survivable for a two-page paper and fatal for a 250-page textbook; CMULAB
(`neulab/cmulab`) for per-span status rather than done/not-done; DocLayNet
(`DS4SD/DocLayNet`) for layout classes and for the finding that it carries **no
reading order**, which is exactly why the *page*, not the block index, is the
unit that survives across two editions.

---

## Exporting

Eleven formats from the same rows, filtered by answer, chapter or completeness —
or all of them at once as a zip with a dataset card.

| Key | Format | Who wants it |
|---|---|---|
| `jsonl` | JSON Lines | training pipelines — the default |
| `json` | JSON | anything that wants one document |
| `csv` / `tsv` | delimited | spreadsheets, quick inspection |
| `xml` | XML | institutional archives |
| `txt` | plain text | eyeballing |
| `moses` | Moses / fairseq | MT training, two aligned files |
| `tmx` | Translation Memory eXchange | OmegaT, memoQ, Trados |
| `xlsx` | Excel | reviewers who do not use a terminal |
| `parquet` | Apache Parquet | columnar analytics |
| `huggingface` | 🤗 `datasets` | `load_dataset()` straight off disk |

Formats that can only represent true pairs **say so and report what they left
out** — including them would shift every later line out of alignment.

### What the text is

`source_text` is what the **parser** read. It is not a human transcription.

Say this plainly to anyone you give the corpus to: **the alignment is a human
judgement and the characters are machine-read.** Treat the pairing as reliable
and the text as needing review before the corpus is used as a reference. The
dataset card says the same.

A block over a diagram carries no text, and a page without a usable text layer
yields none. **Empty means *not recovered*, not *empty on the page*.**

---

## Adding a board, class, subject, language or script

Nothing in the code names one. 32 boards, 23 languages and 12 scripts ship as
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

```bash
python3 shelf.py doctor
python3 shelf.py add FILE --board WB --class 10 --lang Bengali
```

---

## Tests

```bash
cd tulana
python3 check_install.py     #  24 — is this checkout complete and consistent
python3 test_annotation.py   # 123 — alignment, autosave, conflicts, exports, safety
python3 test_browse.py       #  40 — the two-document browser
python3 test_blocks.py       # 645 — every book in the layout corpus
python3 test_naming.py       # 265 — 32 boards × 23 languages × naming styles
python3 windows_check.py     #   8 — cross-platform audit
python3 test_pairs.py        #  95 — cross-page selection, cropping, every format  ┐ need
python3 test_stress.py       # 138 — edge cases, malformed input, database safety  ┘ the PDFs
```

**Around 1,340 checks.** Each suite gets a fresh database per test, so order
never matters, and the set is run twice interleaved to prove it.

> **Three of these need the real PDFs**, not LFS pointers. Without them
> `check_install.py` reports the pointers (which is its job), `test_pairs.py`
> fails one cropping check with *"the PDFs may not be on disk"*, and
> `test_stress.py` stops at `fitz.open`. That is the clone, not the code —
> `git lfs pull` and re-run.

Five checks were verified **by deliberately breaking the thing they protect** —
removing the revision check, overwriting the parser's original text, writing to a
legacy table, creating the search index inside a caller's transaction, and
returning the two browse columns the wrong way round. Each one fails when the
protection is removed; the last was checked by swapping `panes["src"]` and
`panes["tgt"]` in `browse.py`, which turns three tests red and nothing else.

`test_stress.py` feeds in malformed JSON, zero-size pages, inverted boxes,
non-numeric coordinates, null bytes and emoji; asks for pages beyond the end of a
book and negative pages; selects 5,000 blocks at once; and invents an Odisha
Class 8 Odia book to prove a board added in future resolves end to end.

`test_browse.py` is the same instinct aimed at the browser: page numbers of
`10**9`, `-10**9`, `"1e400"`, `None`, `{}` and `"3; DROP TABLE setu_row"`;
`gr.Number`'s float `3.0`, which is what caught a real bug (`int("3.0")` raises);
a corrupt stored page-link; corpus text containing `<script>`; and a project
renamed to `../../etc/passwd` to prove the `setu_meta` key is derived from the
project id and never from anything typed.

**Browser behaviour is not in those suites.** Independent scrolling, the
keyboard, zoom, session isolation and the conflict panel are verified with
Playwright against a running server — the two columns measured at 1270 px of
content in a 693 px box, scrolled independently. Re-check them by hand after a
Gradio upgrade, because that is what breaks them.

---

## Configuration

| Variable | Meaning | Default |
|---|---|---|
| `TULANA_DATA_DIR` | where the PDFs live | discovered |
| `TULANA_STATE_DIR` | database, page cache, exports | `./state` |
| `TULANA_PORT` | preferred port | `7862` |
| `TULANA_VIEW_DPI` | on-screen page resolution | `110` |
| `TULANA_CROP_DPI` | resolution the parallel images are cut at | `300` |

**Back up `state/`.** That folder is the annotators' work — the database and the
cropped images in `state/crops`. The PDFs and the layout can always be fetched
again; the annotations cannot.

Crops are named by content hash, so the same passage cropped twice costs one
file. `POST /api/pairs/crops/prune` reports what no pair refers to any more; add
`?apply=true` to delete it.

---

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Everything blank, no pages render | The PDFs are LFS pointers. `git lfs install && git lfs pull` |
| The Blocks tab is empty | The layout corpus was not found. `check_install.py` says where it looked. |
| A textbook missing from the dropdown | Usually not the file name — **the subject must match too.** A Malayalam *Science* book beside an English *Mathematics* book will never pair. `GET /api/blocks/mapping` names every book as mapped, missing or worth a look. |
| Blocks but no page image | The layout covers that page and the PDF does not — a truncated copy or a different edition. The text is still usable. |
| A block has no text | Diagrams carry none, and a page without a text layer yields none. |
| `{"detail":"Not Found"}` | You opened `/studio/setu/`. That address belonged to an older build. Open the printed link itself; `/studio/` is the block-and-crop workbench. |
| `address already in use` | The studio takes the next free port and prints which one. |
| One column will not scroll | Both columns scroll independently; if one looks stuck, that page is short enough to fit. Try **Show the whole chapter at once**. |
| The interface looks unstyled | Gradio 6 moved `css`/`js`/`head` from the `Blocks` constructor to `launch()`, and the constructor ignores them *silently*. |

---

## Known limitations

Stated plainly, because a tool that hides these costs more time than it saves.

1. **About 29% of rows are one-sided**, and this is structural, not a bug to fix.
   The two editions cut their paragraphs in different places, so a paragraph
   whole on one side is two blocks on the other. A strictly 1:1 row model cannot
   represent that. **Browse both books** lets an annotator *find* these; it does
   not re-pair them. Splitting and re-attaching rows is the next real piece of
   work.
2. **Some editions cannot be paired by page at all** — NCERT class 11 Hindi and
   Tamil Nadu class 10 Tamil share no chapter starting page with their English
   counterparts.
3. **Andhra Pradesh ships bilingual single-file PDFs**, both languages in one
   book, and cannot be paired by this model at all.
4. **The text is machine-read.** See *What the text is*, above.
5. **Gradio share links last about a week.** For a permanent address, put the
   studio behind nginx. The database and images stay on the host, so a restart
   loses no work — only the address changes.
6. **GitHub's free LFS allowance is exhausted by two full clones.**

---

