# Tulana Studio

A workspace for building **parallel corpora and layout ground truth from Indian
school textbooks**. The English edition and its translation open side by side;
an annotator clips matching passages, marks up page layout, and works with the
blocks a document parser has already found.

Everything is board-, class-, subject-, language- and script-agnostic. Adding a
new state board or a new regional language is a row of data, never a code
change.

---

## Before anything else

```bash
git clone https://github.com/sandipanb01/tulana-studio.git
cd tulana-studio
git lfs install && git lfs pull      # the PDFs are LFS objects — see below
cd tulana
python3 -m pip install -r requirements.txt
python3 check_install.py             # tells you exactly what, if anything, is wrong
python3 app.py                       # http://localhost:7862
```

`check_install.py` is the first thing to run after any clone, pull or push. It
reports missing modules, an interface that does not match its backend, PDFs
that are really Git LFS pointers, and a layout corpus it cannot find — each
with the command that fixes it.

### The PDFs are Git LFS objects, and this bites

`board_pdfs/` holds 150 PDFs, about 600 MB, stored through Git LFS. A clone
**without** `git lfs pull` leaves a 132-byte text pointer where each PDF should
be:

```
version https://git-lfs.github.com/spec/v1
oid sha256:798d2f27d45d2ccda3694005c2ed60bc0b413b8b299f3a5d4ade7c5867094896
size 6254823
```

It has the right name and the right extension, so `find … | wc -l` still counts
150 and everything *looks* present. The studio then indexes nothing, or shows
blank pages, with no obvious cause.

```bash
# is this checkout real?
find board_pdfs -name '*.pdf' | while read f; do
  head -c 5 "$f" | grep -q '%PDF-' || echo "POINTER: $f"
done
```

GitHub's free LFS allowance is 1 GB of storage and 1 GB of bandwidth per month.
**Two full clones exhaust it**, after which every clone silently receives
pointers again. If more than a couple of people will clone this, the PDFs
belong on shared storage rather than in Git.

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
    ├── layout.py                human layout annotation
    ├── shelf.py                 register a newly added PDF
    ├── check_install.py         is this checkout complete?
    ├── test_*.py  windows_check.py
    ├── share_gradio.py
    ├── docs/  static/
    └── data → ../board_pdfs     optional; see below
```

**The two folders are joined by `relpath`.** Each layout JSON names the PDF it
was parsed from, and that path matches `board_pdfs/` exactly. 152 books of
layout; 144 of them map onto a PDF that is present.

### `tulana/data` is optional

The studio finds the corpus itself — it checks the configured folder, then
`../board_pdfs`, then a few near neighbours, and says which it chose. Create
the link if you like, or set `TULANA_DATA_DIR`; neither is required.

```bash
ln -s ../board_pdfs data            # Linux, macOS
mklink /J data ..\board_pdfs        # Windows
```

`board_outputs/` is found the same way, including when it is nested a folder
deeper, and the `__MACOSX/._*.json` resource forks a macOS zip leaves behind
are ignored.

---

## What the studio does

**Clip** — both editions side by side. Drag a rectangle around a passage in
English, then around the same passage in the translation, and save the pair.
Clippings are cut from the source at 300 DPI and exported as
`eng_ncert_math_1.png` / `hin_ncert_math_1.png` alongside `manifest.json`,
`pairs.jsonl`, `pairs.csv` and a readable summary.

**Layout** — mark up a page's regions in reading order: title, heading,
paragraph, list, table, figure, caption, equation. Exports as COCO, so the
result can train a layout model or merge with DocLayNet and PubLayNet. Also
scores how far a translated page preserves the original's structure, across six
separate measures.

**Blocks** — the parsed layout over the original PDF page. Click blocks to
select them on either side, shift-click for a range in reading order, and read
the extracted text of the selection in both languages at once. Zoom per pane,
filter by block type, 30 types read from the corpus itself.

**Saved pairs**, **Export** and **Guide** complete the set.

Everything works on a phone: the panes stack and the controls move behind a
menu button.

---

## A shareable link

```bash
python3 share_gradio.py
```

Prints an `https://….gradio.live` address. Annotators need nothing installed.
The link is a tunnel — the database and images stay on the host, so a restart
never loses work, only the address changes. Gradio links last about a week; for
a permanent address, put the studio behind nginx or run the container.

The port walks forward if 7862 is busy, and both `/studio` and `/studio/` work.

---

## Adding a board, class, subject, language or script

Nothing in the code names a board or a language. All five are registries:
**32 boards, 23 languages, 12 scripts** ship as seed data, and more are added
with `POST /api/registry` or a row in `config.py`.

Name a file so the studio can place it. All of these work:

