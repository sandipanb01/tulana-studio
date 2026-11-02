# Extending the annotation subsystem

Written for whoever picks this up next. It says where things are, what to change
to do the six things most likely to be asked for, and which parts are load
bearing.

## Where it lives

```
tulana/
  annotation/                 the subsystem
    core/                     no user-interface library is imported here
      ids.py                  identifiers — positional, never derived from text
      models.py               statuses, kinds, text normalisation
      store.py                connections, schema, migrations, repository base
      schema.sql              every table, all additive
      corpus.py               immutable source layer: dedup + segmentation
      align.py                the alignment suggestion engine
      workspace.py            projects, navigation, progress, sessions
      annotate.py             editing, autosave, revisions, conflicts
      search.py               FTS5 with a LIKE fallback
      exporters.py            the export format registry
      sources.py              the bridge to Tulana's PDF cropping
      aligned.py              the aligned test set (data/aligned_v2) importer
    ui/                       Gradio Blocks
      app.py                  layout and event wiring, no logic
      workspace.py            every annotation callback
      panels.py               saved work, download, manuals
      session.py              the per-session dictionary
      render.py               the HTML fragments
      static/                 annotation.css, annotation.js
      static/work/            the workspace page (index.html, app.js, style.css)
        vendor/katex/         KaTeX 0.16.9, served locally for typeset maths
    api.py                    an HTTP surface over the same services
    docs/                     these manuals
  launch_annotation.py        the entry point
  test_annotation.py          123 tests
  test_aligned.py             the aligned test set: 69 tests, and the real data
  test_mapping.py             boxes on the printed page: 20 tests on built PDFs
  check_mapping.py            audit: every aligned page against its PDF
```

Each layer imports only from the layers below it. `core` imports no Gradio and
no FastAPI, which is what lets the same services drive the Blocks workspace, the
HTTP API and the tests without any of them knowing about each other — and what
makes a different front end later a matter of writing one rather than rewriting
this.

## What it reuses rather than rebuilds

| Existing Tulana | Used for |
|---|---|
| `db.py` SQLite file | the same database; Setu adds `setu_*` tables and writes to nothing else |
| `blocks.py` (`pl_*` tables) | the parsed layout Setu segments; never re-parsed |
| `blocks._find_pdf` | locating a book's PDF under the corpus conventions |
| `pairs._render_crop` | cutting a region out of a page for source verification |
| `pdflib.py` | the single import point for PyMuPDF |
| `config.py` | paths, ports, board names, `free_port` |
| `app.py` (FastAPI) | mounted at `/studio` by the launcher, so one link serves both |

## Rules this code holds to

1. **Never write to the pre-existing tables.** `documents`, `projects`, `clips`,
   `pairs`, `labels`, `pair_labels`, `exports`, `audit` and the `pl_*` tables are
   read-only. Every table this subsystem creates begins with `setu_`. Asserted
   three ways in `test_annotation.py`, and each assertion was verified by
   introducing the violation it forbids.

2. **Schema changes are additive.** `CREATE TABLE IF NOT EXISTS`, and
   `ALTER TABLE ... ADD COLUMN` through `store._add_column`. Bump
   `store.SCHEMA_VERSION` and add a step to `store._migrate`.

3. **Identity is never derived from text.** A segment id comes from
   (book, page, reading-order span).

4. **The parser's extraction is never modified.** `setu_segment.source_text` is
   written once; edits go to `setu_text`.

5. **No write lands without a revision check.** See `annotate.save_text`.

6. **No mutable module-level state in `ui/`.** It would be cross-session
   contamination under the shared link, and the failure is silent. A test walks
   the AST of every UI module and fails on a module-level dict, list or set.

## Three Gradio facts worth knowing before you edit the UI

These each cost an afternoon, and each fails *silently*.

**`css`, `js` and `head` belong to `launch()`, not to `Blocks()`.** They moved in
Gradio 6. Passed to the constructor they are ignored with a warning and the
workspace comes up with collapsed panes and no keyboard. `ui.app.launch_kwargs`
is the one place that assembles them; use it.

