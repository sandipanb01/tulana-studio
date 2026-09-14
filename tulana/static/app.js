/* Tulana Studio — side-by-side clipping of parallel textbook chunks.
   Vanilla JS, no build step. Pointer events throughout, so a finger on a
   tablet behaves exactly like a mouse on a laptop. */
"use strict";
const $  = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const BASE = location.pathname.replace(/\/$/, "");

const api = async (path, opts = {}) => {
  opts.headers = Object.assign({ "Content-Type": "application/json",
    "X-Annotator": localStorage.getItem("studio_who") || "" }, opts.headers || {});
  const r = await fetch(BASE + path, opts);
  if (!r.ok) {
    let msg = r.statusText || `server returned ${r.status}`;
    try {
      const d = (await r.json()).detail;
      if (typeof d === "string") msg = d;
      else if (Array.isArray(d)) msg = d.map(x => x.msg || JSON.stringify(x)).join("; ");
      else if (d) msg = JSON.stringify(d);
    } catch (e) { /* keep the status message */ }
    throw new Error(msg);
  }
  return (r.headers.get("content-type") || "").includes("json") ? r.json() : r.text();
};
const esc = s => String(s ?? "").replace(/[&<>"']/g,
  c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const toast = (m, err = false) => {
  const t = $("#toast"); t.textContent = m; t.className = err ? "err" : "";
  t.style.display = "block"; clearTimeout(t._h);
  t._h = setTimeout(() => t.style.display = "none", 3200);
};
const fmtTime = t => t ? new Date(t * 1000).toLocaleString() : "—";

const S = {
  library: [], combo: null, project: null,
  docs: { src: null, tgt: null },
  zoom: { src: 1, tgt: 1 },
  sel: { src: null, tgt: null },     // {page,x0,y0,x1,y1} in PDF points
  pairs: [], excludedPages: { src: {}, tgt: {} },
  labels: [], chosen: new Set(),
};

/* ── page navigation ───────────────────────────────────────────────────── */
const LOADERS = { Blocks: loadBlocks, Pairs: loadPairs, Export: loadExport, Help: loadDocs };
function show(name) {
  $$("#tabs button").forEach(b => b.classList.toggle("on", b.dataset.page === name));
  $$(".page").forEach(p => p.classList.toggle("on", p.id === "page" + name));
  if (LOADERS[name]) LOADERS[name]().catch(e => toast(e.message, true));
  const sb = $("#side"); if (sb) sb.classList.remove("open");
}
$$("#tabs button").forEach(b => b.onclick = () => show(b.dataset.page));
if ($("#menuBtn")) $("#menuBtn").onclick = () => {
  // each workspace has its own sidebar; toggle whichever is showing
  const sb = $("#bSide") || $("#side");
  if (sb) sb.classList.toggle("open");
};
$("#helpBtn").onclick = () => $("#shade").classList.add("on");
$("#keysClose").onclick = () => $("#shade").classList.remove("on");
$("#shade").onclick = e => { if (e.target.id === "shade") $("#shade").classList.remove("on"); };
$("#who").value = localStorage.getItem("studio_who") || "";
$("#who").onchange = () => localStorage.setItem("studio_who", $("#who").value.trim());

/* ── choosing a textbook ───────────────────────────────────────────────── */
function fill(sel, items, placeholder) {
  sel.innerHTML = (placeholder ? `<option value="">${esc(placeholder)}</option>` : "") +
    items.map(i => `<option value="${esc(i.value)}">${esc(i.label)}</option>`).join("");
}
/* ══════════════ saved pairs ════════════════════════════════════════════════
   A pair is an aligned selection of blocks — either side may span several
   pages, because translated text reflows and a passage that fits one English
   page often runs onto the next. Everything here reads what the Blocks tab
   saved, and can edit, re-check or remove it. */
async function loadPairs() {
  if (!$("#pFilterBook").dataset.filled) {
    const lib = await api("/api/blocks/library");
    const books = [];
    lib.forEach(c => [...c.english_editions, ...c.target_editions]
      .forEach(d => books.push({ value: d.id, label: `${d.book} · ${d.language}` })));
    fill($("#pFilterBook"), books, "Every textbook");
    const langs = [...new Set(lib.flatMap(c => c.target_languages))].sort();
    fill($("#pFilterLang"), langs.map(l => ({ value: l, label: l })), "Every language");
    $("#pFilterBook").dataset.filled = "1";
    ["#pFilterBook", "#pFilterLang", "#pFilterStatus", "#pDrafts"]
      .forEach(x => $(x).onchange = () => loadPairs());
    let t = null;
    $("#pSearch").oninput = () => { clearTimeout(t); t = setTimeout(loadPairs, 300); };
  }
  const q = new URLSearchParams();
  if ($("#pFilterBook").value) q.set("src_book_id", $("#pFilterBook").value);
  if ($("#pFilterLang").value) q.set("language", $("#pFilterLang").value);
  if ($("#pFilterStatus").value) q.set("status", $("#pFilterStatus").value);
  if ($("#pSearch").value.trim()) q.set("search", $("#pSearch").value.trim());
  if ($("#pDrafts").checked) q.set("include_drafts", "true");

  const [data, st] = await Promise.all([
    api(`/api/pairs/block?${q}`), api("/api/pairs/block/stats")]);
  const bits = Object.entries(st.by_status || {})
    .map(([k, v]) => `${v} ${k}`).join(" · ");
  $("#pStats").textContent = st.total
    ? `${st.usable} usable pair(s) — ${bits}` +
      (st.spanning_pages ? ` · ${st.spanning_pages} span more than one page` : "")
    : "Nothing saved yet. Select blocks on both sides in the Blocks tab and press Save pair.";

  if (!data.pairs.length) {
    $("#pList").innerHTML = `<div class="card sm mut">No pair matches that filter.</div>`;
    return;
  }
  $("#pList").innerHTML = data.pairs.map(p => `
    <div class="pcard ${p.status === "excluded" ? "excluded" : ""}" data-id="${p.id}">
      <div class="top">
        <span class="id">#${p.id}</span>
        <span class="ttl">${esc(p.label || "(unlabelled)")}</span>
        <span class="badge ${esc(p.status)}">${esc(p.status)}</span>
        ${p.spans_pages ? `<span class="badge span">spans pages</span>` : ""}
        <span class="sp"></span>
        <span class="sm mut">${esc(p.board || "")} · Class ${p.class || "?"} ·
          ${esc(p.subject || "")} · p${p.src_pages.join(",")} ↔ p${p.tgt_pages.join(",")}</span>
      </div>
      ${p.n_crops ? `<div class="pcrops">${(p.crop_ids || []).map(cid =>
          `<img loading="lazy" src="${BASE}/api/pairs/block/${p.id}/crop/${cid}.png"
                alt="cropped passage">`).join("")}</div>`
        : `<div class="sm faint" style="margin:4px 0 8px">No cropped image —
             the PDF was not on disk when this was saved.
             <button class="btn sm" data-act="recrop">Try again</button></div>`}
      <div class="ptexts">
        <div class="col"><div class="lang">${esc(p.src_language || "source")}
          <span class="mut">${p.src_chars} chars</span></div>
          <div class="body">${esc(p.src_preview || "")}${p.src_chars > 160 ? "…" : ""}</div></div>
        <div class="col"><div class="lang">${esc(p.tgt_language || "target")}
          <span class="mut">${p.tgt_chars} chars</span></div>
          <div class="body">${esc(p.tgt_preview || "")}${p.tgt_chars > 160 ? "…" : ""}</div></div>
      </div>
      <div class="acts">
        <input class="lbl-edit" value="${esc(p.label || "")}" placeholder="Name this passage…">
        <button class="btn sm" data-act="label">Rename</button>
        <button class="btn sm" data-act="open">Open in Blocks</button>
        ${p.status !== "approved" ? `<button class="btn sm" data-act="approve">Approve</button>` : ""}
        ${p.status !== "excluded" ? `<button class="btn sm" data-act="exclude">Exclude</button>`
                                  : `<button class="btn sm" data-act="restore">Restore</button>`}
        <button class="btn sm" data-act="delete">Delete</button>
      </div>
    </div>`).join("");

  $$("#pList .pcard").forEach(card => {
    const id = +card.dataset.id;
    card.querySelectorAll("[data-act]").forEach(b => b.onclick = async () => {
      try {
        if (b.dataset.act === "delete") {
          if (!confirm(`Delete pair #${id}? This cannot be undone.`)) return;
          await api(`/api/pairs/block/${id}`, { method: "DELETE" });
          toast(`Pair #${id} deleted`);
        } else if (b.dataset.act === "label") {
          await api(`/api/pairs/block/${id}`, { method: "PATCH", body: JSON.stringify(
            { label: card.querySelector(".lbl-edit").value }) });
          toast("Renamed");
        } else if (b.dataset.act === "recrop") {
          const r = await api(`/api/pairs/block/${id}/recrop`, { method: "POST" });
          toast(r.crops ? `${r.crops} image(s) cut` :
                (r.problems[0] || "Still no image — is the PDF on disk?"), !r.crops);
        } else if (b.dataset.act === "open") {
          const p = await api(`/api/pairs/block/${id}`);
          openPairInBlocks(p);
          return;
        } else {
          const status = { approve: "approved", exclude: "excluded",
                           restore: "saved" }[b.dataset.act];
          await api(`/api/pairs/block/${id}`, { method: "PATCH",
                                                body: JSON.stringify({ status }) });
          toast(`Pair #${id} ${status}`);
        }
        loadPairs();
      } catch (e) { toast(e.message, true); }
    });
  });
}

/* Reopening a saved pair puts its selection back on the pages it came from,
   so a correction is a small adjustment rather than starting again. */
async function openPairInBlocks(p) {
  show("Blocks");
  await loadBlocks();
  BS("src").book = p.src_book_id; BS("tgt").book = p.tgt_book_id;
  BK.editingPairId = p.id;
  BS("src").page = (p.src_pages || [0])[0];
  BS("tgt").page = (p.tgt_pages || [0])[0];
  ["#bNav", "#bTool", "#bFilter", "#bActions"].forEach(x => $(x).hidden = false);
  await Promise.all([openBlockPage("src"), openBlockPage("tgt")]);
  // Use the ids resolved against today's corpus, not the ones stored when the
  // pair was saved — a re-parse renumbers blocks.
  BS("src").regions = (p.src_regions || []).map(r =>
    ({ page: r.page, x0: r.x0, y0: r.y0, x1: r.x1, y1: r.y1 }));
  BS("tgt").regions = (p.tgt_regions || []).map(r =>
    ({ page: r.page, x0: r.x0, y0: r.y0, x1: r.x1, y1: r.y1 }));
  BS("src").sel = new Set(p.src_block_ids || (p.src_blocks || []).map(b => b.block_id));
  BS("tgt").sel = new Set(p.tgt_block_ids || (p.tgt_blocks || []).map(b => b.block_id));
  if (p.resolves_cleanly === false) {
    toast("Some blocks were renumbered by a corpus reload and were matched by "
        + "page and reading order instead — check the selection before saving", true);
  }
  drawBlocks("src"); drawBlocks("tgt");
  drawRegions("src"); drawRegions("tgt"); refreshSelection();
  toast(`Editing pair #${p.id} — adjust the selection and save`);
}

/* ══════════════ export ═════════════════════════════════════════════════════
   The same pairs, in whichever shape the next tool wants. */
async function loadExport() {
  const [st, formats] = await Promise.all([
    api("/api/pairs/block/stats"), api("/api/pairs/formats")]);
  $("#xStats").textContent = st.usable
    ? `${st.usable} pair(s) available to export`
    : "Nothing to export yet — save some pairs in the Blocks tab first.";

  if (!$("#xBoard").dataset.filled) {
    fill($("#xBoard"), (st.by_board || []).map(b =>
      ({ value: b.board, label: `${b.board} (${b.pairs})` })), "Every board");
    fill($("#xLang"), (st.by_language || []).map(l =>
      ({ value: l.language, label: `${l.language} (${l.pairs})` })), "Every language");
    fill($("#xClass"), [6,7,8,9,10,11,12].map(c =>
      ({ value: c, label: `Class ${c}` })), "Every class");
    $("#xBoard").dataset.filled = "1";
    ["#xBoard","#xLang","#xClass","#xStatus","#xExcluded"]
      .forEach(x => $(x).onchange = refreshExportCount);
  }
  const q = () => {
    const p = new URLSearchParams();
    if ($("#xBoard").value) p.set("board", $("#xBoard").value);
    if ($("#xLang").value) p.set("language", $("#xLang").value);
    if ($("#xClass").value) p.set("cls", $("#xClass").value);
    if ($("#xStatus").value) p.set("status", $("#xStatus").value);
    if ($("#xExcluded").checked) p.set("include_excluded", "true");
    return p;
  };
  window._exportQuery = q;
  $("#xFormats").innerHTML = formats.map(f => `
    <button class="fmt" data-fmt="${esc(f.key)}">
      <b>${esc(f.name)}</b><code>.${esc(f.extension)}</code>
      <span>${esc(f.description)}</span></button>`).join("");
  $$("#xFormats .fmt").forEach(b => b.onclick = () => {
    window.location = `${BASE}/api/pairs/export.${b.dataset.fmt}?${q()}`;
  });
  $("#xBundle").onclick = () => {
    window.location = `${BASE}/api/pairs/export.bundle?${q()}`;
  };
  refreshExportCount();
}
async function refreshExportCount() {
  const p = window._exportQuery ? window._exportQuery() : new URLSearchParams();
  const q = new URLSearchParams(p);
  q.set("limit", "1");
  try {
    const d = await api(`/api/pairs/block?${q}`);
    $("#xCount").textContent = `${d.total} pair(s) match`;
  } catch (e) { $("#xCount").textContent = ""; }
}

let _docs = null;          // the manual list, fetched once

async function loadDocs(name) {
  if (!_docs) _docs = await api("/api/docs");
  const want = typeof name === "string" ? name : (_docs[0] && _docs[0].name);
  $("#docNav").innerHTML = _docs.map(d =>
    `<button class="dl ${d.name === want ? "on" : ""}" data-doc="${esc(d.name)}">${esc(d.title)}</button>`).join("");
  $$("#docNav .dl").forEach(b => b.onclick = () => loadDocs(b.dataset.doc));
  if (!want) return;
  const md = await api("/api/docs/" + want);
  $("#docBody").innerHTML = (window.marked ? marked.parse(md) : `<pre>${esc(md)}</pre>`);
  $("#docBody").scrollTop = 0;
}

/* ── keyboard, global ─────────────────────────────────────────────────── */
document.addEventListener("keydown", e => {
  if (e.key === "Escape") { const sh = $("#shade"); if (sh) sh.classList.remove("on"); }
  const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName || "");
  if (typing || e.altKey) return;
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
    e.preventDefault();
    if ($("#pageBlocks").classList.contains("on")) $("#bSavePair").click();
    return;
  }
  if (e.ctrlKey || e.metaKey) return;
  if (e.key === "?") { const sh = $("#shade"); if (sh) sh.classList.add("on"); }
});

