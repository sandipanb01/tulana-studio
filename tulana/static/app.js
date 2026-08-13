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
const LOADERS = { Pairs: loadPairs, Export: loadExport, Help: loadDocs };
function show(name) {
  $$("#tabs button").forEach(b => b.classList.toggle("on", b.dataset.page === name));
  $$(".page").forEach(p => p.classList.toggle("on", p.id === "page" + name));
  if (LOADERS[name]) LOADERS[name]().catch(e => toast(e.message, true));
  $("#side").classList.remove("open");
}
$$("#tabs button").forEach(b => b.onclick = () => show(b.dataset.page));
$("#menuBtn").onclick = () => $("#side").classList.toggle("open");
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
async function loadLibrary() {
  S.library = await api("/api/library");
  fill($("#selCombo"), S.library.map((c, i) => ({ value: i, label: c.label })),
       "Choose a board and class…");
  $("#selCombo").onchange = onCombo;
  $("#selLang").onchange = onLang;
}
function onCombo() {
  const c = S.library[+$("#selCombo").value];
  S.combo = c;
  if (!c) { fill($("#selLang"), [], "—"); return; }
  fill($("#selLang"), c.target_languages.map(l => ({ value: l, label: l })),
       "Choose the target language…");
  fill($("#selSrcDoc"), c.english_editions.map(d =>
       ({ value: d.id, label: `${d.volume || "Full book"} · ${d.pages} pages` })), "");
  fill($("#selTgtDoc"), [], "—");
}
function onLang() {
  const c = S.combo, lang = $("#selLang").value;
  if (!c || !lang) return;
  const eds = c.target_editions.filter(d => d.language === lang);
  fill($("#selTgtDoc"), eds.map(d =>
       ({ value: d.id, label: `${d.volume || "Full book"} · ${d.pages} pages` })), "");
}
$("#btnOpen").onclick = async () => {
  const c = S.combo, src = +$("#selSrcDoc").value, tgt = +$("#selTgtDoc").value;
  if (!c || !src || !tgt) { toast("Choose a board, class, language and both editions", true); return; }
  try {
    S.project = await api("/api/projects", { method: "POST", body: JSON.stringify({
      board: c.board, cls: c.class, subject: c.subject, src_doc: src, tgt_doc: tgt }) });
    S.docs.src = await api("/api/doc/" + src);
    S.docs.tgt = await api("/api/doc/" + tgt);
    $("#titSrc").textContent = S.docs.src.language + " edition";
    $("#titTgt").textContent = S.docs.tgt.language + " edition";
    $("#grpNav").hidden = false; $("#grpPair").hidden = false;
    renderPane("src"); renderPane("tgt");
    loadOutline(); await loadLabels();
    await refreshCount();
    $("#side").classList.remove("open");
    toast(`Opened ${S.docs.src.language} ↔ ${S.docs.tgt.language}`);
  } catch (e) { toast(e.message, true); }
};

/* ── rendering the pages ───────────────────────────────────────────────────
   Pages are plain <img> elements loaded lazily by the browser. That keeps a
   400-page textbook light: only what is near the viewport is ever fetched,
   and the server caches each rendered page so scrolling back is instant. */
