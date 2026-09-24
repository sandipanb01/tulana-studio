/* Setu — the annotation workspace.
 *
 * Built the way Tulana Studio's Blocks tab is built, for the same reason it
 * works: one file, no framework, no build step, talking to a JSON API. If this
 * has to be opened in five years on a machine with no network, it still runs.
 *
 * THE ONE RULE
 * ------------
 * A block's position travels as a FRACTION of the page — never as pixels.
 * The parser measured its boxes against a raster of some size; the page is
 * drawn here at whatever size fits the pane; a crop is cut at 300 dpi. None of
 * those three knows about the others, and none has to, because fx0..fy1 is
 * independent of all of them. Every overlay measurement below multiplies a
 * fraction by the *measured* size of the image that is actually on screen.
 *
 * PAGES COUNT FROM ZERO
 * ---------------------
 * setu_segment.page holds what the layout JSON said, and PyMuPDF indexes the
 * same way, so the crop renderer is correct. People count from one. Every
 * number shown goes through `shown()`; every number typed comes back through
 * `stored()`. Nowhere else is a page number adjusted.
 */
"use strict";

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const BASE = location.pathname.replace(/\/work\/?$/, "") || "";
const API = `${BASE}/api/setu`;

const shown = p => (p | 0) + 1;
const stored = p => Math.max(0, (parseInt(p, 10) || 1) - 1);
const clamp = (v, lo, hi) => (hi < lo ? lo : Math.max(lo, Math.min(hi, v)));

/* Every call goes through here: the annotator's name rides along as a header
 * so the server can attribute the work, and the server's own `detail` becomes
 * the message a person reads instead of a status code. */
async function api(path, opts = {}) {
  opts.headers = Object.assign({
    "Content-Type": "application/json",
    "X-Annotator": localStorage.getItem("setu_who") || "",
  }, opts.headers || {});
  const r = await fetch(API + path, opts);
  const text = await r.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch { /* not json */ }
  if (!r.ok) {
    const d = body && (body.detail || body.message);
    const err = new Error(typeof d === "string" ? d : (d && d.message) || `HTTP ${r.status}`);
    err.status = r.status; err.body = body;
    throw err;
  }
  return body;
}

let toastTimer = null;
function toast(message, bad = false) {
  const t = $("#toast");
  t.textContent = message; t.className = "toast" + (bad ? " bad" : ""); t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.hidden = true; }, bad ? 7000 : 3200);
}

/* ── state ─────────────────────────────────────────────────────────────
 *
 * One object. Two mirrored sides. Nothing else holds annotation state, which
 * is what lets the whole interface be redrawn from it at any moment.
 */
const W = {
  pid: "", link: null, colors: {}, kinds: [],
  tool: "click", mode: "read", view: "text", lock: false,
  side: {
    src: newSide("src"),
    tgt: newSide("tgt"),
  },
};
function newSide(which) {
  return {
    which, book: "", title: "", language: "", page: 0, lo: 0, hi: 0,
    blocks: [], sel: new Set(), last: null, zoom: 1,
    imageAvailable: false, imageMessage: "", aspect: 1.414,
    chapters: [], crop: null, cropUrl: "",
  };
}
const S = s => W.side[s];
const other = s => (s === "src" ? "tgt" : "src");

/* ── the cascade ───────────────────────────────────────────────────────── */

function fill(sel, rows, valueKey, labelFn, keep) {
  const el = $(sel);
  const before = keep ? el.value : "";
  el.innerHTML = rows.map(r => {
    const v = typeof r === "string" ? r : r[valueKey];
    return `<option value="${esc(v)}">${esc(labelFn(r))}</option>`;
  }).join("");
  el.disabled = rows.length === 0;
  if (before && rows.some(r => (typeof r === "string" ? r : r[valueKey]) === before)) el.value = before;
  return el.value;
}
const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g,
  c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

async function loadBoards() {
  const { boards } = await api("/boards");
  const pairable = boards.filter(b => (b.n_languages || 0) >= 2);
  const rest = boards.filter(b => (b.n_languages || 0) < 2);
  // The value is the board CODE — every other endpoint in the cascade
  // filters on `setu_book.board`, which holds the code, not the display name.
  // Sending the name back returns an empty list and the interface goes blank
  // with nothing to explain why.
  const opt = b => `<option value="${esc(b.code)}">${esc(b.name)}</option>`;
  const el = $("#board");
  el.innerHTML = pairable.map(opt).join("") +
    (rest.length ? `<optgroup label="only one language — cannot be paired">` +
      rest.map(opt).join("") + `</optgroup>` : "");
  el.disabled = false;
  if (pairable.length) el.value = pairable[0].code;
  await onBoard();
}

async function onBoard() {
  const board = $("#board").value;
  const { classes } = await api(`/classes?board=${encodeURIComponent(board)}`);
  // Land on the class with the most books rather than the lowest number: an
  // empty first screen is the commonest way to lose somebody in the first
  // thirty seconds.
  const best = classes.slice().sort((a, b) => (b.n_books || 0) - (a.n_books || 0))[0];
  fill("#klass", classes, "value", c => `Class ${c.value}` + (c.n_books ? ` · ${c.n_books} books` : ""));
  if (best) $("#klass").value = String(best.value);
  await onClass();
}

async function onClass() {
  const board = $("#board").value, cls = $("#klass").value;
  const { subjects } = await api(`/subjects?board=${encodeURIComponent(board)}&class=${encodeURIComponent(cls)}`);
  fill("#subject", subjects, "value", s => s.value + (s.n_languages ? ` · ${s.n_languages} languages` : ""));
  await onSubject();
}

async function onSubject() {
  const q = cascadeQuery();
  const { languages } = await api(`/languages?${q}`);
  fill("#srcLang", languages, "value", l => l.value + (l.n_books ? ` · ${l.n_books}` : ""));
  const eng = languages.find(l => l.value === "English");
  if (eng) $("#srcLang").value = "English";
  await onSrcLang();
}

async function onSrcLang() {
  const q = cascadeQuery(), src = $("#srcLang").value;
  const { books } = await api(`/books?${q}&language=${encodeURIComponent(src)}`);
  fill("#srcBook", books, "book_key", b => bookLabel(b));
  const { languages } = await api(`/languages?${q}`);
  // The language being read on the left is never offered on the right: the
  // two sides must be different editions or there is nothing to compare.
  const rest = languages.filter(l => l.value !== src);
  fill("#tgtLang", rest, "value", l => l.value + (l.n_books ? ` · ${l.n_books}` : ""));
  await onTgtLang();
}

