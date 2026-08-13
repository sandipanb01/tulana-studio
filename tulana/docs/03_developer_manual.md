# Tulana Studio — Developer Manual

## Shape of the system

```
config.py     paths, board/language vocabularies, excluded topics, naming
pdflib.py     the only place PyMuPDF is imported
db.py         schema and transactions
library.py    PDF discovery, metadata inference, pairing, topic exclusion
app.py        HTTP API and static hosting
static/       the interface: index.html, style.css, app.js (no build step)
docs/         these manuals, served in-app under the Guide tab
```

No build tooling and no client framework. The interface is three files served
as they are, which keeps deployment to "copy the folder".

## Data model

| Table | Holds |
|---|---|
| `documents` | one row per PDF: board, class, language, script, volume, pages, checksum |
| `projects` | a pairing of two documents (English ↔ target) with an export name |
| `pairs` | one parallel chunk: sequence number, label, excluded flag, annotator |
| `clips` | one side of a pair: page, rectangle in PDF points, image path, extracted text |
| `labels` | a project's categories: name, colour, one-key shortcut |
| `pair_labels` | which categories a chunk carries |
| `exports` | every ZIP produced |
| `audit` | who did what, when |

**A clipping is a rectangle, not a picture.** `clips.x0..y1` are PDF points on
`clips.page`. The PNG is a rendering of that rectangle, produced at `CROP_DPI`.
Storing the geometry means the whole corpus can be re-cut at another resolution,
or re-examined against the source, without the annotator repeating anything.

## API

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | readiness, document and pair counts, PyMuPDF version |
| `GET /api/library` | board/class combinations that have both an English and a target edition |
| `GET /api/doc/{id}` | document metadata and page dimensions |
| `GET /api/doc/{id}/page/{n}.png?dpi=` | a rendered page (disk-cached, immutable) |
| `GET /api/doc/{id}/page/{n}/text` | page text and excluded-topic verdict |
| `GET /api/doc/{id}/outline` | chapter bookmarks, with excluded ones marked |
| `POST /api/projects` · `GET /api/projects` | create or list pairings |
| `POST /api/pairs` | save a parallel pair; cuts and stores both images |
| `GET /api/projects/{id}/pairs` | everything clipped for a project |
| `PATCH`/`DELETE /api/pairs/{id}` | relabel, exclude, or remove |
| `GET /api/clip/{id}.png` | a stored clipping |
| `GET /api/projects/{id}/export.zip` | the deliverable |
| `GET /api/docs` · `GET /api/docs/{name}` | these manuals, for the in-app Guide |
| `GET`/`POST /api/projects/{id}/labels` · `DELETE /api/labels/{id}` | the category set |
| `PUT /api/pairs/{id}/labels` | apply categories to a chunk |
| `GET /api/projects/{id}/progress` | chunks, coverage, counts per category and annotator |
| `GET /api/sources` · `POST /api/sources/acquire` | textbook archives and links |
| `POST /api/rescan` | re-index the data folder |

## Performance notes

Opening a textbook PDF costs more than drawing a page from it, so up to six
documents are kept open and reused. Rendered pages are cached on disk and served
immutable, making a scroll back instant. Pages are `<img loading="lazy">`, so a
400-page book only fetches what is near the viewport.

Measured on the NCERT corpus: a page renders in ~340 ms cold and ~5 ms once
cached; saving a pair (two 300 DPI cuts plus text extraction) takes under a
second.

## Extending it

The advisor's Phase I is clipping. The model was chosen so later phases do not
need a migration:

- **Text-level pairs** — `clips.text` already holds the text under each
  rectangle where the PDF has a readable layer, so a parallel *text* corpus can
  be exported without re-annotating.
- **More than two languages** — a pair is a group of clips joined by `pair_id`;
  the two-sided assumption lives in the interface, not the schema.
- **Automatic suggestion** — a proposed rectangle is just a `clips` row an
  annotator confirms; nothing about the storage changes.
- **Review workflows** — `pairs` already carries annotator, label, note,
  excluded and reason, which is enough for a second-pass review state.

## Testing

```bash
python3 selftest.py     # end-to-end: index, project, clip, export, integrity
```

It runs against the real PDFs, exercises every endpoint, checks that exported
images are genuine crops of the right pages, and verifies the excluded-topic
path.