function renderPane(side) {
  const doc = S.docs[side], box = $(side === "src" ? "#scrSrc" : "#scrTgt");
  if (!doc) return;
  // Zoom 1 means "fit the pane", so a page is fully visible on any screen —
  // a fixed pixel width cut the right-hand edge off on narrower panes and on
  // phones. Zooming past 1 scrolls horizontally, as expected.
  const fit = Math.max(240, (box.clientWidth || 760) - 26);
  const w = Math.round(fit * S.zoom[side]);
  box.innerHTML = "";
  for (let p = 1; p <= doc.pages; p++) {
    const d = document.createElement("div");
    d.className = "pg"; d.dataset.page = p; d.dataset.side = side;
    d.style.width = w + "px";
    d.innerHTML =
      `<img loading="lazy" width="${w}" src="${BASE}/api/doc/${doc.id}/page/${p}.png" alt="page ${p}">
       <span class="no">${p}</span>`;
    box.appendChild(d);
  }
  attachSelection(box, side);
  box.onscroll = () => onScroll(side);
}
function onScroll(side) {
  const box = $(side === "src" ? "#scrSrc" : "#scrTgt");
  const pages = $$(".pg", box);
  const top = box.scrollTop;
  let cur = 1;
  for (const p of pages) { if (p.offsetTop - box.offsetTop <= top + 60) cur = +p.dataset.page; }
  $(side === "src" ? "#posSrc" : "#posTgt").textContent =
    `page ${cur} of ${S.docs[side].pages}`;
  markExcluded(side, cur);
  if ($("#lockScroll").checked && !onScroll._busy) {
    onScroll._busy = true;
    const other = side === "src" ? "tgt" : "src";
    const ob = $(other === "src" ? "#scrSrc" : "#scrTgt");
    const ratio = box.scrollTop / Math.max(1, box.scrollHeight - box.clientHeight);
    ob.scrollTop = ratio * Math.max(1, ob.scrollHeight - ob.clientHeight);
    setTimeout(() => { onScroll._busy = false; }, 60);
  }
}
/* Ask the server whether the visible page is an excluded topic. Cached per
   page so scrolling does not re-ask. */
async function markExcluded(side, page) {
  const cache = S.excludedPages[side];
  if (cache[page] === undefined) {
    cache[page] = null;
    try {
      const r = await api(`/api/doc/${S.docs[side].id}/page/${page}/text`);
      cache[page] = r.excluded_topic ? (r.matched_term || "excluded") : false;
    } catch (e) { cache[page] = false; }
  }
  const el = $$(`.pg[data-side="${side}"]`).find(x => +x.dataset.page === page);
  if (el) el.classList.toggle("excl", !!cache[page]);
  updateWarn();
}
function updateWarn() {
  const bits = [];
  for (const side of ["src", "tgt"]) {
    const s = S.sel[side];
    if (s && S.excludedPages[side][s.page]) {
      bits.push(`${S.docs[side].language} page ${s.page} looks like ` +
                `${S.excludedPages[side][s.page]}`);
    }
  }
  $("#warnBox").innerHTML = bits.length
    ? `⚠ ${esc(bits.join("; "))}. Geometry and conics are excluded from this corpus —
       saving is still allowed, but the pair will be marked excluded.` : "";
}

$$("[data-zoom]").forEach(b => b.onclick = () => {
  const side = b.dataset.zoom;
  S.zoom[side] = Math.min(2.4, Math.max(0.5, S.zoom[side] + 0.15 * (+b.dataset.d)));
  const keep = S.sel[side];
  renderPane(side);
  if (keep) drawBox(side, keep);
});
$("#btnJump").onclick = () => {
  const go = (side, v) => {
    if (!v || !S.docs[side]) return;
    const box = $(side === "src" ? "#scrSrc" : "#scrTgt");
    const el = $$(".pg", box).find(x => +x.dataset.page === +v);
    if (el) box.scrollTo({ top: el.offsetTop - box.offsetTop - 6, behavior: "smooth" });
  };
  go("src", $("#jumpSrc").value); go("tgt", $("#jumpTgt").value);
};
async function loadOutline() {
  try {
    const o = await api(`/api/doc/${S.docs.src.id}/outline`);
    if (!o.outline.length) { $("#outlineBox").innerHTML =
      `<div class="sm faint" style="padding:8px">This textbook has no chapter bookmarks.</div>`; return; }
    $("#outlineBox").innerHTML = o.outline.map(i =>
      `<button class="oi ${i.excluded_topic ? "excl" : ""}" data-page="${i.page}">
        ${esc(i.title)} <span class="faint">p${i.page}</span></button>`).join("");
    $$("#outlineBox .oi").forEach(b => b.onclick = () => {
      $("#jumpSrc").value = b.dataset.page; $("#btnJump").click();
    });
  } catch (e) { /* bookmarks are optional */ }
}

