"""Where the textbooks come from, and getting them here.

The studio needs PDFs in its data folder. They can arrive three ways, and the
order matters: an archive you already have is unpacked rather than downloaded
again, and only what is genuinely missing is fetched from a link.

Archives are unpacked in place (.7z first, since those commonly wrap a .zip),
and the whole tree is then re-indexed. Nothing here assumes a folder layout.
"""
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

import config

SOURCES_FILE = Path(__file__).parent / "sources.json"
ARCHIVE_SUFFIX = {".zip", ".7z", ".tar", ".tgz"}


def load() -> list:
    try:
        data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [s for s in data.get("sources", []) if isinstance(s, dict)]


def local_archives(root: Path = None) -> list:
    root = root or config.DATA_DIR
    if not root.is_dir():
        return []
    return sorted(p for p in root.rglob("*")
                  if p.is_file() and p.suffix.lower() in ARCHIVE_SUFFIX
                  and not any(x.startswith(".") for x in p.parts))


def status(root: Path = None) -> dict:
    """What the studio has, and what each configured source would still add."""
    root = root or config.DATA_DIR
    pdfs = list(root.rglob("*.pdf")) if root.is_dir() else []
    archives = {p.name.lower(): p for p in local_archives(root)}
    out = []
    for s in load():
        fname = (s.get("file") or "").lower()
        have = bool(fname and fname in archives)
        if not have and fname:
            stem = Path(fname).stem.lower().rstrip("_0123456789 ")
            have = any(Path(a).stem.lower().rstrip("_0123456789 ") == stem
                       for a in archives)
        out.append({**{k: s.get(k) for k in
                       ("name", "file", "url", "provides", "enabled")},
                    "present_locally": have,
                    "fetchable": bool(s.get("url"))})
    return {"data_dir": str(root), "pdfs": len(pdfs),
            "archives": sorted(archives), "sources": out}


def extract_all(root: Path = None, log=print) -> int:
    """Unpack every archive in the data folder, once. `.7z` before `.zip`,
    because a 7z here usually contains the zip."""
    root = root or config.DATA_DIR
    root.mkdir(parents=True, exist_ok=True)
    marks = root / ".extracted"
    done = 0
    seven = shutil.which("7z") or shutil.which("7za")
    for a in sorted(p for p in root.rglob("*.7z")
                    if not any(x.startswith(".") for x in p.parts)):
        mark = marks / (a.name + ".done")
        if mark.exists():
            continue
        if not seven:
            log(f"  [warn] {a.name}: 7-Zip is not installed. "
                f"Install p7zip-full (Linux) or 7-Zip and add it to PATH (Windows).")
            continue
        log(f"  [7z] unpacking {a.name}")
        r = subprocess.run([seven, "x", "-y", f"-o{a.parent}", str(a)],
                           capture_output=True, text=True)
        if r.returncode == 0:
            marks.mkdir(exist_ok=True); mark.write_text("ok"); done += 1
        else:
            log(f"  [warn] 7z failed on {a.name}: {r.stderr.strip()[:120]}")
    for z in sorted(p for p in root.rglob("*.zip")
                    if not any(x.startswith(".") for x in p.parts)):
        mark = marks / (z.name + ".done")
        if mark.exists():
            continue
        try:
            with zipfile.ZipFile(z) as zf:
                names = [n for n in zf.namelist() if not n.startswith("__MACOSX")]
                tops = {n.split("/", 1)[0] for n in names if n.strip("/")}
                dest = z.parent if len(tops) == 1 else z.parent / z.stem
                free = shutil.disk_usage(z.parent).free
                need = sum(i.file_size for i in zf.infolist())
                if free < need * 1.1:
                    log(f"  [error] {z.name} needs {need/2**30:.1f} GB unpacked, "
                        f"only {free/2**30:.1f} GB free — skipped")
                    continue
                log(f"  [zip] unpacking {z.name} ({need/2**20:.0f} MB)")
                zf.extractall(dest)
            marks.mkdir(exist_ok=True); mark.write_text("ok"); done += 1
        except zipfile.BadZipFile:
            log(f"  [warn] {z.name} is not a valid zip — skipped")
    return done


def acquire(root: Path = None, log=print, allow_download=True) -> dict:
    """Make textbooks available: unpack what is here, fetch only what is not."""
    root = root or config.DATA_DIR
    extracted = extract_all(root, log)
    pdfs = len(list(root.rglob("*.pdf"))) if root.is_dir() else 0
    fetched = 0
    if pdfs == 0 and allow_download:
        try:
            import fetcher
        except ImportError:
            log("  [warn] the requests package is missing, so links cannot be "
                "fetched — run: pip install requests")
            return {"extracted": extracted, "fetched": 0, "pdfs": pdfs}
        for s in load():
            if not s.get("enabled") or not s.get("url"):
                continue
            log(f"  [fetch] {s['name']}")
            try:
                fetcher.fetch_url(s["url"], root, log=log)
                fetched += 1
                extract_all(root, log)
            except Exception as e:
                log(f"  [warn] could not fetch {s['name']}: {str(e)[:140]}")
            if list(root.rglob("*.pdf")):
                break
    return {"extracted": extracted, "fetched": fetched,
            "pdfs": len(list(root.rglob("*.pdf"))) if root.is_dir() else 0}
