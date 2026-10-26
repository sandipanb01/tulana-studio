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
      aligned.py              the aligned test set (aligned-docMT-test) importer
    ui/                       Gradio Blocks
      app.py                  layout and event wiring, no logic
      workspace.py            every annotation callback
      panels.py               saved work, download, manuals
      session.py              the per-session dictionary
      render.py               the HTML fragments
      static/                 annotation.css, annotation.js
    api.py                    an HTTP surface over the same services
    docs/                     these manuals
  launch_annotation.py        the entry point
  test_annotation.py          123 tests
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

`aligned-docMT-test/` sits next to `board_outputs/`. It holds 62 book pairs whose
layout JSON an alignment model (gemini-3.5-flash, prompt v4) has rewritten: the
OCR blocks of one translation unit merged into one block (the originals kept in
`members`), a shared `align_id` on both sides of each unit, `align_relation`,
`align_confidence`, `align_note`, `flags`, `part` for a unit over a page break,
and `align_status` per page. Its README calls it pre-annotation for human
verification. The importer turns each pair into an ordinary Setu project whose
rows are the model's units.

**When it runs.** `launch_annotation.import_aligned_set()` at start-up, after the
text layer is built: pairs already imported are skipped, so a restart costs
nothing. `POST /api/setu/aligned/import` does the same from the page (the
"Load … pairs" button). `GET /api/setu/aligned` lists the pairs with progress.
One transaction per pair: a pair imports whole or not at all, and a bad one is
reported without stopping the others.

**What it writes, all of it in `setu_*`:**

- two `setu_book` rows per pair, `dedup_key = "aligned:<pair_id>:src|tgt"`. One
  per side per pair because an English book is merged differently for each
  language. They keep the raw book's `relpath`, so page pictures still work, and
  `corpus.RAW` keeps them out of the board/class/language dropdowns;
- one `setu_segment` per merged block, in reading order. A unit that runs over a
  page break is one segment (its parts folded into the first);
- one `setu_hint` row per segment: what the model said (relation, confidence,
  note, flags, parts, pages, page status);
- a project with one `setu_row` per unit (`origin = 'aligned'`, `confidence` =
  the lower of the two sides' labels as 0.9 / 0.6 / 0.3 — an ordering, not a
  probability). Blocks the model left unpaired become one-sided rows
  (`origin = 'unpaired'`) where they fall, except headers, footers, page
  numbers, pictures and empty blocks (`aligned.wants_row`), which stay
  segments without a row as in every other project.

**Provenance.** `source_text` is rebuilt from the RAW layout in `board_outputs/`
by joining the members' text, so it is byte for byte what the OCR read. Where
the model's text differs, it is written as the passage's first revision in
`setu_text`/`setu_rev`, `updated_by = "model:gemini-3.5-flash"`, reason
`model-correction`. `annotate.sync_edited` and `resync_edited_flags` ignore
model-written text, so `setu_row.edited` stays "corrected by a person"; the
interface, Saved work and the exports report the model's changes separately
(`model_edited`; export columns `source_model_corrected`,
`target_model_corrected`, plus `unit_id` and `model_flags`). `api._actor`
strips a leading `model:` from any name a client sends, and
`annotate._move_text` keeps the model's credit when a person re-pairs a passage.

**Guards.** `workspace.build_rows` refuses an aligned project even with
`force`, and `create_project` refuses to put an aligned book beside anything but
its own partner. A deleted aligned project is imported again, fresh, at the
next start (`_drop_orphans` clears its books first; revision numbers continue
the history `setu_rev` keeps). Every file is untrusted: `safe_relpath` refuses
absolute, `..`, drive-letter and NUL paths; `_load` checks the shape of every
page and block and caps the file size; files that resolve outside their folder
(symlinks) are not read; the folder name must look like a pair id. A refused
pair is reported by name and reason, never by content.

**The two-language Andhra Pradesh books** hold English on odd pages and the
Telugu on the page after, in one file (`lang 'en+te'`). `read_pair` splits the
file by page, using the English page named in each `align_id`. The page view
returns `prev_page`/`next_page` (the nearest pages holding text) and
`book.aligned`; for an aligned book the workspace steps with them, so it skips
the other language's pages.

**Kannada** is `kn` in the Karnataka books and `ka` in the Maharashtra ones; the
importer goes by the language *name*, never the code.

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
python3 test_aligned.py             # the aligned test set, seconds
SETU_ALIGNED_FULL=1 python3 test_aligned.py   # also all 62 real pairs, about a minute
```

`test_aligned.py` builds a small pair in the dataset's own shape and checks the
mapping, provenance, re-import, the rebuild guard, exports, the bilingual split
and a set of hostile files. When `aligned-docMT-test/` and `board_outputs/` are
in the checkout it also checks the real pairs against `export_summary.json`'s
unit counts, and every passage's source against the raw OCR.

Each test gets its own database, so order never matters. The alignment-accuracy
test uses the real corpus when present and skips itself when not.

The browser-side behaviour — synchronised scrolling, the keyboard, zoom,
session isolation, the conflict panel — is not covered by this suite. It was
verified with Playwright against a running server; the checks are described in
the report and are worth re-running by hand after a Gradio upgrade, because that
is what breaks them.