async function onTgtLang() {
  const q = cascadeQuery(), tgt = $("#tgtLang").value;
  if (!tgt) { $("#tgtBook").innerHTML = ""; $("#tgtBook").disabled = true; return; }
  const { books } = await api(`/books?${q}&language=${encodeURIComponent(tgt)}`);
  fill("#tgtBook", books, "book_key", b => bookLabel(b));
}

const cascadeQuery = () =>
  `board=${encodeURIComponent($("#board").value)}&class=${encodeURIComponent($("#klass").value)}` +
  `&subject=${encodeURIComponent($("#subject").value)}`;
const bookLabel = b =>
  `${b.volume || b.book} — ${b.num_pages}pp · ${(b.n_segments || 0).toLocaleString()} pieces of text`;

/* ── opening two books ─────────────────────────────────────────────────── */

async function openBooks() {
  const src = $("#srcBook").value, tgt = $("#tgtBook").value;
  if (!src || !tgt) return toast("Choose a book on each side first.", true);
  if (src === tgt) return toast("The two sides must be different books.", true);

  $("#open").disabled = true;
  $("#open").textContent = "Opening…";
  try {
    const proj = await api("/projects", {
      method: "POST",
      body: JSON.stringify({ src_book: src, tgt_book: tgt, annotator: who() }),
    });
    W.pid = proj.pid;
    const outline = await api(`/projects/${W.pid}/outline`);
    for (const s of ["src", "tgt"]) {
      const o = outline[s], st = S(s);
      Object.assign(st, {
        book: o.book_key, title: o.title, language: o.language,
        lo: o.first_page, hi: o.last_page, chapters: o.chapters,
        page: o.first_page, sel: new Set(), last: null, crop: null, cropUrl: "",
      });
      fillChapters(s);
    }
    const { link } = await api(`/projects/${W.pid}/link`);
    W.link = link && Object.keys(link).length ? link : null;
    if (W.link) {
      S("src").page = clamp(W.link.src_page | 0, S("src").lo, S("src").hi);
      S("tgt").page = clamp(W.link.tgt_page | 0, S("tgt").lo, S("tgt").hi);
      W.lock = true;
      $("#lockPages").checked = true;
    }
    ["#gChapter", "#gPage", "#gView", "#gTool", "#gMode", "#gFilter"].forEach(id => { $(id).hidden = false; });
    $("#unlink").hidden = !W.link;
    await Promise.all([openPage("src"), openPage("tgt")]);
    refreshSelection();
    loadProgress();
  } catch (e) {
    toast(e.message, true);
  } finally {
    $("#open").disabled = false;
    $("#open").textContent = "Open side by side";
  }
}

function fillChapters(s) {
  const st = S(s);
  const el = $(s === "src" ? "#srcChapter" : "#tgtChapter");
  el.innerHTML = `<option value="">Whole book</option>` + st.chapters.map(c => {
    const num = (c.chapter_no || "").trim();
    let title = (c.chapter || "").replace(/\s+/g, " ").slice(0, 60);
    // The parser usually leaves the number at the front of the title too, so
    // joining them blindly gives "3 3 Arithmetic Progression".
    let label = (num && title.startsWith(num)) ? title : `${num} ${title}`.trim();
    if (!label) label = "Front matter";
    if (c.display_page) label += `  ·  from page ${c.display_page}`;
    return `<option value="${c.display_page == null ? "" : c.display_page}">${esc(label)}</option>`;
  }).join("");
}

/* ── one page of one book ──────────────────────────────────────────────── */

async function openPage(s) {
  const st = S(s);
  if (!st.book) return;
  const noise = $("#noise").checked ? "&noise=1" : "";
  let data;
  try {
    data = await api(`/pages/${st.book}/${st.page}/blocks?pid=${encodeURIComponent(W.pid)}${noise}`);
  } catch (e) {
    toast(e.message, true);
    return;
  }
  st.blocks = data.blocks;
  st.imageAvailable = data.image_available;
  st.imageMessage = data.image_message;
  st.lo = data.first_page; st.hi = data.last_page;
  st.title = data.book.title || data.book.book;
  st.language = data.book.language || "";

  // The selection deliberately survives a page turn: a passage that fits one
  // English page often runs onto the next in the other language, and clearing
  // at the page boundary would make such a pair impossible to hold.
  assignColours();
  renderSide(s);
  syncPageBoxes();
  renderOffset();
}

function assignColours() {
  const seen = new Map();
  for (const s of ["src", "tgt"]) for (const b of S(s).blocks)
    seen.set(b.kind || "other", (seen.get(b.kind || "other") || 0) + 1);
  const PALETTE = ["#2563eb", "#0f766e", "#7c3aed", "#b42318", "#0369a1",
    "#4d7c0f", "#a21caf", "#155e75", "#854d0e", "#9f1239",
    "#1e40af", "#3f6212", "#6b21a8", "#0e7490"];
  const order = [...seen.entries()].sort((a, b) => b[1] - a[1]).map(e => e[0]);
  W.kinds = order;
  order.forEach((k, i) => { if (!W.colors[k]) W.colors[k] = PALETTE[i % PALETTE.length]; });
  const f = $("#kindFilter"), keep = f.value;
  f.innerHTML = `<option value="">All kinds of block</option>` +
    order.map(k => `<option value="${esc(k)}">${esc(kindName(k))} · ${seen.get(k)}</option>`).join("");
  if (keep) f.value = keep;
  $("#legend").innerHTML = order.slice(0, 12).map(k =>
    `<span class="lgd" style="background:${W.colors[k]}">${esc(kindName(k))}</span>`).join("");
}
const kindName = k => (k || "other").replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());

