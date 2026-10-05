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
    blocks: [], sel: new Set(), picked: new Map(), last: null, zoom: 1,
    imageAvailable: false, imageMessage: "", aspect: 1.414,
    chapters: [], crop: null, cropUrl: "",
  };
}
const S = s => W.side[s];
const other = s => (s === "src" ? "tgt" : "src");

/* ── the save pipeline ─────────────────────────────────────────────────────
 *
 * Every keystroke that changes a passage becomes a DRAFT, keyed by the pair
 * (row) and side it belongs to. A draft is:
 *
 *   * what every editor on the page shows — the column above and the panel
 *     below read the same draft, so the two can never disagree, and an older
 *     copy can never quietly be sent over a newer one;
 *   * what gets sent — one request at a time per passage, retried with growing
 *     pauses when the connection or the server is down;
 *   * what survives — kept in this browser's own storage until the server
 *     confirms it, so a closed tab, a crash, a dropped connection or a server
 *     restart loses nothing. Anything unsent is sent when the page next opens.
 *
 * Three things a draft is never allowed to do: be sent empty (a cleared box is
 * someone about to retype, not a correction), be sent to the wrong passage
 * (if the pairing changed underneath it, it asks the server where its passage
 * lives now), or be dropped without the annotator being told.
 */

const DRAFT_KEY = "setu.drafts.v1";
const DRAFTS = new Map();          // "rid|side" -> draft
const flushTimers = new Map();     // "rid|side" -> timeout
let storageOk = true;
let warnedStorage = false;

const dkey = (rid, side) => `${rid}|${side}`;
const INVISIBLE = /[\s​‌‍⁠﻿]+/g;
const isBlank = t => !String(t || "").replace(INVISIBLE, "");

/* What an editable box really contains. A box emptied in Chrome holds a lone
 * <br>, which innerText reports as "\n" — that is how passages used to be
 * saved as empty. Trailing whitespace is never content either. */
function cleanText(el) {
  const t = String(el.innerText || "").replace(/ /g, " ");
  return isBlank(t) ? "" : t.replace(/[ \t\r\n]+$/, "");
}
const sameText = (a, b) =>
  String(a || "").replace(/[ \t\r\n]+$/, "") === String(b || "").replace(/[ \t\r\n]+$/, "");

function loadDrafts() {
  try {
    const raw = localStorage.getItem(DRAFT_KEY);
    if (!raw) return 0;
    const list = JSON.parse(raw);
    if (!Array.isArray(list)) return 0;
    for (const d of list) {
      if (!d || !d.rid || (d.side !== "src" && d.side !== "tgt") || typeof d.text !== "string") continue;
      // Whatever it was doing when the page went away, it was not confirmed.
      if (d.state === "saving" || d.state === "failed") d.state = "dirty";
      d.tries = 0;
      DRAFTS.set(dkey(d.rid, d.side), d);
    }
    return DRAFTS.size;
  } catch { return 0; }
}

let persistTimer = null;
function persistDrafts(now = false) {
  const write = () => {
    const keep = [...DRAFTS.values()]
      .filter(d => d.state !== "saved")
      .map(({ rid, side, sid, pid, text, base, state, server, err }) =>
        ({ rid, side, sid, pid, text, base, state, server, err, at: Date.now() }));
    try {
      if (keep.length) localStorage.setItem(DRAFT_KEY, JSON.stringify(keep));
      else localStorage.removeItem(DRAFT_KEY);
      storageOk = true;
    } catch {
      storageOk = false;
      if (!warnedStorage) {
        warnedStorage = true;
        toast("This browser will not let Setu keep a safety copy of unsaved text "
            + "(private window, or storage full). Saving still works — but do not "
            + "close the tab while the top bar says something is unsaved.", true);
      }
    }
  };
  clearTimeout(persistTimer);
  if (now) write(); else persistTimer = setTimeout(write, 250);
}

function draftFor(rid, side) { return rid ? DRAFTS.get(dkey(rid, side)) : undefined; }

/* The text a passage should be shown with: an unsaved draft wins over what the
 * server last sent, because it is newer and it is the annotator's. */
function textOf(block, side) {
  const d = block && block.rid ? draftFor(block.rid, side) : null;
  return d && d.state !== "refused" ? d.text : ((block && block.text) || "");
}

/* An editor changed. Record it, show it everywhere the same passage is on
 * screen, and arrange for it to be sent. */
function noteEdit(rid, side, sid, text, base, from) {
  if (!rid) return;
  const key = dkey(rid, side);
  let d = DRAFTS.get(key);
  if (!d) {
    d = { rid, side, sid, pid: W.pid, text, base: base | 0, state: "dirty", tries: 0 };
    DRAFTS.set(key, d);
  }
  d.text = text;
  d.sid = d.sid || sid;
  if (d.state !== "saving") d.state = "dirty";
  d.err = "";
  mirror(rid, side, text, from);
  persistDrafts();
  updateSaveDot();
  if (isBlank(text)) {
    clearTimeout(flushTimers.get(key));    // a cleared box is never sent
    return;
  }
  scheduleFlush(key, 900);
}

function scheduleFlush(key, ms) {
  clearTimeout(flushTimers.get(key));
  flushTimers.set(key, setTimeout(() => flush(key), ms));
}

/* Every editor showing this passage, except the one being typed in, follows
 * along — so the column and the panel below always say the same thing. */
function mirror(rid, side, text, except) {
  const sel = `[data-edit-rid="${CSS.escape(rid)}"][data-edit-side="${side}"]`;
  document.querySelectorAll(sel).forEach(el => {
    if (el === except || el === document.activeElement) return;
    if (el.innerText !== text) el.innerText = text;
  });
}

/* A fetch that hands back the response instead of throwing, so the save path
 * can tell a conflict from a refusal from a dead connection. */
function rawFetch(path, opts = {}) {
  const headers = Object.assign({
    "Content-Type": "application/json",
    "X-Annotator": (() => { try { return localStorage.getItem("setu_who") || ""; } catch { return ""; } })(),
  }, opts.headers || {});
  return fetch(API + path, Object.assign({}, opts, { headers }));
}
const bodyMessage = b => {
  const d = b && (b.detail || b.message);
  return typeof d === "string" ? d : (d && d.message) || "";
};

async function flush(key, opts = {}) {
  clearTimeout(flushTimers.get(key));
  const d = DRAFTS.get(key);
  if (!d || d.state === "saved" || d.state === "refused" || d.state === "conflict") return;
  if (d.state === "saving") return;                   // the reply will look again
  if (isBlank(d.text)) return;
  const sent = d.text;
  d.state = "saving";
  updateSaveDot();
  try {
    const r = await rawFetch(`/rows/${encodeURIComponent(d.rid)}`, {
      method: "PATCH", keepalive: !!opts.keepalive,
      body: JSON.stringify({ [d.side]: sent, [`${d.side}_rev`]: d.base | 0,
                             annotator: who(), reason: "edit" }),
    });
    let body = null;
    try { body = await r.json(); } catch { /* not json */ }

    if (r.ok) {
      const got = body && body[d.side];
      const rev = got && got.rev != null ? got.rev : d.base;
      applySaved(d.rid, d.side, got && typeof got.text === "string" ? got.text : sent, rev);
      d.tries = 0;
      if (d.text === sent) {                         // nothing typed since it left
        d.state = "saved";
        DRAFTS.delete(key);
        flashSaved(d.rid, d.side);
      } else {
        d.base = rev; d.state = "dirty";
        scheduleFlush(key, 300);
      }
      lastSaved = Date.now();
    } else if (r.status === 409) {
      d.state = "conflict";
      d.server = { text: body && typeof body.current === "string" ? body.current : "",
                   rev: body && body.rev != null ? body.rev : d.base };
      showConflict(d);
    } else if (r.status === 404) {
      // The pairing changed — this passage now lives in another row, or the
      // row it was in was merged away. Find it and send it there.
      if (!(await retarget(d))) {
        d.state = "refused";
        d.err = "This passage is no longer in any pair, so the change could not be "
              + "saved. Your text is still in the box — copy it before moving on.";
        showRefused(d);
      }
    } else if (r.status === 400) {
      d.state = "refused";
      d.err = bodyMessage(body) || "That change could not be saved.";
      showRefused(d);
    } else {
      throw new Error(bodyMessage(body) || `the server answered ${r.status}`);
    }
  } catch (e) {
    // Offline, server restarting, proxy hiccup. The draft is safe in this
    // browser; try again, waiting longer each time, up to half a minute.
    d.state = "failed";
    d.tries = (d.tries | 0) + 1;
    d.err = String(e && e.message || e);
    scheduleFlush(key, Math.min(30000, 2000 * 2 ** Math.min(d.tries - 1, 4)));
  } finally {
    persistDrafts();
    updateSaveDot();
  }
}