/* ── the snipping tool ─────────────────────────────────────────────────────
   Behaves the way people expect from a desktop snipping tool: crosshair,
   drag to draw, live size readout, and — the part that was missing — a box
   you can then resize from any of eight handles or drag bodily to reposition.
   `touch-action: none` on the page is what stops a finger drag from scrolling
   the pane instead of drawing, which made it feel broken on tablets. */
const HANDLES = ["nw", "n", "ne", "e", "se", "s", "sw", "w"];

function pageScale(side, pgEl) {
  const img = pgEl.querySelector("img");
  const ptWidth = S.docs[side].page_sizes?.[0]?.w || 595;
  return (img.clientWidth || pgEl.offsetWidth) / ptWidth;   // px per PDF point
}

function attachSelection(box, side) {
  let mode = null;          // 'draw' | 'move' | handle name
  let pgEl = null, anchor = null, origin = null, el = null;

  const clientToLocal = (ev, target) => {
    const r = target.getBoundingClientRect();
    return { x: ev.clientX - r.left, y: ev.clientY - r.top, w: r.width, h: r.height };
  };

  box.addEventListener("pointerdown", ev => {
    if (ev.button === 2) return;
    const handle = ev.target.closest(".hnd");
    const frame = ev.target.closest(".selbox");
    const pg = ev.target.closest(".pg");
    if (!pg) return;
    pgEl = pg;
    const p = clientToLocal(ev, pg);
    if (handle) {
      mode = handle.dataset.h;
      origin = { ...S.sel[side] };
    } else if (frame) {
      mode = "move";
      origin = { ...S.sel[side] };
      anchor = p;
    } else {
      mode = "draw";
      anchor = p;
      S.sel[side] = { page: +pg.dataset.page, x0: 0, y0: 0, x1: 0, y1: 0 };
    }
    pg.setPointerCapture(ev.pointerId);
    ev.preventDefault();
  });

  box.addEventListener("pointermove", ev => {
    if (!mode || !pgEl) return;
    const sc = pageScale(side, pgEl);
    const p = clientToLocal(ev, pgEl);
    const clampX = v => Math.max(0, Math.min(p.w, v));
    const clampY = v => Math.max(0, Math.min(p.h, v));
    let px0, py0, px1, py1;
    if (mode === "draw") {
      px0 = Math.min(anchor.x, clampX(p.x)); py0 = Math.min(anchor.y, clampY(p.y));
      px1 = Math.max(anchor.x, clampX(p.x)); py1 = Math.max(anchor.y, clampY(p.y));
    } else if (mode === "move") {
      const dx = p.x - anchor.x, dy = p.y - anchor.y;
      const w = (origin.x1 - origin.x0) * sc, h = (origin.y1 - origin.y0) * sc;
      px0 = Math.max(0, Math.min(p.w - w, origin.x0 * sc + dx));
      py0 = Math.max(0, Math.min(p.h - h, origin.y0 * sc + dy));
      px1 = px0 + w; py1 = py0 + h;
    } else {
      px0 = origin.x0 * sc; py0 = origin.y0 * sc;
      px1 = origin.x1 * sc; py1 = origin.y1 * sc;
      if (mode.includes("w")) px0 = clampX(p.x);
      if (mode.includes("e")) px1 = clampX(p.x);
      if (mode.includes("n")) py0 = clampY(p.y);
      if (mode.includes("s")) py1 = clampY(p.y);
      if (px1 < px0) [px0, px1] = [px1, px0];
      if (py1 < py0) [py0, py1] = [py1, py0];
    }
    S.sel[side] = { page: +pgEl.dataset.page,
                    x0: px0 / sc, y0: py0 / sc, x1: px1 / sc, y1: py1 / sc };
    drawBox(side, S.sel[side], mode === "draw");
  });

  const finish = ev => {
    if (!mode) return;
    const drawing = mode === "draw";
    mode = null;
    const sel = S.sel[side];
    if (!sel) return;
    const sc = pageScale(side, pgEl);
    if (drawing && ((sel.x1 - sel.x0) * sc < 14 || (sel.y1 - sel.y0) * sc < 14)) {
      S.sel[side] = null;                 // a tap, not a drag
      drawBox(side, null);
    } else {
      drawBox(side, sel, false);
      markExcluded(side, sel.page);
    }
    refreshSelInfo();
  };
  box.addEventListener("pointerup", finish);
  box.addEventListener("pointercancel", finish);
}