function renderSide(s) {
  const st = S(s);
  const host = $(s === "src" ? "#hostSrc" : "#hostTgt");
  const box = $(s === "src" ? "#scrollSrc" : "#scrollTgt");
  const fitW = Math.max(220, (box.clientWidth || 560) - 28);
  const w = Math.round(fitW * st.zoom);
  $(s === "src" ? "#zoomSrc" : "#zoomTgt").textContent = Math.round(st.zoom * 100) + "%";
  host.style.width = w + "px";

  $(s === "src" ? "#titleSrc" : "#titleTgt").textContent =
    `${st.language || (s === "src" ? "Left" : "Right")} — ${st.title || ""}`;
  $(s === "src" ? "#whereSrc" : "#whereTgt").textContent =
    `page ${shown(st.page)} of ${shown(st.hi)} · ${st.blocks.length} blocks` +
    (st.imageAvailable ? "" : " · no scan on disk");

  // Only ask for the image when the server has already said it can render it.
  // Letting an <img> discover a missing PDF by 404 works, but logs a red error
  // that reads like a fault to whoever opens the developer tools next.
  // Text first. The corpus this serves is a translation-checking corpus —
  // what an annotator compares is the words, not the paper — and the scans are
  // 1.5 GB of Git LFS that usually are not there. The page with its block
  // outlines is a second view for when provenance is the question.
  if (st.imageAvailable && W.view === "page") {
    host.classList.remove("textonly");
    host.innerHTML = `<img width="${w}" alt="" src="${API}/pages/${st.book}/${st.page}/image.png">`;
    const img = host.querySelector("img");
    img.onload = () => { drawBlocks(s); drawCrop(s); };
    drawBlocks(s);
    drawCrop(s);
  } else {
    renderText(s);
  }
}

/* No scan on disk — which on a Git LFS checkout is the ordinary case, and on
 * an exhausted LFS allowance is the permanent one.
 *
 * The first version of this drew a dashed rectangle of the right proportions
 * with the blocks outlined on it. That is honest and it is almost useless: a
 * title page carries two blocks, so the annotator faces a large empty box with
 * two small outlines in it and nothing to read. The text is what they are here
 * to check, and the text does not need the scan.
 *
 * So the same blocks are laid out as a readable column instead, in reading
 * order, each one clickable exactly as its outline would have been — same
 * dataset attributes, same handler, same selection. Only the picture is gone.
 */
function renderText(s) {
  const st = S(s);
  const host = $(s === "src" ? "#hostSrc" : "#hostTgt");
  host.classList.add("textonly");
  host.style.width = "100%";

  const only = $("#kindFilter").value, dim = $("#dim").checked;
  const rows = st.blocks.map((b, i) => {
    if (only && b.kind !== only && !dim) return "";
    const on = st.sel.has(b.sid);
    const state = !b.rid ? "lonely" : (b.status && b.status !== "pending" ? "done" : "pending");
    const faded = (only && b.kind !== only) || (dim && !on);
    const text = (b.text || "").trim();
    const editable = W.mode === "edit" && b.rid;
    return `<div class="trow blk ${state}${on ? " on" : ""}${faded ? " dim" : ""}"` +
      ` data-sid="${esc(b.sid)}" data-i="${i}" data-rid="${esc(b.rid || "")}"` +
      ` data-rev="${b.rev | 0}" data-side="${s}"` +
      ` style="--c:${W.colors[b.kind || "other"] || "#666"}">` +
      `<div class="tmeta"><span class="tkind">${esc(kindName(b.kind))}</span>` +
      `<span>page ${b.display_page}</span>` +
      (b.rid ? `<span>pair #${b.row_seq}</span>` : `<span class="tlonely">no counterpart</span>`) +
      (b.edited ? `<span class="tedit">corrected</span>` : "") +
      (b.rid && b.status && b.status !== "pending"
        ? `<span class="tdone">${esc(statusLabel(b.status))}</span>` : "") +
      `</div><div class="tbody"${editable ? ' contenteditable="true" spellcheck="false"' : ""}>` +
      `${text ? esc(text) : (editable ? "" : "<i>the parser found no text here</i>")}</div>` +
      `</div>`;
  }).join("");

  host.innerHTML =
    `<div class="nosc">No scan of this book on this machine — showing the text. ` +
    `Everything except the page picture and the crop tool works as usual.` +
    `<br><span class="tiny">${esc(st.imageMessage || "")}</span></div>` +
    (rows || `<div class="nosc">The parser found nothing on page ${shown(st.page)}. ` +
      `Try the next page.</div>`);
}

/* The overlay. Everything here is a fraction times the MEASURED size of what
 * is actually on screen, which is why it is correct at any zoom and whatever
 * DPI the page happened to be rendered at. */
function drawBlocks(s) {
  const st = S(s);
  const host = $(s === "src" ? "#hostSrc" : "#hostTgt");
  if (host.classList.contains("textonly")) return;   // the column draws itself
  const surface = host.querySelector("img");
  if (!surface) return;
  const W_ = surface.clientWidth || surface.offsetWidth;
  const H_ = surface.clientHeight || surface.offsetHeight;
  if (!W_ || !H_) return;

  host.querySelectorAll(".blk").forEach(e => e.remove());
  const only = $("#kindFilter").value, dim = $("#dim").checked, order = $("#order").checked;

  // Draw the largest blocks first so the smaller ones sit on top. A page
  // header often overlaps the heading beneath it, and in document order the
  // larger box is painted last and swallows every click meant for what is
  // inside it.
  const area = b => Math.max(0, b.fx1 - b.fx0) * Math.max(0, b.fy1 - b.fy0);
  const painted = st.blocks.map((b, i) => ({ b, i })).sort((p, q) => area(q.b) - area(p.b));

  const frag = document.createDocumentFragment();
  for (const { b, i } of painted) {
    const hidden = only && b.kind !== only;
    if (hidden && !dim) continue;
    const on = st.sel.has(b.sid);
    const el = document.createElement("div");
    const state = !b.rid ? "lonely" : (b.status && b.status !== "pending" ? "done" : "pending");
    el.className = "blk " + state + (on ? " on" : "") + ((hidden || (dim && !on)) ? " dim" : "");
    el.style.cssText =
      `--c:${W.colors[b.kind || "other"] || "#666"};left:${b.fx0 * W_}px;top:${b.fy0 * H_}px;` +
      `width:${(b.fx1 - b.fx0) * W_}px;height:${(b.fy1 - b.fy0) * H_}px`;
    el.dataset.sid = b.sid; el.dataset.i = i;
    el.title = `${kindName(b.kind)} · page ${b.display_page}` +
      (b.rid ? ` · pair #${b.row_seq} · ${b.status || "pending"}` : " · no counterpart found") +
      (b.edited ? " · corrected by hand" : " · as the parser read it");
    el.innerHTML = `<span class="lb">${esc(kindName(b.kind))}</span>` +
      (order ? `<span class="no">${b.seq}</span>` : "");
    frag.appendChild(el);
  }
  host.appendChild(frag);
}