(async function boot() {
  try {
    const h = await api("/api/health");
    if (!h.pdf_ready) toast("PyMuPDF is not installed on the server", true);
    // Blocks is the landing tab, and a tab's data loads when it is shown. On a
    // fresh page load nothing has been shown, so say so explicitly rather than
    // leaving the first thing anyone sees empty.
    await loadBlocks();
  } catch (e) { toast("Backend unreachable: " + e.message, true); }
})();

/* ══════════════ parsed blocks ══════════════════════════════════════════════
   Both editions side by side with the parser's blocks overlaid. Click a block
   to select it, click again to unselect; shift-click takes the range in
   reading order. The extracted text of what is selected appears underneath,
   both languages at once — which is the whole point: seeing that the Marathi
   block you picked says what the English one does.

   Boxes arrive as fractions of the page, so the overlay is correct at any
   zoom and at whatever DPI the page happens to be rendered. */
const BK = {
  combo: null, labels: [], colors: {},
  side: { src: { book:null, page:0, pages:0, blocks:[], sel:new Set(), zoom:1, last:null, w:0, h:0 },
          tgt: { book:null, page:0, pages:0, blocks:[], sel:new Set(), zoom:1, last:null, w:0, h:0 } },
};
const BS = s => BK.side[s];
const bhost = s => $(s === "src" ? "#bHostSrc" : "#bHostTgt");

