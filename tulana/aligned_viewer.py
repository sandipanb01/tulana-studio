"""
Viewer for the aligned textbook data (data/aligned_v2): pick a book pair and an English page; see the
English page and its counterpart page(s) as boxes (same colour = same translation unit), the paired texts
below, and report problems (saved to <aligned>/viewer_reports.jsonl, which git ignores).

    python3 tulana/aligned_viewer.py                        from the repository root
    python3 aligned_viewer.py                               from tulana/
    python3 tulana/aligned_viewer.py --aligned PATH --port 7864 [--share]

The data is found by itself: --aligned, else TULANA_ALIGNED_DIR, else data/aligned_v2 in the repository.
Page images are not in the delivery, so boxes are drawn on blank pages of the right size; Setu
(launch_annotation.py) shows the same pairs over the printed page.

Written by the aligner team (document-mt-alignment-bodhan-iitr). Adapted for tulana-studio: it runs from
any folder, reads every file as UTF-8, works with Gradio 5 and 6, and treats the data and every typed
value as untrusted: nothing from a file reaches the page unescaped, a page or pair that is not in the
data is refused, and a report is size-capped and written only to that one file.
"""
import argparse, colorsys, datetime, html, inspect, json, math, os, re, threading, unicodedata
from pathlib import Path

import gradio as gr

HERE = Path(__file__).resolve().parent
REPO = HERE.parent if HERE.name == "tulana" else HERE
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}")     # a pair id: one folder name, never a path
REPORTS = "viewer_reports.jsonl"