/* Toggling a class beats redrawing. A full redraw replaces every element, so
 * the one under the cursor is destroyed mid-click — and on a page with a
 * hundred blocks it is visibly slow for something that changed one box. */
function markSelected(s) {
  const st = S(s);
  const host = $(s === "src" ? "#hostSrc" : "#hostTgt");
  const dim = $("#dim").checked, only = $("#kindFilter").value;
  host.querySelectorAll(".blk").forEach(el => {
    const b = st.blocks[+el.dataset.i];
    const on = st.sel.has(el.dataset.sid);
    el.classList.toggle("on", on);
    const hidden = only && b && b.kind !== only;
    el.classList.toggle("dim", !!(hidden || (dim && !on)));
  });
}

for (const s of ["src", "tgt"]) {
  const host = $(s === "src" ? "#hostSrc" : "#hostTgt");
  host.addEventListener("click", ev => {
    if (W.tool !== "click") return;
    // Clicking inside a box you are editing places the cursor. Selecting the
    // block as well would fight the caret on every keystroke.
    if (ev.target.closest('[contenteditable="true"]')) return;
    const el = ev.target.closest(".blk");
    if (!el) return;
    const st = S(s), sid = el.dataset.sid, i = +el.dataset.i;
    if (ev.shiftKey && st.last !== null) {
      const [a, b] = [Math.min(st.last, i), Math.max(st.last, i)];
      for (let k = a; k <= b; k++) st.sel.add(st.blocks[k].sid);
    } else if (ev.metaKey || ev.ctrlKey) {
      st.sel.has(sid) ? st.sel.delete(sid) : st.sel.add(sid);
      st.last = i;
    } else {
      // One block at a time is what an annotator almost always means, and it
      // is the only way the pair below can be unambiguous.
      st.sel.clear(); st.sel.add(sid); st.last = i;
    }
    markSelected(s);
    refreshSelection();
  });
}

/* ── the crop tool ─────────────────────────────────────────────────────── */

for (const s of ["src", "tgt"]) {
  const host = $(s === "src" ? "#hostSrc" : "#hostTgt");
  let mode = null, start = null;

  const at = ev => {
    const surface = host.querySelector("img");
    const r = surface.getBoundingClientRect();
    return { x: (ev.clientX - r.left) / r.width, y: (ev.clientY - r.top) / r.height };
  };

  host.addEventListener("pointerdown", ev => {
    if (W.tool !== "crop") return;
    // Nothing to cut from when there is no scan. Say so once rather than
    // letting a drag do nothing and look broken.
    if (!host.querySelector("img")) {
      toast("There is no scan of this page on this machine, so nothing can be "
            + "cut from it. Run: git lfs pull", true);
      return;
    }
    if (ev.target.closest(".cx")) { S(s).crop = null; drawCrop(s); return; }
    mode = ev.target.closest(".grip") ? "resize" : (ev.target.closest(".crop") ? "move" : "draw");
    start = at(ev);
    if (mode === "draw") S(s).crop = { x0: start.x, y0: start.y, x1: start.x, y1: start.y };
    else if (mode === "move") start.base = Object.assign({}, S(s).crop);
    host.setPointerCapture(ev.pointerId);
    ev.preventDefault();
  });

  host.addEventListener("pointermove", ev => {
    if (!mode) return;
    const p = at(ev), c = S(s).crop;
    if (!c) return;
    const lim = v => Math.max(0, Math.min(1, v));
    if (mode === "draw" || mode === "resize") {
      c.x1 = lim(p.x); c.y1 = lim(p.y);
    } else {
      const dx = p.x - start.x, dy = p.y - start.y;
      c.x0 = lim(start.base.x0 + dx); c.y0 = lim(start.base.y0 + dy);
      c.x1 = lim(start.base.x1 + dx); c.y1 = lim(start.base.y1 + dy);
    }
    drawCrop(s);
  });

  host.addEventListener("pointerup", ev => {
    if (!mode) return;
    mode = null;
    host.releasePointerCapture(ev.pointerId);
    const c = S(s).crop;
    if (!c) return;
    const box = norm(c);
    // A tap is not a rectangle.
    if ((box.x1 - box.x0) * (box.y1 - box.y0) < 0.00006) { S(s).crop = null; drawCrop(s); return; }
    S(s).crop = box;
    drawCrop(s);
    cutCrop(s);
  });
}
const norm = c => ({
  x0: Math.min(c.x0, c.x1), y0: Math.min(c.y0, c.y1),
  x1: Math.max(c.x0, c.x1), y1: Math.max(c.y0, c.y1),
});

function drawCrop(s) {
  const host = $(s === "src" ? "#hostSrc" : "#hostTgt");
  host.querySelectorAll(".crop").forEach(e => e.remove());
  const c = S(s).crop;
  if (!c) return;
  const surface = host.querySelector("img");
  if (!surface) return;
  const W_ = surface.clientWidth, H_ = surface.clientHeight;
  const b = norm(c);
  const el = document.createElement("div");
  el.className = "crop";
  el.style.cssText = `left:${b.x0 * W_}px;top:${b.y0 * H_}px;` +
    `width:${(b.x1 - b.x0) * W_}px;height:${(b.y1 - b.y0) * H_}px`;
  el.innerHTML = `<span class="cx" title="Remove">×</span><span class="grip"></span>`;
  host.appendChild(el);
}

function cutCrop(s) {
  const st = S(s), c = st.crop;
  if (!c) return;
  const q = `x0=${c.x0.toFixed(5)}&y0=${c.y0.toFixed(5)}&x1=${c.x1.toFixed(5)}&y1=${c.y1.toFixed(5)}`;
  st.cropUrl = `${API}/pages/${st.book}/${st.page}/crop.png?${q}`;
  renderCrops();
}

function renderCrops() {
  const out = [];
  for (const s of ["src", "tgt"]) {
    const st = S(s);
    if (!st.crop || !st.cropUrl) continue;
    out.push(`<figure><img src="${st.cropUrl}" alt="" ` +
      `onerror="this.replaceWith(Object.assign(document.createElement('div'),` +
      `{className:'tiny muted',textContent:'That region could not be cut — the scan is not on this machine.'}))">` +
      `<figcaption>${esc(st.language || s)} · page ${shown(st.page)}, as printed</figcaption></figure>`);
  }
  $("#crops").innerHTML = out.join("");
}

/* ── the pair under the panes ──────────────────────────────────────────── */