const BLOCK_COLOURS = ["#c2404a","#1f4e79","#c98a1b","#2e7bb8","#6a8f2f","#7a4fc0",
  "#a8552f","#c2571f","#158a4a","#8a7bb8","#b8433a","#607089","#7d879c","#9aa5b8"];

async function loadBlocks() {
  if (!BK.labels.length) {
    const s = await api("/api/blocks/stats");
    BK.labels = s.labels || [];
    BK.labels.forEach((l, i) => BK.colors[l.label] = BLOCK_COLOURS[i % BLOCK_COLOURS.length]);
    $("#bCorpus").innerHTML = s.books
      ? `${s.books} books · ${s.pages.toLocaleString()} pages ·
         ${s.blocks.toLocaleString()} blocks · ${s.by_language.length} languages`
      : `No parsed layout loaded.`;
    fill($("#bLabel"), BK.labels.map(l => ({ value: l.label, label: `${l.label} (${l.n})` })),
         "All block types");
    $("#bLegend").innerHTML = BK.labels.slice(0, 14).map(l =>
      `<span class="lgd"><i style="background:${BK.colors[l.label]}"></i>${esc(l.label)}</span>`).join("");
  }
  if (!$("#bCombo").dataset.filled) {
    BK.library = await api("/api/blocks/library");
    fill($("#bCombo"), BK.library.map((c, i) => ({ value: i, label: c.label })),
         "Choose a board and class…");
    $("#bCombo").dataset.filled = "1";
    $("#bCombo").onchange = () => {
      const c = BK.library[+$("#bCombo").value]; BK.combo = c;
      if (!c) return;
      fill($("#bLang"), c.target_languages.map(l => ({ value: l, label: l })),
           "Choose the target language…");
      fill($("#bSrcDoc"), c.english_editions.map(d =>
        ({ value: d.id, label: `${d.book} · ${d.num_pages}pp · ${d.n_blocks} blocks` })), "");
      fill($("#bTgtDoc"), [], "—");
    };
    $("#bLang").onchange = () => {
      const c = BK.combo, lang = $("#bLang").value;
      if (!c || !lang) return;
      fill($("#bTgtDoc"), c.target_editions.filter(d => d.language === lang).map(d =>
        ({ value: d.id, label: `${d.book} · ${d.num_pages}pp · ${d.n_blocks} blocks` })), "");
    };
  }
}
$("#bOpen").onclick = async () => {
  const s = +$("#bSrcDoc").value, t = +$("#bTgtDoc").value;
  if (!s || !t) { toast("Choose a board, class, language and both editions", true); return; }
  BS("src").book = s; BS("src").page = 0; BS("src").sel.clear(); BS("src").regions = [];
  BS("tgt").book = t; BS("tgt").page = 0; BS("tgt").sel.clear(); BS("tgt").regions = [];
  BK.editingPairId = null;
  ["#bNav","#bTool","#bFilter","#bActions"].forEach(x => $(x).hidden = false);
  await Promise.all([openBlockPage("src"), openBlockPage("tgt")]);
  $("#bSide").classList.remove("open");
};