/* Draw (or clear) the selection frame, with resize handles once the drag ends. */
function drawBox(side, sel, live) {
  $$(`.pg[data-side="${side}"] .selbox`).forEach(b => b.remove());
  if (!sel) return;
  const pg = $$(`.pg[data-side="${side}"]`).find(x => +x.dataset.page === sel.page);
  if (!pg) return;
  const sc = pageScale(side, pg);
  const b = document.createElement("div");
  b.className = "selbox" + (live ? " live" : "");
  const w = (sel.x1 - sel.x0) * sc, h = (sel.y1 - sel.y0) * sc;
  Object.assign(b.style, { left: sel.x0 * sc + "px", top: sel.y0 * sc + "px",
                           width: w + "px", height: h + "px" });
  b.innerHTML = `<span class="dim">${Math.round(w)} × ${Math.round(h)}</span>` +
    (live ? "" : HANDLES.map(h2 => `<i class="hnd h-${h2}" data-h="${h2}"></i>`).join(""));
  pg.appendChild(b);
}
function refreshSelInfo() {
  const s = S.sel.src, t = S.sel.tgt;
  const part = (x, side) => x
    ? `${S.docs[side].language} p${x.page} ✓`
    : `${S.docs[side]?.language || side} — not selected`;
  $("#selInfo").innerHTML = `${esc(part(s, "src"))}<br>${esc(part(t, "tgt"))}`;
  $("#btnSave").disabled = !(s && t);
  updateWarn();
}
$("#btnClear").onclick = () => {
  S.sel = { src: null, tgt: null };
  $$(".selbox").forEach(b => b.remove());
  refreshSelInfo();
};
$("#btnSave").onclick = savePair;

async function savePair() {
  if (!S.project || !S.sel.src || !S.sel.tgt) {
    toast("Select a region on both pages first", true); return; }
  $("#btnSave").disabled = true;
  try {
    const r = await api("/api/pairs", { method: "POST", body: JSON.stringify({
      project_id: S.project.id, src: S.sel.src, tgt: S.sel.tgt,
      label: $("#pairLabel").value.trim() }) });
    if (S.chosen.size) {
      try {
        await api(`/api/pairs/${r.pair_id}/labels`, { method: "PUT",
          body: JSON.stringify({ label_ids: [...S.chosen] }) });
      } catch (e) { /* the pair is saved; a failed label is not worth losing it */ }
    }
    toast(r.excluded
      ? `Saved pair ${r.seq} — marked excluded (geometry)`
      : `Saved pair ${r.seq}`);
    $("#pairLabel").value = "";
    S.chosen.clear(); drawLabels();
    $("#btnClear").click();
    await refreshCount();
  } catch (e) { toast(e.message, true); $("#btnSave").disabled = false; }
}
async function refreshCount() {
  if (!S.project) return;
  const p = await api(`/api/projects/${S.project.id}/pairs`);
  S.pairs = p;
  const kept = p.filter(x => !x.excluded).length;
  $("#pairCount").textContent =
    `${p.length} pair${p.length === 1 ? "" : "s"} saved` +
    (p.length - kept ? ` · ${p.length - kept} excluded` : "");
}

