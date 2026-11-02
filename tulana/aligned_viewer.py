"""
Viewer for the exported aligned data (data/aligned): pick a pair and an English page; see the English
page and its counterpart page(s) as boxes (same colour = same translation unit), the paired texts
below, and report problems (saved to <aligned>/viewer_reports.jsonl).

  .venv/bin/python scripts/aligned_viewer.py --aligned data/aligned --port 7864 [--share]

Page images are not in the delivery, so boxes are drawn on blank pages of the right size.
"""
import argparse, colorsys, datetime, html, json, os, re, threading

import gradio as gr

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
.pg h4{margin:4px 0;font-size:14px}
.pg svg{width:100%;height:auto;border:1px solid #ccc;background:#fff}
table.units{width:100%;border-collapse:collapse;table-layout:fixed;font-size:14px}
table.units td,table.units th{border:1px solid #ccc;padding:6px;vertical-align:top;text-align:left}
table.units td{white-space:pre-wrap;overflow-wrap:anywhere}
.sw{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:4px;vertical-align:middle}
.note{color:#777;font-size:12px}
.st{display:inline-block;padding:1px 8px;border-radius:9px;font-size:12px;background:#eee}
.bad{background:#fde2e1}
tr.na td{background:#fff3f2}
"""
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
    return (f"{c.get('aligned', 0)}/{n} aligned" + (f', <b style="color:#c0392b">{bad} not aligned</b>' if bad else "")
            + (f", {c['not_processed']} not processed" if c.get("not_processed") else ""))


def color(k):
    r, g, b = colorsys.hsv_to_rgb((k * 0.17) % 1, 0.75, 0.85)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def esc(t):
    return html.escape(t or "", quote=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aligned", default="data/aligned_v2")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=7864)
    ap.add_argument("--share", action="store_true")
    a = ap.parse_args()

    summary = json.load(open(os.path.join(a.aligned, "export_summary.json")))
    # export_summary stores paths as written; re-root them under --aligned so this works after unzipping elsewhere
    pair_files = {r["pair"]: [os.path.join(a.aligned, r["pair"], f.split("/" + r["pair"] + "/", 1)[1]) for f in r["files"]]
                  for r in summary}
    pairs = sorted(pair_files, key=lambda p: (p.startswith("NCERT"), p))
    cache = {}

    def load(pid):
        if pid in cache:
            return cache[pid]
        books = [json.load(open(f)) for f in pair_files[pid]]
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
        d = {"en": en, "tg": tg, "en_pages": en_pages, "where": where, "bilingual": len(books) == 1, "en_parts": en_parts}
        # English pages whose own text, or the text of the target pages shown with them, is not all aligned
        d["bad_pages"] = [pg for pg in en_pages if any(
            page_counts(p).get(s) for p in [en["pages"][pg]] + [tg["pages"][t] for t in target_pages(d, pg)]
            for s in NOT_ALIGNED)]
        cache[pid] = d
        return d

    def target_pages(d, en_page):
        ep = d["en"]["pages"][en_page]
        tpages = sorted({p for b in ep["blocks"] if b.get("align_id") for p in d["where"].get(b["align_id"], ())})
        if not tpages and ep["align_status"] in ("alignment_failed", "unparseable"):
            tpages = [en_page + 1] if d["bilingual"] else ([en_page] if en_page < len(d["tg"]["pages"]) and
                                                            d["en"]["num_pages"] == d["tg"]["num_pages"] else [])
        return tpages

    def pair_label(pid):
        tot = {}
        for f in pair_files[pid]:
            s = json.load(open(f))["alignment"].get("summary")
            if not s:
                return pid
            for k in ("text_blocks", "aligned", "not_processed"):
                tot[k] = tot.get(k, 0) + s[k]
        n = tot["text_blocks"] - tot["not_processed"]
        return f"{pid} · {100 * tot['aligned'] / n:.1f}% aligned" if n else pid

    def svg(page, ids, title):
        W, H = page["width"], page["height"]
        parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
        for b in page["blocks"]:
            x0, y0, x1, y1 = b["bbox_xyxy"]
            aid = b.get("align_id")
            tip = esc((b.get("text") or "")[:300])
            if aid and aid in ids:
                c = color(ids[aid])
                for m in b.get("members", []):
                    mx0, my0, mx1, my1 = m["bbox_xyxy"]
                    parts.append(f'<rect x="{mx0}" y="{my0}" width="{mx1-mx0}" height="{my1-my0}" fill="none" stroke="#bbb" stroke-dasharray="6,4" stroke-width="2"/>')
                parts.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-width="6"><title>{tip}</title></rect>')
                parts.append(f'<text x="{x0+8}" y="{y0+38}" font-size="36" fill="{c}" font-family="sans-serif">u{ids[aid]}{" "+b["part"] if b.get("part") else ""}</text>')
            elif block_state(b, page) in NOT_ALIGNED:
                parts.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#e74c3c" fill-opacity="0.08" stroke="#e74c3c" stroke-width="4" stroke-dasharray="14,8"><title>NOT ALIGNED ({block_state(b, page)}): {tip}</title></rect>')
            else:
                dash = ' stroke-dasharray="4,6"' if not b.get("text") else ""
                parts.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="#999" stroke-width="3"{dash}><title>{tip or b["label"]}</title></rect>')
        parts.append("</svg>")
        return f'<div class="pg"><h4>{esc(title)}</h4>{"".join(parts)}</div>'

    def render(pid, en_page):
        if not pid or en_page is None:
            return "", ""
        d = load(pid); en_page = int(en_page)
        ep = d["en"]["pages"][en_page]
        ids = {}
        for b in sorted(ep["blocks"], key=lambda b: b["order"]):
            if b.get("align_id") and b["align_id"] not in ids:
                ids[b["align_id"]] = len(ids) + 1
        tpages = target_pages(d, en_page)
        lang = d["tg"]["alignment"].get("language", "target").replace("English + ", "")
        st = ep["align_status"]
        tcounts = " · ".join(f'{lang} p{tp}: {counts_txt(page_counts(d["tg"]["pages"][tp]))}' for tp in tpages)
        head = (f'<p><span class="st {"bad" if st in ("alignment_failed", "unparseable") else ""}">{st}</span> '
                f'English page {en_page} ↔ {lang} page(s) {", ".join(map(str, tpages)) or "—"} · {len(ids)} units<br>'
                f'OCR text blocks — English p{en_page}: {counts_txt(page_counts(ep))}{" · " + tcounts if tcounts else ""}<br>'
                f'<span class="note">same colour = same translation unit; dashed grey = original OCR blocks merged; '
                f'<span style="color:#c0392b">dashed red = not aligned</span>; grey = no text or not processed; '
                f'hover a box for its text</span></p>')
        pages_html = svg(ep, ids, f"English · {d['en']['book']} p{en_page}")
        for tp in tpages:
            pages_html += svg(d["tg"]["pages"][tp], ids, f"{lang} · {d['tg']['book']} p{tp}")
        # units table
        tblocks = {}
        for tp in tpages:
            for b in d["tg"]["pages"][tp]["blocks"]:
                if b.get("align_id") in ids:
                    tblocks.setdefault(b["align_id"], []).append((tp, b))
        rows = []
        for b in sorted(ep["blocks"], key=lambda b: b["order"]):
            aid = b.get("align_id")
            if aid in ids:
                k = ids[aid]
                # a unit spanning pages: show every part on BOTH sides, marked with its page
                en_ps = d["en_parts"].get(aid, [(en_page, b)])
                joined = lambda ps: "\n\n".join((f"[p{pg}] " if len(ps) > 1 else "") + x["text"] for pg, x in ps)
                en_txt, tg_txt = joined(en_ps), joined(tblocks.get(aid, []))
                fl = [f for x in [x for _, x in en_ps] + [x for _, x in tblocks.get(aid, [])] for f in x.get("flags", [])]
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
        why = s + (f' ({b["align_note"]})' if b.get("align_note") else "")
        cls, c = ("na", "#e74c3c") if s in NOT_ALIGNED else ("", "#999")
        return (f'<tr class="{cls}"><td><span class="sw" style="background:{c}"></span>not aligned<div class="note">'
                f'{esc(where + why)}</div></td><td>{esc(en_txt)}</td><td>{esc(tg_txt)}</td></tr>')

    def page_list(pid, only_bad):
        d = load(pid)
        return d["bad_pages"] if only_bad else d["en_pages"]

    def pages_for(pid, sel=None, only_bad=False):
        """Page list for a pair; if a search match in this pair is selected, open its page."""
        ps = page_list(pid, only_bad)
        want = sel.split("|")[1].strip() if sel and sel.split("|")[0].strip() == pid else None
        first = str(ps[0]) if ps else None
        return gr.update(choices=[str(p) for p in ps], value=want or first)

    def find(query):
        """Search English and target text across all pairs; returns matches as 'pair | page'."""
        q = (query or "").strip()
        if len(q) < 3:
            return gr.update(choices=[], value=None), "Type at least 3 characters."
        norm = lambda s: re.sub(r"\\[A-Za-z]+|[\s{}$]", "", s or "").lower()   # ignore LaTeX commands, braces, $, spaces
        qn = norm(q)
        hits = []
        for pid in pairs:
            d = load(pid)
            for side in ("en", "tg"):
                for p in d[side]["pages"]:
                    for b in p["blocks"]:
                        if qn in norm(b.get("text")):
                            if side == "en":
                                pg = p["page"]
                            else:
                                pg = next((int(m.group(1)) for m in [re.search(r"/p(\d+)/", b.get("align_id") or "")] if m), None)
                            if pg is not None and pg in d["en_pages"]:
                                hits.append(f"{pid} | {pg}")
            if len(hits) > 200:
                break
        hits = list(dict.fromkeys(hits))
        return gr.update(choices=hits, value=hits[0] if hits else None), f"{len(hits)} match(es)"

    def jump(sel, cur_pair):
        """Same pair: just move the page. Other pair: switch pair; pages_for then opens the matched page."""
        if not sel:
            return gr.update(), gr.update()
        pid, pg = [s.strip() for s in sel.split("|")]
        if pid != cur_pair:
            return gr.update(value=pid), gr.update()
        return gr.update(), gr.update(value=pg)

    def step(pid, pg, k, only_bad=False):
        ps = page_list(pid, only_bad)
        if not ps:
            return gr.update()
        pg = int(pg) if pg not in (None, "") else ps[0]
        if k > 0:
            nxt = [p for p in ps if p > pg]
            return str(nxt[0] if nxt else ps[-1])
        prv = [p for p in ps if p < pg]
        return str(prv[-1] if prv else ps[0])

    def report(name, pid, pg, units, issue):
        if not (name or "").strip() or not (issue or "").strip():
            raise gr.Error("Please enter your name and describe the problem.")
        rec = {"at": datetime.datetime.now().isoformat(timespec="seconds"), "annotator": name.strip(), "pair": pid,
               "en_page": int(pg), "units": units or "", "issue": issue.strip()}
        with _lock, open(os.path.join(a.aligned, "viewer_reports.jsonl"), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        gr.Info("Report saved. Thank you!")
        return "", ""

    with gr.Blocks(title="Aligned textbook viewer", css=CSS, head=KATEX_HEAD) as app:
        gr.Markdown("## Aligned textbook viewer\nEnglish page ↔ translation. Each translation unit has one colour "
                    "on both pages and one row in the table. Page images are not available, so boxes are drawn on "
                    "blank pages.")
        with gr.Row():
            pair = gr.Dropdown(choices=[(pair_label(p), p) for p in pairs], value=pairs[0], label="Book pair", scale=3)
            prev_b = gr.Button("◀ Prev", scale=0)
            page = gr.Dropdown(choices=[], label="English page", scale=1, allow_custom_value=True)
            next_b = gr.Button("Next ▶", scale=0)
            only_bad = gr.Checkbox(label="Only pages with not-aligned text", value=False, scale=1)
        with gr.Accordion("Find text (e.g. 'Ex (5) Divide')", open=False):
            with gr.Row():
                q = gr.Textbox(label="Search English or translated text", scale=3)
                go = gr.Button("Search", scale=0)
            with gr.Row():
                res = gr.Dropdown(choices=[], label="Matches (pair | English page)", scale=3, allow_custom_value=True)
                info = gr.Markdown()
        top = gr.HTML()
        table = gr.HTML()
        with gr.Accordion("Report a problem on this page", open=False):
            with gr.Row():
                name = gr.Textbox(label="Your name", scale=1)
                units = gr.Textbox(label="Unit(s), e.g. u4 or u4,u5", scale=1)
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

    app.queue().launch(server_name=a.host, server_port=a.port, show_api=False, share=a.share)


if __name__ == "__main__":
    main()