async function openBlockPage(side) {
  const st = BS(side);
  if (st.book === null) return;
  try {
    const d = await api(`/api/blocks/page/${st.book}/${st.page}`);
    st.blocks = d.blocks || []; st.pages = d.pages; st.w = d.width; st.h = d.height;
    st.imageAvailable = !!d.image_available;
    // The selection deliberately survives a page turn. A passage that fits
    // one English page often runs onto the next in the target language, so
    // clearing at the page boundary would make a cross-page pair impossible.
    st.last = null;
    $(side === "src" ? "#bTitSrc" : "#bTitTgt").textContent =
      `${d.book.language} — ${d.book.book}`;
    $(side === "src" ? "#bPosSrc" : "#bPosTgt").textContent =
      `page ${st.page + 1} of ${d.pages} · ${st.blocks.length} blocks`
      + (d.book.pdf_present ? "" : " · PDF not on disk");
    $(side === "src" ? "#bPageSrc" : "#bPageTgt").value = st.page;
    renderBlockSide(side);
    setTimeout(() => drawRegions(side), 60);
    refreshSelection();
  } catch (e) { toast(e.message, true); }
}

function renderBlockSide(side) {
  const st = BS(side), h = bhost(side);
  const box = $(side === "src" ? "#bScrSrc" : "#bScrTgt");
  const fitW = Math.max(240, (box.clientWidth || 600) - 28);
  const w = Math.round(fitW * st.zoom);
  const aspect = (st.h && st.w) ? st.h / st.w : 1.414;
  $(side === "src" ? "#bZoomSrc" : "#bZoomTgt").textContent = Math.round(st.zoom * 100) + "%";
  h.style.width = w + "px";
  // Only request the image when the server has said it can render it. Letting
  // an <img> discover a missing PDF by 404 works, but logs a red error that
  // reads like a bug to whoever opens the developer tools next.
  if (st.imageAvailable) {
    h.innerHTML = `<img width="${w}" src="${BASE}/api/blocks/page-image/${st.book}/${st.page}.png" alt="">`;
    const img = h.querySelector("img");
    if (img) img.onload = () => drawBlocks(side);
  } else {
    h.innerHTML = "";
    blockFallback(side, w, aspect);
  }
  drawBlocks(side);
}
// When the PDF is absent the layout is still usable: the blocks are drawn on a
// blank page of the right proportions rather than the tab showing nothing.
window.blockFallback = (side, w, aspect) => {
  const h = bhost(side);
  const d = document.createElement("div");
  d.className = "blank";
  d.style.cssText = `width:${w}px;height:${Math.round(w * aspect)}px`;
  d.textContent = "The PDF for this book is not on disk — blocks and text are shown without the page image.";
  h.appendChild(d);
  drawBlocks(side);
};