async function flushAll(opts = {}) {
  const keys = [...DRAFTS.keys()].filter(k => {
    const d = DRAFTS.get(k);
    return d && (d.state === "dirty" || d.state === "failed") && !isBlank(d.text);
  });
  if (opts.keepalive) persistDrafts(true);
  await Promise.all(keys.map(k => flush(k, opts)));
  // One wait for anything already in flight, so callers that are about to
  // change a pairing do not race a save addressed to the old one.
  for (let i = 0; i < 40 && [...DRAFTS.values()].some(d => d.state === "saving"); i++)
    await new Promise(res => setTimeout(res, 50));
}

/* A draft addressed to a row that no longer holds its passage. */
async function retarget(d) {
  if (!d.sid || !d.pid) return false;
  try {
    const at = await api(`/projects/${encodeURIComponent(d.pid)}/where?sid=${encodeURIComponent(d.sid)}`);
    if (!at || !at.rid || at.side !== d.side) return false;
    DRAFTS.delete(dkey(d.rid, d.side));
    Object.assign(d, { rid: at.rid, base: at.rev | 0, state: "dirty" });
    DRAFTS.set(dkey(d.rid, d.side), d);
    scheduleFlush(dkey(d.rid, d.side), 100);
    return true;
  } catch { return false; }
}

/* The server confirmed a save: every copy of that block on this page learns it. */
function applySaved(rid, side, text, rev) {
  for (const s of ["src", "tgt"]) {
    const st = S(s);
    const lists = [st.blocks, [...st.picked.values()]];
    for (const list of lists) for (const b of list) {
      if (b.rid !== rid || s !== side) continue;
      b.text = text; b.rev = rev;
      b.edited = !sameText(text, b.source_text || "");
    }
  }
  const cached = ROWCACHE.get(rid);
  if (cached && cached[side]) {
    cached[side].text = text; cached[side].rev = rev;
    cached[side].edited = !sameText(text, cached[side].source || "");
  }
  document.querySelectorAll(`[data-edit-rid="${CSS.escape(rid)}"][data-edit-side="${side}"]`)
    .forEach(el => {
      el.dataset.rev = rev;
      const row = el.closest(".trow");
      if (row) {
        row.dataset.rev = rev;
        const meta = row.querySelector(".tmeta");
        const tag = meta && meta.querySelector(".tedit");
        const edited = !sameText(text, (S(side).blocks.find(b => b.rid === rid) || {}).source_text || "");
        if (meta && edited && !tag) {
          const t = document.createElement("span"); t.className = "tedit"; t.textContent = "corrected";
          meta.appendChild(t);
        } else if (tag && !edited) tag.remove();
      }
    });
  savedDirty = true;
  // The panel's label ("corrected by hand") and its "Put back" button follow
  // at once, instead of waiting for the pair to be selected again.
  if ($("#textSrc").dataset.rid === rid || $("#textTgt").dataset.rid === rid) refreshSelection();
}

function flashSaved(rid, side) {
  document.querySelectorAll(`.trow[data-rid="${CSS.escape(rid)}"][data-side="${side}"]`).forEach(row => {
    row.classList.add("saved");
    setTimeout(() => row.classList.remove("saved"), 1400);
  });
}

/* The one line in the top bar that always tells the truth about saving. */
let lastSaved = 0;
function updateSaveDot() {
  const el = $("#saveDot");
  if (!el) return;
  const all = [...DRAFTS.values()];
  const need = all.filter(d => d.state === "conflict" || d.state === "refused").length;
  const failing = all.filter(d => d.state === "failed").length;
  const busy = all.filter(d => d.state === "saving" || d.state === "dirty").length;
  let text, cls;
  if (need) { text = `${need} change${need === 1 ? "" : "s"} need${need === 1 ? "s" : ""} you`; cls = "need"; }
  else if (failing) { text = navigator.onLine === false
      ? "Offline — kept on this computer" : "Not saved yet — trying again"; cls = "fail"; }
  else if (busy) { text = "Saving…"; cls = "busy"; }
  else { text = lastSaved ? "All changes saved" : "Nothing to save"; cls = "ok"; }
  el.textContent = text;
  el.className = "savedot " + cls;
  el.hidden = !W.pid && !all.length;
  el.title = storageOk ? "Unsaved text is also kept in this browser until the server confirms it."
                       : "This browser will not keep a safety copy — keep the tab open until this says saved.";
}
const unsavedCount = () => [...DRAFTS.values()].filter(d => d.state !== "saved" && !isBlank(d.text)).length;

/* ── when a save cannot simply go through ──────────────────────────────── */

function showConflict(d) {
  const box = $("#conflict");
  if (!box) return;
  box.dataset.key = dkey(d.rid, d.side);
  $("#cfTheirs").textContent = d.server && d.server.text || "(empty)";
  $("#cfMine").textContent = d.text;
  box.hidden = false;
}
$("#cfMineBtn") && ($("#cfMineBtn").onclick = () => {
  const d = DRAFTS.get($("#conflict").dataset.key);
  $("#conflict").hidden = true;
  if (!d) return;
  // Mine goes on top of theirs as a new revision; theirs stays in the history.
  d.base = d.server ? d.server.rev | 0 : d.base;
  d.state = "dirty"; d.server = null;
  flush(dkey(d.rid, d.side));
});
$("#cfTheirsBtn") && ($("#cfTheirsBtn").onclick = () => {
  const key = $("#conflict").dataset.key, d = DRAFTS.get(key);
  $("#conflict").hidden = true;
  if (!d) return;
  DRAFTS.delete(key);
  if (d.server) { applySaved(d.rid, d.side, d.server.text, d.server.rev); mirror(d.rid, d.side, d.server.text, null); }
  persistDrafts(); updateSaveDot(); refreshSelection();
});

function showRefused(d) {
  saveState(d.err, true);
  toast(d.err, true);
}


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

/* Opening two books, from the dropdowns or from a remembered session.
 *
 * `want` lets "Continue where you left off" reuse this exact path rather than
 * keep a second one of its own: the server returns the SAME project for the
 * same two books, so reopening IS opening. A resumed session that took its own
 * route could drift into a state a fresh one never reaches, and that class of
 * bug stays invisible until somebody's work is already inside it. */
async function openBooks(want) {
  const src = (want && want.src) || $("#srcBook").value;
  const tgt = (want && want.tgt) || $("#tgtBook").value;
  if (!src || !tgt) return toast("Choose a book on each side first.", true);
  if (src === tgt) return toast("The two sides must be different books.", true);

  const btn = want ? $("#resumeGo") : $("#open");
  const said = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Opening…";
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
        page: o.first_page, sel: new Set(), picked: new Map(), last: null, crop: null, cropUrl: "",
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
    // A remembered position wins over the page link, because it is where this
    // person actually was, while the link is where the project says the two
    // editions correspond. Both are clamped to the book: a position saved
    // before a re-ingest can name a page that no longer exists.
    if (want && want.place) {
      if (want.place.src_page != null)
        S("src").page = clamp(want.place.src_page | 0, S("src").lo, S("src").hi);
      if (want.place.tgt_page != null)
        S("tgt").page = clamp(want.place.tgt_page | 0, S("tgt").lo, S("tgt").hi);
    }
    ["#gChapter", "#gPage", "#gView", "#gTool", "#gMode", "#gFilter"].forEach(id => { $(id).hidden = false; });
    $("#unlink").hidden = !W.link;
    await Promise.all([openPage("src"), openPage("tgt")]);
    refreshSelection();
    loadProgress();
    savedBooksFilled = false;              // the Saved tab's dropdown is stale
    return true;
  } catch (e) {
    toast(e.message, true);
    return false;
  } finally {
    btn.disabled = false;
    btn.textContent = said;
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

  // A selected block on this page is the freshest copy of it.
  for (const b of st.blocks) if (st.picked.has(b.sid)) st.picked.set(b.sid, b);

  const mateLang = sideLang(other(s));
  const only = $("#kindFilter").value, dim = $("#dim").checked;
  const rows = st.blocks.map((b, i) => {
    if (only && b.kind !== only && !dim) return "";
    const on = st.sel.has(b.sid);
    const state = !b.rid ? "lonely" : (b.status && b.status !== "pending" ? "done" : "pending");
    const faded = (only && b.kind !== only) || (dim && !on);
    const shownText = textOf(b, s);
    const text = shownText.trim();
    const editable = W.mode === "edit" && b.rid;
    const drafted = !!draftFor(b.rid, s);
    // Where its partner is — the one fact that decides what to do with a
    // block. "pair #1263" alone used to be shown on blocks that had no
    // partner at all.
    const partner = !b.rid
      ? `<span class="tlonely">not in any pair</span>`
      : b.paired
        ? `<span>pair #${b.row_seq}${b.mate_display_page != null ? ` ↔ p${b.mate_display_page}` : ""}</span>`
        : `<span>pair #${b.row_seq}</span><span class="tnomate">no ${esc(mateLang)} paired</span>`;
    return `<div class="trow blk ${state}${on ? " on" : ""}${faded ? " dim" : ""}${b.rid && !b.paired ? " onesided" : ""}"` +
      ` data-sid="${esc(b.sid)}" data-i="${i}" data-rid="${esc(b.rid || "")}"` +
      ` data-rev="${b.rev | 0}" data-side="${s}"` +
      ` style="--c:${W.colors[b.kind || "other"] || "#666"}">` +
      `<div class="tmeta"><span class="tkind">${esc(kindName(b.kind))}</span>` +
      `<span>page ${b.display_page}</span>` + partner +
      ((b.edited || drafted) ? `<span class="tedit">corrected</span>` : "") +
      (b.rid && b.status && b.status !== "pending"
        ? `<span class="tdone">${esc(statusLabel(b.status))}</span>` : "") +
      `</div><div class="tbody"` +
      (editable ? ` contenteditable="true" spellcheck="false" data-edit-rid="${esc(b.rid)}"` +
                  ` data-edit-side="${s}" data-sid="${esc(b.sid)}" data-rev="${b.rev | 0}"` : "") +
      `>${text ? esc(shownText) : (editable ? "" : "<i>the parser found no text here</i>")}</div>` +
      `</div>`;
  }).join("");

  // The scan only matters in the page view, so in the text view nobody is
  // told about it. It used to say "No scan of this book" above every page,
  // which read like a fault when nothing was wrong.
  const banner = (W.view === "page" && !st.imageAvailable)
    ? `<div class="nosc">No scan of this page on this machine — showing the text instead. `
      + `Everything except the page picture and the crop tool works as usual.`
      + `<br><span class="tiny">${esc(st.imageMessage || "")}</span></div>`
    : "";
  host.innerHTML = banner +
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
    } else if (st.sel.size === 1 && st.sel.has(sid)) {
      // A second click on the selected block lets it go — the quickest way to
      // say "not this one" without reaching for Esc.
      st.sel.clear(); st.last = null;
    } else {
      // One block at a time is what an annotator almost always means, and it
      // is the only way the pair below can be unambiguous.
      st.sel.clear(); st.sel.add(sid); st.last = i;
    }
    // Keep the block itself, so it is still known when its page has turned.
    st.picked = new Map([...st.sel].map(x =>
      [x, st.blocks.find(b => b.sid === x) || st.picked.get(x)]).filter(([, b]) => b));
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

