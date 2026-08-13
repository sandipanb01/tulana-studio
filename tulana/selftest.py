#!/usr/bin/env python3
"""Tulana Studio — end-to-end self-test.

Starts the application against the real textbook PDFs and exercises the whole
annotator journey: index the library, open two editions, render pages, clip a
parallel pair, verify the clipping really is the region that was asked for,
check the excluded-topic path, and export the ZIP the project expects.

    python3 selftest.py

Exit code is the number of failures.
"""
import io
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
PORT = int(os.environ.get("SELFTEST_PORT", "7899"))
B = f"http://localhost:{PORT}"
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"PASS  {name}" + (f"  ({detail})" if detail else ""))
    else:
        failed += 1
        print(f"FAIL  {name}  {detail}")


def get(path, raw=False, timeout=240):
    r = urllib.request.urlopen(B + path, timeout=timeout)
    data = r.read()
    return data if raw else json.loads(data)


def post(path, body, timeout=240):
    req = urllib.request.Request(
        B + path, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "X-Annotator": "selftest"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def code_of(path, method="GET"):
    try:
        req = urllib.request.Request(B + path, method=method)
        return urllib.request.urlopen(req, timeout=60).status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def main():
    srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "app:app",
                            "--port", str(PORT)], cwd=HERE,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(120):
            try:
                get("/api/health", timeout=3)
                break
            except Exception:
                time.sleep(0.5)
        run()
    finally:
        srv.terminate()
    print(f"\n===== {passed} passed, {failed} failed =====")
    return failed