function drawBlocks(side) {
  const st = BS(side), h = bhost(side);
  if (!h) return;
  [...h.querySelectorAll(".blk")].forEach(e => e.remove());
  const surface = h.querySelector("img") || h.querySelector(".blank");
  if (!surface) return;
  const W = surface.clientWidth || surface.offsetWidth;
  const H = surface.clientHeight || surface.offsetHeight;
  const only = $("#bLabel").value, dim = $("#bDim").checked, order = $("#bShowOrder").checked;
  // Draw the largest blocks first so the smaller ones sit on top. A page header
  // often overlaps the heading beneath it, and in document order the larger box
  // is painted last and swallows every click meant for what is inside it.
  const area = b => Math.max(0, (b.fx1 - b.fx0)) * Math.max(0, (b.fy1 - b.fy0));
  const painted = st.blocks
    .map((b, i) => ({ b, i }))
    .sort((p, q) => area(q.b) - area(p.b));
  painted.forEach(({ b, i }) => {
    const hidden = only && b.label !== only;
    if (hidden && !dim) return;
    const el = document.createElement("div");
    const on = st.sel.has(b.id);
    el.className = "blk" + (on ? " on" : "") + ((hidden || (dim && !on)) ? " dim" : "");
    el.style.cssText = `--c:${BK.colors[b.label] || "#666"};left:${b.fx0*W}px;top:${b.fy0*H}px;` +
      `width:${(b.fx1-b.fx0)*W}px;height:${(b.fy1-b.fy0)*H}px`;
    el.dataset.id = b.id; el.dataset.i = i;
    el.title = `${b.label} · ${b.type} · order ${b.ord} · confidence ${b.conf}`;
    el.innerHTML = `<span class="lb">${esc(b.label || b.type || "")}</span>` +
                   (order ? `<span class="no">${b.ord}</span>` : "");
    h.appendChild(el);
  });
  renderPageMap();
}

["src","tgt"].forEach(side => {
  const h = bhost(side);
  if (!h) return;
  h.addEventListener("click", ev => {
    const el = ev.target.closest(".blk");
    if (!el) return;
    const st = BS(side), id = +el.dataset.id, i = +el.dataset.i;
    if (ev.shiftKey && st.last !== null) {
      // a range in reading order, which is what "everything from here to there"
      // means on a page — not the order the two were clicked in
      const [a, b] = [Math.min(st.last, i), Math.max(st.last, i)];
      for (let k = a; k <= b; k++) st.sel.add(st.blocks[k].id);
    } else {
      st.sel.has(id) ? st.sel.delete(id) : st.sel.add(id);
      st.last = i;
    }
    markSelected(side); refreshSelection();
  });
});

/* Toggling a class beats redrawing. A full redraw replaces every element, so
   the one under the cursor is destroyed mid-click — and on a page with a
   hundred blocks it is visibly slow for something that changed one box. */
function markSelected(side) {
  const st = BS(side), h = bhost(side);
  if (!h) return;
  const dim = $("#bDim").checked, only = $("#bLabel").value;
  h.querySelectorAll(".blk").forEach(el => {
    const id = +el.dataset.id;
    const on = st.sel.has(id);
    el.classList.toggle("on", on);
    const b = st.blocks[+el.dataset.i];
    const hidden = only && b && b.label !== only;
    el.classList.toggle("dim", !!(hidden || (dim && !on)));
  });
  renderPageMap();
}

let _selTimer = null;
function refreshSelection() {
  const s = BS("src"), t = BS("tgt");
  const n = s.sel.size + t.sel.size + s.regions.length + t.regions.length;
  const part = x => {
    const st = BS(x), bits = [];
    if (st.sel.size) bits.push(`${st.sel.size} block(s)`);
    if (st.regions.length) bits.push(`${st.regions.length} crop(s)`);
    return bits.join(" + ") || "nothing";
  };
  $("#bSelInfo").textContent = n
    ? `source: ${part("src")} · target: ${part("tgt")}`
    : "Nothing selected — click blocks, or switch to Drag to crop";
  $("#bText").hidden = (s.sel.size + t.sel.size) === 0;
  renderPageMap();
  previewCrops();
  scheduleDraft();
  clearTimeout(_selTimer);
  if (!n) return;
  _selTimer = setTimeout(async () => {
    try {
      const r = await api("/api/blocks/selection/pair", { method: "POST",
        body: JSON.stringify({ src_block_ids: [...s.sel], tgt_block_ids: [...t.sel] }) });
      const render = (sel, el, head) => {
        $(head).textContent = sel.n_blocks
          ? `${sel.n_blocks} block(s) · ${sel.n_chars} characters` : "Nothing selected";
        $(el).innerHTML = sel.blocks.map(b =>
          `<div class="blkt"><b>${esc(b.label || "")}</b>${esc(b.text || "")}</div>`).join("")
          || `<div class="sm faint">No text in the selected blocks — diagrams and
               images carry none, and a page without a text layer yields none.</div>`;
      };
      render(r.source, "#bTextSrc", "#bTextHeadSrc");
      render(r.target, "#bTextTgt", "#bTextHeadTgt");
      BK.lastText = r;
    } catch (e) { toast(e.message, true); }
  }, 180);
}

