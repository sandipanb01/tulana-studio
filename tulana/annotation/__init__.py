"""Setu — Tulana Studio's bilingual annotation subsystem.

Setu (सेतु, "bridge") is where an annotator reads a textbook in English beside
the same textbook in an Indian language, corrects what the layout parser got
wrong on either side, and says whether the two really match.

It lives inside Tulana Studio and reuses it: the same repository, the same
textbook corpus, the same SQLite database, the same PDF and cropping utilities.
It adds tables of its own (all prefixed ``setu_``) and writes to nothing that
existed before it.

Three layers, each importing only from the one below::

    ui/       the Gradio Blocks workspace
    api.py    an HTTP surface over the same services
    core/     identifiers, storage, corpus, alignment, annotation, export

``core`` imports no user-interface library at all, which is what lets the same
services drive the Gradio workspace, the HTTP API and the tests without any of
them knowing about each other.
"""

__all__ = ["core", "ui", "api"]
__version__ = "1.0.0"
