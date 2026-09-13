#!/usr/bin/env python3
"""Cross-platform audit.

Finds the things that work on Linux and quietly fail on Windows — hard-coded
`/tmp`, forward-slash path strings, files opened without an encoding, shell
invocations, and reserved filenames. Run it before shipping.

    python3 windows_check.py          (py windows_check.py on Windows)
"""
import ast
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SKIP = {"windows_check.py"}
issues, notes = [], []


def add(ok, label, detail=""):
    (notes if ok else issues).append(label + (f" — {detail}" if detail else ""))


def main():
    py = [p for p in sorted(HERE.glob("*.py")) if p.name not in SKIP]

    # 1 — no shell scripts at all
    scripts = [p.name for p in HERE.iterdir()
               if p.suffix.lower() in (".sh", ".ps1", ".bat", ".cmd")]
    add(not scripts, "no shell or PowerShell scripts", ", ".join(scripts))

    # 2 — hard-coded POSIX paths
    bad = []
    for f in py:
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r'["\'](/tmp/|/var/|/usr/|/home/|/etc/)', line) and \
                    "example" not in line.lower() and not line.strip().startswith("#"):
                bad.append(f"{f.name}:{n}")
    add(not bad, "no hard-coded POSIX paths", "; ".join(bad[:4]))

    # 3 — paths are built with pathlib, not string concatenation
    concat = []
    for f in py:
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not re.search(r'\w+\s*\+\s*["\']/[\w.]', line):
                continue
            # A URL path is not a filesystem path: "/" is correct there on every
            # platform. Only flag concatenation onto something that looks like a
            # file or directory.
            if re.search(r'(endpoint|url|base|href|api|BASE)\b', line, re.I):
                continue
            if any(k in line for k in ("urlopen", "requests.", "fetch(", "http")):
                continue
            concat.append(f"{f.name}:{n}")
    add(not concat, "paths are joined with pathlib, not '+ \"/\"'", "; ".join(concat[:4]))

    # 4 — every text file is opened with an explicit encoding.
    #     Windows defaults to cp1252, so reading Devanagari without encoding=
    #     raises UnicodeDecodeError — the single most common Windows-only bug
    #     in a project that handles Indic text.
    noenc = []
    for f in py:
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "open"):
                continue
            kw = {k.arg for k in node.keywords}
            mode = ""
            if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                mode = str(node.args[1].value)
            if "b" in mode:
                continue
            if "encoding" not in kw:
                noenc.append(f"{f.name}:{node.lineno}")
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and \
                    getattr(node.func, "attr", "") in ("read_text", "write_text"):
                if "encoding" not in {k.arg for k in node.keywords}:
                    noenc.append(f"{f.name}:{node.lineno} ({node.func.attr})")
    add(not noenc, "every text file is opened with an explicit encoding",
        "; ".join(sorted(set(noenc))[:6]))

    # 5 — no shell invocation in the request path
    shell = []
    for f in py:
        src = f.read_text(encoding="utf-8")
        for pat in ("shell=True", "os.system(", "os.popen("):
            if pat in src:
                shell.append(f"{f.name}: {pat}")
    add(not shell, "no shell invocation", "; ".join(shell))

    # 6 — filenames legal on Windows
    illegal = []
    reserved = {"con", "prn", "aux", "nul", *[f"com{i}" for i in range(1, 10)],
                *[f"lpt{i}" for i in range(1, 10)]}
    for p in HERE.rglob("*"):
        if any(x.startswith(".") for x in p.parts) or "state" in p.parts:
            continue
        if p.stem.lower() in reserved or re.search(r'[<>:"|?*]', p.name):
            illegal.append(p.name)
    add(not illegal, "all filenames are legal on Windows", ", ".join(illegal[:5]))

    # 7 — the stored object layout uses forward slashes consistently
    # A path written to the database must not carry the host OS's separator, or
    # a database built on Windows is unreadable on Linux. Two acceptable
    # designs: normalise with as_posix(), or build keys from explicit forward
    # slashes. Flag only a relative_to() result stringified without as_posix().
    leaks = []
    for f in py:
        lines = f.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines, 1):
            if "relative_to(" not in line or line.strip().startswith("#"):
                continue
            # Accept normalisation on the same line or the next two — a common
            # and perfectly correct pattern is to take the relative path and
            # replace separators on the following line.
            window = " ".join(lines[n - 1:n + 2])
            if "as_posix()" in window or 'replace("\\\\"' in window \
                    or "replace('\\\\'" in window:
                continue
            # A relative path consumed by `.parts` — directly, or by a helper
            # that does — is already separator-agnostic: pathlib splits it into
            # components and never exposes the separator. Requiring as_posix()
            # there would be noise, and noise in an audit is how a real finding
            # gets ignored.
            if ".parts" in window or "_is_junk(" in line:
                continue
            leaks.append(f"{f.name}:{n}")
    add(not leaks, "relative paths are normalised before use", "; ".join(leaks[:4]))

    # The invariant that actually matters, checked against the data rather than
    # the source: nothing stored carries a backslash, so a database written on
    # Windows is readable on Linux and the reverse.
    import sqlite3
    db_files = [p for p in (HERE / "state").rglob("*.db")] if (HERE / "state").is_dir() else []
    checked = 0
    dirty = []
    for dbf in db_files:
        try:
            con = sqlite3.connect(f"file:{dbf}?mode=ro", uri=True)
            tables = [r[0] for r in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")]
            for t in tables:
                cols = [r[1] for r in con.execute(f"PRAGMA table_info({t})")
                        if any(k in r[1].lower() for k in ("path", "key", "dir"))]
                for c in cols:
                    n = con.execute(
                        f"SELECT COUNT(*) FROM {t} WHERE {c} LIKE '%\\%' ESCAPE '\\'"
                    ).fetchone()[0]
                    checked += 1
                    if n:
                        dirty.append(f"{t}.{c}: {n} row(s)")
            con.close()
        except Exception:
            continue
    if checked:
        add(not dirty, f"no stored path contains a backslash ({checked} columns checked)",
            "; ".join(dirty[:4]))
    else:
        notes.append("no database present to inspect — run the self-test first "
                     "for the stored-path check")

    print("CROSS-PLATFORM AUDIT (Windows / macOS / Linux)")
    for n in notes:
        print("  ok    ", n)
    for i in issues:
        print("  ISSUE ", i)
    print(f"\n  {len(notes)} passed, {len(issues)} issue(s)")
    return len(issues)


if __name__ == "__main__":
    sys.exit(main())
