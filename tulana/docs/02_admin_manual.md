# Tulana Studio — Administrator Manual

## Installing

```bash
pip install -r requirements.txt
TULANA_DATA_DIR=/path/to/pdfs python3 app.py     # http://localhost:7862
```

`TULANA_DATA_DIR` is the folder holding the textbook PDFs. Any layout works —
board, class, language and volume are inferred from each file's own path, so a
tidy archive and a folder someone dropped files into both work.

Other settings, all optional:

| Variable | Meaning | Default |
|---|---|---|
| `TULANA_DATA_DIR` | where the PDFs live | `./data` |
| `TULANA_STATE_DIR` | database, clippings, exports | `./state` |
| `TULANA_PORT` | port to serve on | `7862` |
| `TULANA_VIEW_DPI` | on-screen page resolution | `110` |
| `TULANA_CROP_DPI` | resolution clippings are cut at | `300` |

## Publishing a public link

```bash
pip install gradio
TULANA_DATA_DIR=/path/to/pdfs python3 share_gradio.py
```

This prints an `https://….gradio.live` address serving the studio, so an
annotator anywhere can work without any installation. The link is a tunnel, not
a copy: clippings are still written to this machine's `state/` folder, so a
restart — and the new link that comes with it — never loses work. Gradio links
are ephemeral by design; for a permanent address put the studio behind nginx or
run the container.

## Categories

Every project starts with a default set — Definition, Theorem, Example,
Exercise, Activity, Table, Figure caption, Summary — each with a colour and a
one-key shortcut, in the manner of doccano's label sets. Add your own through
`POST /api/projects/{id}/labels` with a name, colour and shortcut; remove one
with `DELETE /api/labels/{id}`.

Categories are carried into `manifest.json`, `pairs.jsonl` and `pairs.csv`, so
a downstream consumer can select on them without opening an image.

`GET /api/projects/{id}/progress` reports chunks clipped, how many are included
or excluded, how much of the source book has been touched, counts per category
and counts per annotator. The Saved pairs tab shows the same at the top.

## Checking the textbook sources

```bash
python3 check_sources.py
```

Run it on the machine that will host the studio — reachability depends on that
machine's network, so it is the only place the answer means anything. For each
source it says whether the archive is already on disk, or whether the link
genuinely returns a file, following the confirmation step Drive requires for
large files. A BLOCKED verdict almost always means the file is not shared as
**Anyone with the link**.

## Where the textbooks come from

`sources.json` lists the archives and links the corpus is built from — the
board-wise textbook archive, the NCERT chapter PDFs, and the reference corpora.
The **Export** tab shows each one with its status: already in the data folder,
downloadable, or to be added manually.

Two buttons there:

- **Unpack what is here** — extracts any `.7z` / `.zip` in the data folder.
  Nested archives are handled (`.7z` containing a `.zip`), and free disk space is
  checked before anything is written.
- **Unpack and download what is missing** — the same, then fetches any
  configured link whose content is still absent. Nothing already present is
  downloaded again.

Google Drive links must be shared as **Anyone with the link**; a sign-in-only
link cannot be fetched by any server.

On Windows, install **7-Zip** and add it to `PATH` so `.7z` archives can be
unpacked; plain `.zip` needs nothing extra.

## Adding textbooks

Copy the PDFs into the data folder and either restart, or call
`POST /api/rescan`. Indexing is idempotent and re-runs cheaply: a file whose
checksum is unchanged is skipped.

A board and class becomes available to annotators as soon as it has **an English
edition and at least one other language**. Until then it is not offered, because
there is nothing to pair.

## How naming works

Board and language vocabularies overlap — `guj` names both Gujarat and
Gujarati, `pun` both Punjab and Punjabi. The leading segment of a filename is
read as the board and removed before languages are considered, so
`GUJ_EN_10.pdf` is correctly the Gujarat **English** edition. Files with no
board token at all, in English or Hindi, are treated as NCERT, which is how that
collection is organised.

To support a new board or language, add it to `BOARD_TOKENS` / `LANG_TOKENS` in
`config.py`. Nothing in the interface needs changing.

## Excluded topics

`EXCLUDED_TOPICS` in `config.py` lists the terms that mark a page as out of
scope — geometry, conics and related chapters, in English and in several Indian
languages. Pages matching are flagged in the interface and pairs saved from them
are recorded as excluded rather than blocked, so the annotator keeps judgement
and the record stays honest.

## What is stored, and where

| | |
|---|---|
| `state/studio.db` | documents, projects, pairs, clippings, audit trail |
| `state/crops/` | clipped images, as `PROJECT/eng_1.png` |
| `state/pages/` | rendered page images (a cache; safe to delete) |
| `state/exports/` | every ZIP produced |

Back up `state/`. That folder is the annotators' work; the PDFs can always be
re-obtained.

Every clipping records the page and the rectangle in PDF points as well as the
image, so the entire corpus can be re-cut at a different resolution without
anyone re-doing the work.

## Auditing

The `audit` table records project creation, every pair saved or deleted, and
every export, with the annotator's name and a timestamp. `GET /api/exports`
lists exports with their pair counts.

## Deployment

The studio is a single FastAPI application with no external services. Put it
behind nginx or Caddy for TLS, or run it in the provided container. Persist
`state/` and mount the PDFs read-only.
