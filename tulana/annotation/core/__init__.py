"""The annotation core — everything that is not a user interface.

Layered, and each layer imports only from the ones below it::

    exporters  search  annotate  workspace  align
                      corpus
                      store
                  ids   models

Nothing here imports Gradio, FastAPI or anything else from a presentation
layer. That is what lets the same services drive the Gradio workspace, the HTTP
API and the tests without any of them knowing about each other — and what makes
a different front end later a matter of writing one, not of rewriting this.
"""

from . import align, annotate, corpus, exporters, ids, models, search, store, workspace  # noqa: F401

__all__ = ["align", "annotate", "corpus", "exporters", "ids", "models",
           "search", "store", "workspace"]