**`allowed_paths` must include `STATE_DIR`.** Gradio refuses to serve a file
outside the working directory, the system temp directory, or a path it has been
told about. Both the rendered page images and the export files live under
`STATE_DIR`, which is configurable. Without this, "Check the printed page" and
every download fail — and only on installations that configured their storage
deliberately.

**A component with `visible=False` is not in the DOM at all.** An earlier
version of the keyboard shortcuts clicked six invisible proxy buttons; there was
nothing to click. `annotation.js` drives the real radio instead.

## The aligned test set (`core/aligned.py`)

`data/aligned_v2/` sits in the repository beside `board_outputs/` (or wherever
`TULANA_ALIGNED_DIR` points; an older checkout's `aligned-docMT-test/` is still
found). It is the aligner team's delivery, copied unchanged from
`data/aligned_v2` of document-mt-alignment-bodhan-iitr: 62
book pairs whose layout JSON an alignment model (gemini-3.5-flash, prompt v4)
has rewritten, exported with `scripts/export_aligned.py --merge paragraph
--align-meta`, then revised (v2). The folder's own `README.md` describes every
field, `CHANGELOG.md` and `changelog.jsonl` every v2 change. In short:

- the OCR blocks of one segment merged into one block (the originals kept in
  `members`), and a shared `align_id` on both sides of each segment;
- paragraph-level merging: consecutive model units of one paragraph joined
  into one segment, the units listed in `merged_units` (28,817 segments in v2,
  30,192 in v1, from 42,309 units); `part` (`"1/2"`) on a segment that runs
  over a page break;
- v2: 359 English pages dropped (`align_status: dropped_page_mismatch`, with
  `drop_reason` and `drop_detail`); every unit with an English part there
  unlinked on both sides; those blocks and the page's other text blocks
  `align_state: page_dropped` (`align_note` `page_dropped` or
  `counterpart_page_dropped`), counted under `page_dropped`; and markup put
  back on 3,302 translation blocks (`markup_restored: true`). In
  `export_summary.json`, `units` stays v1's and `v2.units_removed` says how
  many went;
- per block `aligned` and `align_state` (`aligned`, `unpaired`, `page_failed`,
  `not_processed`, `no_text`, `page_dropped`), `align_relation`,
  `align_confidence`, `align_note`, `flags`;
- per page `align_status` and `align_summary` (counts of OCR text blocks by
  state), per file `alignment.summary` with `aligned_pct`;
- `export_summary.json` (per pair: files, `units`, `units_before_merge`,
  `merge`), `failed_pages.tsv` (the 116 English pages that failed).

Its README calls it pre-annotation for human verification. The importer turns
each pair into an ordinary Setu project whose rows are the model's segments.

**Deliveries are sets.** The folder can be replaced by a new export with the
same pair ids, so a pair id alone does not say which data a project holds.
`describe(root)` hashes every `.json` and `.tsv` in the folder (relative path
and bytes; cached by size and mtime) and reads its level from
`export_summary.json` (`merge: "paragraph"` → `paragraph`, else `unit`). Each
distinct fingerprint is one row of `setu_aligned_set`
(`set_id = ids.derive("as", fingerprint)`, `level`, `label`, counts, `current`).
`setu_aligned_pair` maps each project to its set and pair id, with a JSON
`summary` (per-side and total counts, `aligned_pct`, `not_aligned`). Books are
keyed `dedup_key = "aligned:<set_id>:<pair_id>:<side>"` and their `book_key`
is derived from the set too, so two deliveries never share a book, a segment
or a row.

- `resolve_set` makes the folder's set the current one (creating it if new).
  `pairs(con)` lists the current set; `earlier_pairs(con)` lists pairs of
  other sets that hold an answer or a correction — the only ones the picker
  shows from an earlier delivery. Nothing of an earlier set is ever changed.