$("#bClearSel").onclick = () => {
  ["src","tgt"].forEach(s => {
    BS(s).sel.clear(); BS(s).last = null; BS(s).regions = [];
    markSelected(s); drawRegions(s); });
  refreshSelection();
};
$("#bSelAll").onclick = () => {
  const only = $("#bLabel").value;
  ["src","tgt"].forEach(s => {
    BS(s).blocks.forEach(b => { if (!only || b.label === only) BS(s).sel.add(b.id); });
    markSelected(s);
  });
  refreshSelection();
};
$("#bCopy").onclick = async () => {
  const r = BK.lastText;
  if (!r) { toast("Select some blocks first", true); return; }
  const text = `${r.source.text}\n\n---\n\n${r.target.text}`;
  try { await navigator.clipboard.writeText(text); toast("Extracted text copied"); }
  catch (e) { toast("Could not reach the clipboard — select the text and copy it", true); }
};
$("#bLabel").onchange = () => { drawBlocks("src"); drawBlocks("tgt"); };
$("#bDim").onchange = () => { drawBlocks("src"); drawBlocks("tgt"); };
$("#bShowOrder").onchange = () => { drawBlocks("src"); drawBlocks("tgt"); };
$$("[data-bzoom]").forEach(b => b.onclick = () => {
  const side = b.dataset.bzoom, st = BS(side);
  st.zoom = Math.min(4, Math.max(0.3, st.zoom + 0.25 * (+b.dataset.d)));
  renderBlockSide(side);
});
$$("[data-bfit]").forEach(b => b.onclick = () => {
  const side = b.dataset.bfit; BS(side).zoom = 1; renderBlockSide(side);
});
function turnBlockPage(delta) {
  const both = $("#bLock").checked;
  for (const side of (both ? ["src","tgt"] : ["src"])) {
    const st = BS(side);
    if (st.book === null) continue;
    const n = st.page + delta;
    if (n >= 0 && n < st.pages) { st.page = n; openBlockPage(side); }
  }
}
$("#bPrev").onclick = () => turnBlockPage(-1);
$("#bNext").onclick = () => turnBlockPage(1);
["#bPageSrc","#bPageTgt"].forEach((sel, i) => $(sel).onchange = () => {
  const side = i === 0 ? "src" : "tgt", st = BS(side), v = +$(sel).value;
  if (st.book !== null && v >= 0 && v < st.pages) { st.page = v; openBlockPage(side); }
});
$("#bSplit").addEventListener("pointerdown", ev => {
  ev.preventDefault(); $("#bSplit").setPointerCapture(ev.pointerId);
  const move = e => {
    const w = $("#bPanes").getBoundingClientRect();
    const pct = Math.min(80, Math.max(20, ((e.clientX - w.left) / w.width) * 100));
    $("#bPaneSrc").style.flex = `0 0 ${pct}%`;
    $("#bPaneTgt").style.flex = `0 0 ${100 - pct}%`;
  };
  const up = () => { window.removeEventListener("pointermove", move);
                     window.removeEventListener("pointerup", up); };
  window.addEventListener("pointermove", move); window.addEventListener("pointerup", up);
});
document.addEventListener("keydown", e => {
  if (!$("#pageBlocks").classList.contains("on")) return;
  if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName || "")) return;
  if (e.key === "ArrowRight") turnBlockPage(1);
  if (e.key === "ArrowLeft") turnBlockPage(-1);
  if (e.key === "Escape") $("#bClearSel").click();
  if (e.key === "+" || e.key === "=") { BS("src").zoom = Math.min(4, BS("src").zoom+0.25);
    BS("tgt").zoom = BS("src").zoom; renderBlockSide("src"); renderBlockSide("tgt"); }
  if (e.key === "-") { BS("src").zoom = Math.max(0.3, BS("src").zoom-0.25);
    BS("tgt").zoom = BS("src").zoom; renderBlockSide("src"); renderBlockSide("tgt"); }
});




/* ══════════════ the crop tool ══════════════════════════════════════════════
   Two ways to say what a passage is, because they answer different questions.

   **Clicking blocks** takes what the parser found, and brings its text with it.
   **Dragging a rectangle** takes what a person decided. A figure with its
   caption and the line beneath may be one passage to a reader and three blocks
   to the parser — and a hand-drawn diagram or a margin note was never a block
   at all, so no amount of clicking would ever reach it.

   Both work across pages, both are kept automatically, and both are cut from
   the original PDF as parallel images. */
function setTool(name) {
  BK.tool = name;
  $$(".segbtn").forEach(b => b.classList.toggle("on", b.dataset.tool === name));
  ["src", "tgt"].forEach(s => {
    const h = bhost(s);
    if (h) h.classList.toggle("cropping", name === "crop");
  });
  $("#bToolHint").textContent = name === "crop"
    ? "Drag a rectangle over the passage. Drag inside one to move it, the corner to resize."
    : "Click a block to select it. Shift-click for a range.";
  drawRegions("src"); drawRegions("tgt");
}
$$(".segbtn").forEach(b => b.onclick = () => setTool(b.dataset.tool));

