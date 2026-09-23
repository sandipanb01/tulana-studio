#!/usr/bin/env python3
"""Publish Setu and the rest of Tulana Studio on a public link.

    python3 share_gradio.py

Prints an ``https://….gradio.live`` address. The link is a tunnel, not a copy:
everything is still stored in this machine's ``state/`` folder, so restarting —
and getting a new link — never loses an annotation.

WHY THIS FILE IS FOUR LINES LONG
--------------------------------
It used to be a launcher in its own right: it built a small landing page, put
the studio under ``/studio``, and pointed a button at ``/studio/setu/``, which
is where the annotation workspace lived when it was served by FastAPI.

The workspace is now a Gradio application in its own right, built by
``annotation.ui.app.build()`` and served at the root of the server, with the
older studio mounted beneath it at ``/studio``. This file was not updated when
that changed, so it went on serving a landing page whose main button pointed at
``/studio/setu/`` — an address that no longer exists. Anyone who started the
system with this file got a page that looked right, a button that led to

    {"detail":"Not Found"}

and no annotation workspace anywhere, because this file never built one.

Two launchers that must agree about where things live will eventually disagree,
and the one people run is not always the one that was kept current. So this is
no longer a launcher. ``launch_annotation.py`` is the single entry point, and
this delegates to it — including every option it takes:

    python3 share_gradio.py --no-share
    python3 share_gradio.py --port 7900
    python3 share_gradio.py --prepare

``README.md`` and ``docs/05_admin.md`` still name this file, and so do people's
notes, so the name keeps working.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from launch_annotation import main  # noqa: E402


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
