# Tulana Studio

A workspace for building **parallel corpora from Indian school textbooks**. The
English edition and its translation open side by side with the blocks a document
parser has already found on each page. You select the blocks that say the same
thing on each side — across pages if the passage runs on — and the two regions
are **cropped from the original PDFs and saved automatically**, as images and as
text. The corpus is then exported in whichever format the next tool needs.

Board-, class-, subject-, language- and script-agnostic. Adding a state board or
a regional language is a row of data, never a code change.

---

## Before anything else

```bash
git clone https://github.com/sandipanb01/tulana-studio.git
cd tulana-studio
git lfs install && git lfs pull      # the PDFs are LFS objects — see below
cd tulana
python3 -m pip install -r requirements.txt
python3 check_install.py             # says exactly what, if anything, is wrong
python3 app.py                       # http://localhost:7862
```

`check_install.py` is the first thing to run after any clone, pull or push. It
reports missing modules, an interface that does not match its backend, PDFs that
are really Git LFS pointers, and a layout corpus it cannot find — each with the
command that fixes it.

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
    ├── app.py  config.py  db.py  library.py  pdflib.py
    ├── blocks.py                the parsed-layout corpus
    ├── pairs.py                 saved pairs and export
    ├── layout.py                layout annotation (API only)
    ├── shelf.py                 register a newly added PDF
    ├── check_install.py         is this checkout complete?
    ├── test_*.py  windows_check.py
    ├── share_gradio.py
    └── docs/  static/
```

**The two folders are joined by `relpath`.** Each layout JSON names the PDF it
was parsed from, and that path matches `board_pdfs/` exactly. 152 books of
layout; 144 of them map onto a PDF that is present.

The studio finds both folders itself — including `board_outputs/output/` nested
a level deeper — and ignores the `__MACOSX/._*.json` resource forks a macOS zip
leaves behind. `tulana/data` is optional; set `TULANA_DATA_DIR` if you keep the
PDFs somewhere else.

---

## The four tabs

### Blocks

Choose a board and class, then the target language, then the two editions. Both
pages open side by side with their blocks overlaid, each labelled and coloured
by type, numbered in reading order.

**Two tools, because they answer different questions.**

*Click blocks* takes what the parser found and brings its text with it.
Shift-click takes a range in reading order. *Drag to crop* takes what **you**
decide: draw a rectangle over the passage, drag inside it to move, the corner to
resize, **×** to remove. A figure with its caption may be one passage to a reader
and three blocks to the parser — and a hand-drawn diagram or a margin note was
never a block at all, so no amount of clicking would reach it.

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

---

## What the text is

`source_text` and `target_text` are what the **parser** read inside the selected
blocks, joined in reading order. They are not a human transcription.

Say this plainly to anyone you give the corpus to: **the alignment is a human
judgement and the characters are machine-read.** Treat the pairing as reliable
and the text as needing review before the corpus is used as a reference. The
dataset card says the same.

A block over a diagram carries no text, and a page without a usable text layer
yields none. Empty means *not recovered*, not *empty on the page*.

---

## A shareable link

```bash
python3 share_gradio.py
```

Prints an `https://….gradio.live` address. Annotators need nothing installed.
The link is a tunnel — the database and images stay on the host, so a restart
never loses work, only the address changes. Gradio links last about a week; for
a permanent address, put the studio behind nginx.

Both `/studio` and `/studio/` work, assets are fingerprinted so a deployed
change cannot be served stale, and the port walks forward if 7862 is busy.

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

---

## Tests

```bash
python3 check_install.py     22 — is this checkout complete and consistent
python3 test_pairs.py       107 — cross-page selection, cropping, autosave, every format
python3 test_stress.py      138 — edge cases, malformed input, database safety
python3 test_blocks.py      645 — every book in the layout corpus
python3 test_naming.py      265 — 32 boards × 23 languages × naming styles
python3 windows_check.py      8 — cross-platform audit
```

**1,185 checks**, run twice interleaved to prove they do not depend on order.

`test_stress.py` feeds in malformed JSON, zero-size pages, inverted boxes,
non-numeric coordinates, null bytes and emoji; asks for pages beyond the end of
a book and negative pages; selects 5000 blocks at once; checks box placement at
72 and 150 dpi; and invents an Odisha Class 8 Odia book to prove a board added
in future resolves end to end.

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

`shelf.py` is the deliberate exception — registering a document is its whole
purpose — and it only inserts a row or updates the metadata columns of one it
matched by path, so an existing document keeps its `id` and no saved work can be
orphaned.

**Earlier work is not deleted.** PDF clipping and hand-drawn layout annotation
were removed from the *interface*, not from the database. Everything they saved
is untouched and still reachable through the API.

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
`git lfs install && git lfs pull`.

**The Blocks tab is empty.** The layout corpus was not found.
`check_install.py` says where it looked.

**A textbook is missing from the dropdown.** `GET /api/blocks/mapping` names
every book as mapped, missing or worth a look. The commonest cause is not the
file name: the **subject must match too** — a Malayalam *Science* book beside an
English *Mathematics* book will never pair.

**A page shows blocks but no image.** The layout covers that page and the PDF
does not — a truncated copy, or a different edition. The blocks and text are
still usable.

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
