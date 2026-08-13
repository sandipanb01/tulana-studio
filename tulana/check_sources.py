#!/usr/bin/env python3
"""Check that every configured textbook source is reachable.

Run this on the machine that will host the studio — it is the only place the
answer is meaningful, because reachability depends on that machine's network.

    python3 check_sources.py

For each source it reports whether the archive is already on disk (in which
case nothing needs downloading), and if not, whether the link actually returns
a file. Google Drive links are followed through the confirmation step that
Drive requires for large files, so a "reachable" verdict here means the studio
can genuinely fetch it.

Exit code is the number of sources that are neither present nor reachable.
"""
import sys

import config
import sources


def main():
    st = sources.status(config.DATA_DIR)
    print("TEXTBOOK SOURCES")
    print(f"  data folder : {st['data_dir']}")
    print(f"  PDFs present: {st['pdfs']}")
    if st["archives"]:
        print(f"  archives    : {', '.join(st['archives'])}")
    print()

    try:
        import fetcher
    except ImportError:
        print("  requests is not installed — run: pip install requests")
        return 1

    blocked = 0
    for s in st["sources"]:
        name = s["name"]
        if s["present_locally"]:
            print(f"  [have]      {name}")
            print(f"              already in the data folder — no download needed")
            continue
        if not s.get("url"):
            print(f"  [add]       {name}")
            print(f"              no link configured; copy {s.get('file') or 'the archive'} "
                  f"into the data folder")
            continue
        fid = fetcher.drive_file_id(s["url"])
        print(f"  [check]     {name}")
        print(f"              {s['url'][:78]}")
        if fid:
            print(f"              Google Drive file id: {fid}")
        try:
            info = fetcher.probe_remote(s["url"])
        except Exception as e:
            info = {}
            print(f"              probe failed: {str(e)[:90]}")
        if info.get("filename"):
            size = info.get("size")
            print(f"  [ok]        reachable — {info['filename']}"
                  + (f", {size / 2**20:.0f} MB" if size else ""))
        else:
            blocked += 1
            print("  [BLOCKED]   the link did not return a file.")
            print("              Most often this means the file is not shared as")
            print("              'Anyone with the link', or this machine has no")
            print("              route to Google. Open the link in a private browser")
            print("              window: if it asks you to sign in, change the")
            print("              sharing setting.")
        print()

    if blocked:
        print(f"  {blocked} source(s) could not be fetched. The studio still runs —")
        print("  copy those archives into the data folder instead.")
    else:
        print("  Every source is either present or reachable.")
    return blocked


if __name__ == "__main__":
    sys.exit(main())