/* ── what is selected, and what it means ───────────────────────────────────
 *
 * A pair is a ROW. Clicking a block names the row it is in — and nothing else.
 * Selecting a block on each side does NOT make them a pair: if they are in
 * two different rows, the screen says so and offers "Pair these two". The
 * first version showed any two selected blocks side by side as if they were a
 * pair, and the answer then went to only one of them — usually one whose other
 * half was empty.
 *
 * A selection survives turning the page, on purpose: the English passage is
 * often on page 106 and its Marathi on page 108. `picked` keeps the selected
 * block itself, so it is still known after its page has scrolled away.
 */

const ROWCACHE = new Map();       // rid -> the server's view of that row

function selectedBlock(s) {
  const st = S(s);
  if (st.sel.size !== 1) return null;
  const sid = [...st.sel][0];
  return st.blocks.find(b => b.sid === sid) || st.picked.get(sid) || null;
}

/* What the two selections add up to. */
function selectionState() {
  const nL = S("src").sel.size, nR = S("tgt").sel.size;
  const L = selectedBlock("src"), R = selectedBlock("tgt");
  if (nL > 1 || nR > 1) return { kind: "many", L, R };
  if (L && R) {
    if (L.rid && L.rid === R.rid) return { kind: "pair", rid: L.rid, L, R };
    return { kind: "mismatch", L, R };
  }
  if (L) return { kind: "one", rid: L.rid || "", L, from: "src" };
  if (R) return { kind: "one", rid: R.rid || "", R, from: "tgt" };
  return { kind: "none" };
}

/* The whole row, both sides, from the server — needed whenever the partner
 * of the selected block is on a page that is not on screen. */
async function fetchRow(rid, fresh = false) {
  if (!rid) return null;
  if (!fresh && ROWCACHE.has(rid)) return ROWCACHE.get(rid);
  try {
    const row = await api(`/rows/${encodeURIComponent(rid)}`);
    ROWCACHE.set(rid, row);
    return row;
  } catch { return null; }
}

/* A block-shaped object for one side of a row, whether or not its page is on
 * screen — so the panel can show and edit a partner on page 108 while page 106
 * is the one being read. */
function sideOfRow(row, s) {
  if (!row || !row[s] || !row[s].present) return null;
  const on = S(s).blocks.find(b => b.sid === row[s].sid);
  if (on) return on;
  return {
    sid: row[s].sid, rid: row.rid, row_seq: row.seq, text: row[s].text,
    source_text: row[s].source, rev: row[s].rev, edited: row[s].edited,
    kind: row[s].kind, page: row[s].page,
    display_page: row[s].page == null ? null : row[s].page + 1,
    status: row.status, note: row.note, paired: !!(row.src.present && row.tgt.present),
    offPage: true,
  };
}

const sideLang = s => S(s).language || (s === "src" ? "English" : "the other language");
const langName = s => S(s).language || (s === "src" ? "left-hand" : "right-hand");

let selToken = 0;
async function refreshSelection() {
  const token = ++selToken;
  const sel = selectionState();
  const counts = ["src", "tgt"].map(s => S(s).sel.size);

  // What each box in the panel shows, and the row it belongs to.
  let row = null;
  if (sel.kind === "pair" || (sel.kind === "one" && sel.rid)) {
    row = await fetchRow(sel.rid, true);
    if (token !== selToken) return;           // a newer click won the race
  }
  const show = { src: null, tgt: null };
  if (sel.kind === "pair") { show.src = sel.L; show.tgt = sel.R; }
  else if (sel.kind === "one") {
    show[sel.from] = sel[sel.from === "src" ? "L" : "R"];
    const mate = other(sel.from);
    show[mate] = row ? sideOfRow(row, mate) : null;
  } else if (sel.kind === "mismatch") { show.src = sel.L; show.tgt = sel.R; }

  const editable = W.mode === "edit" && (sel.kind === "pair" || sel.kind === "one");
  for (const s of ["src", "tgt"]) {
    const el = $(s === "src" ? "#textSrc" : "#textTgt");
    const lbl = $(s === "src" ? "#lblSrc" : "#lblTgt");
    const orig = $(s === "src" ? "#origSrc" : "#origTgt");
    const b = show[s];
    if (el === document.activeElement && b && el.dataset.editRid === b.rid) continue;   // never yank a box out from under the cursor

    el.dataset.sid = b ? b.sid : "";
    el.dataset.rid = b && b.rid ? b.rid : "";
    el.dataset.editRid = b && b.rid && editable ? b.rid : "";
    el.dataset.editSide = s;
    el.dataset.rev = b ? (b.rev | 0) : 0;
    el.classList.toggle("gap", !b);
    el.classList.remove("nopartner");

    if (!b) {
      orig.hidden = true;
      el.contentEditable = "false";
      lbl.textContent = langName(s);
      if (sel.kind === "one" && sel.rid) {
        el.classList.add("nopartner");
        el.innerText = `No ${sideLang(s)} passage is paired with this one.\n\n`
          + `If it is on another page, turn the ${s === "src" ? "left" : "right"}-hand `
          + `page to it, click it, and press “Pair these two”.\n`
          + `If the ${sideLang(s)} book really has nothing here, answer “Missing or incomplete”.`;
      } else el.innerText = "";
      continue;
    }

    el.innerText = textOf(b, s);
    const where = b.display_page != null ? `page ${b.display_page}` : "";
    lbl.textContent = [langName(s), where, kindName(b.kind),
      b.rid ? `pair #${b.row_seq}` : "not in any pair",
      (b.edited || draftFor(b.rid, s)) ? "corrected by hand" : "as the parser read it"]
      .filter(Boolean).join(" · ");
    orig.hidden = !(editable && b.rid && (b.edited || draftFor(b.rid, s)));
    el.contentEditable = editable && b.rid ? "true" : "false";
  }

  renderPairBar(sel, row);
  renderAnswers(sel, row);

  $("#selInfo").textContent =
    sel.kind === "none" ? (W.pid ? "Nothing selected — click a block on either page."
                                 : "Choose two textbooks and press “Open side by side”.")
    : sel.kind === "many" ? `selected: ${counts[0]} on the left, ${counts[1]} on the right — `
                          + "pairing and answering work one block per side; click a single block."
    : sel.kind === "mismatch" ? "These two blocks are not paired with each other yet."
    : sel.kind === "pair" ? `pair #${sel.L.row_seq} — both sides selected`
    : sel.rid ? `pair #${(sel.L || sel.R).row_seq}` +
                (row && row.src.present && row.tgt.present ? "" : ` · nothing on the ${sel.from === "src" ? "right" : "left"} yet`)
    : "This block is not in any pair (headers and page numbers are left out). Select a block on the other side to pair it.";
}

