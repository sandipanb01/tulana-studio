#!/usr/bin/env python3
"""Start Setu, the annotation workspace, and print a link to share.

    python3 launch_annotation.py                 # public link + local link
    python3 launch_annotation.py --no-share      # this machine only
    python3 launch_annotation.py --port 7870
    python3 launch_annotation.py --prepare       # build the text layer, then start

What it does, in order:

1. Makes sure the annotation database has the textbook text in it, and offers
   to build it if not. This takes about a minute and happens once.
2. Builds the Gradio interface.
3. Launches it, passing the stylesheet and browser script to ``launch()``,
   which is where Gradio 6 expects them.
4. Mounts the rest of Tulana Studio underneath the same server at ``/studio``,
   so one link reaches both the annotation workspace and the existing block,
   pair and export tools.
5. Prints the links.

Sharing is a tunnel, not a copy. Every annotation is written to this machine's
``state/`` folder, so restarting the process — and getting a new link — never
loses anybody's work.
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
import time
import webbrowser
from pathlib import Path
from urllib.parse import urljoin

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import config  # noqa: E402

MOUNT = "/studio"


def _log_setup(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S")
    # Gradio and its HTTP stack are chatty at INFO and drown out anything
    # actually worth seeing in a terminal somebody is watching.
    for noisy in ("httpx", "httpcore", "urllib3", "asyncio", "matplotlib"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def _import_parsed_layout() -> bool:
    """Read ``board_outputs/`` into Tulana's own parsed-layout tables.

    Setu builds on those tables rather than re-parsing anything, so on a fresh
    checkout they have to exist first. Doing it here rather than printing a
    Python one-liner for somebody to paste is the difference between a tool
    that starts and a tool that needs a developer present the first time.
    """
    import blocks
    import db

    found = blocks.find_corpus()
    if not found:
        print("[setu] no parsed layout found. Setu needs the JSON files that "
              "the document parser produced.")
        print(f"[setu] looked beside {config.DATA_DIR} and under the repository "
              f"for a 'board_outputs/output' folder.")
        return False
    print(f"[setu] reading the parsed layout from {found}")
    with db.tx() as con:
        blocks.ensure_schema(con)
        report = blocks.ingest(con, log=lambda _m: None)
    print(f"[setu] {report['books']} books, {report['pages']:,} pages, "
          f"{report['blocks']:,} blocks")
    for problem in report.get("problems", [])[:5]:
        print(f"[setu]   {problem}")
    return bool(report["books"])


def prepare(force: bool = False) -> bool:
    """Make sure the annotation text layer exists. Returns True if usable."""
    from annotation.core import corpus, store

    with store.ro() as con:
        counts = corpus.CorpusRepo(con).counts()
    if counts["books"] and not force:
        print(f"[setu] {counts['books']} textbooks ready "
              f"({counts['segments']:,} pieces of text)")
        return True

    print("[setu] preparing the textbook text — about a minute, once")
    try:
        with store.connect() as con:
            report = corpus.build(con, rebuild=force, log_fn=lambda m: print("[setu]", m))
    except Exception as exc:
        # Almost always the same cause on a fresh checkout: the parsed layout
        # has not been imported yet. Import it and try once more, rather than
        # handing the problem back.
        print(f"[setu] {exc}")
        try:
            if not _import_parsed_layout():
                return False
            with store.connect() as con:
                report = corpus.build(con, rebuild=force,
                                      log_fn=lambda m: print("[setu]", m))
        except Exception as exc2:
            print(f"[setu] could not prepare the textbooks: {exc2}")
            return False
    if report["errors"]:
        print(f"[setu] {len(report['errors'])} book(s) could not be read:")
        for e in report["errors"][:5]:
            print(f"[setu]   {e['book']}: {e['error']}")
    if report["unmapped_labels"]:
        print(f"[setu] parser labels with no mapping: {report['unmapped_labels']}")
    return bool(report["books_built"] or report["books_skipped"])


def at(base: str, path: str = "") -> str:
    """Join a base URL to a path below it.

    Gradio returns the share URL without a trailing slash and the local URL
    with one, depending on version and platform. Concatenating blindly
    produced ``https://xxxx.gradio.livestudio/`` once, printed as the headline
    instruction; urljoin against a normalised base cannot.
    """
    if not base:
        return ""
    root = base if base.endswith("/") else base + "/"
    return urljoin(root, path.lstrip("/")) if path else root


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Start the Setu annotation workspace.")
    ap.add_argument("--port", type=int, default=int(os.environ.get("TULANA_PORT", "7862")),
                    help="preferred port; the next free one is used if it is taken")
    ap.add_argument("--host", default=os.environ.get("TULANA_HOST", "0.0.0.0"))
    ap.add_argument("--no-share", action="store_true",
                    help="do not create a public gradio.live link")
    ap.add_argument("--prepare", action="store_true",
                    help="rebuild the textbook text layer before starting")
    ap.add_argument("--open", action="store_true", help="open a browser window")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    _log_setup(args.verbose)

    try:
        import gradio as gr
    except ImportError:
        print("Gradio is not installed. Run:  pip install gradio")
        return 2

    if not prepare(force=args.prepare):
        return 1

    # Page images are regenerable and can accumulate; sweep once at start-up
    # rather than on a timer competing with an annotator's autosave.
    try:
        from annotation.core import sources
        swept = sources.prune_cache()
        if swept["removed"]:
            print(f"[setu] cleared {swept['removed']} cached page images")
    except Exception as exc:                     # pragma: no cover - best effort
        logging.getLogger("setu").debug("cache sweep skipped: %s", exc)

    from annotation.ui import app as ui

    ok, note = ui.ready()
    print(f"[setu] {note}")
    if not ok:
        return 1

    demo = ui.build()

    # Gradio's queue is what keeps one annotator's slow save from blocking
    # everyone else's typing. The default concurrency limit is 1 per event,
    # which would serialise every autosave across all users.
    demo.queue(default_concurrency_limit=12, max_size=256)

    port = config.free_port(args.port)
    if port != args.port:
        print(f"[setu] port {args.port} was busy, using {port}")

    launch = ui.launch_kwargs(
        server_name=args.host, server_port=port, share=not args.no_share,
        prevent_thread_lock=True, inbrowser=False, show_error=True,
        max_threads=64)

    server_app, local_url, share_url = demo.launch(**launch)

    # The rest of Tulana Studio, under the same server. Mounted after launch
    # because a sub-application mounted onto a running server never receives
    # startup events — so it is also initialised explicitly, which is the bug
    # that once left every dropdown empty with no explanation.
    studio_url = ""
    try:
        from app import app as studio_app, initialise
        initialise()
        server_app.mount(MOUNT, studio_app)
        studio_url = at(share_url or local_url, MOUNT.lstrip("/") + "/")
    except Exception as exc:
        logging.getLogger("setu").warning(
            "the rest of Tulana Studio could not be mounted: %s", exc)

    public = at(share_url)
    local = at(local_url)

    print(f"""
{'=' * 72}
  SETU IS RUNNING — the parallel textbook annotation workspace

  Share this link with your annotators:
      {public or '(no public link — see the note below)'}

  On this machine:
      {local}
""" + (f"""  The rest of Tulana Studio (blocks, saved pairs, page images):
      {studio_url}
""" if studio_url else "") + f"""
  Textbooks : {config.DATA_DIR}
  Your work : {config.STATE_DIR}

  Several people can use the link at the same time. Each gets their own
  session; nobody sees anyone else's unsaved text. Two people editing the
  same pair are both told, and neither is overwritten.

  Keep this process running. Closing it ends the link — annotations are
  already saved on this machine and will be there when it restarts.
{'=' * 72}
""")

    if not share_url and not args.no_share:
        print("  The gradio.live tunnel could not be created. This machine may have\n"
              "  no route to Gradio's tunnel service, or the service may be down.\n"
              "  The workspace still works on the local link above, and on this\n"
              "  machine's address on the local network.\n")
    if args.open and (public or local):
        try:
            webbrowser.open(public or local)
        except Exception:                        # pragma: no cover - headless
            pass

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\n[setu] shutting down. Everything saved is on disk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