const ANSWERS = [
  ["exact", "Exact"], ["needs_correction", "Needs correction"],
  ["incomplete", "Missing or incomplete"], ["structural_mismatch", "Structural mismatch"],
  ["unclear", "Unclear"], ["not_applicable", "Not applicable"],
];

function selectedBlock(s) {
  const st = S(s);
  if (st.sel.size !== 1) return null;
  const sid = [...st.sel][0];
  return st.blocks.find(b => b.sid === sid) || null;
}

/* The pair currently in view. A block on either side names a row, and that row
 * is what the answer belongs to. */
function currentPair() {
  for (const s of ["src", "tgt"]) {
    const b = selectedBlock(s);
    if (b && b.rid) return { rid: b.rid, from: s, block: b };
  }
  return null;
}

function refreshSelection() {
  const counts = ["src", "tgt"].map(s => S(s).sel.size);
  const pair = currentPair();

  for (const s of ["src", "tgt"]) {
    const st = S(s);
    const el = $(s === "src" ? "#textSrc" : "#textTgt");
    const lbl = $(s === "src" ? "#lblSrc" : "#lblTgt");
    const orig = $(s === "src" ? "#origSrc" : "#origTgt");
    let block = selectedBlock(s);

    // When one side is selected and the other is not, show the counterpart
    // from the pair rather than an empty box — that IS the parallel text.
    if (!block && pair) {
      const mate = S(s).blocks.find(b => b.rid === pair.rid);
      block = mate || null;
    }
    el.dataset.sid = block ? block.sid : "";
    el.dataset.rid = block ? (block.rid || "") : "";
    el.dataset.rev = block ? (block.rev || 0) : "0";
    el.classList.toggle("gap", !block);
    if (!block) {
      el.textContent = pair
        ? "Nothing on this side — the machine found no counterpart here."
        : "";
      lbl.textContent = st.language || (s === "src" ? "Left" : "Right");
      orig.hidden = true;
    } else {
      el.textContent = block.text || "";
      lbl.textContent = `${st.language || s} · page ${block.display_page} · ${kindName(block.kind)}` +
        (block.rid ? ` · pair #${block.row_seq}` : " · no counterpart found") +
        (block.edited ? " · corrected by hand" : " · as the parser read it");
      orig.hidden = !block.edited || W.mode !== "edit";
    }
    el.contentEditable = (W.mode === "edit" && block && block.rid) ? "true" : "false";
  }

  $("#answerRow").hidden = !pair;
  if (pair) {
    $("#answers").innerHTML = ANSWERS.map(([k, label], i) =>
      `<button class="ans${pair.block.status === k ? " on" : ""}" data-status="${k}">` +
      `<kbd>${i + 1}</kbd>${esc(label)}</button>`).join("");
    $("#note").value = pair.block.note || "";
    $("#note").dataset.rid = pair.rid;
  }

  $("#selInfo").textContent = counts[0] + counts[1] === 0
    ? (W.pid ? "Nothing selected — click a block on either page." : "Choose two textbooks and press “Open side by side”.")
    : `selected: ${counts[0]} on the left, ${counts[1]} on the right` +
      (pair ? ` · pair #${pair.block.row_seq}` : " · this block has no counterpart");
}

$("#answers").addEventListener("click", ev => {
  const b = ev.target.closest(".ans");
  if (b) setAnswer(b.dataset.status);
});

async function setAnswer(status) {
  const pair = currentPair();
  if (!pair) return;
  try {
    await api(`/rows/${pair.rid}/status`, {
      method: "POST",
      body: JSON.stringify({ status, note: $("#note").value, annotator: who() }),
    });
    for (const s of ["src", "tgt"])
      for (const b of S(s).blocks) if (b.rid === pair.rid) b.status = status;
    saveState("Saved.");
    refreshSelection();
    ["src", "tgt"].forEach(drawBlocksKeepingScroll);
    loadProgress();
  } catch (e) { saveState(e.message, true); }
}
const drawBlocksKeepingScroll = s => drawBlocks(s);

/* ── editing ───────────────────────────────────────────────────────────
 *
 * The box on screen is a VIEW. The record is setu_text, and a save carries the
 * revision the box was showing, so it cannot land on top of somebody else's
 * work. POTATO's text_edit widget lost edits by treating the editor as the
 * record; this keeps the two apart.
 */
let saveTimer = null;
for (const s of ["src", "tgt"]) {
  const el = $(s === "src" ? "#textSrc" : "#textTgt");
  el.addEventListener("input", () => {
    saveState("…");
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => saveText(s), 1400);
  });
  el.addEventListener("blur", () => { clearTimeout(saveTimer); saveText(s); });
}

/* An edit made in the column itself — the doccano-shaped gesture: the text you
 * are reading is the text you correct, in the place you are reading it.
 *
 * The rules are the same as the panel editor's, because they are the same
 * rules: the box is a view, setu_text is the record, and the save carries the
 * revision the box was showing so it cannot land on somebody else's work.
 */
for (const side of ["src", "tgt"]) {
  const host = $(side === "src" ? "#hostSrc" : "#hostTgt");
  host.addEventListener("blur", async ev => {
    const body = ev.target.closest && ev.target.closest(".tbody[contenteditable=true]");
    if (!body) return;
    const row = body.closest(".trow");
    const rid = row && row.dataset.rid;
    if (!rid) return;
    const block = S(side).blocks.find(b => b.sid === row.dataset.sid);
    if (!block) return;
    const text = body.innerText.replace(/\u00a0/g, " ");
    if (text === (block.text || "")) return;
    try {
      const out = await api(`/rows/${rid}`, {
        method: "PATCH",
        body: JSON.stringify({ [side]: text, [`${side}_rev`]: block.rev | 0,
                               annotator: who(), reason: "edit" }),
      });
      const got = out && out[side];
      block.text = text; block.edited = true;
      if (got && got.rev != null) { block.rev = got.rev; row.dataset.rev = got.rev; }
      row.classList.add("saved");
      setTimeout(() => row.classList.remove("saved"), 1400);
      const meta = row.querySelector(".tmeta");
      if (meta && !meta.querySelector(".tedit")) {
        const tag = document.createElement("span");
        tag.className = "tedit"; tag.textContent = "corrected";
        meta.appendChild(tag);
      }
      saveState("Saved.");
      if (S(side).sel.has(block.sid)) refreshSelection();
    } catch (e) {
      saveState(e.status === 409
        ? "Somebody else changed this while you were typing — nothing of yours was lost, it is in the history."
        : e.message, true);
    }
  }, true);   // capture: blur does not bubble
}