/* ── categories, the doccano way: a named set with one-key shortcuts ────── */
async function loadLabels() {
  if (!S.project) return;
  S.labels = await api(`/api/projects/${S.project.id}/labels`);
  drawLabels();
}
function drawLabels() {
  $("#labelChips").innerHTML = S.labels.map(l =>
    `<button class="lchip ${S.chosen.has(l.id) ? "on" : ""}" data-id="${l.id}"
       style="--c:${esc(l.color)}">
       ${l.shortcut ? `<kbd>${esc(l.shortcut)}</kbd>` : ""}${esc(l.name)}</button>`).join("");
  $$("#labelChips .lchip").forEach(b => b.onclick = () => toggleLabel(+b.dataset.id));
}
function toggleLabel(id) {
  S.chosen.has(id) ? S.chosen.delete(id) : S.chosen.add(id);
  drawLabels();
}

/* ── saved pairs ───────────────────────────────────────────────────────── */
async function loadPairs() {
  const projects = await api("/api/projects");
  if (!projects.length) {
    $("#pairGrid").innerHTML = `<div class="card">Nothing clipped yet. Open a textbook on the Clip tab.</div>`;
    return;
  }
  if (!$("#pairProject").options.length || $("#pairProject").dataset.n != projects.length) {
    fill($("#pairProject"), projects.map(p =>
      ({ value: p.id, label: `${p.name} — ${p.n_pairs} pairs` })), "");
    $("#pairProject").dataset.n = projects.length;
    if (S.project) $("#pairProject").value = S.project.id;
    $("#pairProject").onchange = loadPairs;
    $("#showExcluded").onchange = loadPairs;
  }
  const pid = +$("#pairProject").value || projects[0].id;
  const pairs = await api(`/api/projects/${pid}/pairs`);
  try {
    const pr = await api(`/api/projects/${pid}/progress`);
    $("#progressCard").innerHTML = `
      <div class="row" style="gap:26px;flex-wrap:wrap">
        <div><b style="font-size:24px">${pr.pairs}</b><div class="sm faint">chunks clipped</div></div>
        <div><b style="font-size:24px">${pr.included}</b><div class="sm faint">included</div></div>
        <div><b style="font-size:24px">${pr.excluded}</b><div class="sm faint">excluded</div></div>
        <div><b style="font-size:24px">${pr.pages_covered}</b><div class="sm faint">of ${pr.source_pages} pages touched (${pr.coverage_pct}%)</div></div>
      </div>
      ${pr.by_label.some(l => l.n) ? `<div class="row" style="gap:8px;flex-wrap:wrap;margin-top:12px">` +
        pr.by_label.filter(l => l.n).map(l =>
          `<span class="tag" style="background:${esc(l.color)}22;color:${esc(l.color)}">${esc(l.name)} ${l.n}</span>`).join("") +
        `</div>` : ""}
      ${pr.by_annotator.length ? `<div class="sm mut" style="margin-top:10px">by annotator: ` +
        pr.by_annotator.map(a => `${esc(a.who)} ${a.n}`).join(" · ") + `</div>` : ""}`;
  } catch (e) { $("#progressCard").innerHTML = ""; }
  const showX = $("#showExcluded").checked;
  const list = pairs.filter(p => showX || !p.excluded);
  $("#pairsStat").textContent = `${list.length} shown of ${pairs.length}`;
  $("#pairGrid").innerHTML = list.map(p => {
    const s = p.clips.src || {}, t = p.clips.tgt || {};
    return `<div class="pcard" data-id="${p.id}">
      <div class="h"><b>Pair ${p.seq}</b>
        ${p.label ? `<span class="sm mut">${esc(p.label)}</span>` : ""}
        ${(p.labels || []).map(l =>
            `<span class="tag" style="background:${esc(l.color)}22;color:${esc(l.color)}">${esc(l.name)}</span>`).join("")}
        ${p.excluded ? `<span class="tag excl">excluded</span>` : ""}
        <span class="sp"></span><span class="sm faint">p${s.page ?? "?"} / p${t.page ?? "?"}</span></div>
      <div class="imgs">
        <img loading="lazy" src="${BASE}/api/clip/${s.id}.png" alt="source clipping">
        <img loading="lazy" src="${BASE}/api/clip/${t.id}.png" alt="target clipping">
      </div>
      <div class="ft"><span class="sm faint">${esc(p.annotator || "—")} · ${esc(fmtTime(p.created_at))}</span>
        <span class="sp"></span>
        <button class="btn sm" data-toggle="${p.id}">${p.excluded ? "Include" : "Exclude"}</button>
        <button class="btn sm" data-del="${p.id}">Delete</button></div>
    </div>`;
  }).join("") || `<div class="card">No pairs match this filter.</div>`;
  $$("#pairGrid [data-del]").forEach(b => b.onclick = async () => {
    if (!confirm("Delete this pair and its two clippings?")) return;
    try { await api(`/api/pairs/${b.dataset.del}`, { method: "DELETE" });
          toast("Pair deleted"); loadPairs(); } catch (e) { toast(e.message, true); }
  });
  $$("#pairGrid [data-toggle]").forEach(b => b.onclick = async () => {
    const card = b.closest(".pcard");
    const wasExcluded = card.querySelector(".tag.excl") !== null;
    try {
      await api(`/api/pairs/${b.dataset.toggle}`, { method: "PATCH",
        body: JSON.stringify({ excluded: !wasExcluded }) });
      loadPairs();
    } catch (e) { toast(e.message, true); }
  });
}