```
KER_ML_10.pdf                       BOARD_LANG_CLASS
Kerala_Class10_Malayalam_Maths.pdf  written out
kerala-class-9-malayalam.pdf        hyphenated
SCERT_Kerala_Std10_Malayalam.pdf    Std, Grade, Class
Kerala_Class_X_Malayalam.pdf        roman numerals
Kerala/Class 10/Malayalam/maths.pdf folders instead of a long name
```

Board and language codes overlap — `guj` names both Gujarat and Gujarati,
`pun` both Punjab and Punjabi — and that is handled: the board token is
identified and consumed before languages are read.

**If a textbook does not appear**, press *Why is a textbook missing?* on the
Clip tab, or call `GET /api/library/diagnose`. Every PDF is accounted for as
usable, unpaired or unreadable, with the reason and the fix. The commonest
cause is not the file name at all — the **subject must match too**. A Malayalam
*Science* book beside an English *Mathematics* book will never pair.

Registering a PDF by hand, when the name genuinely cannot say what it is:

```bash
python3 shelf.py doctor
python3 shelf.py add FILE --board WB --class 10 --lang Bengali
```

---

## Tests

```bash
python3 check_install.py     is this checkout complete and consistent
python3 test_stress.py       edge cases, malformed input, database safety
python3 test_blocks.py       every book in the layout corpus, sampled pages
python3 test_naming.py       32 boards × 23 languages × every naming style
python3 windows_check.py     cross-platform audit
python3 selftest.py          the clipping workspace, end to end
```

`test_stress.py` feeds in malformed JSON, zero-size pages, inverted boxes,
non-numeric coordinates, null bytes and emoji; asks for pages beyond the end of
a book and negative pages; selects 5000 blocks at once; re-ingests to prove
nothing duplicates; checks box placement at 72 and 150 dpi; and invents an
Odisha Class 8 Odia book to prove a board added in future resolves end to end.

It also proves the safety contract below rather than asserting it.

---

## The annotation database is protected

`blocks.py` and `layout.py` create their own tables with
`CREATE TABLE IF NOT EXISTS` and never write to `documents`, `projects`,
`clips`, `pairs`, `labels`, `pair_labels`, `exports` or `audit`. No `ALTER`, no
`DROP`.

`test_stress.py` checks this two ways: it reads the source of each module for
writes to those tables, and it seeds a project and a pair, runs everything, and
hashes all eight tables before and after. If a future change ever writes to one
of them, the test fails.

`shelf.py` is the deliberate exception — registering a document is its whole
purpose — and it only ever inserts a row or updates the metadata columns of one
it matched by path, so an existing document keeps its `id` and no clip or pair
can be orphaned.

---

## Windows, Linux, macOS

Python 3.10 or newer. **No PowerShell, no bash, no Node, no build step, no
database server, no external binaries.** `.zip` and `.7z` are both read in pure
Python.

The interpreter is named `py` (or `python`) on Windows and `python3` on Linux
and macOS — Debian and Ubuntu ship no `python` command at all. That naming is
the only difference; the files are identical.

`windows_check.py` audits the things that work on Linux and fail on Windows:
hard-coded POSIX paths, text files opened without an explicit encoding (Windows
defaults to cp1252, which cannot read Devanagari), shell invocation, filenames
that are illegal on Windows, and any OS-specific separator reaching the
database.

---

## Configuration

| variable | meaning | default |
|---|---|---|
| `TULANA_DATA_DIR` | where the PDFs live | discovered |
| `TULANA_STATE_DIR` | database, clippings, exports | `./state` |
| `TULANA_PORT` | preferred port | `7862` |
| `TULANA_VIEW_DPI` | on-screen page resolution | `110` |
| `TULANA_CROP_DPI` | resolution clippings are cut at | `300` |

Back up `state/`. That folder is the annotators' work; the PDFs and the layout
can always be fetched again.

---

## Troubleshooting

**The dropdown is empty.** Look at the startup log — it names the folder it
searched and says whether the files it found were Git LFS pointers. Then run
`check_install.py`.

**A textbook is missing from the dropdown.** *Why is a textbook missing?* on
the Clip tab, or `GET /api/library/diagnose`.

**The Blocks tab is empty.** The layout corpus was not found. `check_install.py`
says where it looked.

**A page shows blocks but no image.** The layout covers that page but the PDF
does not — a truncated copy, or a different edition. The blocks and their text
are still usable.

**A change does not appear after deploying.** Assets are fingerprinted, so this
should not happen; if it does, reload once with cache disabled. If a whole tab
is missing, `check_install.py` will say whether the Python or the interface was
the half that did not get copied.

**`address already in use`.** The studio takes the next free port and prints
which one it chose.