async function saveText(s) {
  if (W.mode !== "edit") return;
  const el = $(s === "src" ? "#textSrc" : "#textTgt");
  const rid = el.dataset.rid, sid = el.dataset.sid;
  if (!rid) return;
  const block = S(s).blocks.find(b => b.sid === sid);
  if (!block) return;
  const text = el.innerText.replace(/ /g, " ");
  if (text === (block.text || "")) return;
  try {
    const out = await api(`/rows/${rid}`, {
      method: "PATCH",
      body: JSON.stringify({
        [s]: text, [`${s}_rev`]: block.rev | 0,
        annotator: who(), reason: "edit",
      }),
    });
    const side = out && out[s];
    block.text = text;
    block.edited = true;
    if (side && side.rev != null) { block.rev = side.rev; el.dataset.rev = side.rev; }
    saveState("Saved.");
    drawBlocks(s);
  } catch (e) {
    if (e.status === 409) {
      saveState("Somebody else changed this while you were typing — nothing of yours was thrown away, it is in the history. Turn the page and back to see theirs.", true);
    } else {
      saveState(e.message, true);
    }
  }
}

for (const s of ["src", "tgt"]) {
  $(s === "src" ? "#origSrc" : "#origTgt").addEventListener("click", async () => {
    const el = $(s === "src" ? "#textSrc" : "#textTgt");
    const rid = el.dataset.rid;
    if (!rid) return;
    try {
      await api(`/rows/${rid}/restore`, {
        method: "POST", body: JSON.stringify({ side: s, rev: 0, annotator: who() }),
      });
      await openPage(s);
      refreshSelection();
      saveState("Put back what the parser read.");
    } catch (e) { saveState(e.message, true); }
  });
}

function saveState(message, bad = false) {
  const el = $("#saveState");
  el.textContent = message;
  el.style.color = bad ? "var(--warn)" : "";
  if (bad) toast(message, true);
}

/* ── moving about ──────────────────────────────────────────────────────── */

function syncPageBoxes() {
  $("#srcPage").value = shown(S("src").page);
  $("#tgtPage").value = shown(S("tgt").page);
  $("#srcPage").min = shown(S("src").lo); $("#srcPage").max = shown(S("src").hi);
  $("#tgtPage").min = shown(S("tgt").lo); $("#tgtPage").max = shown(S("tgt").hi);
}

function renderOffset() {
  const a = S("src"), b = S("tgt");
  const live = a.page - b.page;
  let text;
  if (W.link) {
    const held = W.link.offset | 0;
    const word = held > 0 ? "ahead of" : "behind";
    text = held === 0
      ? "Linked — the two editions are level."
      : `Linked — the English edition runs ${Math.abs(held)} page${Math.abs(held) === 1 ? "" : "s"} ${word} the other.`;
    if (live !== held) text += ` You have moved them ${live > held ? "+" : ""}${live - held} further apart.`;
  } else if (live) {
    text = `English page ${shown(a.page)} is beside page ${shown(b.page)}. If those two really say the same thing, press the button below.`;
  } else {
    text = `Both on page ${shown(a.page)}.`;
  }
  $("#offset").textContent = text;
}

async function turn(s, delta) {
  const st = S(s);
  const before = st.page;
  st.page = clamp(st.page + delta, st.lo, st.hi);
  if (st.page === before) { toast(delta < 0 ? "Already the first page." : "Already the last page."); return; }
  const jobs = [openPage(s)];
  if (W.lock) {
    const o = S(other(s));
    o.page = clamp(o.page + delta, o.lo, o.hi);
    jobs.push(openPage(other(s)));
  }
  await Promise.all(jobs);
  refreshSelection();
}

async function goTo(s, displayPage) {
  const st = S(s);
  const want = clamp(stored(displayPage), st.lo, st.hi);
  if (want === st.page) { syncPageBoxes(); return; }
  const delta = want - st.page;
  st.page = want;
  const jobs = [openPage(s)];
  if (W.lock) {
    const o = S(other(s));
    o.page = clamp(o.page + delta, o.lo, o.hi);
    jobs.push(openPage(other(s)));
  }
  await Promise.all(jobs);
  refreshSelection();
}

async function turnBoth(delta) {
  for (const s of ["src", "tgt"]) S(s).page = clamp(S(s).page + delta, S(s).lo, S(s).hi);
  await Promise.all([openPage("src"), openPage("tgt")]);
  refreshSelection();
}

/* ── wiring ────────────────────────────────────────────────────────────── */

const who = () => $("#who").value.trim();
$("#who").value = localStorage.getItem("setu_who") || "";
$("#who").addEventListener("change", () => localStorage.setItem("setu_who", who()));

$("#board").onchange = () => onBoard().catch(e => toast(e.message, true));
$("#klass").onchange = () => onClass().catch(e => toast(e.message, true));
$("#subject").onchange = () => onSubject().catch(e => toast(e.message, true));
$("#srcLang").onchange = () => onSrcLang().catch(e => toast(e.message, true));
$("#tgtLang").onchange = () => onTgtLang().catch(e => toast(e.message, true));
$("#open").onclick = openBooks;

$("#srcPage").onchange = () => goTo("src", $("#srcPage").value);
$("#tgtPage").onchange = () => goTo("tgt", $("#tgtPage").value);
$("#prevBoth").onclick = () => turnBoth(-1);
$("#nextBoth").onclick = () => turnBoth(1);
$("#lockPages").onchange = e => { W.lock = e.target.checked; };
$("#srcChapter").onchange = e => { if (e.target.value) goTo("src", e.target.value); };
$("#tgtChapter").onchange = e => { if (e.target.value) goTo("tgt", e.target.value); };

$("#link").onclick = async () => {
  if (!W.pid) return;
  try {
    const { link } = await api(`/projects/${W.pid}/link`, {
      method: "POST",
      body: JSON.stringify({ src_page: S("src").page, tgt_page: S("tgt").page, annotator: who() }),
    });
    W.link = link; W.lock = true; $("#lockPages").checked = true; $("#unlink").hidden = false;
    renderOffset();
    toast("Saved for everyone working on these two books.");
  } catch (e) { toast(e.message, true); }
};
$("#unlink").onclick = async () => {
  try {
    await api(`/projects/${W.pid}/link`, { method: "POST", body: JSON.stringify({ clear: true }) });
    W.link = null; $("#unlink").hidden = true; renderOffset();
    toast("Unlinked. Each side moves on its own again.");
  } catch (e) { toast(e.message, true); }
};