KATEX_HEAD = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
"""
RENDER_MATH_JS = """() => { setTimeout(() => { try { document.querySelectorAll('.units').forEach(el =>
  renderMathInElement(el, {delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
  throwOnError:false})); } catch(e) {} }, 50); }"""
CSS = """
.pages{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
.pg{flex:1 1 320px;min-width:280px;max-width:560px}
.pg h4{margin:4px 0;font-size:15px}
.pg svg{width:100%;height:auto;border:1px solid #c8d1e0;background:#fff}
table.units{width:100%;border-collapse:collapse;table-layout:fixed;font-size:16px}
table.units td,table.units th{border:1px solid #c8d1e0;padding:7px;vertical-align:top;text-align:left}
table.units th{background:#eef3fb}
table.units td{white-space:pre-wrap;overflow-wrap:anywhere}
.sw{display:inline-block;width:13px;height:13px;border-radius:2px;margin-right:5px;vertical-align:middle}
.note{color:#5b6472;font-size:13px}
.st{display:inline-block;padding:1px 8px;border-radius:9px;font-size:13px;background:#e8eef9;color:#1d4ed8}
.bad{background:#fde2e1;color:#b42318}
tr.na td{background:#fff3f2}
.msg{font-size:16px;padding:10px 0}
"""
THEME = gr.themes.Default(primary_hue="blue", secondary_hue="blue", neutral_hue="slate")
NOT_ALIGNED = ("unpaired", "page_failed")     # text the app should treat as having no counterpart

_lock = threading.Lock()


def block_state(b, page):
    """align_state from the export (--align-meta); derived the same way for exports without it."""
    if "align_state" in b:
        return b["align_state"]
    st = page.get("align_status", "not_processed")
    if not (b.get("text") or "").strip():
        return "no_text"
    if b.get("align_id"):
        return "aligned"
    return {"alignment_failed": "page_failed", "unparseable": "page_failed"}.get(st, st if st == "not_processed" else "unpaired")


def page_counts(page):
    c = {}
    for b in page["blocks"]:
        s = block_state(b, page)
        if s != "no_text":
            c[s] = c.get(s, 0) + len(b.get("members") or [b])
    return c


def counts_txt(c):
    n = sum(c.values())
    bad = sum(c.get(s, 0) for s in NOT_ALIGNED)
    return (f"{c.get('aligned', 0)}/{n} aligned" + (f', <b style="color:#b42318">{bad} not aligned</b>' if bad else "")
            + (f", {c['not_processed']} not processed" if c.get("not_processed") else ""))


def color(k):
    # Every hue but red: red is kept for text that has no counterpart.
    r, g, b = colorsys.hsv_to_rgb(0.07 + ((k * 0.17) % 1) * 0.83, 0.75, 0.85)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def esc(t):
    return html.escape(str(t) if t is not None else "", quote=True)


def num(v, default=0.0):
    """A finite number from the data, or *default*: never text inside an SVG attribute."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return default
    return f if math.isfinite(f) else default


def rect(bb):
    if not isinstance(bb, (list, tuple)) or len(bb) != 4:
        bb = (0, 0, 0, 0)
    x0, y0, x1, y1 = (num(v) for v in bb)
    return f'x="{x0:.1f}" y="{y0:.1f}" width="{max(0.0, x1 - x0):.1f}" height="{max(0.0, y1 - y0):.1f}"', x0, y0


def clean(s, limit, one_line=False):
    """Typed text for the report file: no control characters, a fixed maximum length."""
    s = str(s or "")
    if one_line:
        s = " ".join(s.split())
    s = "".join(ch for ch in s if ch in "\n\t" or unicodedata.category(ch)[0] != "C")
    return s.strip()[:limit]


def inside(path, folder):
    """True when *path* is *folder* or lies under it (both already resolved)."""
    return path == folder or folder in path.parents


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def default_aligned():
    env = os.environ.get("TULANA_ALIGNED_DIR", "").strip()
    places = ([Path(env)] if env else []) + [REPO / "data" / "aligned_v2", Path.cwd() / "data" / "aligned_v2",
                                            REPO / "aligned-docMT-test"]
    for p in places:
        if (p / "export_summary.json").is_file():
            return str(p)
    return str(REPO / "data" / "aligned_v2")


def pair_files_from(root, summary):
    """pair id -> its JSON files, every one inside the pair's own folder.

    export_summary stores paths as written on the aligner team's machine; they are re-rooted under the
    data folder, and a path that would leave the pair's folder is dropped."""
    out = {}
    for r in summary if isinstance(summary, list) else []:
        if not isinstance(r, dict):
            continue
        pid = str(r.get("pair") or "")
        if not SAFE_ID.fullmatch(pid):
            continue
        folder = (root / pid).resolve()
        if not folder.is_dir() or not inside(folder, root):
            continue
        files = []
        for f in r.get("files") or []:
            tail = str(f).replace("\\", "/").split("/" + pid + "/", 1)
            if len(tail) != 2:
                continue
            p = (folder / tail[1]).resolve()
            if inside(p, folder) and p.suffix == ".json" and p.is_file():
                files.append(p)
        if not files:       # the summary's paths did not resolve: the pair folder's own files
            files = sorted(p for p in folder.rglob("*.json")
                           if p.is_file() and inside(p.resolve(), folder))
        if files:
            out[pid] = files
    return out


def main():
    ap = argparse.ArgumentParser(description="Viewer for the aligned textbook data.")
    ap.add_argument("--aligned", default=None,
                    help="the aligned data folder (default: TULANA_ALIGNED_DIR, else data/aligned_v2)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=7864)
    ap.add_argument("--share", action="store_true")
    a = ap.parse_args()

    root = Path(a.aligned or default_aligned()).resolve()
    try:
        summary = read_json(root / "export_summary.json")
    except (OSError, ValueError) as exc:
        raise SystemExit(f"No aligned data at {root} ({type(exc).__name__}). "
                         "Expected data/aligned_v2 with its export_summary.json; or pass --aligned PATH.")
    pair_files = pair_files_from(root, summary)
    if not pair_files:
        raise SystemExit(f"{root} holds no readable book pairs.")
    pairs = sorted(pair_files, key=lambda p: (p.startswith("NCERT"), p))
    cache = {}

    def _load(pid):
        books = [read_json(f) for f in pair_files[pid]]
        if len(books) == 1:      # bilingual (AP): English on odd pages from 13, Telugu on the next page
            en = tg = books[0]
            en_pages = [p["page"] for p in en["pages"] if p["align_status"] != "not_processed" and p["page"] % 2 == 1]
        else:
            en = next(b for b in books if b["alignment"]["lang"] == "en")
            tg = next(b for b in books if b["alignment"]["lang"] != "en")
            en_pages = [p["page"] for p in en["pages"] if p["align_status"] != "not_processed"]
        where = {}          # align_id -> target pages
        for p in tg["pages"]:
            for b in p["blocks"]:
                if b.get("align_id") and (len(books) > 1 or p["page"] not in en_pages):
                    where.setdefault(b["align_id"], set()).add(p["page"])
        en_parts = {}       # align_id -> [(page, block)] on the English side (a unit can span pages)
        for p in en["pages"]:
            if len(books) > 1 or p["page"] in en_pages:
                for b in p["blocks"]:
                    if b.get("align_id"):
                        en_parts.setdefault(b["align_id"], []).append((p["page"], b))
        d = {"en": en, "tg": tg, "en_pages": en_pages, "where": where, "bilingual": len(books) == 1,
             "en_parts": en_parts}
        # English pages whose own text, or the text of the target pages shown with them, is not all aligned
        d["bad_pages"] = [pg for pg in en_pages if any(
            page_counts(p).get(s) for p in [en["pages"][pg]] + [tg["pages"][t] for t in target_pages(d, pg)]
            for s in NOT_ALIGNED)]
        return d

    def load(pid):
        if pid in cache:
            return cache[pid]
        try:
            d = _load(pid)
        except Exception as exc:        # a broken pair is shown as broken; the others still work
            d = {"broken": type(exc).__name__, "en_pages": [], "bad_pages": []}
        cache[pid] = d
        return d

    def target_pages(d, en_page):
        ep = d["en"]["pages"][en_page]
        tpages = sorted({p for b in ep["blocks"] if b.get("align_id") for p in d["where"].get(b["align_id"], ())})
        if not tpages and ep["align_status"] in ("alignment_failed", "unparseable"):
            tpages = [en_page + 1] if d["bilingual"] else ([en_page] if en_page < len(d["tg"]["pages"]) and
                                                            d["en"]["num_pages"] == d["tg"]["num_pages"] else [])
        return [t for t in tpages if 0 <= t < len(d["tg"]["pages"])]

    def pair_label(pid):
        tot = {}
        try:
            for f in pair_files[pid]:
                s = read_json(f)["alignment"].get("summary")
                if not s:
                    return pid
                for k in ("text_blocks", "aligned", "not_processed"):
                    tot[k] = tot.get(k, 0) + int(s[k])
        except Exception:
            return pid
        n = tot["text_blocks"] - tot["not_processed"]
        return f"{pid} · {100 * tot['aligned'] / n:.1f}% aligned" if n > 0 else pid

    def as_page(pid, pg):
        """A typed or chosen page number that really is one of this pair's English pages, else None."""
        if pid not in pair_files:
            return None
        try:
            n = int(str(pg).strip())
        except (TypeError, ValueError):
            return None
        return n if n in load(pid)["en_pages"] else None

    def svg(page, ids, title):
        W, H = num(page.get("width"), 1000.0), num(page.get("height"), 1400.0)
        W, H = (W if W > 0 else 1000.0), (H if H > 0 else 1400.0)
        parts = [f'<svg viewBox="0 0 {W:.1f} {H:.1f}" xmlns="http://www.w3.org/2000/svg">']
        for b in page["blocks"]:
            where_, x0, y0 = rect(b.get("bbox_xyxy"))
            aid = b.get("align_id")
            tip = esc((b.get("text") or "")[:300])
            if aid and aid in ids:
                c = color(ids[aid])
                for m in b.get("members") or []:
                    if isinstance(m, dict):
                        parts.append(f'<rect {rect(m.get("bbox_xyxy"))[0]} fill="none" stroke="#bbb" '
                                     f'stroke-dasharray="6,4" stroke-width="2"/>')
                parts.append(f'<rect {where_} fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-width="6">'
                             f'<title>{tip}</title></rect>')
                part = " " + esc(b["part"]) if b.get("part") else ""
                parts.append(f'<text x="{x0 + 8:.1f}" y="{y0 + 38:.1f}" font-size="36" fill="{c}" '
                             f'font-family="sans-serif">u{ids[aid]}{part}</text>')
            elif block_state(b, page) in NOT_ALIGNED:
                parts.append(f'<rect {where_} fill="#e74c3c" fill-opacity="0.08" stroke="#e74c3c" stroke-width="4" '
                             f'stroke-dasharray="14,8"><title>NOT ALIGNED ({esc(block_state(b, page))}): {tip}'
                             f'</title></rect>')
            else:
                dash = ' stroke-dasharray="4,6"' if not b.get("text") else ""
                parts.append(f'<rect {where_} fill="none" stroke="#999" stroke-width="3"{dash}>'
                             f'<title>{tip or esc(b.get("label"))}</title></rect>')
        parts.append("</svg>")
        return f'<div class="pg"><h4>{esc(title)}</h4>{"".join(parts)}</div>'

    def render(pid, en_page):
        if not pid:
            return "", ""
        if pid not in pair_files:
            return '<p class="msg">Choose a book pair from the list.</p>', ""
        d = load(pid)
        if d.get("broken"):
            return f'<p class="msg">This pair could not be read ({esc(d["broken"])}). The others are fine.</p>', ""
        if en_page in (None, ""):
            return "", ""
        n = as_page(pid, en_page)
        if n is None:
            return '<p class="msg">That is not one of this pair\'s English pages. Choose a page from the list.</p>', ""
        en_page = n
        ep = d["en"]["pages"][en_page]
        ids = {}
        for b in sorted(ep["blocks"], key=lambda b: num(b.get("order"))):
            if b.get("align_id") and b["align_id"] not in ids:
                ids[b["align_id"]] = len(ids) + 1
        tpages = target_pages(d, en_page)
        lang = str(d["tg"]["alignment"].get("language", "target")).replace("English + ", "")
        st = ep["align_status"]
        tcounts = " · ".join(f'{esc(lang)} p{tp}: {counts_txt(page_counts(d["tg"]["pages"][tp]))}' for tp in tpages)
        head = (f'<p><span class="st {"bad" if st in ("alignment_failed", "unparseable") else ""}">{esc(st)}</span> '
                f'English page {en_page} ↔ {esc(lang)} page(s) {", ".join(map(str, tpages)) or "—"} · {len(ids)} units<br>'
                f'OCR text blocks — English p{en_page}: {counts_txt(page_counts(ep))}{" · " + tcounts if tcounts else ""}<br>'
                f'<span class="note">same colour = same translation unit; dashed grey = original OCR blocks merged; '
                f'<span style="color:#b42318">dashed red = not aligned</span>; grey = no text or not processed; '
                f'hover a box for its text</span></p>')
        pages_html = svg(ep, ids, f"English · {d['en'].get('book', '')} p{en_page}")
        for tp in tpages:
            pages_html += svg(d["tg"]["pages"][tp], ids, f"{lang} · {d['tg'].get('book', '')} p{tp}")
        # units table
        tblocks = {}
        for tp in tpages:
            for b in d["tg"]["pages"][tp]["blocks"]:
                if b.get("align_id") in ids:
                    tblocks.setdefault(b["align_id"], []).append((tp, b))
        rows = []
        for b in sorted(ep["blocks"], key=lambda b: num(b.get("order"))):
            aid = b.get("align_id")
            if aid in ids:
                k = ids[aid]
                # a unit spanning pages: show every part on BOTH sides, marked with its page
                en_ps = d["en_parts"].get(aid, [(en_page, b)])
                joined = lambda ps: "\n\n".join((f"[p{pg}] " if len(ps) > 1 else "") + str(x.get("text") or "")
                                                for pg, x in ps)
                en_txt, tg_txt = joined(en_ps), joined(tblocks.get(aid, []))
                fl = [f for x in [x for _, x in en_ps] + [x for _, x in tblocks.get(aid, [])]
                      for f in (x.get("flags") or []) if isinstance(f, str)]
                meta = f'{b.get("align_relation", "")}, {b.get("align_confidence", "")}'
                flags = "".join(f'<div class="note">⚑ {esc(f[:300])}</div>' for f in dict.fromkeys(fl))
                rows.append(f'<tr><td><span class="sw" style="background:{color(k)}"></span><b>u{k}</b>'
                            f'<div class="note">{esc(meta)}</div></td><td>{esc(en_txt)}</td><td>{esc(tg_txt)}{flags}</td></tr>')
            elif b.get("text"):
                rows.append(not_aligned_row(b, ep, "", b["text"], ""))
        for tp in tpages:
            tpg = d["tg"]["pages"][tp]
            for x in tpg["blocks"]:
                if x.get("text") and not x.get("align_id"):
                    rows.append(not_aligned_row(x, tpg, f"p{tp}: ", "", x["text"]))
        table = (f'<table class="units"><tr><th style="width:110px">Unit</th><th>English</th><th>{esc(lang)}</th></tr>'
                 + "".join(rows) + "</table>")
        return head + f'<div class="pages">{pages_html}</div>', f'<div class="units">{table}</div>'

    def not_aligned_row(b, page, where, en_txt, tg_txt):
        s = block_state(b, page)
        why = str(s) + (f' ({b["align_note"]})' if b.get("align_note") else "")
        cls, c = ("na", "#e74c3c") if s in NOT_ALIGNED else ("", "#999")
        return (f'<tr class="{cls}"><td><span class="sw" style="background:{c}"></span>not aligned<div class="note">'
                f'{esc(where + why)}</div></td><td>{esc(en_txt)}</td><td>{esc(tg_txt)}</td></tr>')

    def page_list(pid, only_bad):
        if pid not in pair_files:
            return []
        d = load(pid)
        return d["bad_pages"] if only_bad else d["en_pages"]

    def pages_for(pid, sel=None, only_bad=False):
        """Page list for a pair; if a search match in this pair is selected, open its page."""
        ps = page_list(pid, only_bad)
        want = None
        if sel and "|" in str(sel):
            sp, _, sg = str(sel).partition("|")
            if sp.strip() == pid and as_page(pid, sg) is not None and (not only_bad or int(sg) in ps):
                want = str(int(sg))
        first = str(ps[0]) if ps else None
        return gr.update(choices=[str(p) for p in ps], value=want or first)

    def find(query):
        """Search English and target text across all pairs; returns matches as 'pair | page'."""
        q = (query or "").strip()[:200]
        if len(q) < 3:
            return gr.update(choices=[], value=None), "Type at least 3 characters."
        norm = lambda s: re.sub(r"\\[A-Za-z]+|[\s{}$]", "", str(s or "")).lower()   # ignore LaTeX commands, braces, $, spaces
        qn = norm(q)
        if not qn:
            return gr.update(choices=[], value=None), "Type some letters or numbers."
        hits = []
        for pid in pairs:
            d = load(pid)
            if d.get("broken"):
                continue
            for side in ("en", "tg"):
                for p in d[side]["pages"]:
                    for b in p["blocks"]:
                        if qn in norm(b.get("text")):
                            if side == "en":
                                pg = p["page"]
                            else:
                                pg = next((int(m.group(1)) for m in [re.search(r"/p(\d+)/", str(b.get("align_id") or ""))] if m), None)
                            if pg is not None and pg in d["en_pages"]:
                                hits.append(f"{pid} | {pg}")
            if len(hits) > 200:
                break
        hits = list(dict.fromkeys(hits))
        return gr.update(choices=hits, value=hits[0] if hits else None), f"{len(hits)} match(es)"

    def jump(sel, cur_pair):
        """Same pair: just move the page. Other pair: switch pair; pages_for then opens the matched page."""
        if not sel or "|" not in str(sel):
            return gr.update(), gr.update()
        pid, _, pg = (s.strip() for s in str(sel).partition("|"))
        if pid not in pair_files or as_page(pid, pg) is None:
            return gr.update(), gr.update()
        if pid != cur_pair:
            return gr.update(value=pid), gr.update()
        return gr.update(), gr.update(value=str(int(pg)))

    def step(pid, pg, k, only_bad=False):
        ps = page_list(pid, only_bad)
        if not ps:
            return gr.update()
        try:
            pg = int(str(pg).strip())
        except (TypeError, ValueError):
            return str(ps[0])
        if k > 0:
            nxt = [p for p in ps if p > pg]
            return str(nxt[0] if nxt else ps[-1])
        prv = [p for p in ps if p < pg]
        return str(prv[-1] if prv else ps[0])

    def report(name, pid, pg, units, issue):
        name, units, issue = clean(name, 80, True), clean(units, 200, True), clean(issue, 4000)
        if not name or not issue:
            raise gr.Error("Please enter your name and describe the problem.")
        n = as_page(pid, pg)
        if n is None:
            raise gr.Error("Choose a book pair and one of its pages first.")
        rec = {"at": datetime.datetime.now().isoformat(timespec="seconds"), "annotator": name, "pair": pid,
               "en_page": n, "units": units, "issue": issue}
        try:
            with _lock, open(root / REPORTS, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except OSError as exc:
            raise gr.Error(f"The report could not be saved ({type(exc).__name__}). Please try again.")
        gr.Info("Report saved. Thank you!")
        return "", ""

    blocks_kw = {"title": "Aligned textbook viewer"}
    launch_kw = {"server_name": a.host, "server_port": a.port, "share": a.share}
    # Gradio 5 takes the look in Blocks(); Gradio 6 moved it to launch() and replaced show_api.
    takes = inspect.signature(gr.Blocks.__init__).parameters
    launches = inspect.signature(gr.Blocks.launch).parameters
    for key, value in {"css": CSS, "head": KATEX_HEAD, "theme": THEME}.items():
        if key in takes:
            blocks_kw[key] = value
        elif key in launches:
            launch_kw[key] = value
    if "show_api" in launches:
        launch_kw["show_api"] = False
    elif "footer_links" in launches:
        launch_kw["footer_links"] = ["gradio", "settings"]
    if "run_history" in launches:
        launch_kw["run_history"] = False

    with gr.Blocks(**blocks_kw) as app:
        gr.Markdown("## Aligned textbook viewer\nEnglish page ↔ translation. Each translation unit has one colour "
                    "on both pages and one row in the table. Page images are not available here, so boxes are drawn "
                    "on blank pages; Setu shows the same pairs over the printed page.")
        with gr.Row():
            pair = gr.Dropdown(choices=[(pair_label(p), p) for p in pairs], value=pairs[0], label="Book pair", scale=3)
            prev_b = gr.Button("◀ Prev", scale=0)
            page = gr.Dropdown(choices=[], label="English page", scale=1, allow_custom_value=True)
            next_b = gr.Button("Next ▶", scale=0)
            only_bad = gr.Checkbox(label="Only pages with not-aligned text", value=False, scale=1)
        with gr.Accordion("Find text (e.g. 'Ex (5) Divide')", open=False):
            with gr.Row():
                q = gr.Textbox(label="Search English or translated text", scale=3, max_lines=1)
                go = gr.Button("Search", scale=0)
            with gr.Row():
                res = gr.Dropdown(choices=[], label="Matches (pair | English page)", scale=3, allow_custom_value=True)
                info = gr.Markdown()
        top = gr.HTML()
        table = gr.HTML()
        with gr.Accordion("Report a problem on this page", open=False):
            with gr.Row():
                name = gr.Textbox(label="Your name", scale=1, max_lines=1)
                units = gr.Textbox(label="Unit(s), e.g. u4 or u4,u5", scale=1, max_lines=1)
            issue = gr.Textbox(label="What is wrong? (wrong pairing, missing text, wrong correction, …)", lines=3)
            send = gr.Button("Save report", variant="primary")

        pair.change(pages_for, [pair, res, only_bad], page)
        only_bad.change(lambda p, o: pages_for(p, None, o), [pair, only_bad], page)
        page.change(render, [pair, page], [top, table]).then(None, None, None, js=RENDER_MATH_JS)
        prev_b.click(lambda p, g, o: step(p, g, -1, o), [pair, page, only_bad], page)
        next_b.click(lambda p, g, o: step(p, g, +1, o), [pair, page, only_bad], page)
        go.click(find, q, [res, info]); q.submit(find, q, [res, info])
        res.change(jump, [res, pair], [pair, page])
        send.click(report, [name, pair, page, units, issue], [units, issue])
        app.load(pages_for, pair, page)

    app.queue().launch(**launch_kw)


if __name__ == "__main__":
    main()
