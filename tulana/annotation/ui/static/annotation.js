/* Setu — the browser-side behaviour Gradio cannot express on its own.
 *
 * Three jobs, and deliberately only three:
 *
 *   1. Synchronised scrolling between the two text panes.
 *   2. Keyboard shortcuts.
 *   3. Zoom and view controls.
 *
 * Everything else — loading, saving, navigation, status — is a Gradio event
 * handled in Python. This file never touches annotation data and never sends
 * anything to the server; the worst a bug in here can do is make the page look
 * wrong, which is the whole reason the boundary is drawn where it is.
 *
 * Gradio re-renders components as it pleases, so nothing here may hold a
 * reference to a DOM node across time. Everything re-queries on use, and the
 * listeners are attached by delegation on `document` where possible and
 * re-attached by a MutationObserver where not.
 *
 * Passed to `demo.launch(head=...)`. In Gradio 6 the Blocks constructor
 * silently ignores `head`, `css` and `js` — they moved to launch() — so a
 * version bump that lost this file would leave the workspace working but
 * unstyled and unscrolled.
 */
(function () {
  'use strict';

  if (window.__setuReady) return;
  window.__setuReady = true;

  var SRC = '#setu_src textarea';
  var TGT = '#setu_tgt textarea';

  function $(sel) { return document.querySelector(sel); }
  function panes() { return [$(SRC), $(TGT)]; }

  /* ── 1. synchronised scrolling ──────────────────────────────────────────
   *
   * Proportional rather than line-for-line: the two languages have different
   * lengths — Hindi runs about 15% longer than English in this corpus — so
   * matching absolute scroll positions would drift apart within a paragraph.
   *
   * The loop guard matters more than it looks. Setting `b.scrollTop` fires a
   * scroll event on b, which would scroll a, which would scroll b… The guard
   * plus one rAF per gesture keeps it to a single pass, and means a fast
   * trackpad flick costs one frame of work rather than a hundred.
   */
  var sync = { on: true, busy: false };

  function mirror(from, to) {
    if (!sync.on || sync.busy || !from || !to) return;
    var fromRange = from.scrollHeight - from.clientHeight;
    var toRange = to.scrollHeight - to.clientHeight;
    if (fromRange <= 0 || toRange <= 0) return;
    sync.busy = true;
    window.requestAnimationFrame(function () {
      try {
        to.scrollTop = (from.scrollTop / fromRange) * toRange;
      } finally {
        // Released on the next frame, after the scroll event this caused has
        // been dispatched and ignored.
        window.requestAnimationFrame(function () { sync.busy = false; });
      }
    });
  }

  document.addEventListener('scroll', function (ev) {
    var t = ev.target;
    if (!t || t.tagName !== 'TEXTAREA') return;
    var p = panes();
    if (t === p[0]) mirror(p[0], p[1]);
    else if (t === p[1]) mirror(p[1], p[0]);
  }, true);   // capture: scroll does not bubble

  function setSync(on) {
    sync.on = !!on;
    try { localStorage.setItem('setu.sync', sync.on ? '1' : '0'); } catch (e) {}
    var btn = $('#setu_sync_btn');
    if (btn) {
      btn.setAttribute('data-on', sync.on ? '1' : '0');
      btn.textContent = sync.on ? 'Scrolling: linked' : 'Scrolling: separate';
      btn.title = sync.on
        ? 'Both sides scroll together. Click to unlink them.'
        : 'Each side scrolls on its own. Click to link them.';
    }
    if (sync.on) { var p = panes(); mirror(p[0], p[1]); }
  }

  /* ── 2. zoom and view ───────────────────────────────────────────────────
   *
   * A CSS custom property, so one value moves the editor text, the line
   * height and the pane padding together. Purely visual: nothing here is sent
   * to the server, and no annotation data is touched.
   */
  var view = { size: 16, height: 420, compact: false, focus: false };

  function applyView() {
    var r = document.documentElement;
    r.style.setProperty('--setu-text', view.size + 'px');
    r.style.setProperty('--setu-pane-h', view.height + 'px');
    document.body.classList.toggle('setu-compact', view.compact);
    document.body.classList.toggle('setu-focus', view.focus);
    try {
      localStorage.setItem('setu.view', JSON.stringify(view));
    } catch (e) {}
    var lbl = $('#setu_zoom_label');
    if (lbl) lbl.textContent = view.size + 'px';
  }

  function zoom(delta) {
    view.size = Math.max(12, Math.min(30, view.size + delta));
    view.height = Math.max(240, Math.min(900, view.height + delta * 14));
    applyView();
  }

  function resetView() {
    view.size = 16; view.height = 420; view.compact = false; view.focus = false;
    applyView();
  }

  function taller(delta) {
    view.height = Math.max(200, Math.min(1000, view.height + delta));
    applyView();
  }

  /* ── 3. keyboard ────────────────────────────────────────────────────────
   *
   * Shortcuts drive the real Gradio buttons by clicking them, so there is
   * exactly one implementation of every action and the keyboard can never do
   * something the buttons cannot.
   *
   * Ctrl/Cmd+Z and Ctrl/Cmd+Shift+Z are deliberately NOT intercepted while the
   * cursor is in a text box: the browser's own undo stack is what an annotator
   * means by undo, and replacing it with a coarser one would be a downgrade
   * dressed up as a feature.
   */
  function click(id) {
    var el = document.getElementById(id) || document.querySelector('#' + id + ' button');
    if (el) { el.click(); return true; }
    return false;
  }

  /* Set the answer by clicking the real radio button.
   *
   * An earlier version clicked six invisible proxy buttons instead. Gradio 6
   * does not render a component with `visible=False` into the DOM at all, so
   * there was nothing to click and the number keys silently did nothing.
   * Driving the control the annotator would click themselves removes both the
   * proxies and the possibility of the two disagreeing.
   *
   * Index 0 is "Not checked yet"; the six answers are 1..6, which is exactly
   * the number printed on each one. */
  function setStatus(n) {
    var fieldset = document.getElementById('setu_status');
    if (!fieldset) return false;
    var radios = fieldset.querySelectorAll('input[type="radio"]');
    if (n < 0 || n >= radios.length) return false;
    var r = radios[n];
    if (r.checked) return true;      // already set; do not churn the server
    r.click();
    return true;
  }

  function inEditor(el) {
    return el && (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT'
                  || el.isContentEditable);
  }

  document.addEventListener('keydown', function (e) {
    var mod = e.ctrlKey || e.metaKey;
    var key = (e.key || '').toLowerCase();

    if (mod && key === 's') { e.preventDefault(); click('setu_save'); return; }
    if (mod && (e.key === '=' || e.key === '+')) { e.preventDefault(); zoom(1); return; }
    if (mod && e.key === '-') { e.preventDefault(); zoom(-1); return; }
    if (mod && key === '0') { e.preventDefault(); resetView(); return; }

    if (e.altKey && e.key === 'ArrowRight') { e.preventDefault(); click('setu_next'); return; }
    if (e.altKey && e.key === 'ArrowLeft') { e.preventDefault(); click('setu_prev'); return; }

    // Unmodified single keys only outside a text box, or typing "1" into a
    // paragraph would silently restatus the pair.
    if (mod || e.altKey || e.shiftKey || inEditor(document.activeElement)) return;
    if (key >= '1' && key <= '6') { e.preventDefault(); setStatus(parseInt(key, 10)); return; }
    if (key === 'n') { e.preventDefault(); click('setu_next_pending'); return; }
    if (key === 'j') { e.preventDefault(); click('setu_next'); return; }
    if (key === 'k') { e.preventDefault(); click('setu_prev'); return; }
  });

  /* ── wiring ─────────────────────────────────────────────────────────────
   *
   * The toolbar is plain HTML inside a gr.HTML block rather than Gradio
   * buttons, because every one of these actions is purely visual. Routing a
   * zoom click through a server event would add a round trip to something that
   * should be instant, and would put view state into session state where it
   * does not belong.
   */
  function wireToolbar() {
    var bar = $('#setu_viewbar');
    if (!bar || bar.getAttribute('data-wired') === '1') return;
    bar.setAttribute('data-wired', '1');
    bar.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-act]');
      if (!b) return;
      ev.preventDefault();
      var act = b.getAttribute('data-act');
      if (act === 'sync') setSync(!sync.on);
      else if (act === 'zoom-in') zoom(1);
      else if (act === 'zoom-out') zoom(-1);
      else if (act === 'zoom-reset') resetView();
      else if (act === 'taller') taller(80);
      else if (act === 'shorter') taller(-80);
      else if (act === 'compact') { view.compact = !view.compact; applyView(); }
      else if (act === 'focus') { view.focus = !view.focus; applyView(); }
    });
  }

  function restore() {
    try {
      var v = JSON.parse(localStorage.getItem('setu.view') || 'null');
      if (v && typeof v.size === 'number') {
        view.size = v.size; view.height = v.height || 420;
        view.compact = !!v.compact; view.focus = !!v.focus;
      }
    } catch (e) {}
    var s = null;
    try { s = localStorage.getItem('setu.sync'); } catch (e) {}
    applyView();
    setSync(s === null ? true : s === '1');
  }

  /* Gradio swaps components in and out as tabs change and events return, so
   * the toolbar can appear long after load and can be replaced afterwards.
   * Re-wiring on mutation is cheaper and more reliable than guessing a delay. */
  var obs = new MutationObserver(function () {
    wireToolbar();
    var p = panes();
    if (p[0] && p[0].getAttribute('data-setu') !== '1') {
      p[0].setAttribute('data-setu', '1');
      p[0].setAttribute('spellcheck', 'false');
    }
    if (p[1] && p[1].getAttribute('data-setu') !== '1') {
      p[1].setAttribute('data-setu', '1');
      p[1].setAttribute('spellcheck', 'false');
    }
  });

  function start() {
    restore();
    wireToolbar();
    obs.observe(document.body, { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }

  window.setuView = { zoom: zoom, reset: resetView, setSync: setSync,
                      state: function () { return { view: view, sync: sync.on }; } };
})();