/* The strip between the texts and the answers: "Pair these two", or "Unpair". */
function renderPairBar(sel, row) {
  const bar = $("#pairBar");
  if (!bar) return;
  bar.hidden = true; bar.innerHTML = "";
  if (!W.pid) return;

  if (sel.kind === "mismatch") {
    const L = sel.L, R = sel.R, lose = [];
    if (L.paired && L.mate_sid) lose.push(`the ${sideLang("src")} passage is now paired with another `
      + `${sideLang("tgt")} passage${L.mate_display_page ? ` (page ${L.mate_display_page})` : ""}, which will be left on its own`);
    if (R.paired && R.mate_sid) lose.push(`the ${sideLang("tgt")} passage is now paired with another `
      + `${sideLang("src")} passage${R.mate_display_page ? ` (page ${R.mate_display_page})` : ""}, which will be left on its own`);
    bar.innerHTML =
      `<div class="pb-text"><b>These two are not a pair yet.</b> ` +
      `Left is page ${L.display_page}${L.rid ? `, pair #${L.row_seq}` : ""}; ` +
      `right is page ${R.display_page}${R.rid ? `, pair #${R.row_seq}` : ""}. ` +
      `If they say the same thing, pair them — pages do not have to match.` +
      (lose.length ? `<br><span class="tiny">Pairing them means ${esc(lose.join("; and "))}. ` +
                     `Answers already given to those pairs go back to “Not checked yet” (kept in the history).</span>` : "") +
      `</div><button class="btn primary" id="doPair">⇄ Pair these two <kbd>p</kbd></button>`;
    bar.hidden = false;
    $("#doPair").onclick = pairSelected;
    return;
  }
  if ((sel.kind === "pair" || sel.kind === "one") && row && row.src.present && row.tgt.present) {
    bar.innerHTML =
      `<div class="pb-text tiny muted">Paired: ${esc(sideLang("src"))} page ${row.src.page + 1} ↔ ` +
      `${esc(sideLang("tgt"))} page ${row.tgt.page + 1}${row.origin === "manual" ? " · paired by hand" : ""}.` +
      ` If these are not translations of each other, unpair them.</div>` +
      `<button class="btn ghost" id="doUnpair">Unpair</button>`;
    bar.hidden = false;
    $("#doUnpair").onclick = () => unpairRow(row);
  }
}

/* The answers, with the ones that compare two passages switched off when
 * there is only one passage to look at. */
const TWO_SIDED = new Set(["exact", "needs_correction", "structural_mismatch"]);
function renderAnswers(sel, row) {
  const ok = (sel.kind === "pair" || sel.kind === "one") && sel.rid && row;
  $("#answerRow").hidden = !ok;
  if (!ok) return;
  const both = row.src.present && row.tgt.present;
  $("#answers").innerHTML = ANSWERS.map(([k, label], i) => {
    const off = !both && TWO_SIDED.has(k);
    return `<button class="ans${row.status === k ? " on" : ""}${off ? " off" : ""}" data-status="${k}"` +
      (off ? ` title="There is only one passage here, so there is nothing to compare it with. Pair it first, or answer Missing or incomplete."` : "") +
      `><kbd>${i + 1}</kbd>${esc(label)}</button>`;
  }).join("");
  const note = $("#note");
  if (note !== document.activeElement || note.dataset.rid !== row.rid) {
    note.value = row.note || "";
    note.dataset.rid = row.rid;
  }
}

$("#answers").addEventListener("click", ev => {
  const b = ev.target.closest(".ans");
  if (b) setAnswer(b.dataset.status);
});

async function setAnswer(status) {
  const sel = selectionState();
  if (!((sel.kind === "pair" || sel.kind === "one") && sel.rid)) {
    if (sel.kind === "mismatch") toast("Pair the two blocks first — press “Pair these two” — then answer.", true);
    return;
  }
  const row = await fetchRow(sel.rid);
  if (row && TWO_SIDED.has(status) && !(row.src.present && row.tgt.present)) {
    toast(`There is nothing on the ${row.src.present ? "right" : "left"} to compare with. `
        + "If the partner is on another page, select it and pair them; "
        + "otherwise answer “Missing or incomplete”.", true);
    return;
  }
  await flushNote();
  try {
    const out = await api(`/rows/${encodeURIComponent(sel.rid)}/status`, {
      method: "POST",
      body: JSON.stringify({ status, note: $("#note").value, annotator: who() }),
    });
    if (out && out.row) ROWCACHE.set(sel.rid, out.row);
    for (const s of ["src", "tgt"]) {
      for (const b of [...S(s).blocks, ...S(s).picked.values()])
        if (b.rid === sel.rid) { b.status = status; b.note = $("#note").value; }
    }
    document.querySelectorAll(`.trow[data-rid="${CSS.escape(sel.rid)}"] .tdone`).forEach(e => e.remove());
    document.querySelectorAll(`.trow[data-rid="${CSS.escape(sel.rid)}"] .tmeta`).forEach(meta => {
      if (status === "pending") return;
      const t = document.createElement("span"); t.className = "tdone"; t.textContent = statusLabel(status);
      meta.appendChild(t);
    });
    saveState("Saved.");
    savedDirty = true;
    refreshSelection();
    ["src", "tgt"].forEach(drawBlocks);
    loadProgress();
  } catch (e) { saveState(e.message, true); toast(e.message, true); }
}

/* The note saves itself too — it used to be sent only when an answer was
 * clicked, so a note typed after answering was lost on moving on. */
let noteTimer = null;
$("#note").addEventListener("input", () => {
  clearTimeout(noteTimer);
  noteTimer = setTimeout(flushNote, 1200);
});
$("#note").addEventListener("blur", () => flushNote());
async function flushNote() {
  clearTimeout(noteTimer);
  const el = $("#note"), rid = el.dataset.rid;
  if (!rid) return;
  const cached = ROWCACHE.get(rid);
  if (cached && (cached.note || "") === el.value) return;
  try {
    const out = await api(`/rows/${encodeURIComponent(rid)}/status`, {
      method: "POST", body: JSON.stringify({ note: el.value, annotator: who() }),
    });
    if (out && out.row) ROWCACHE.set(rid, out.row);
    for (const s of ["src", "tgt"])
      for (const b of [...S(s).blocks, ...S(s).picked.values()]) if (b.rid === rid) b.note = el.value;
    savedDirty = true;
  } catch (e) { saveState("The note could not be saved: " + e.message, true); }
}

/* ── pairing and unpairing ─────────────────────────────────────────────── */

async function pairSelected() {
  const sel = selectionState();
  if (sel.kind !== "mismatch") return;
  const L = sel.L, R = sel.R;
  const btn = $("#doPair");
  if (btn) { btn.disabled = true; btn.textContent = "Pairing…"; }
  try {
    // Nothing may still be on its way to a row that is about to change.
    await flushAll();
    const out = await api(`/projects/${encodeURIComponent(W.pid)}/pair`, {
      method: "POST",
      body: JSON.stringify({ src_sid: L.sid, tgt_sid: R.sid, annotator: who() }),
    });
    ROWCACHE.clear();
    await reloadKeepingSelection([L.sid], [R.sid]);
    savedDirty = true;
    loadProgress();
    toast(out && out.changed === false ? "Those two were already a pair."
      : "Paired. Now answer: do these two say the same thing?");
  } catch (e) {
    toast(e.message, true);
    if (btn) { btn.disabled = false; btn.textContent = "⇄ Pair these two"; }
  }
}

async function unpairRow(row) {
  if (!confirm(`Unpair #${row.seq}?\n\nThe ${sideLang("src")} and the ${sideLang("tgt")} `
      + "will each stand on their own until you pair them with something else. "
      + "Corrections stay with their text; the answer goes back to “Not checked yet”.")) return;
  try {
    await flushAll();
    await api(`/rows/${encodeURIComponent(row.rid)}/unpair`, {
      method: "POST", body: JSON.stringify({ annotator: who() }) });
    ROWCACHE.clear();
    await reloadKeepingSelection([row.src.sid], []);
    savedDirty = true;
    loadProgress();
    toast("Unpaired. Now select its real partner on the other side, or answer “Missing or incomplete”.");
  } catch (e) { toast(e.message, true); }
}

/* Reload both visible pages after the pairing changed, and put the selection
 * back on the same blocks — whatever pages they are on. */
async function reloadKeepingSelection(srcSids, tgtSids) {
  for (const [s, sids] of [["src", srcSids], ["tgt", tgtSids]]) {
    const st = S(s);
    st.sel = new Set(sids.filter(Boolean));
    st.picked = new Map();
  }
  await Promise.all([openPage("src"), openPage("tgt")]);
  for (const s of ["src", "tgt"]) {
    const st = S(s);
    for (const sid of st.sel) {
      const b = st.blocks.find(x => x.sid === sid);
      if (b) st.picked.set(sid, b);
      else {                                    // its page is not on screen
        try {
          const at = await api(`/projects/${encodeURIComponent(W.pid)}/where?sid=${encodeURIComponent(sid)}`);
          const r = await fetchRow(at.rid, true);
          const sb = sideOfRow(r, s);
          if (sb) st.picked.set(sid, sb);
        } catch { st.sel.delete(sid); }
      }
    }
    markSelected(s);
  }
  refreshSelection();
}

