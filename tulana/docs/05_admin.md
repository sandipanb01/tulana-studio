# Running the studio

## Starting it

```
python3 app.py            # http://localhost:7862
python3 share_gradio.py   # the same, plus a public gradio.live link
```

If 7862 is busy the studio takes the next free port and prints which one.

## Before anything else

```
python3 check_install.py
```

Reports missing modules, an interface that does not match its backend, PDFs that
are really Git LFS pointers, and a layout corpus it cannot find — each with the
command that fixes it. Run it after every clone, pull or push.

## The two folders

```
board_pdfs/          the original textbook PDFs
board_outputs/       the parsed layout, one JSON per book
```

They are joined by `relpath`: each layout JSON names the PDF it came from. The
studio finds both by itself, including when `board_outputs` is nested a folder
deeper, and ignores the `__MACOSX` litter a macOS zip leaves behind.

`GET /api/blocks/mapping` reports every book as mapped, missing, or worth a
look.

## The PDFs are Git LFS objects

A clone **without** `git lfs pull` leaves a 132-byte pointer where each PDF
should be. The name is right, the extension is right, and `find | wc -l` still
counts them — but nothing renders.

```
git lfs install && git lfs pull
```

`check_install.py` reads the first five bytes of each file, so this can never be
mistaken for something else.

## Where the work lives

Everything is in `state/`: the database, the page cache, the cropped images in
`state/crops`, exports. **Back up that folder.**

Crops are named by content hash, so the same passage cropped twice costs one
file. `POST /api/pairs/crops/prune` reports what no pair refers to any more;
add `?apply=true` to delete it. `TULANA_CROP_DPI` sets the resolution — 300 by
default, which is what a page is worth reading at. The PDFs and the layout can always be fetched again; the annotators'
pairs cannot.

## Adding a board, language or subject

Nothing in the code names one. 32 boards, 23 languages and 12 scripts ship as
seed data, and more are added with `POST /api/registry` or a row in
`config.py`.

Name a file so the studio can place it — `KER_ML_10.pdf`,
`Kerala_Class10_Malayalam_Maths.pdf`, or folders like
`Kerala/Class 10/Malayalam/maths.pdf` all work. Where a name says nothing, the
parser's own text is used as evidence: the script is measured from the
characters, and for a script shared by several languages, orthographic markers
decide between them.

## Tests

```
python3 check_install.py   is this checkout complete
python3 test_stress.py     edge cases and database safety
python3 test_blocks.py     the whole layout corpus
python3 test_pairs.py      saving, cropping, editing and every export format
python3 test_naming.py     boards, languages, naming styles
python3 windows_check.py   cross-platform audit
```

## The earlier work is still there

Clipping from PDFs and hand-drawn layout annotation were removed from the
interface, not from the database. Anything saved by them is untouched in
`clips`, `pairs`, `layout_pages` and `layout_regions`, and still reachable
through the API.