- Setu v7 imported the unit-level delivery before sets existed; its books
  carry `aligned:<pair_id>:<side>`. `adopt_legacy` (idempotent, run at every
  start) files those projects under `LEGACY_SET = "as_LEGACYUNIT"`.
  `_find_set` maps a unit-level folder to the legacy set when it has not
  claimed a fingerprint yet, so a v7 install whose folder was never replaced
  does not import its pairs a second time.
- `status(con)` says what is in the folder and what of it is imported,
  including `new_set` and `known_sets`, and never writes.

**When it runs.** `launch_annotation.import_aligned_set()` at start-up, after
the text layer is built: it adopts v7 projects, then imports what is waiting,
or — when nothing is — makes the folder's set current, so putting an earlier
export back lists its pairs again. Pairs already imported are skipped, so a
restart costs a hash of the folder (well under a second for its 58 MB).
`POST /api/setu/aligned/import` does the same from the page (the "Load …
pairs" button). `GET /api/setu/aligned` returns `pairs`, `earlier` and
`status`, with the server's folder path removed. One transaction per pair: a
pair imports whole or not at all, and a bad one is reported without stopping
the others.

**What it writes, all of it in `setu_*`:**

- two `setu_book` rows per pair. One per side per pair per set, because an
  English book is merged differently for each language and each delivery.
  They keep the raw book's `relpath`, so page pictures still work, and
  `corpus.RAW` keeps them out of the board/class/language dropdowns;
- one `setu_segment` per merged block, in reading order. A segment that runs
  over a page break is one segment (its parts folded into the first), with
  `block_ids` naming every member on every page;
- one `setu_hint` per segment: what the model said (relation, confidence,
  note, flags, parts, pages, page status) and, from schema 5, `state` (the
  `align_state`) and `units` (the `merged_units`, JSON); from schema 6,
  `markup` (the model put markup back on it);
- one `setu_seg_part` per part of every segment: page, box as fractions of the
  page, and the member boxes when there are several — what the page view
  draws, including the second half of a segment on the page it runs onto;
- one `setu_page_meta` per page: status, the counts by state including
  `page_dropped` (counted from the blocks, which on every page of the delivery
  agree with `align_summary`), `drop_reason`, and the page's pixel size — for
  drawing it blank at the right shape, and for choosing the part of the PDF
  page the parser measured on (below);
- a project with one `setu_row` per segment pair (`origin = 'aligned'`,
  `confidence` = the lower of the two sides' labels as 0.9 / 0.6 / 0.3 — an
  ordering, not a probability). Text the model left unpaired becomes a
  one-sided row (`origin = 'unpaired'`) where it falls, except what
  `aligned.wants_row` leaves out: `not_processed`, `no_text` and
  `page_dropped` blocks, `page_furniture` notes and the noise kinds (headers,
  footers, page numbers, pictures), which stay segments without a row as in
  every other project.

**The share aligned** is `aligned / (text_blocks − not_processed)` over both
files of a pair — the aligner team's viewer's own formula (`pct`), checked
against it on all 62 pairs. In v2 `text_blocks` includes `page_dropped`, so
dropped text counts as not aligned, as in the viewer. `attention_near` finds the nearest pages either
way whose `unpaired + page_failed > 0`, for "Only pages with text not
aligned".

**Provenance.** `source_text` is rebuilt from the RAW layout in
`board_outputs/` by joining the members' text, so it is byte for byte what the
OCR read. Where the model's text differs, it is written as the passage's first
revision in `setu_text`/`setu_rev`, `updated_by = "model:gemini-3.5-flash"`,
reason `model-correction`. `annotate.sync_edited` and `resync_edited_flags`
ignore model-written text, so `setu_row.edited` stays "corrected by a person";
the interface, Saved work and the exports report the model's changes
separately (`model_edited`; export columns `source_model_corrected`,
`target_model_corrected`, plus `unit_id`, `model_flags` and `model_units`).
`api._actor` strips a leading `model:` from any name a client sends, and
`annotate._move_text` keeps the model's credit when a person re-pairs a
passage.

**Guards.** `workspace.build_rows` refuses an aligned project even with
`force`, and `create_project` refuses to put an aligned book beside anything
but its own partner. A deleted aligned project is imported again, fresh, at the
next start (`_drop_orphans` clears its books first; revision numbers continue
the history `setu_rev` keeps). Every file is untrusted: `safe_relpath` refuses
absolute, `..`, drive-letter and NUL paths; `_load` checks the shape of every
page and block and caps the file size; an unknown `align_state` is worked out
again from the block (`block_state`, the viewer's own rule), `merged_units`
are filtered to short safe labels, malformed summaries are dropped; files that
resolve outside their folder (symlinks) are not read; the folder name must
look like a pair id. A refused pair is reported by name and reason, never by
content.

**The page view.** `GET /pages/{book}/{page}/blocks` adds, for an aligned
book, `page_meta`, `attention_prev`/`attention_next` and `parts` (`sid`,
`part`, `of`, `box`, `members`, `state`, `seg_page`, `rid`, `row_seq`,
`status`, `paired`). `prev_page`/`next_page` come from `setu_seg_part` when
the book has parts, so a page holding nothing but the rest of a passage is
still a page; v7 books, which have none, fall back to `setu_segment`. Without
scans the workspace draws the page blank at its real shape (`.blankpage`)
with one box per part: one colour per pair on both pages (`pairColour`, never
in the red band), red dashes for `unpaired`/`page_failed`, member boxes dashed
inside, a box on a later page selecting the whole passage
(`selectElsewhere`). In the text view the same continuation is one "continued"
card. The workspace's page-hop for an empty column (the two-language books)
now follows the direction of travel and never fires on a page with parts.

**Maths.** KaTeX 0.16.9 (MIT, from npm) is vendored under
`ui/static/work/vendor/katex/` and loaded only when a page is first shown, so
it works with no outside network. `typeset()` runs auto-render with `$…$` and
`$$…$$`, `throwOnError: false` and KaTeX's default `trust: false` (no
`\href`, no HTML). It never runs in Correct it mode or inside anything
editable, and it only changes the DOM, never the text that is saved.

**Exports.** The Excel writer keeps every string as text: openpyxl would store
one that starts with `=` as a formula, which Excel then evaluates (a line of
maths opened as `#NAME?`). CSV and the other formats are written exactly as
saved.

**The two-language Andhra Pradesh books** hold English on odd pages and the
Telugu on the page after, in one file (`lang 'en+te'`). `read_pair` splits the
file by page, using the English page named in each `align_id`. The page view
returns `prev_page`/`next_page` (the nearest pages holding text) and
`book.aligned`; for an aligned book the workspace steps with them, so it skips
the other language's pages.

**Kannada** is `kn` in the Karnataka books and `ka` in the Maharashtra ones; the
importer goes by the language *name*, never the code.

**Schema 5 and 6.** `setu_hint.state` and `setu_hint.units` (5) and
`setu_hint.markup`, `setu_page_meta.page_dropped` and `.drop_reason` (6) are
added by `store._migrate` to an older database; the four new tables are
created by `schema.sql` (`CREATE TABLE IF NOT EXISTS`). Nothing outside
`setu_*` is touched, and no v7 row is rewritten.

**The scans under the boxes (`core/sources.py`).** Every box is a fraction of
the image the parser measured on, and that image was a render of the PDF
page. PyMuPDF draws a page's CropBox; pdftoppm and pdf2image, the usual OCR
front ends, draw its MediaBox. Where the two differ, fractions of one drawn
over the other put every box beside its text. A scanned book adds a third
case: the parser read the scan itself, and the scan can sit inside the page
with margins round it. `page_area` therefore takes, per page, the scan's own
rectangle when an image on the page has exactly the parser's pixel size
(drawn upright, covering most of the page), and otherwise the box whose
shape (rotation applied) matches the parser's image
(`raster_size`: `setu_page_meta`, else the studio's `pl_pages`), and `_render`
draws that box; the choice and how well it fits (`fit_error`, relative
difference of aspect ratios; `FIT_TOLERANCE` 1.5%) travel with every
`SourceView`. `_find_pdf` takes a book's PDF at its relative path, or else by
file name — and of several files with that name, the one whose folders match
the most of the relative path; a tie finds nothing, because NCERT's English
and Hindi chapters share names. `test_mapping.py` proves all of it on PDFs
built for the purpose; `check_mapping.py` audits every aligned page against
the real PDFs — shape, the PDF's own words inside the boxes, and an ink test
that searches shifts and scales of all the boxes for the best fit (a matched
filter: ink above the page's average) — and exits with the number of book
sides that need a look.

**The screen.** Read mode draws the book's own formatting (`richHTML`): maths
set aside first for KaTeX, then an allow-list of tags (tables, `br`, `b`,
`sup`, lists…) written back with no attribute but a numeric
`colspan`/`rowspan`, `**bold**` to bold, everything else escaped — so nothing
in a passage can run, link or load. Correct it mode shows and saves the raw
text. Without scans, `boxText` writes each passage's words into its box, sized
to it. Page data is kept for 20 s (`PAGECACHE`, emptied by any write) and the
pages either side are fetched in advance, so a page turn is instant. `--txt`
(A+ / A−, 15–30 px, remembered per browser) sizes the passages and answers.

`GET /api/setu/health` does a real read and reports the durability pragmas
actually in force.

## Adding a board, a language or a book

A data operation. Drop the parsed JSON into `board_outputs/output/` and restart
the launcher — it imports anything new into `pl_*` and segments it. Books
already built are skipped, so a new textbook costs only itself.

Nothing enumerates boards or languages. The cascade is `GROUP BY` over
`setu_book`, so a board that exists in the data appears in the dropdown and one
that does not, does not. `config.BOARDS` only supplies a display name.

A right-to-left language needs one entry in `ui.workspace.RTL_SCRIPTS`, keyed by
the script name the corpus records — not by language.

## Adding an export format

One function:

```python
@register("yaml", "YAML", "yaml", "application/yaml",
          note="One document per pair.")
def _yaml(rows, fh, meta):
    n = 0
    for r in rows:
        fh.write("---\n")
        for k, v in r.items():
            fh.write(f"{k}: {v!r}\n")
        n += 1
    return n
```

It appears in the Download tab immediately — the list is generated from the
registry. `binary=True` for a handle opened in binary mode, `requires="pkg"` for
an optional dependency (reported unavailable with the install command rather
than failing at download time), `pairs_only=True` if one-sided rows cannot be
represented. Return the number of records actually written; that is what the
"left out" count is computed from.

## Adding a status

Add a `Status` to `models.STATUSES`. Progress counters, filters, the radio, the
exports and the manual all read from that tuple.

One constraint the keyboard imposes: `annotation.js` maps a digit to the radio
at that index, so the `shortcut` values must stay equal to the position in
`STATUSES`. A test asserts it.

## Improving the aligner

`align.py` is self-contained and takes two lists of segment dicts. The weights at
the top were fitted against the page-parallel Maharashtra editions, where the
correct answer is known to be on the same page; the test suite re-measures that
against the real corpus and fails below 90%.

Worth attention: a length model (Gale–Church) for the fills, which are currently
pure order-matching; character-level similarity for transliterated proper nouns;
cross-lingual embeddings, at the cost of a model dependency in a tool that
currently has none.

Changing the aligner does not disturb existing work: rows are generated once, and
`build_rows` refuses to discard rows carrying human answers unless forced.

## Moving to PostgreSQL

1. Write `PostgresRepository(Repository)` in `store.py` with the same six
   methods. The services call only those.
2. Translate `schema.sql`: `INTEGER PRIMARY KEY` → `BIGSERIAL`, `REAL` →
   `DOUBLE PRECISION`. `INSERT ... ON CONFLICT DO UPDATE` is already PostgreSQL
   syntax.
3. Replace `setu_seg_fts` with a `tsvector` column and a GIN index;
   `search.SearchRepo._matching_sids` is the only caller.
4. Keep the revision check exactly as it is — it is ordinary optimistic
   concurrency and needs no database-specific locking.

No service, endpoint or interface file changes.

## What production would add

The boundary is deliberate. These are cleanly possible and none is present:

* real authentication and roles — there are no accounts, only a name field
* reviewer stages and adjudication — `setu_status_rev` already records who set
  what and when, which is the data those need
* backups and monitoring — the database is one SQLite file
* background export jobs — exports are synchronous, which is fine at this size
* several application instances — SQLite WAL allows one writer at a time, which
  is what the move to PostgreSQL is for

## Performance, measured

On the 121-book corpus (132,678 segments):

| Operation | Time |
|---|---|
| First-time build | ~16 s, one transaction per book |
| Creating a project (1,826 rows) | ~0.1 s |
| Aligning two 2,000-segment books | ~0.01 s |
| One save, 12 concurrent writers | 12 ms median, 154 ms p95 |
| A page of 50 rows | ~5 ms |
| FTS search over 132k segments | ~10 ms |
| Source-view crop, first / cached | 92 ms / 0.2 ms |

Navigation is index-backed (`WHERE seq > ? ORDER BY seq LIMIT 1`), so moving
through a 200,000-row corpus costs the same as through a 200-row one. Nothing
loads a whole book into memory except the aligner, which needs both books at
once. Exports stream through a cursor.

The autosave timer is the one standing cost: one event every three seconds per
open tab. The handler compares four values in the session dictionary and returns
without touching the database when nothing changed, so an annotator reading
rather than typing costs a dictionary comparison.

## Observability

`setu_event` is an append-only log of every project creation, build, text save,
status change, attach, split, merge and export, with actor and session.
`GET /api/setu/events` reads it. It records *what* happened and how much, never
the text itself — a log is not a place to duplicate a corpus, and a test asserts
that a saved secret does not appear in it.

`GET /api/setu/health` does a real read and reports the durability pragmas
actually in force.

## Tests

```bash
python3 test_annotation.py          # 123 tests, about 75 seconds
python3 test_annotation.py -v
python3 test_aligned.py             # the aligned test set, about 15 seconds
python3 test_mapping.py             # boxes on the printed page, seconds
python3 check_mapping.py            # every aligned page against the real PDFs (git lfs pull first)
SETU_ALIGNED_FULL=1 python3 test_aligned.py   # also all 62 real pairs, about 2½ minutes
```

`test_aligned.py` builds a small pair in the dataset's own shape — a model
correction on each side, OCR blocks merged into one passage, two units joined
into a paragraph over a page break, an empty block, unpaired text, a page never
sent and a page that failed — and checks the mapping, provenance, re-import,
the rebuild guard, states and page counts, the page-view API, exports, the
bilingual split, deliveries as sets (a new delivery beside the old one's work,
a Setu v7 database upgraded, a folder put back), the launcher's messages, and a
set of hostile files. When `data/aligned_v2/` and `board_outputs/` are in
the checkout it also checks the real pairs against the dataset's own numbers:
pairs per book pair from `export_summary.json`, every page's counts and status,
the share aligned by the viewer's formula, and every passage's source against
the raw OCR (four pairs by default, all 62 with `SETU_ALIGNED_FULL=1`).

The browser side of the aligned set — the picker, the page counts, "Only pages
with text not aligned", the blank-page view and its colours, continuation
boxes and cards, typeset maths in Read mode only, the notes, and a v7 database
upgraded — was checked with Playwright against a running server on the real
data (78 checks on a fresh install of v2, 83 on an upgraded Setu v7 database).

Each test gets its own database, so order never matters. The alignment-accuracy
test uses the real corpus when present and skips itself when not.

The browser-side behaviour — synchronised scrolling, the keyboard, zoom,
session isolation, the conflict panel — is not covered by this suite. It was
verified with Playwright against a running server; the checks are described in
the report and are worth re-running by hand after a Gradio upgrade, because that
is what breaks them.
