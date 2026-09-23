"""The Gradio Blocks interface.

Everything in this package is presentation. It calls the service layer in
``annotation.core`` and holds no state of its own — not a cache, not a
connection, not a "current row". Per-session state lives in a ``gr.State``,
which Gradio gives each browser session separately; that is the whole of the
concurrency design, and it only holds if nothing here keeps anything at module
level.
"""

from . import app, panels, render, session, workspace  # noqa: F401

__all__ = ["app", "panels", "render", "session", "workspace"]
