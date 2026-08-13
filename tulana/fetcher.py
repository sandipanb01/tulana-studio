"""Fetch ground-truth archives straight into the backend from a URL.

Ground-truth collections are large and live wherever they live — a Drive share,
an institutional file server, an S3 link. Asking someone to download 3 GB to a
laptop and re-upload it is wasteful when the server can pull it directly.

The awkward part is Google Drive: for anything above roughly 100 MB it does not
return the file, it returns an HTML interstitial ("Google Drive can't scan this
file for viruses") carrying a confirmation token that must be replayed on a
second request, on the same cookie session. That flow — and the several URL
shapes Drive has used over the years — is handled here so the caller only ever
has to paste the normal share link.
"""
from __future__ import annotations

import re
import shutil
import time
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

CHUNK = 4 * 1024 * 1024
BROWSER_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def drive_file_id(url: str) -> str | None:
    """Pull the file id out of any of Drive's link shapes."""
    for pat in (r"/file/d/([A-Za-z0-9_-]{20,})",
                r"[?&]id=([A-Za-z0-9_-]{20,})",
                r"/d/([A-Za-z0-9_-]{20,})"):
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


def _filename_from(resp, fallback: str) -> str:
    cd = resp.headers.get("content-disposition", "")
    m = re.search(r"filename\*=UTF-8''([^;]+)", cd) or re.search(r'filename="([^"]+)"', cd)
    if m:
        return Path(unquote(m.group(1))).name
    path = urlparse(resp.url).path
    if path and Path(path).suffix:
        return Path(path).name
    return fallback


def _looks_like_html(resp) -> bool:
    return "text/html" in (resp.headers.get("content-type") or "").lower()


def probe_remote(url: str, timeout: int = 25) -> dict:
    """Find out what a link *would* download, without downloading it.

    Costs one short request. Used to skip a multi-gigabyte transfer when the
    same archive is already sitting in the data folder — the difference
    between an annotator waiting an hour and starting immediately."""
    import requests
    out = {"filename": None, "size": None}
    fid = drive_file_id(url)
    target = (f"https://drive.usercontent.google.com/download?id={fid}"
              f"&export=download&confirm=t") if fid else url
    try:
        s = requests.Session()
        s.headers["User-Agent"] = BROWSER_UA
        r = s.get(target, stream=True, timeout=timeout, allow_redirects=True)
        if r.status_code == 200 and not _looks_like_html(r):
            out["filename"] = _filename_from(r, "")
            cl = r.headers.get("content-length")
            out["size"] = int(cl) if cl and cl.isdigit() else None
        r.close()
    except Exception:
        pass
    return out


def fetch_url(url: str, dest_dir: Path, log=print, progress=None,
              should_stop=None) -> Path:
    """Download `url` into `dest_dir`, returning the written path.

    Streams to a `.part` file and renames only on success, so an interrupted
    download is never mistaken for a complete one. Refuses to start if the
    reported size will not fit, leaving room to unpack as well as to store.
    """
    import requests

    dest_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = BROWSER_UA

    fid = drive_file_id(url)
    if fid:
        log(f"  [fetch] Google Drive file {fid}")
        candidates = [
            f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t",
            f"https://drive.google.com/uc?export=download&id={fid}&confirm=t",
            f"https://drive.google.com/uc?export=download&id={fid}",
        ]
    else:
        candidates = [url]

    resp = None
    last_err = None
    for attempt in candidates:
        try:
            r = session.get(attempt, stream=True, timeout=60, allow_redirects=True)
        except Exception as e:                       # network/DNS/TLS
            last_err = e
            continue
        if r.status_code != 200:
            last_err = RuntimeError(f"HTTP {r.status_code}")
            r.close()
            continue
        if _looks_like_html(r) and fid:
            # The virus-scan interstitial: replay the confirm token it carries.
            body = r.text[:200000]
            r.close()
            token = None
            m = re.search(r'name="confirm"\s+value="([^"]+)"', body) \
                or re.search(r"[?&]confirm=([0-9A-Za-z_-]+)", body)
            if m:
                token = m.group(1)
            form = re.search(r'action="(https://[^"]+)"', body)
            uuid = re.search(r'name="uuid"\s+value="([^"]+)"', body)
            if form:
                target = form.group(1).replace("&amp;", "&")
                params = {"id": fid, "export": "download",
                          "confirm": token or "t"}
                if uuid:
                    params["uuid"] = uuid.group(1)
                try:
                    r = session.get(target, params=params, stream=True,
                                    timeout=60, allow_redirects=True)
                except Exception as e:
                    last_err = e
                    continue
            elif token:
                try:
                    r = session.get(
                        f"https://drive.usercontent.google.com/download"
                        f"?id={fid}&export=download&confirm={token}",
                        stream=True, timeout=60, allow_redirects=True)
                except Exception as e:
                    last_err = e
                    continue
            if _looks_like_html(r):
                last_err = RuntimeError(
                    "Drive returned a web page instead of the file — the link may "
                    "require sign-in. Set sharing to 'Anyone with the link'.")
                r.close()
                continue
        resp = r
        break

    if resp is None:
        raise RuntimeError(f"could not download: {last_err}")

    total = int(resp.headers.get("content-length") or 0)
    name = _filename_from(resp, "download.zip")
    free = shutil.disk_usage(dest_dir).free
    if total and free < total * 2.2:
        resp.close()
        raise RuntimeError(
            f"not enough disk space: {name} is {total / 2**30:.1f} GB and needs "
            f"about {total * 2.2 / 2**30:.1f} GB including unpacking, but only "
            f"{free / 2**30:.1f} GB is free")

    part = dest_dir / (name + ".part")
    got, t0, last = 0, time.time(), 0.0
    log(f"  [fetch] downloading {name}"
        + (f" ({total / 2**20:.0f} MB)" if total else " (size unknown)"))
    with open(part, "wb") as fh:
        for block in resp.iter_content(CHUNK):
            if should_stop is not None and should_stop():
                fh.close()
                part.unlink(missing_ok=True)
                resp.close()
                raise RuntimeError("download cancelled")
            if not block:
                continue
            fh.write(block)
            got += len(block)
            now = time.time()
            if now - last > 3:
                pct = f"{got * 100 // total}%" if total else f"{got / 2**20:.0f} MB"
                rate = got / max(1e-6, now - t0) / 2**20
                msg = f"downloading {name}: {pct} at {rate:.1f} MB/s"
                log("  [fetch] " + msg)
                if progress:
                    progress(msg)
                last = now
    resp.close()
    if total and got < total:
        part.unlink(missing_ok=True)
        raise RuntimeError(f"download ended early ({got} of {total} bytes)")
    final = dest_dir / name
    if final.exists():
        final.unlink()
    part.rename(final)
    log(f"  [fetch] saved {name} ({got / 2**20:.0f} MB in {time.time() - t0:.0f}s)")
    return final