function drawRegions(side) {
  const st = BS(side), h = bhost(side);
  if (!h) return;
  [...h.querySelectorAll(".crop")].forEach(e => e.remove());
  const surface = h.querySelector("img") || h.querySelector(".blank");
  if (!surface) return;
  const W = surface.clientWidth || surface.offsetWidth;
  const H = surface.clientHeight || surface.offsetHeight;
  st.regions.filter(r => r.page === st.page).forEach(r => {
    const i = st.regions.indexOf(r);
    const el = document.createElement("div");
    el.className = "crop";
    el.style.cssText = `left:${r.x0*W}px;top:${r.y0*H}px;` +
      `width:${(r.x1-r.x0)*W}px;height:${(r.y1-r.y0)*H}px`;
    el.dataset.i = i;
    el.innerHTML = `<span class="cn">crop ${i + 1}</span>` +
      `<button class="cx" title="Remove">×</button><i class="grip"></i>`;
    h.appendChild(el);
  });
  renderRegionList();
}

function renderRegionList() {
  const box = $("#bRegions");
  if (!box) return;
  const rows = [];
  for (const side of ["src", "tgt"]) {
    BS(side).regions.forEach((r, i) => rows.push({ side, i, r }));
  }
  box.innerHTML = rows.length ? rows.map(({ side, i, r }) => `
    <div class="rgi" data-side="${side}" data-i="${i}">
      <span class="nm">${side === "src" ? "source" : "target"} · page ${r.page}
        · crop ${i + 1}</span>
      <button data-go>go</button><button data-del>✕</button>
    </div>`).join("")
    : `<div class="sm faint">No crops drawn.</div>`;
  box.querySelectorAll(".rgi").forEach(el => {
    const side = el.dataset.side, i = +el.dataset.i;
    el.querySelector("[data-del]").onclick = () => {
      BS(side).regions.splice(i, 1);
      drawRegions(side); refreshSelection();
    };
    el.querySelector("[data-go]").onclick = () => {
      const r = BS(side).regions[i];
      if (r && BS(side).page !== r.page) { BS(side).page = r.page; openBlockPage(side); }
    };
  });
}

["src", "tgt"].forEach(side => {
  const h = bhost(side);
  if (!h) return;
  let mode = null, start = null, origin = null, idx = -1, live = null;
  const at = ev => {
    const surface = h.querySelector("img") || h.querySelector(".blank");
    const r = surface.getBoundingClientRect();
    return { x: (ev.clientX - r.left) / r.width, y: (ev.clientY - r.top) / r.height };
  };
  h.addEventListener("pointerdown", ev => {
    const st = BS(side);
    if (st.book === null || ev.button === 2) return;
    const existing = ev.target.closest(".crop");
    if (existing) {
      if (ev.target.classList.contains("cx")) {
        st.regions.splice(+existing.dataset.i, 1);
        drawRegions(side); refreshSelection();
        ev.preventDefault(); return;
      }
      idx = +existing.dataset.i;
      origin = { ...st.regions[idx] };
      start = at(ev);
      mode = ev.target.classList.contains("grip") ? "resize" : "move";
    } else {
      if (BK.tool !== "crop") return;
      start = at(ev);
      st.regions.push({ page: st.page, x0: start.x, y0: start.y,
                        x1: start.x, y1: start.y });
      idx = st.regions.length - 1;
      mode = "draw";
    }
    h.setPointerCapture(ev.pointerId);
    ev.preventDefault();
  });
  h.addEventListener("pointermove", ev => {
    if (!mode || idx < 0) return;
    const st = BS(side), p = at(ev), r = st.regions[idx];
    const clamp = v => Math.max(0, Math.min(1, v));
    if (mode === "draw") {
      r.x0 = clamp(Math.min(start.x, p.x)); r.x1 = clamp(Math.max(start.x, p.x));
      r.y0 = clamp(Math.min(start.y, p.y)); r.y1 = clamp(Math.max(start.y, p.y));
    } else if (mode === "move") {
      const dx = p.x - start.x, dy = p.y - start.y;
      const w = origin.x1 - origin.x0, ht = origin.y1 - origin.y0;
      r.x0 = clamp(Math.min(1 - w, origin.x0 + dx)); r.x1 = r.x0 + w;
      r.y0 = clamp(Math.min(1 - ht, origin.y0 + dy)); r.y1 = r.y0 + ht;
    } else {
      r.x1 = clamp(Math.max(origin.x0 + 0.005, p.x));
      r.y1 = clamp(Math.max(origin.y0 + 0.005, p.y));
    }
    drawRegions(side);
    const el = h.querySelector(`.crop[data-i="${idx}"]`);
    if (el) el.classList.add("live");
  });
  const finish = () => {
    if (!mode) return;
    const st = BS(side), r = st.regions[idx];
    const drawing = mode === "draw";
    mode = null;
    // a tap is not a rectangle
    if (drawing && r && (r.x1 - r.x0 < 0.006 || r.y1 - r.y0 < 0.006)) {
      st.regions.splice(idx, 1);
    }
    drawRegions(side);
    refreshSelection();
  };
  h.addEventListener("pointerup", finish);
  h.addEventListener("pointercancel", finish);
});

/* ── the selection is kept without being asked ─────────────────────────────
   Written as a draft while the annotator works, so a closed tab, a lost
   connection or a stray reload costs nothing. It becomes an ordinary pair the
   moment they press Save. */