def run():
    import config
    from pdflib import fitz

    # ---------------------------------------------------------- library ----
    h = get("/api/health")
    check("server is ready", h.get("ok") and h.get("pdf_ready"),
          f"{h.get('documents')} documents, PyMuPDF {h.get('pymupdf')}")
    check("textbooks are indexed", h["documents"] > 50, f"{h['documents']}")

    lib = get("/api/library")
    check("board/class combinations offered", len(lib) >= 5, f"{len(lib)}")
    check("every combination has both sides",
          all(c["english_editions"] and c["target_editions"] for c in lib))
    check("combinations are named in words",
          all("Class" in c["label"] and "_" not in c["label"] for c in lib),
          lib[0]["label"] if lib else "")
    langs = sorted({l for c in lib for l in c["target_languages"]})
    check("multiple target languages available", len(langs) >= 5, ", ".join(langs))

    ncert = [c for c in lib if c["board"] == "NCERT" and c["class"] == 10]
    check("NCERT class 10 is pairable", bool(ncert))
    combo = ncert[0] if ncert else lib[0]
    src = combo["english_editions"][0]
    tgt = combo["target_editions"][0]

    # ---------------------------------------------------------- rendering --
    doc = get(f"/api/doc/{src['id']}")
    check("document metadata includes page sizes",
          doc["pages"] > 0 and doc.get("page_sizes"), f"{doc['pages']} pages")
    t0 = time.time()
    png = get(f"/api/doc/{src['id']}/page/2.png", raw=True)
    cold = (time.time() - t0) * 1000
    t0 = time.time()
    get(f"/api/doc/{src['id']}/page/2.png", raw=True)
    warm = (time.time() - t0) * 1000
    check("a page renders", png[:4] == b"\x89PNG", f"{len(png)//1024} KB")
    check("rendered pages are cached", warm < cold / 2 + 30,
          f"{cold:.0f} ms cold, {warm:.0f} ms warm")
    check("page out of range is refused",
          code_of(f"/api/doc/{src['id']}/page/99999.png") == 404)
    check("unknown document is refused", code_of("/api/doc/999999") == 404)

    txt = get(f"/api/doc/{src['id']}/page/2/text")
    check("page text and topic verdict returned",
          "excluded_topic" in txt and "chars" in txt,
          f"{txt['chars']} chars, excluded={txt['excluded_topic']}")
    outline = get(f"/api/doc/{src['id']}/outline")
    check("outline endpoint responds", "outline" in outline,
          f"{len(outline['outline'])} bookmarks")

    # ----------------------------------------------------------- project ---
    proj = post("/api/projects", {"board": combo["board"], "cls": combo["class"],
                                  "subject": combo["subject"],
                                  "src_doc": src["id"], "tgt_doc": tgt["id"]})
    check("project created", proj.get("id"), proj.get("name"))
    again = post("/api/projects", {"board": combo["board"], "cls": combo["class"],
                                   "subject": combo["subject"],
                                   "src_doc": src["id"], "tgt_doc": tgt["id"]})
    check("re-opening the same pairing reuses the project",
          again["id"] == proj["id"])

    # -------------------------------------------------------------- clip ---
    region = {"page": 2, "x0": 60, "y0": 120, "x1": 520, "y1": 300}
    pair = post("/api/pairs", {"project_id": proj["id"], "src": region,
                               "tgt": dict(region), "label": "Self-test pair"})
    check("a parallel pair saves", pair.get("pair_id"), f"seq {pair.get('seq')}")
    check("both sides produced an image",
          pair["sides"]["src"]["image"] and pair["sides"]["tgt"]["image"])

    pairs = get(f"/api/projects/{proj['id']}/pairs")
    mine = [p for p in pairs if p["id"] == pair["pair_id"]][0]
    check("the pair records page and rectangle",
          mine["clips"]["src"]["page"] == 2 and mine["clips"]["src"]["x1"] == 520)
    clip_png = get(f"/api/clip/{mine['clips']['src']['id']}.png", raw=True)
    check("the clipping image is served", clip_png[:4] == b"\x89PNG",
          f"{len(clip_png)//1024} KB")

    # the clipping must actually be that region of that page, not a whole page
    from PIL import Image
    rel = get(f"/api/doc/{src['id']}")["path"]
    full = config.DATA_DIR / Path(*rel.split("/"))
    with fitz.open(full) as d:
        page_rect = fitz.Rect(d[1].rect)
    # the request is intersected with the page, so the expectation must be too
    want = fitz.Rect(region["x0"], region["y0"], region["x1"], region["y1"]) & page_rect
    expect_ratio = want.width / want.height
    got = Image.open(io.BytesIO(clip_png))
    check("the clipping matches the requested rectangle",
          abs(got.width / got.height - expect_ratio) < 0.05,
          f"{got.width}x{got.height}, ratio {got.width/got.height:.2f} vs {expect_ratio:.2f}")
    check("the clipping is cut at print resolution, not screen resolution",
          got.width > want.width * 2, f"{got.width}px for {want.width:.0f}pt")
    check("the clipping is a region, not the whole page",
          got.height < page_rect.height * 300 / 72 * 0.95,
          f"{got.height}px vs full page {page_rect.height*300/72:.0f}px")

    # ---------------------------------------------------------- rejection --
    check("a too-small selection is refused",
          code_of_post("/api/pairs", {"project_id": proj["id"],
                                      "src": {"page": 2, "x0": 10, "y0": 10,
                                              "x1": 11, "y1": 11},
                                      "tgt": dict(region)}) == 400)
    check("a page beyond the book is refused",
          code_of_post("/api/pairs", {"project_id": proj["id"],
                                      "src": {"page": 99999, "x0": 10, "y0": 10,
                                              "x1": 200, "y1": 200},
                                      "tgt": dict(region)}) == 400)
    check("an unknown project is refused",
          code_of_post("/api/pairs", {"project_id": 999999, "src": region,
                                      "tgt": dict(region)}) == 404)

    # ------------------------------------------------------------ export ---
    z = get(f"/api/projects/{proj['id']}/export.zip", raw=True)
    zf = zipfile.ZipFile(io.BytesIO(z))
    names = zf.namelist()
    folder = config.project_folder(proj["board"], proj["class"], proj["subject"])
    want_src = config.clip_name(proj["src_language"], proj["board"], proj["subject"], 1)
    want_tgt = config.clip_name(proj["tgt_language"], proj["board"], proj["subject"], 1)
    check("export folder is named for the textbook",
          all(n.startswith(folder + "/") for n in names), folder)
    check("clippings are named language_board_subject_number",
          f"{folder}/{want_src}" in names and f"{folder}/{want_tgt}" in names,
          f"{want_src} / {want_tgt}")
    for ext in ("jpg", "pdf"):
        alt = want_src.rsplit(".", 1)[0] + "." + ext
        check(f"each clipping is also exported as {ext.upper()}",
              f"{folder}/{alt}" in names, alt)
    for extra in ("manifest.json", "pairs.jsonl", "pairs.csv", "parallel.tsv", "README.md"):
        check(f"export contains {extra}", any(n.endswith(extra) for n in names))
    man = json.loads(zf.read([n for n in names if n.endswith("manifest.json")][0]))
    check("manifest records pages and coordinates",
          man["pairs"] and man["pairs"][0]["src_page"] == 2 and
          man["pairs"][0]["src_bbox"][2] == 520)
    check("manifest names the two languages",
          man["project"]["src_language"] and man["project"]["tgt_language"],
          f"{man['project']['src_language']} ↔ {man['project']['tgt_language']}")
    imgs = [n for n in names if n.endswith(".png")]
    check("every manifest pair has both images on disk",
          len(imgs) == 2 * len(man["pairs"]), f"{len(imgs)} images")
    check("a JPG clipping is a real JPEG",
          zf.read([n for n in names if n.endswith(".jpg")][0])[:3] == b"\xff\xd8\xff")
    check("a PDF clipping is a real PDF",
          zf.read([n for n in names if n.endswith(".pdf")][0])[:5] == b"%PDF-")

    # --------------------------------------------------------- lifecycle ---
    patched = patch(f"/api/pairs/{pair['pair_id']}", {"excluded": True,
                                                      "reason": "self-test"})
    check("a pair can be marked excluded", patched["excluded"] == 1)
    z2 = get(f"/api/projects/{proj['id']}/export.zip", raw=True)
    n2 = [n for n in zipfile.ZipFile(io.BytesIO(z2)).namelist() if n.endswith(".png")]
    check("excluded pairs are left out of exports by default", len(n2) < len(imgs),
          f"{len(imgs)} -> {len(n2)}")
    z3 = get(f"/api/projects/{proj['id']}/export.zip?include_excluded=true", raw=True)
    n3 = [n for n in zipfile.ZipFile(io.BytesIO(z3)).namelist() if n.endswith(".png")]
    check("excluded pairs can be included on request", len(n3) == len(imgs))

    delete(f"/api/pairs/{pair['pair_id']}")
    left = get(f"/api/projects/{proj['id']}/pairs")
    check("a pair can be deleted",
          all(p["id"] != pair["pair_id"] for p in left))

    # ------------------------------------------------------------ labels ---
    labels = get(f"/api/projects/{proj['id']}/labels")
    check("a default label set is created with the project", len(labels) >= 6,
          ", ".join(l["name"] for l in labels[:4]))
    check("labels carry a colour and a one-key shortcut",
          all(l["color"].startswith("#") for l in labels) and
          any(l["shortcut"] for l in labels))
    made = post(f"/api/projects/{proj['id']}/labels",
                {"name": "Proof", "color": "#884499", "shortcut": "9"})
    check("a label can be added", made["name"] == "Proof")
    check("duplicate labels are refused",
          code_of_post(f"/api/projects/{proj['id']}/labels",
                       {"name": "Proof"}) == 409)
    pair2 = post("/api/pairs", {"project_id": proj["id"], "src": region,
                                "tgt": dict(region), "label": "labelled"})
    applied = put(f"/api/pairs/{pair2['pair_id']}/labels",
                  {"label_ids": [labels[0]["id"], made["id"]]})
    check("labels can be applied to a chunk", len(applied) == 2,
          ", ".join(a["name"] for a in applied))
    back = get(f"/api/projects/{proj['id']}/pairs")
    tagged = [p for p in back if p["id"] == pair2["pair_id"]][0]
    check("labels come back with the chunk", len(tagged["labels"]) == 2)

    prog = get(f"/api/projects/{proj['id']}/progress")
    check("progress reports chunks, coverage and label counts",
          prog["pairs"] >= 1 and "by_label" in prog and "by_annotator" in prog,
          f"{prog['pairs']} chunks, {prog['coverage_pct']}% of pages touched")
    zl = get(f"/api/projects/{proj['id']}/export.zip?include_excluded=true", raw=True)
    zlf = zipfile.ZipFile(io.BytesIO(zl))
    mani = json.loads(zlf.read([n for n in zlf.namelist()
                                if n.endswith("manifest.json")][0]))
    check("labels are carried into the export",
          any(m.get("labels") for m in mani["pairs"]),
          str([m.get("labels") for m in mani["pairs"] if m.get("labels")][:1]))
    delete(f"/api/labels/{made['id']}")
    check("a label can be removed",
          all(l["name"] != "Proof" for l in get(f"/api/projects/{proj['id']}/labels")))

    # ----------------------------------------------------------- sources ---
    st = get("/api/sources")
    check("source archives and links are declared", len(st["sources"]) >= 3,
          f"{len(st['sources'])} sources, {st['pdfs']} PDFs")
    drive = [s for s in st["sources"] if "drive.google" in (s.get("url") or "")]
    check("both Drive links are configured", len(drive) >= 2,
          f"{len(drive)} links")
    import fetcher as _f
    check("every configured Drive link resolves to a file id",
          all(_f.drive_file_id(s["url"]) for s in drive),
          ", ".join((_f.drive_file_id(s["url"]) or "?")[:12] for s in drive))
    check("unpacking is available without downloading",
          code_of("/api/sources/acquire?download=false", "POST") == 200)

    # -------------------------------------------------------------- docs ---
    docs = get("/api/docs")
    check("documentation is served in-app", len(docs) >= 4, f"{len(docs)} documents")
    body = urllib.request.urlopen(B + "/api/docs/" + docs[0]["name"]).read().decode()
    check("a manual has real content", len(body) > 1500, f"{len(body)} chars")
    check("a bad document name is refused", code_of("/api/docs/..%2Fapp") in (400, 404))

    # --------------------------------------------------------- interface ---
    html = urllib.request.urlopen(B + "/").read().decode()
    check("the interface loads", "Tulana Studio" in html)
    for asset in ("style.css", "app.js"):
        check(f"{asset} is served", code_of("/static/" + asset) == 200)
    check("the interface is mobile-ready",
          "viewport" in html and "max-width:900px" in
          urllib.request.urlopen(B + "/static/style.css").read().decode())


def code_of_post(path, body):
    try:
        req = urllib.request.Request(
            B + path, data=json.dumps(body).encode(), method="POST",
            headers={"Content-Type": "application/json"})
        return urllib.request.urlopen(req, timeout=120).status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def put(path, body):
    req = urllib.request.Request(
        B + path, data=json.dumps(body).encode(), method="PUT",
        headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def patch(path, body):
    req = urllib.request.Request(
        B + path, data=json.dumps(body).encode(), method="PATCH",
        headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def delete(path):
    req = urllib.request.Request(B + path, method="DELETE")
    return urllib.request.urlopen(req, timeout=120).read()


if __name__ == "__main__":
    sys.exit(main())