/* ── export ────────────────────────────────────────────────────────────── */
async function loadExport() {
  const projects = await api("/api/projects");
  $("#exportCard").innerHTML = projects.length ? `
    <div class="row" style="flex-wrap:wrap">
      <select id="expProject">${projects.map(p =>
        `<option value="${p.id}">${esc(p.name)} — ${p.n_pairs} pairs</option>`).join("")}</select>
      <label class="row2"><input type="checkbox" id="expIncl"> include excluded pairs</label>
      <label class="row2">formats
        <select id="expFmt">
          <option value="png,jpg,pdf">PNG + JPG + PDF</option>
          <option value="png">PNG only</option>
          <option value="jpg">JPG only</option>
          <option value="pdf">PDF only</option>
        </select></label>
      <button class="btn primary" id="btnExport">Download ZIP</button>
    </div>
    <p class="sm mut" style="margin:12px 0 0">The archive is a folder such as
      <code>NCERT_class10_math/</code> holding
      <code>eng_ncert_math_1.png</code> and <code>hin_ncert_math_1.png</code> —
      the same number is the same passage — plus <code>manifest.json</code>,
      <code>pairs.jsonl</code>, <code>pairs.csv</code>,
      <code>parallel.tsv</code> and a readable <code>README.md</code>.</p>`
    : `<div class="sm mut">No projects yet.</div>`;
  const b = $("#btnExport");
  if (b) b.onclick = () => {
    const pid = $("#expProject").value, inc = $("#expIncl").checked;
    const fmt = $("#expFmt") ? $("#expFmt").value : "png,jpg,pdf";
    window.location =
      `${BASE}/api/projects/${pid}/export.zip?include_excluded=${inc}&formats=${fmt}`;
  };
  await loadSources();
  const rows = await api("/api/exports");
  $("#expRows").innerHTML = rows.map(r =>
    `<tr><td>${esc(r.name)}</td><td>${r.n_pairs}</td><td class="sm">${esc(r.formats)}</td>
     <td class="sm faint">${esc(fmtTime(r.created_at))}</td></tr>`).join("")
    || `<tr><td colspan="4" class="sm faint">Nothing exported yet.</td></tr>`;
}