$$(".segbtn").forEach(b => b.onclick = () => {
  const group = b.dataset.tool ? "tool" : (b.dataset.view ? "view" : "mode");
  $$(`.segbtn[data-${group}]`).forEach(x => x.classList.toggle("on", x === b));
  W[group] = b.dataset[group];
  if (group === "view") {
    $("#viewHint").textContent = W.view === "page"
      ? "The printed page with the parser's blocks drawn on it. Needs the scans."
      : "The text of both editions, side by side. This is the view for checking translations.";
    ["src", "tgt"].forEach(renderSide);
    refreshSelection();
  } else if (group === "tool") {
    $("#toolHint").textContent = W.tool === "crop"
      ? "Drag a rectangle over the page. Drag inside it to move it, the corner to resize, × to remove."
      : "Click a block to put its text below. Shift-click for a run, Ctrl-click to add one.";
  } else {
    $("#modeHint").textContent = W.mode === "edit"
      ? "Correcting. Type straight into either column — it saves when you click away."
      : "Reading. Nothing you type can change the text.";
    ["src", "tgt"].forEach(renderSide);
    refreshSelection();
  }
});
$("#toolHint").textContent = "Click a block to put its text below. Shift-click for a run, Ctrl-click to add one.";

["#kindFilter", "#dim", "#order"].forEach(id => $(id).onchange = () => ["src", "tgt"].forEach(drawBlocks));
$("#noise").onchange = async () => { await Promise.all([openPage("src"), openPage("tgt")]); refreshSelection(); };

$$(".z").forEach(b => b.onclick = () => {
  const s = b.dataset.zoom, by = +b.dataset.by;
  const st = S(s);
  st.zoom = by === 0 ? 1 : clamp(st.zoom + by * 0.25, 0.3, 4);
  renderSide(s);
});

$("#sideToggle").onclick = () => $("#side").classList.toggle("hidden");
$("#help").onclick = () => { $("#keys").hidden = false; };

/* the draggable split */
(() => {
  const split = $("#split"), panes = $("#panes");
  let dragging = false;
  split.addEventListener("pointerdown", e => { dragging = true; split.setPointerCapture(e.pointerId); });
  split.addEventListener("pointermove", e => {
    if (!dragging) return;
    const r = panes.getBoundingClientRect();
    const pct = clamp(((e.clientX - r.left) / r.width) * 100, 20, 80);
    $("#paneSrc").style.flex = `0 0 ${pct}%`;
    $("#paneTgt").style.flex = `0 0 ${100 - pct}%`;
  });
  split.addEventListener("pointerup", e => {
    dragging = false; split.releasePointerCapture(e.pointerId);
    ["src", "tgt"].forEach(renderSide);
  });
})();

/* keyboard */
document.addEventListener("keydown", e => {
  if (e.key === "Control") document.body.classList.add("hidelabels");
  const t = e.target;
  const typing = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
  if (typing) return;

  if (e.key >= "1" && e.key <= "6") { const a = ANSWERS[+e.key - 1]; if (a) setAnswer(a[0]); return; }
  if (e.key === "ArrowLeft") { e.altKey ? turn("src", -1) : e.shiftKey ? turn("tgt", -1) : turnBoth(-1); return; }
  if (e.key === "ArrowRight") { e.altKey ? turn("src", 1) : e.shiftKey ? turn("tgt", 1) : turnBoth(1); return; }
  if (e.key === "Escape") { ["src", "tgt"].forEach(s => { S(s).sel.clear(); markSelected(s); }); refreshSelection(); return; }
  if (e.key === "e") { $$(`.segbtn[data-mode]`).find(b => b.dataset.mode !== W.mode)?.click(); return; }
  if (e.key === "c") { $$(`.segbtn[data-tool]`).find(b => b.dataset.tool !== W.tool)?.click(); return; }
  if (e.key === "n") { nextUnanswered(); return; }
  if (e.key === "+" || e.key === "=") { ["src", "tgt"].forEach(s => { S(s).zoom = clamp(S(s).zoom + 0.25, 0.3, 4); renderSide(s); }); return; }
  if (e.key === "-") { ["src", "tgt"].forEach(s => { S(s).zoom = clamp(S(s).zoom - 0.25, 0.3, 4); renderSide(s); }); return; }
});
document.addEventListener("keyup", e => {
  if (e.key === "Control") document.body.classList.remove("hidelabels");
});

/* POTATO's jump-to-next-unannotated, over this page then onward. */
async function nextUnanswered() {
  const st = S("src");
  const here = st.blocks.find(b => b.rid && (!b.status || b.status === "pending") && !st.sel.has(b.sid));
  if (here) {
    st.sel.clear(); st.sel.add(here.sid);
    st.last = st.blocks.indexOf(here);
    markSelected("src"); refreshSelection();
    return;
  }
  if (st.page < st.hi) { await turn("src", 1); nextUnanswered(); }
  else toast("Nothing left unanswered on this side of the book.");
}

async function loadProgress() {
  if (!W.pid) return;
  try {
    const p = await api(`/projects/${W.pid}/progress`);
    const done = p.done != null ? p.done : (p.total - (p.pending || 0));
    $("#progress").hidden = false;
    $("#progress").textContent = `${(done || 0).toLocaleString()} / ${(p.total || 0).toLocaleString()} answered`;
  } catch { /* the bar is a courtesy, never a blocker */ }
}

/* tabs */
$$(".tab").forEach(t => t.onclick = () => {
  $$(".tab").forEach(x => x.classList.toggle("on", x === t));
  $$(".page").forEach(p => p.classList.toggle("on", p.id === "page" + t.dataset.tab));
  if (t.dataset.tab === "Saved") loadSaved();
  if (t.dataset.tab === "Get") loadFormats();
  if (t.dataset.tab === "Guide") loadDocs();
});

/* ── saved work ────────────────────────────────────────────────────────── */