/* ── editing ───────────────────────────────────────────────────────────────
 *
 * Two places to type — the column above and the panel below — and one rule
 * for both: what is typed becomes the passage's draft, the draft is what both
 * places show, and the draft is what gets sent. See "the save pipeline".
 */

function editorBase(el) {
  const rid = el.dataset.editRid, s = el.dataset.editSide;
  const d = draftFor(rid, s);
  return d ? d.base : (el.dataset.rev | 0);
}

/* Paste as plain text. A rich paste brings hidden markup with it, and
 * innerText of that is not what the person saw. */
document.addEventListener("paste", ev => {
  const el = ev.target.closest && ev.target.closest('[contenteditable="true"][data-edit-rid]');
  if (!el) return;
  ev.preventDefault();
  const text = (ev.clipboardData || window.clipboardData).getData("text/plain") || "";
  if (!document.execCommand || !document.execCommand("insertText", false, text)) {
    const r = window.getSelection().getRangeAt(0);
    r.deleteContents(); r.insertNode(document.createTextNode(text)); r.collapse(false);
    el.dispatchEvent(new Event("input", { bubbles: true }));
  }
}, true);

document.addEventListener("input", ev => {
  const el = ev.target.closest && ev.target.closest('[contenteditable="true"][data-edit-rid]');
  if (!el || !el.dataset.editRid) return;
  const text = cleanText(el);
  noteEdit(el.dataset.editRid, el.dataset.editSide, el.dataset.sid || "", text, editorBase(el), el);
  saveState(text ? "…" : "The passage is empty. Type the corrected text — an empty "
    + "passage is never saved, and leaving it empty puts the text back.", !text);
}, true);

/* Leaving a box: send it now. Left empty: put the last saved text back and
 * say so — the old behaviour saved the emptiness and said "Saved." */
document.addEventListener("blur", ev => {
  const el = ev.target.closest && ev.target.closest('[contenteditable="true"][data-edit-rid]');
  if (!el || !el.dataset.editRid) return;
  const rid = el.dataset.editRid, s = el.dataset.editSide, key = dkey(rid, s);
  const d = DRAFTS.get(key);
  if (!d) return;
  if (isBlank(d.text)) {
    DRAFTS.delete(key);
    clearTimeout(flushTimers.get(key));
    const b = [...S(s).blocks, ...S(s).picked.values()].find(x => x.rid === rid)
           || sideOfRow(ROWCACHE.get(rid), s);
    const back = (b && b.text) || "";
    el.innerText = back;
    mirror(rid, s, back, el);
    persistDrafts(); updateSaveDot();
    saveState("The passage was left empty, so nothing was saved and the text is back. "
      + "To mark it as wrong, use an answer instead.", true);
    return;
  }
  flush(key);
}, true);

async function saveText() { await flushAll(); }   // kept: older callers flush everything