let _draftTimer = null;
function scheduleDraft() {
  clearTimeout(_draftTimer);
  _draftTimer = setTimeout(async () => {
    const s = BS("src"), t = BS("tgt");
    if (s.book === null || t.book === null) return;
    try {
      await api("/api/pairs/block/draft", { method: "POST", body: JSON.stringify({
        src_book_id: s.book, tgt_book_id: t.book,
        src_block_ids: [...s.sel], tgt_block_ids: [...t.sel],
        src_regions: s.regions, tgt_regions: t.regions }) });
      if (s.sel.size || t.sel.size || s.regions.length || t.regions.length)
        setBlockSaveState("Kept automatically");
    } catch (e) {
      // Say so. Silence here would let an annotator believe the work is safe.
      setBlockSaveState(`Not kept on the server (${e.message})`, true);
    }
  }, 1600);
}
function setBlockSaveState(text, warn) {
  const el = $("#bSaveState");
  if (!el) return;
  el.textContent = text || "";
  el.style.color = warn ? "var(--danger)" : "";
}
window.addEventListener("pagehide", () => {
  const s = BS("src"), t = BS("tgt");
  if (s.book === null ||
      !(s.sel.size || t.sel.size || s.regions.length || t.regions.length)) return;
  try {
    navigator.sendBeacon(`${BASE}/api/pairs/block/draft`, new Blob([JSON.stringify({
      src_book_id: s.book, tgt_book_id: t.book,
      src_block_ids: [...s.sel], tgt_block_ids: [...t.sel],
      src_regions: s.regions, tgt_regions: t.regions })],
      { type: "application/json" }));
  } catch (e) {}
});

/* which pages the current selection touches — otherwise a selection made three
   pages ago is invisible once you have turned away from it */
function pagesTouched(side) {
  const st = BS(side), here = new Set(st.blocks.map(b => b.id));
  const onThis = [...st.sel].filter(id => here.has(id)).length;
  return { onThisPage: onThis, elsewhere: st.sel.size - onThis };
}
function renderPageMap() {
  const s = pagesTouched("src"), t = pagesTouched("tgt");
  const bits = [];
  if (s.elsewhere) bits.push(`${s.elsewhere} source block(s) selected on other pages`);
  if (t.elsewhere) bits.push(`${t.elsewhere} target block(s) selected on other pages`);
  const el = $("#bPageMap");
  if (el) el.textContent = bits.join(" · ");
}

/* What the crop will look like, before it is saved. The pair is meant to be
   read side by side, so seeing the two regions together is the check that
   matters — far more than a count of selected blocks. */
function previewCrops() {
  const box = $("#bPreview");
  if (!box) return;
  const rows = [];
  for (const side of ["src", "tgt"]) {
    const st = BS(side);
    const here = st.blocks.filter(b => st.sel.has(b.id));
    if (!here.length) { rows.push(null); continue; }
    const x0 = Math.min(...here.map(b => b.fx0)), y0 = Math.min(...here.map(b => b.fy0));
    const x1 = Math.max(...here.map(b => b.fx1)), y1 = Math.max(...here.map(b => b.fy1));
    rows.push({ side, x0, y0, x1, y1, n: here.length, page: st.page });
  }
  box.hidden = !rows.some(Boolean);
  box.innerHTML = rows.filter(Boolean).map(r => `
    <div class="pv">
      <div class="sm faint">${r.side === "src" ? "source" : "target"} · page ${r.page}
        · ${r.n} block(s)</div>
      <div class="pvbox" style="aspect-ratio:${Math.max(0.05,(r.x1-r.x0))}/${Math.max(0.05,(r.y1-r.y0))}">
        <img src="${BASE}/api/blocks/page-image/${BS(r.side).book}/${r.page}.png"
             style="width:${100/Math.max(0.02,(r.x1-r.x0))}%;
                    margin-left:${-100*r.x0/Math.max(0.02,(r.x1-r.x0))}%;
                    margin-top:${-100*r.y0/Math.max(0.02,(r.y1-r.y0))*((r.x1-r.x0)/(r.y1-r.y0))*0}%;
                    transform:translateY(${-100*r.y0/Math.max(0.02,(r.y1-r.y0))}%)">
      </div>
    </div>`).join("");
}

$("#bSavePair").onclick = async () => {
  const s = BS("src"), t = BS("tgt");
  const has = x => BS(x).sel.size || BS(x).regions.length;
  if (!has("src") && !has("tgt")) {
    toast("Select some blocks, or drag a crop, first", true); return; }
  if (!has("src") || !has("tgt")) {
    if (!confirm("Only one side has anything selected. Save it anyway?")) return;
  }
  try {
    const p = await api("/api/pairs/block", { method: "POST", body: JSON.stringify({
      src_book_id: s.book, tgt_book_id: t.book,
      src_block_ids: [...s.sel], tgt_block_ids: [...t.sel],
      src_regions: s.regions, tgt_regions: t.regions,
      label: $("#bLabel2").value, status: "saved",
      pair_id: BK.editingPairId || null }) });
    const nimg = (p.src_crops || []).concat(p.tgt_crops || [])
      .filter(c => c.path).length;
    toast((BK.editingPairId ? `Pair #${p.id} updated` : `Saved pair #${p.id}`)
          + (nimg ? ` · ${nimg} image(s) cut` : " · no image, the PDF is not on disk"));
    setBlockSaveState(`Saved as pair #${p.id}${nimg ? ` with ${nimg} image(s)` : ""}`);
    BK.editingPairId = null;
    $("#bLabel2").value = "";
    ["src", "tgt"].forEach(x => {
      BS(x).sel.clear(); BS(x).regions = []; drawBlocks(x); drawRegions(x); });
    refreshSelection();
  } catch (e) { toast(e.message, true); }
};
