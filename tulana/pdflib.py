"""Single import point for PyMuPDF.

The package is importable as `pymupdf`; `fitz` is a compatibility alias that is
not present in every build. Importing it in one place keeps a missing alias from
breaking one feature at a time.
"""
_error = None
try:
    import pymupdf as fitz
except Exception as _e1:            # pragma: no cover - depends on install
    try:
        import fitz                 # type: ignore
    except Exception as _e2:
        fitz = None                 # type: ignore
        _error = (f"PyMuPDF is not importable as 'pymupdf' or 'fitz' "
                  f"({_e1} / {_e2}). Install it:  pip install PyMuPDF")


def available() -> bool:
    return fitz is not None


def version() -> str:
    return "not installed" if fitz is None else getattr(fitz, "__version__", "unknown")


def error():
    return _error