for (const s of ["src", "tgt"]) {
  $(s === "src" ? "#origSrc" : "#origTgt").addEventListener("click", async () => {
    const el = $(s === "src" ? "#textSrc" : "#textTgt");
    const rid = el.dataset.rid;
    if (!rid) return;
    // A restore replaces whatever was being typed, so the draft goes first.
    const key = dkey(rid, s);
    DRAFTS.delete(key); clearTimeout(flushTimers.get(key)); persistDrafts(true); updateSaveDot();
    try {
      const out = await api(`/rows/${encodeURIComponent(rid)}/restore`, {
        method: "POST", body: JSON.stringify({ side: s, rev: 0, annotator: who() }),
      });
      ROWCACHE.delete(rid);
      const got = out && (out[s] || out);
      if (got && typeof got.text === "string") {
        applySaved(rid, s, got.text, got.rev | 0);
        mirror(rid, s, got.text, null);
      }
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
  rememberPlace();
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
  rememberPlace();
}

async function turnBoth(delta) {
  for (const s of ["src", "tgt"]) S(s).page = clamp(S(s).page + delta, S(s).lo, S(s).hi);
  await Promise.all([openPage("src"), openPage("tgt")]);
  refreshSelection();
  rememberPlace();
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
    W.link = null; $("#unlink").hidden = true;
    W.lock = false; $("#lockPages").checked = false;   // or they still move as one
    renderOffset();
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

/* The filters apply at once in both views. In the text view drawBlocks does
 * nothing — the column draws itself — so the filter used to wait for the next
 * page turn, and passages seemed to vanish for no reason. */
["#kindFilter", "#dim", "#order"].forEach(id => $(id).onchange = () =>
  ["src", "tgt"].forEach(s => { if (!S(s).book) return; W.view === "page" ? drawBlocks(s) : renderSide(s); }));
$("#noise").onchange = async () => { await Promise.all([openPage("src"), openPage("tgt")]); refreshSelection(); };

$$(".z").forEach(b => b.onclick = () => {
  const s = b.dataset.zoom, by = +b.dataset.by;
  const st = S(s);
  st.zoom = by === 0 ? 1 : clamp(st.zoom + by * 0.25, 0.3, 4);
  renderSide(s);
});

/* The toggle lives inside the sidebar, so hiding the sidebar hid the only
 * way to get it back. It moves to the header while the sidebar is away. */
$("#sideToggle").onclick = () => {
  const away = $("#side").classList.toggle("hidden");
  document.body.classList.toggle("side-away", away);
};
$("#help").onclick = () => { $("#keys").hidden = false; };
$("#keysClose").onclick = () => { $("#keys").hidden = true; };
$("#keys").onclick = e => { if (e.target.id === "keys") $("#keys").hidden = true; };

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
  // turn() already carries the other side when the pages are locked, so a
  // plain arrow honours the lock instead of overriding it.
  if (e.key === "ArrowLeft") { e.altKey ? turn("src", -1) : e.shiftKey ? turn("tgt", -1) : turn("src", -1); return; }
  if (e.key === "ArrowRight") { e.altKey ? turn("src", 1) : e.shiftKey ? turn("tgt", 1) : turn("src", 1); return; }
  if (e.key === "Escape") { ["src", "tgt"].forEach(s => { S(s).sel.clear(); S(s).picked.clear(); markSelected(s); }); refreshSelection(); return; }
  if (e.key === "p") { if (selectionState().kind === "mismatch") pairSelected(); return; }
  if (e.key === "e") { $$(`.segbtn[data-mode]`).find(b => b.dataset.mode !== W.mode)?.click(); return; }
  if (e.key === "c") { $$(`.segbtn[data-tool]`).find(b => b.dataset.tool !== W.tool)?.click(); return; }
  if (e.key === "n") { nextUnanswered(); return; }
  if (e.key === "?") { $("#keys").hidden = false; return; }
  if (e.key === "+" || e.key === "=") { ["src", "tgt"].forEach(s => { S(s).zoom = clamp(S(s).zoom + 0.25, 0.3, 4); renderSide(s); }); return; }
  if (e.key === "-") { ["src", "tgt"].forEach(s => { S(s).zoom = clamp(S(s).zoom - 0.25, 0.3, 4); renderSide(s); }); return; }
});
document.addEventListener("keyup", e => {
  if (e.key === "Control") document.body.classList.remove("hidelabels");
});

/* POTATO's jump-to-next-unannotated, over this page then onward. */
async function nextUnanswered() {
  if (!W.pid) return;
  await flushAll();
  const sel = selectionState();
  const here = (sel.L || sel.R || {}).row_seq;
  const from = Number.isFinite(here) ? here : -1;
  try {
    const { row } = await api(`/projects/${encodeURIComponent(W.pid)}/next?seq=${from}&direction=1&status=pending`);
    if (!row) { toast("Nothing left unanswered after this point in the book."); return; }
    const full = await fetchRow(row.rid, true);
    if (!full) return;
    for (const s of ["src", "tgt"]) {
      if (full[s].present && full[s].page != null) S(s).page = clamp(full[s].page, S(s).lo, S(s).hi);
    }
    await reloadKeepingSelection(full.src.present ? [full.src.sid] : [],
                                 full.tgt.present ? [full.tgt.sid] : []);
    rememberPlace();
    const on = $(`.trow[data-rid="${CSS.escape(row.rid)}"]`);
    if (on) on.scrollIntoView({ block: "center" });
  } catch (e) { toast(e.message, true); }
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
  if (t.dataset.tab === "Saved") flushAll().then(() => loadSaved(0));
  if (t.dataset.tab === "Get") flushAll().then(loadGet);
  if (t.dataset.tab === "Guide") loadDocs();
});
function goTab(name) { ($$(".tab").find(t => t.dataset.tab === name) || {}).onclick?.(); }

/* ── coming back to work you started ───────────────────────────────────────
 *
 * The problem this solves: an annotator answers three hundred pairs, closes
 * the tab, and comes back on Monday. Their work is safe in the database — but
 * finding it again meant remembering a board, a class, a subject and two
 * editions, and picking the same two books out of a hundred and twenty. Get
 * one wrong and you are staring at an empty project wondering where it went.
 *
 * So the first thing in the sidebar is a list of what has been worked on,
 * newest first, with how far each one got. Choosing one reopens the two books
 * AND puts the annotator back on the pages they were reading.
 */

let WORKBENCH = [];

async function loadWorkbench() {
  try {
    const { projects } = await api(`/workbench?annotator=${encodeURIComponent(who())}`);
    WORKBENCH = projects || [];
  } catch { WORKBENCH = []; }                 // a missing list is never fatal

  const withWork = WORKBENCH.filter(p => (p.answered || 0) > 0 || p.place?.src_page != null);
  const show = withWork.length ? withWork : WORKBENCH;
  $("#gResume").hidden = !show.length;
  if (!show.length) return;

  // The sidebar is narrow, so the option carries a short name and the full
  // one rides in the title, where a hover shows it without widening anything.
  $("#resume").innerHTML = show.map(p =>
    `<option value="${esc(p.pid)}" title="${esc(p.label || p.name || p.pid)}">` +
    `${esc(shortLabel(p))}</option>`).join("");
  describeResume();
}

/* "MH · 10 · English ⇄ Gujarati" fits; the full board name does not. */
function shortLabel(p) {
  const bits = [p.board || "", p.class ? `Class ${p.class}` : "",
                [p.src_language, p.tgt_language].filter(Boolean).join(" ⇄ ")];
  return bits.filter(Boolean).join(" · ") || p.name || p.pid;
}

function describeResume() {
  const p = WORKBENCH.find(x => x.pid === $("#resume").value);
  if (!p) { $("#resumeNote").textContent = ""; return; }
  const bits = [p.where];
  if (p.corrected) bits.push(`${p.corrected.toLocaleString()} corrected`);
  if (p.place && p.place.src_page != null) {
    bits.push(`you were on page ${shown(p.place.src_page)} ↔ ${shown(p.place.tgt_page ?? p.place.src_page)}`);
  }
  if (p.touched) bits.push(ago(p.touched));
  $("#resumeNote").textContent = bits.filter(Boolean).join(" · ");
}
$("#resume").onchange = describeResume;

function ago(ts) {
  const s = Math.max(0, Date.now() / 1000 - (+ts || 0));
  if (s < 90) return "just now";
  if (s < 5400) return `${Math.round(s / 60)} minutes ago`;
  if (s < 129600) return `${Math.round(s / 3600)} hours ago`;
  const d = Math.round(s / 86400);
  return d === 1 ? "yesterday" : `${d} days ago`;
}

$("#resumeGo").onclick = async () => {
  const p = WORKBENCH.find(x => x.pid === $("#resume").value);
  if (!p) return;
  const ok = await openBooks({ src: p.src_book, tgt: p.tgt_book, place: p.place });
  if (!ok) return;
  if (W.view === "text" || W.view === "page") applyView(p.place && p.place.view);
  const at = (p.place && p.place.src_page != null)
    ? ` You were on page ${shown(S("src").page)}.` : "";
  toast(`Back in ${p.label || p.name}. ${p.where}.${at}`);
};

/* The view is restored only if it is one of the two that exist — a stored
 * value from an older version is ignored rather than trusted. */
function applyView(v) {
  if (v !== "text" && v !== "page") return;
  const b = $$(".segbtn[data-view]").find(x => x.dataset.view === v);
  if (b && !b.classList.contains("on")) b.click();
}

/* Where the annotator is, remembered after they stop moving. Debounced,
 * because a page turn is cheap and a write is not, and never awaited by
 * anything the annotator is waiting for. */
let placeTimer = null;
function rememberPlace() {
  if (!W.pid) return;
  clearTimeout(placeTimer);
  placeTimer = setTimeout(() => {
    api(`/projects/${W.pid}/place`, {
      method: "POST",
      body: JSON.stringify({
        place: {
          src_page: S("src").page, tgt_page: S("tgt").page,
          src_book: S("src").book, tgt_book: S("tgt").book,
          view: W.view, mode: W.mode,
        },
      }),
    }).catch(() => { /* a forgotten position is a nuisance, never an error */ });
  }, 1200);
}

/* ── saved work ────────────────────────────────────────────────────────────
 *
 * Built to Tulana Studio's Saved-pairs shape, and for the same reason: an
 * annotator reviewing their own work needs to filter it, search it, and jump
 * back to the passage it came from. The one difference that matters is that
 * this reads across EVERY project, because someone returning to check what
 * they did last week has no project open.
 */

const SAVED_PAGE = 25;
let savedOffset = 0;
let savedBooksFilled = false;

function savedQuery(offset) {
  const q = new URLSearchParams();
  if ($("#sBook").value) q.set("pid", $("#sBook").value);
  const st = $("#sStatus").value;
  if (st === "__done") q.set("answered", "done");
  else if (st === "__pending") q.set("answered", "pending");
  else if (st === "__attention") q.set("attention", "1");
  else if (st) q.set("status", st);
  if ($("#sChapter").value) q.set("chapter_no", $("#sChapter").value);
  if ($("#sSearch").value.trim()) q.set("search_text", $("#sSearch").value.trim());
  if ($("#sEdited").checked) q.set("edited", "true");
  q.set("limit", SAVED_PAGE);
  q.set("offset", Math.max(0, offset | 0));
  return q;
}

async function loadSaved(offset) {
  if (offset != null) savedOffset = Math.max(0, offset | 0);
  const list = $("#savedList");
  list.setAttribute("aria-busy", "true");
  let data;
  try {
    data = await api(`/saved?${savedQuery(savedOffset)}`);
  } catch (e) {
    list.innerHTML = `<div class="card muted">That could not be loaded: ${esc(e.message)}</div>`;
    list.removeAttribute("aria-busy");
    return;
  }
  list.removeAttribute("aria-busy");

  if (!savedBooksFilled) {
    const projects = data.projects || [];
    $("#sBook").innerHTML = `<option value="">Every textbook</option>` +
      projects.map(p => `<option value="${esc(p.pid)}">${esc(projectLabel(p))}` +
        `${p.answered ? ` — ${p.answered.toLocaleString()} answered` : ""}</option>`).join("");
    savedBooksFilled = true;
    fillSavedChapters();
    // The list just fetched covers every textbook. If a textbook is open, the
    // dropdown is set to it — so fetch again for that one, or the dropdown and
    // the list below it would disagree.
    if (W.pid && projects.some(p => p.pid === W.pid)) {
      $("#sBook").value = W.pid;
      return loadSaved(0);
    }
  }

  const t = data.tally || {};
  const opt = $('#sStatus option[value="__attention"]');
  if (opt) opt.textContent = `Needs attention${t.attention ? ` (${t.attention})` : ""}`;
  $("#savedStats").textContent = t.total
    ? `${(t.answered || 0).toLocaleString()} of ${(t.total || 0).toLocaleString()} ` +
      `pairs answered` + (t.corrected ? ` · ${t.corrected.toLocaleString()} corrected by hand` : "") +
      (t.attention ? ` · ${t.attention.toLocaleString()} need attention` : "") +
      ` · ${statusSentence(t.by_status || {})}`
    : "Nothing here yet. Open two textbooks in the Annotate tab and start answering.";

  const rows = data.rows || [];
  const total = data.total || 0;
  if (!rows.length) {
    list.innerHTML = `<div class="card muted">${
      total ? "No pair matches that filter." :
      "Nothing has been answered yet — open two textbooks and start in the Annotate tab."
    }</div>`;
    $("#savedPager").hidden = true;
    return;
  }

  list.innerHTML = rows.map(r => savedCard(r)).join("");
  $$("#savedList .scard [data-act]").forEach(b => b.onclick = ev => {
    ev.stopPropagation();
    savedAction(b.dataset.act, b.closest(".scard").dataset);
  });
  $$("#savedList .scard").forEach(c => c.onclick = () => savedAction("open", c.dataset));

  const from = savedOffset + 1, to = Math.min(savedOffset + rows.length, total);
  $("#savedPager").hidden = total <= SAVED_PAGE;
  $("#sRange").textContent = `${from.toLocaleString()}–${to.toLocaleString()} of ${total.toLocaleString()}`;
  $("#sPrev").disabled = savedOffset <= 0;
  $("#sNext").disabled = to >= total;
}

function projectLabel(p) {
  const bits = [p.board, p.class ? `Class ${p.class}` : "", p.subject,
                [p.src_language, p.tgt_language].filter(Boolean).join(" ⇄ ")];
  return bits.filter(Boolean).join(" · ") || p.name || p.pid;
}

function statusSentence(by) {
  const order = ["exact", "needs_correction", "incomplete",
                 "structural_mismatch", "unclear", "not_applicable"];
  const bits = order.filter(k => by[k]).map(k => `${by[k].toLocaleString()} ${statusLabel(k).toLowerCase()}`);
  return bits.length ? bits.join(" · ") : "none answered yet";
}

function savedCard(r) {
  const pages = `${r.src_display != null ? "p" + r.src_display : "—"} ↔ ` +
                `${r.tgt_display != null ? "p" + r.tgt_display : "—"}`;
  const chapter = [r.chapter_no, r.chapter].filter(Boolean).join(" ");
  const corrected = r.src_edited || r.tgt_edited;
  // A side with no passage says so in words. "nothing on this side" read as
  // though the annotator's text had been lost.
  const body = (side, lang) => {
    if (!r[`${side}_present`])
      return `<div class="body missing">No ${esc(lang)} passage is paired with this one.</div>`;
    const t = snip(r[`${side}_text`]);
    if (!t) return `<div class="body missing bad">Saved empty — open it to put the text back.</div>`;
    return `<div class="body${side === "tgt" ? " indic" : ""}">${esc(t)}</div>`;
  };
  return `
  <div class="scard ${r.status === "pending" ? "pending" : ""}${r.attention ? " attn" : ""}"
       data-rid="${esc(r.rid)}" data-pid="${esc(r.pid)}"
       data-src="${r.src_page == null ? "" : r.src_page}"
       data-tgt="${r.tgt_page == null ? "" : r.tgt_page}"
       data-src-sid="${esc(r.src_sid || "")}" data-tgt-sid="${esc(r.tgt_sid || "")}">
    <div class="top">
      <span class="seq">#${r.seq}</span>
      <span class="badge ${esc(r.status)}">${esc(statusLabel(r.status))}</span>
      ${corrected ? `<span class="badge edited">corrected</span>` : ""}
      ${!(r.src_present && r.tgt_present) ? `<span class="badge onesided">one side only</span>` : ""}
      ${chapter ? `<span class="muted">${esc(chapter)}</span>` : ""}
      <span class="spacer"></span>
      <span class="muted tiny">${esc(pages)}${r.kind ? " · " + esc(r.kind) : ""}
        ${r.updated_by ? " · " + esc(r.updated_by) : ""}</span>
    </div>
    ${r.attention ? `<div class="attn-why tiny">⚠ ${esc(r.attention)}</div>` : ""}
    <div class="two">
      <div class="scol">
        <div class="lang tiny muted">${esc(r.src_language || "left")}${r.src_edited ? " · corrected" : ""}</div>
        ${body("src", r.src_language || "left-hand")}
      </div>
      <div class="scol">
        <div class="lang tiny muted">${esc(r.tgt_language || "right")}${r.tgt_edited ? " · corrected" : ""}</div>
        ${body("tgt", r.tgt_language || "right-hand")}
      </div>
    </div>
    ${r.note ? `<div class="note-shown tiny">Note: ${esc(r.note)}</div>` : ""}
    <div class="acts">
      <button class="btn sm" data-act="open">Open in Annotate</button>
      ${r.attention && !(r.src_present && r.tgt_present) && TWO_SIDED.has(r.status)
        ? `<button class="btn sm" data-act="missing">Change to “Missing or incomplete”</button>` : ""}
      ${r.status !== "pending"
        ? `<button class="btn sm" data-act="clear">Undo my answer</button>` : ""}
    </div>
  </div>`;
}

async function savedAction(act, d) {
  if (act === "clear" || act === "missing") {
    const status = act === "clear" ? "pending" : "incomplete";
    if (act === "clear" && !confirm("Put this pair back to “Not checked yet”? Any text you "
               + "corrected is kept — only the answer is removed.")) return;
    try {
      await api(`/rows/${encodeURIComponent(d.rid)}/status`, {
        method: "POST", body: JSON.stringify({ status, annotator: who() }) });
      ROWCACHE.delete(d.rid);
      toast(act === "clear" ? "Answer removed — the pair is waiting again"
                            : "Changed to “Missing or incomplete”.");
      loadSaved();
      loadProgress();
    } catch (e) { toast(e.message, true); }
    return;
  }
  // "open" — the two pages this pair is on, with its blocks selected, so the
  // panel shows it straight away.
  if (d.pid && d.pid !== W.pid) {
    const p = WORKBENCH.find(x => x.pid === d.pid);
    if (!p) { toast("Open that textbook in the Annotate tab first.", true); return; }
    goTab("Work");
    const ok = await openBooks({ src: p.src_book, tgt: p.tgt_book });
    if (!ok) return;
  }
  if (!W.pid) { toast("Open two textbooks in the Annotate tab first.", true); return; }
  goTab("Work");
  for (const [side, want] of [["src", d.src], ["tgt", d.tgt]]) {
    if (want === "" || want == null) continue;
    const st = S(side);
    st.page = clamp(parseInt(want, 10) || 0, st.lo, st.hi);
  }
  await reloadKeepingSelection([d.srcSid].filter(Boolean), [d.tgtSid].filter(Boolean));
  rememberPlace();
  const firstOn = $(`.trow[data-rid="${CSS.escape(d.rid)}"]`);
  if (firstOn) firstOn.scrollIntoView({ block: "center" });
}

function fillSavedChapters() {
  const opts = $("#srcChapter") ? [...$("#srcChapter").options] : [];
  const seen = new Set();
  const rows = opts.map(o => o.value).filter(v => v && !seen.has(v) && seen.add(v));
  if (!rows.length) return;
  $("#sChapter").innerHTML = `<option value="">Every chapter</option>` +
    opts.filter(o => o.value).map(o =>
      `<option value="${esc(o.value)}">${esc(o.textContent)}</option>`).join("");
}

const snip = (t, n = 220) => {
  const s = (t || "").replace(/\s+/g, " ").trim();
  return s.length > n ? s.slice(0, n) + "…" : s;
};
const statusLabel = k => (ANSWERS.find(a => a[0] === k) || [k, "Not checked yet"])[1];

let savedSearchTimer = null;
$("#sSearch").oninput = () => {
  clearTimeout(savedSearchTimer);
  savedSearchTimer = setTimeout(() => loadSaved(0), 300);
};
["#sBook", "#sStatus", "#sChapter", "#sEdited"].forEach(sel => {
  $(sel).onchange = () => loadSaved(0);
});
$("#sRefresh").onclick = () => loadSaved();
$("#sPrev").onclick = () => loadSaved(savedOffset - SAVED_PAGE);
$("#sNext").onclick = () => loadSaved(savedOffset + SAVED_PAGE);

/* ── download ──────────────────────────────────────────────────────────────
 *
 * Tulana Studio's Export tab, with Setu's eleven formats: say what to include,
 * see how many rows that is, then pick a shape. Each format describes itself
 * so nobody has to know what TMX is before deciding they do not want it.
 */

let getLoaded = false;

async function loadGet() {
  try {
    if (!getLoaded) {
      const [{ formats }, saved] = await Promise.all([
        api("/formats"), api("/saved?limit=1")]);
      const projects = saved.projects || [];
      $("#xBook").innerHTML = projects.map(p =>
        `<option value="${esc(p.pid)}">${esc(projectLabel(p))}</option>`).join("")
        || `<option value="">No textbook has been opened yet</option>`;
      if (W.pid && projects.some(p => p.pid === W.pid)) $("#xBook").value = W.pid;

      $("#xFormats").innerHTML = formats.map(f => `
        <button class="fmt${f.available === false ? " off" : ""}" data-fmt="${esc(f.key)}"
                ${f.available === false ? "disabled" : ""}>
          <b>${esc(f.label || f.name || f.key)}</b><code>.${esc(f.ext || f.extension || f.key)}</code>
          <span>${esc(f.description || FORMAT_HINT[f.key] || "")}</span>
          ${f.available === false
            ? `<em class="tiny">needs ${esc(f.install || "an extra package")}</em>` : ""}
        </button>`).join("");
      $$("#xFormats .fmt").forEach(b => b.onclick = () => download(b.dataset.fmt));
      ["#xBook", "#xStatus", "#xChapter"].forEach(s => $(s).onchange = refreshGetCount);
      getLoaded = true;
    }
    fillGetChapters();
    await refreshGetCount();
  } catch (e) { toast(e.message, true); }
}

/* Plain-language descriptions, for the formats whose own description is a
 * one-word name that means nothing to a person who has not met it. */
const FORMAT_HINT = {
  xlsx: "An Excel workbook. Opens in Excel, LibreOffice or Google Sheets.",
  csv: "A plain table. Opens in any spreadsheet, and in almost any program.",
  tsv: "Like CSV, but separated by tabs instead of commas.",
  json: "One structured file, for a programmer.",
  jsonl: "One line of JSON per pair — the usual shape for training data.",
  xml: "Structured text, for tools that expect XML.",
  txt: "Just the two texts, one pair after another.",
  tmx: "Translation memory. Opens in OmegaT, memoQ and Trados.",
  moses: "Two matching text files, the shape machine-translation training wants.",
  parquet: "A compact table for data tools like pandas or Spark.",
  huggingface: "A ready-made dataset folder for the Hugging Face library.",
};

function getQuery() {
  const q = new URLSearchParams();
  const st = $("#xStatus").value;
  if (st === "__done") q.set("only_done", "1");
  else if (st) q.set("status", st);
  if ($("#xChapter").value) q.set("chapter_no", $("#xChapter").value);
  return q;
}

function getPid() { return $("#xBook").value || W.pid || ""; }

async function refreshGetCount() {
  const pid = getPid();
  if (!pid) {
    $("#getStats").textContent = "Nothing to download yet — open two textbooks first.";
    $("#xCount").textContent = "";
    return;
  }
  // /saved speaks a slightly different language from the export endpoint;
  // translate, so the count describes exactly what the download will contain.
  const q = new URLSearchParams();
  const st = $("#xStatus").value;
  if (st === "__done") q.set("answered", "done");
  else if (st) q.set("status", st);
  if ($("#xChapter").value) q.set("chapter_no", $("#xChapter").value);
  q.set("pid", pid); q.set("limit", "1");
  try {
    const d = await api(`/saved?${q}`);
    const t = d.tally || {};
    $("#getStats").textContent =
      `${(t.answered || 0).toLocaleString()} of ${(t.total || 0).toLocaleString()} pairs answered` +
      (t.corrected ? ` · ${t.corrected.toLocaleString()} corrected by hand` : "");
    $("#xCount").textContent = `${(d.total || 0).toLocaleString()} pair(s) match — that is what a download will contain.`;
  } catch (e) { $("#xCount").textContent = ""; }
}

function fillGetChapters() {
  const opts = $("#srcChapter") ? [...$("#srcChapter").options].filter(o => o.value) : [];
  if (!opts.length) return;
  $("#xChapter").innerHTML = `<option value="">Every chapter</option>` +
    opts.map(o => `<option value="${esc(o.value)}">${esc(o.textContent)}</option>`).join("");
}

function download(fmt) {
  const pid = getPid();
  if (!pid) return toast("Open two textbooks first.", true);
  window.location = `${API}/projects/${pid}/export.${encodeURIComponent(fmt)}?${getQuery()}`;
  $("#getNote").textContent = "The file should appear in your downloads in a moment.";
}
$("#xBundle").onclick = () => {
  const pid = getPid();
  if (!pid) return toast("Open two textbooks first.", true);
  window.location = `${API}/projects/${pid}/export-bundle.zip?${getQuery()}`;
  $("#getNote").textContent = "Building the bundle — a large book can take a minute.";
};

/* ── the guide ─────────────────────────────────────────────────────────── */

/* The manual is long on purpose, so the navigation lists the sections inside
 * the open document as well as the documents themselves. Someone looking for
 * "what does Structural mismatch mean" reaches it in one click instead of
 * scrolling a manual that was written to be read once from the top. */
let docsLoaded = false;
let docList = [];

async function loadDocs() {
  if (docsLoaded) return;
  try {
    const { docs } = await api("/docs");
    docList = docs || [];
    if (!docList.length) {
      $("#docNav").innerHTML = "";
      $("#doc").innerHTML = `<p class="muted">No manual is installed on this server.</p>`;
      return;
    }
    docsLoaded = true;
    await showDoc(docList[0].name);
  } catch (e) { toast(e.message, true); }
}

async function showDoc(name) {
  let text;
  try {
    const r = await fetch(`${API}/docs/${encodeURIComponent(name)}`);
    if (!r.ok) throw new Error(`that page could not be loaded (${r.status})`);
    text = await r.text();
  } catch (e) {
    $("#doc").innerHTML = `<p class="muted">${esc(e.message)}</p>`;
    return;
  }
  $("#doc").innerHTML = markdown(text);
  $("#doc").scrollTop = 0;
  buildDocNav(name);
}

function buildDocNav(current) {
  const heads = $$("#doc h2, #doc h3");
  $("#docNav").innerHTML = docList.map(d => {
    const on = d.name === current;
    const inner = on ? heads.map(h =>
      `<button class="sec${h.tagName === "H3" ? " deep" : ""}" data-to="${esc(h.id)}">${esc(h.textContent)}</button>`
    ).join("") : "";
    return `<button class="dl${on ? " on" : ""}" data-doc="${esc(d.name)}">${esc(d.title)}</button>${inner}`;
  }).join("");

  $$("#docNav .dl").forEach(b => b.onclick = () => showDoc(b.dataset.doc));
  $$("#docNav .sec").forEach(b => b.onclick = () => {
    const h = document.getElementById(b.dataset.to);
    if (h) h.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

/* Enough Markdown for the manuals, and no dependency to go stale.
 *
 * Three things it must get right that the first version did not: consecutive
 * lines are ONE paragraph (a manual written in wrapped prose was coming out as
 * a line per paragraph), list items are wrapped in a real <ul> or <ol>, and a
 * blockquote is a blockquote. Everything is escaped before any tag is put
 * around it, so a document can contain < and & without becoming markup. */
function markdown(md) {
  const out = [];
  let para = [], list = null, inCode = false, inTable = false;

  const inline = t => esc(t)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
    .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<i>$2</i>")
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2" rel="noopener">$1</a>');

  const closePara = () => {
    if (para.length) { out.push(`<p>${inline(para.join(" "))}</p>`); para = []; }
  };
  const closeList = () => { if (list) { out.push(`</${list}>`); list = null; } };
  const closeTable = () => { if (inTable) { out.push("</table>"); inTable = false; } };
  const closeAll = () => { closePara(); closeList(); closeTable(); };

  for (const raw of md.split("\n")) {
    const l = raw.replace(/\s+$/, "");

    if (l.startsWith("```")) {
      closeAll();
      inCode = !inCode;
      out.push(inCode ? "<pre><code>" : "</code></pre>");
      continue;
    }
    if (inCode) { out.push(esc(raw)); continue; }

    if (!l.trim()) { closeAll(); continue; }

    if (/^\|/.test(l)) {
      closePara(); closeList();
      if (/^[\s|:-]+$/.test(l)) continue;           // the |---|---| separator
      const cells = l.split("|").slice(1, -1);
      if (!inTable) { out.push("<table>"); inTable = true; }
      out.push("<tr>" + cells.map(c => `<td>${inline(c.trim())}</td>`).join("") + "</tr>");
      continue;
    }
    closeTable();

    if (/^#{1,6} /.test(l)) {
      closeAll();
      const n = l.match(/^#+/)[0].length;
      const text = l.slice(n + 1);
      out.push(`<h${n} id="${slug(text)}">${inline(text)}</h${n}>`);
      continue;
    }
    if (/^(---+|\*\*\*+|___+)$/.test(l)) { closeAll(); out.push("<hr>"); continue; }
    if (/^> ?/.test(l)) {
      closeAll();
      out.push(`<blockquote>${inline(l.replace(/^> ?/, ""))}</blockquote>`);
      continue;
    }

    const bullet = l.match(/^\s*[-*+] +(.*)$/);
    const number = l.match(/^\s*\d+[.)] +(.*)$/);
    if (bullet || number) {
      closePara(); 
      const want = bullet ? "ul" : "ol";
      if (list !== want) { closeList(); out.push(`<${want}>`); list = want; }
      out.push(`<li>${inline((bullet || number)[1])}</li>`);
      continue;
    }
    closeList();
    para.push(l.trim());                   // an ordinary line joins the paragraph
  }
  closeAll();
  return out.join("\n");
}

const slug = t => String(t).toLowerCase().replace(/[^a-z0-9]+/g, "-")
                           .replace(/^-|-$/g, "").slice(0, 60);

/* ── start ─────────────────────────────────────────────────────────────── */

/* The text column does not depend on the window's width, and redrawing it
 * would take the cursor out of a box mid-word. Only the page picture is
 * redrawn when the window changes size. */
window.addEventListener("resize", () => {
  if (W.view !== "page") return;
  ["src", "tgt"].forEach(s => { if (S(s).book) renderSide(s); });
});

/* Leaving, by any route: send what is unsent with requests that outlive the
 * page, and keep a copy in this browser in case they do not arrive. */
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") { flushNote(); flushAll({ keepalive: true }); }
});
window.addEventListener("pagehide", () => { flushNote(); flushAll({ keepalive: true }); });
window.addEventListener("beforeunload", e => {
  if (!unsavedCount()) return;
  persistDrafts(true);
  flushAll({ keepalive: true });
  e.preventDefault(); e.returnValue = "";        // the browser asks "Leave site?"
});
window.addEventListener("online", () => {
  for (const [k, d] of DRAFTS) if (d.state === "failed") scheduleFlush(k, 200);
  updateSaveDot();
});
window.addEventListener("offline", updateSaveDot);
let savedDirty = false;

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

  // What was worked on before, so somebody coming back on Monday does not have
  // to reconstruct it from memory. Loaded after the dropdowns, because it is a
  // convenience and must never delay the interface being usable.
  loadWorkbench();
  refreshSelection();

  // Anything typed last time that the server never confirmed is sent now.
  const pending = loadDrafts();
  if (pending) {
    toast(`Sending ${pending} change${pending === 1 ? "" : "s"} from last time that had `
        + "not reached the server yet…");
    for (const [k, d] of DRAFTS) {
      if (d.state === "conflict" && d.server) showConflict(d);
      else if (d.state === "dirty") scheduleFlush(k, 600);
    }
  }
  updateSaveDot();
})();

/* Typing a name is how work is attributed, so the resume list is rebuilt when
 * it changes: what you were doing is per-person. */
$("#who").addEventListener("change", () => loadWorkbench());
