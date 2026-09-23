# Setu — the annotation subsystem

**सेतु**, "bridge". Where an annotator reads a textbook in English beside the
same textbook in an Indian language, corrects what the document parser got wrong
on either side, and says whether the two really match.

This is a subsystem of Tulana Studio, not a separate application. It lives in
the same repository, reads the same textbook corpus, writes to the same SQLite
database, and reuses Tulana's PDF and cropping utilities. It adds tables of its
own — all prefixed `setu_` — and writes to nothing that existed before it.

```bash
cd tulana
python3 launch_annotation.py          # public link + local link
python3 launch_annotation.py --help
```

The first start prepares the textbook text: about a minute, once.

## The shape of it

```
ui/       Gradio Blocks — layout, events, the browser-side script
api.py    an HTTP surface over the same services
core/     identifiers, storage, corpus, alignment, annotation, export, sources
```

`core` imports no user-interface library. That is what lets the same services
drive the Gradio workspace, the HTTP API and 123 tests without any of them
knowing about each other, and it is the property to preserve if you change
anything here.

## What each module is for

| Module | Responsibility |
|---|---|
| `core/ids.py` | identifiers derived from position, never from text |
| `core/models.py` | statuses, segment kinds, Unicode normalisation, maths detection |
| `core/store.py` | connections, durability pragmas, schema, migrations, repository base |
| `core/corpus.py` | deduplicating parsed books and cutting them into segments |
| `core/align.py` | proposing which segment pairs with which |
| `core/workspace.py` | projects, rows, navigation, progress, sessions, soft locks |
| `core/annotate.py` | editing, revisions, conflicts, split and merge |
| `core/search.py` | FTS5 with a `LIKE` fallback |
| `core/exporters.py` | the format registry |
| `core/sources.py` | the bridge to Tulana's PDF cropping, for source verification |
| `ui/app.py` | Gradio layout and event wiring — no annotation logic |
| `ui/workspace.py` | every annotation callback |
| `ui/session.py` | the per-session dictionary |
| `ui/render.py` | the only module that emits HTML |

## The five guarantees

1. **The parser's extraction is never modified.** It is stored in
   `setu_segment.source_text` and written once; edits live in `setu_text`. So
   "restore the original" works on any pair, at any distance in the future.
2. **No write lands blind.** Every save carries the revision it was based on.
   A save that would overwrite somebody else's is refused and both versions are
   shown.
3. **Every version is kept.** `setu_rev` is append-only; nothing deletes from it.
4. **Nothing writes to the tables that existed before.** `db.py` is untouched.
5. **No mutable module-level state in the interface.** Per-session state lives
   in a `gr.State`; that is the whole of the concurrency design.

Each is enforced by a test, and each test was verified by introducing the
failure it is meant to catch.

## Reading further

- `docs/01_manual.md` — the annotator's manual, for someone who has never
  annotated before
- `docs/02_faq.md` — the questions people actually ask
- `docs/03_for_developers.md` — how to add a board, a language, an export
  format or a status; what a PostgreSQL port involves; the Gradio version traps

Those three are also served inside the application, under **Help**.

## Tests

```bash
python3 test_annotation.py
```

123 tests, each with its own database, about 75 seconds. The alignment-accuracy
test measures against the real corpus when it is present and skips itself when
it is not.

Browser behaviour — synchronised scrolling, keyboard shortcuts, zoom, session
isolation, the conflict panel — is not in that suite. It was verified with
Playwright against a running server, and is worth re-checking by hand after a
Gradio upgrade, because that is what breaks it.