/* ── where the textbooks come from ─────────────────────────────────────── */
async function loadSources() {
  const st = await api("/api/sources");
  $("#srcCard").innerHTML = `
    <div class="sm mut">Reading textbooks from <code>${esc(st.data_dir)}</code> —
      <b>${st.pdfs}</b> PDF${st.pdfs === 1 ? "" : "s"} available.</div>
    <table class="list" style="margin-top:10px">
      <thead><tr><th>Source</th><th>Provides</th><th>Status</th></tr></thead>
      <tbody>${st.sources.map(s => `<tr>
        <td>${esc(s.name)}${s.file ? `<div class="sm faint">${esc(s.file)}</div>` : ""}</td>
        <td class="sm">${esc(s.provides || "")}</td>
        <td class="sm">${s.present_locally
            ? `<span class="tag">in the data folder</span>`
            : s.fetchable ? `<span class="tag excl">can be downloaded</span>`
                          : `<span class="sm faint">add it manually</span>`}</td>
      </tr>`).join("")}</tbody></table>
    <div class="row" style="margin-top:12px">
      <button class="btn" id="btnUnpack">Unpack what is here</button>
      <button class="btn" id="btnFetch">Unpack and download what is missing</button>
    </div>
    <div id="srcLog" class="sm mut" style="margin-top:10px"></div>`;
  const run = async (download) => {
    $("#srcLog").textContent = download
      ? "Working — downloading can take a while on a slow link…" : "Working…";
    try {
      const r = await api(`/api/sources/acquire?download=${download}`, { method: "POST" });
      $("#srcLog").innerHTML = `Finished: ${r.pdfs} PDFs available, ` +
        `${r.documents} indexed.<br><span class="faint">` +
        esc((r.steps || []).slice(-6).join(" · ")) + `</span>`;
      await loadLibrary();
      toast(`${r.pdfs} textbooks available`);
    } catch (e) { $("#srcLog").textContent = "Failed: " + e.message; }
  };
  $("#btnUnpack").onclick = () => run(false);
  $("#btnFetch").onclick = () => run(true);
}

/* ── documentation ─────────────────────────────────────────────────────── */
let _docs = null;
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

/* ── keyboard ──────────────────────────────────────────────────────────── */
document.addEventListener("keydown", e => {
  if (e.key === "Escape") { $("#shade").classList.remove("on"); $("#btnClear").click(); return; }
  const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName || "");
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
    e.preventDefault(); savePair(); return; }
  if (typing || e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.key === "?") { $("#shade").classList.add("on"); return; }
  if (e.key.toLowerCase() === "l") { $("#lockScroll").checked = !$("#lockScroll").checked; return; }
  const byKey = S.labels.find(l => l.shortcut && l.shortcut === e.key);
  if (byKey) { toggleLabel(byKey.id); return; }
  if (e.key === "+" || e.key === "=") { $$('[data-zoom="src"][data-d="1"]')[0]?.click(); return; }
  if (e.key === "-") { $$('[data-zoom="src"][data-d="-1"]')[0]?.click(); return; }
});

let _fitTimer;
window.addEventListener("resize", () => {
  clearTimeout(_fitTimer);
  _fitTimer = setTimeout(() => {
    for (const side of ["src", "tgt"]) {
      if (!S.docs[side]) continue;
      const keep = S.sel[side];
      renderPane(side);
      if (keep) drawBox(side, keep);
    }
  }, 200);
});

/* ── split handle ──────────────────────────────────────────────────────── */
$("#split").addEventListener("pointerdown", ev => {
  ev.preventDefault(); $("#split").setPointerCapture(ev.pointerId);
  const move = e => {
    const wrap = $("#panes").getBoundingClientRect();
    const pct = Math.min(80, Math.max(20, ((e.clientX - wrap.left) / wrap.width) * 100));
    $("#paneSrc").style.flex = `0 0 ${pct}%`;
    $("#paneTgt").style.flex = `0 0 ${100 - pct}%`;
  };
  const up = () => { window.removeEventListener("pointermove", move);
                     window.removeEventListener("pointerup", up); };
  window.addEventListener("pointermove", move); window.addEventListener("pointerup", up);
});

/* ── boot ──────────────────────────────────────────────────────────────── */
(async function boot() {
  try {
    const h = await api("/api/health");
    if (!h.pdf_ready) toast("PyMuPDF is not installed on the server", true);
    await loadLibrary();
    refreshSelInfo();
  } catch (e) { toast("Backend unreachable: " + e.message, true); }
})();