async function loadSaved() {
  if (!W.pid) { $("#savedList").innerHTML = `<p class="muted">Open two textbooks first.</p>`; return; }
  const f = $("#savedFilter").value;
  const q = f === "__done" ? "only_done=1" : (f ? `status=${encodeURIComponent(f)}` : "");
  try {
    const data = await api(`/projects/${W.pid}/rows?limit=60&${q}`);
    $("#savedNote").textContent = `${(data.total || 0).toLocaleString()} pairs`;
    $("#savedList").innerHTML = (data.rows || []).map(r => `
      <div class="card" data-src="${r.src && r.src.page != null ? r.src.page : ""}"
           data-tgt="${r.tgt && r.tgt.page != null ? r.tgt.page : ""}">
        <div class="top">
          <b>#${r.seq}</b>
          <span class="badge ${esc(r.status)}">${esc(statusLabel(r.status))}</span>
          <span>${esc([r.chapter_no, r.chapter].filter(Boolean).join(" "))}</span>
          <span class="spacer"></span>
          <span>${r.src && r.src.page != null ? "p" + (r.src.page + 1) : "—"} ↔ ${r.tgt && r.tgt.page != null ? "p" + (r.tgt.page + 1) : "—"}</span>
        </div>
        <div class="two">
          <div>${esc(snip(r.src && r.src.text))}</div>
          <div>${esc(snip(r.tgt && r.tgt.text))}</div>
        </div>
      </div>`).join("") || `<p class="muted">Nothing here yet.</p>`;
    $$("#savedList .card").forEach(card => card.onclick = async () => {
      const a = card.dataset.src, b = card.dataset.tgt;
      if (a !== "") S("src").page = clamp(+a, S("src").lo, S("src").hi);
      if (b !== "") S("tgt").page = clamp(+b, S("tgt").lo, S("tgt").hi);
      $$(".tab")[0].click();
      await Promise.all([openPage("src"), openPage("tgt")]);
      refreshSelection();
    });
  } catch (e) { toast(e.message, true); }
}
const snip = (t, n = 150) => { const s = (t || "").replace(/\s+/g, " "); return s.length > n ? s.slice(0, n) + "…" : s; };
const statusLabel = k => (ANSWERS.find(a => a[0] === k) || [k, "Not checked yet"])[1];
$("#savedFilter").onchange = loadSaved;
$("#savedRefresh").onclick = loadSaved;

/* ── download ──────────────────────────────────────────────────────────── */

let formatsLoaded = false;
async function loadFormats() {
  if (formatsLoaded) return;
  try {
    const { formats } = await api("/formats");
    $("#fmt").innerHTML = formats.map(f =>
      `<option value="${esc(f.key)}"${f.available ? "" : " disabled"}>` +
      `${esc(f.label)} (.${esc(f.ext)})${f.available ? "" : " — needs " + esc(f.install || "an extra package")}` +
      `</option>`).join("");
    formatsLoaded = true;
  } catch (e) { toast(e.message, true); }
}
$("#download").onclick = () => {
  if (!W.pid) return toast("Open two textbooks first.", true);
  const scope = $("#scope").value;
  const q = scope === "__done" ? "only_done=1" : (scope ? `status=${encodeURIComponent(scope)}` : "");
  window.location = `${API}/projects/${W.pid}/export.${$("#fmt").value}?${q}`;
  $("#getNote").textContent = "The file should appear in your downloads.";
};
$("#downloadAll").onclick = () => {
  if (!W.pid) return toast("Open two textbooks first.", true);
  window.location = `${API}/projects/${W.pid}/export-bundle.zip`;
};

/* ── the guide ─────────────────────────────────────────────────────────── */

let docsLoaded = false;
async function loadDocs() {
  if (docsLoaded) return;
  try {
    const { docs } = await api("/docs");
    $("#docNav").innerHTML = docs.map((d, i) =>
      `<button data-name="${esc(d.name)}"${i === 0 ? ' class="on"' : ""}>${esc(d.title)}</button>`).join("");
    $$("#docNav button").forEach(b => b.onclick = () => {
      $$("#docNav button").forEach(x => x.classList.toggle("on", x === b));
      showDoc(b.dataset.name);
    });
    if (docs.length) showDoc(docs[0].name);
    docsLoaded = true;
  } catch (e) { toast(e.message, true); }
}
async function showDoc(name) {
  const r = await fetch(`${API}/docs/${encodeURIComponent(name)}`);
  $("#doc").innerHTML = markdown(await r.text());
}
/* Enough Markdown for the three manuals, and no dependency to go stale. */
function markdown(md) {
  const lines = md.split("\n");
  const out = []; let inTable = false, inCode = false;
  const inline = t => esc(t)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
    .replace(/(^|[^*])\*([^*]+)\*/g, "$1<i>$2</i>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" rel="noopener">$1</a>');
  for (const raw of lines) {
    const l = raw.replace(/\s+$/, "");
    if (l.startsWith("```")) { inCode = !inCode; out.push(inCode ? "<pre><code>" : "</code></pre>"); continue; }
    if (inCode) { out.push(esc(raw)); continue; }
    if (/^\|/.test(l)) {
      const cells = l.split("|").slice(1, -1);
      if (/^[\s|:-]+$/.test(l)) continue;
      if (!inTable) { out.push("<table>"); inTable = true; }
      out.push("<tr>" + cells.map(c => `<td>${inline(c.trim())}</td>`).join("") + "</tr>");
      continue;
    }
    if (inTable) { out.push("</table>"); inTable = false; }
    if (/^#{1,4} /.test(l)) { const n = l.match(/^#+/)[0].length; out.push(`<h${n}>${inline(l.slice(n + 1))}</h${n}>`); continue; }
    if (/^[-*] /.test(l)) { out.push(`<li>${inline(l.slice(2))}</li>`); continue; }
    if (/^\d+\. /.test(l)) { out.push(`<li>${inline(l.replace(/^\d+\. /, ""))}</li>`); continue; }
    if (/^---+$/.test(l)) { out.push("<hr>"); continue; }
    out.push(l ? `<p>${inline(l)}</p>` : "");
  }
  if (inTable) out.push("</table>");
  return out.join("\n");
}

/* ── start ─────────────────────────────────────────────────────────────── */

window.addEventListener("resize", () => { ["src", "tgt"].forEach(s => { if (S(s).book) renderSide(s); }); });
window.addEventListener("pagehide", () => { ["src", "tgt"].forEach(saveText); });

(async () => {
  try {
    const meta = await api("/meta");
    const c = meta.corpus || {};
    $("#corpus").textContent =
      `${(c.books || 0).toLocaleString()} textbooks · ` +
      `${(c.segments || 0).toLocaleString()} pieces of text`;
  } catch { /* the line is a courtesy */ }
  try { await loadBoards(); }
  catch (e) { toast("The textbook list could not be loaded: " + e.message, true); }
  refreshSelection();
})();
