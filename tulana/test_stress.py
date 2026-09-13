#!/usr/bin/env python3
"""Ironclad stress test — the whole corpus, plus the edge cases.

Two things this exists to protect:

  * **A new board, class, language or script must not break an existing one.**
    Every dimension present is exercised, and the resolution logic is validated
    against ground truth rather than asserted.

  * **The original database must never be touched.** Proved by hashing every
    pre-existing table before and after running everything, and by reading the
    source for writes to them — not by trusting a comment.

    python3 test_stress.py
"""
import hashlib
import json
import os
import random
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

import blocks
import config
import db
import library

passed = failed = 0
random.seed(11)
PROTECTED = ("documents", "projects", "clips", "pairs", "labels",
             "pair_labels", "exports", "audit")


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"FAIL  {name}  {detail}")


def section(t):
    print(f"\n── {t} " + "─" * max(0, 58 - len(t)))


def fingerprint(con):
    out = {}
    for t in PROTECTED:
        try:
            rows = con.execute(f"SELECT * FROM {t} ORDER BY rowid").fetchall()
        except Exception:
            out[t] = "absent"
            continue
        blob = "|".join("~".join(str(v) for v in tuple(r)) for r in rows)
        out[t] = f"{len(rows)}:{hashlib.sha256(blob.encode()).hexdigest()[:16]}"
    return out


def reset_corpus_tables(con):
    """Start from a clean corpus.

    Each suite ingests deliberately odd books — malformed JSON, a zero-size
    page, an invented future board. Leaving them behind made the next suite's
    corpus-wide counts wrong, so a run's result depended on what had run
    before. Only the layout tables are cleared; the studio's own tables are
    never touched."""
    for t in ("pl_blocks", "pl_pages", "pl_books"):
        try:
            con.execute(f"DELETE FROM {t}")
        except Exception:
            pass
    con.commit()


def main():
    con = db.connect()
    blocks.ensure_schema(con)
    reset_corpus_tables(con)

    # ══ the database must be untouchable ══════════════════════════════════
    section("database safety")
    here = Path(__file__).parent
    for mod in ("blocks.py", "layout.py"):
        src = (here / mod).read_text(encoding="utf-8")
        writes = re.findall(
            r"(?:INSERT\s+(?:OR\s+\w+\s+)?INTO|UPDATE|DELETE\s+FROM|ALTER\s+TABLE|"
            r"DROP\s+TABLE)\s+([a-z_]+)", src, re.I)
        bad = sorted({w for w in writes if w in PROTECTED})
        check(f"{mod} never writes to a pre-existing table", not bad, str(bad))
        check(f"{mod} contains no ALTER or DROP",
              not re.search(r"ALTER\s+TABLE|DROP\s+TABLE", src, re.I))

    # seed real work, then run everything and compare
    library.scan(con, config.DATA_DIR, log=lambda m: None)
    pairs = library.pairable(con)
    if pairs:
        c = pairs[0]
        docs = con.execute("""SELECT id, language FROM documents
                              WHERE board=? AND class=? AND subject=?""",
                           (c["board"], c["class"], c["subject"])).fetchall()
        en = [d for d in docs if d["language"] == "English"]
        tg = [d for d in docs if d["language"] != "English"]
        if en and tg:
            # Re-runnable: a second run must reuse the seed rather than collide
            # with the UNIQUE constraint on (src_doc, tgt_doc).
            row = con.execute("SELECT id FROM projects WHERE src_doc=? AND tgt_doc=?",
                              (en[0]["id"], tg[0]["id"])).fetchone()
            if row:
                pid = row["id"]
            else:
                con.execute("""INSERT INTO projects(name, board, class, subject,
                               src_doc, tgt_doc, created_at) VALUES('stress',?,?,?,?,?,0)""",
                            (c["board"], c["class"], c["subject"],
                             en[0]["id"], tg[0]["id"]))
                pid = con.execute("SELECT id FROM projects WHERE src_doc=? AND tgt_doc=?",
                                  (en[0]["id"], tg[0]["id"])).fetchone()["id"]
            if not con.execute("SELECT 1 FROM pairs WHERE project_id=? AND label=?",
                               (pid, "must survive")).fetchone():
                con.execute("""INSERT INTO pairs(project_id, seq, label, created_at)
                               VALUES(?,1,'must survive',0)""", (pid,))
            con.commit()
    before = fingerprint(con)

    res = blocks.ingest(con, data_dir=config.DATA_DIR, log=lambda m: None)
    if not res["books"]:
        print("\nNo parsed-layout corpus found — place the parser output beside the "
              "data folder.")
        return 1
    try:
        import layout
        layout.ensure_schema(con)
    except Exception:
        pass
    con.commit()
    after = fingerprint(con)
    changed = [t for t in before if before[t] != after[t]]
    check("every pre-existing table is byte-identical after a full run",
          not changed, f"changed: {changed}")
    check("the seeded annotation survived",
          con.execute("SELECT COUNT(*) FROM pairs WHERE label='must survive'"
                      ).fetchone()[0] == 1)
    check("database integrity", con.execute("PRAGMA integrity_check").fetchone()[0] == "ok")
    check("no foreign key violations",
          len(con.execute("PRAGMA foreign_key_check").fetchall()) == 0)

    # ══ corpus coverage ═══════════════════════════════════════════════════
    section("corpus")
    s = blocks.stats(con)
    print(f"   {s['books']} books · {s['pages']:,} pages · {s['blocks']:,} blocks · "
          f"{s['books_with_pdf']} mapped to a PDF")
    check("books ingested", s["books"] > 0)
    check("pages ingested", s["pages"] > 0)
    check("blocks ingested", s["blocks"] > 0)
    rows = [dict(r) for r in con.execute("SELECT * FROM pl_books")]
    unresolved = [r["relpath"] for r in rows
                  if not (r["board"] and r["class"] and r["language"])]
    check("every book resolved board, class and language",
          not unresolved, f"{len(unresolved)}: {unresolved[:2]}")
    check("every language carries a script",
          all(r["script"] for r in rows if r["language"]))
    boards = sorted({r["board"] for r in rows if r["board"]})
    langs = sorted({r["language"] for r in rows if r["language"]})
    scripts = sorted({r["script"] for r in rows if r["script"]})
    classes = sorted({r["class"] for r in rows if r["class"]})
    print(f"   boards {boards}")
    print(f"   languages {langs}")
    print(f"   scripts {scripts} · classes {classes}")

    # ══ every dimension is exercised, not just counted ════════════════════
    section("every board, language and class")
    for b in boards:
        bk = [r for r in rows if r["board"] == b]
        check(f"board {b}: books resolve a class", all(r["class"] for r in bk),
              f"{sum(1 for r in bk if not r['class'])} without")
        d = blocks.page_blocks(con, bk[0]["id"], 0)
        check(f"board {b}: first page serves", isinstance(d.get("blocks"), list))
    for l in langs:
        bk = [r for r in rows if r["language"] == l]
        check(f"language {l}: has a script", all(r["script"] for r in bk))
        mid = bk[0]["num_pages"] // 2
        d = blocks.page_blocks(con, bk[0]["id"], mid)
        check(f"language {l}: a middle page serves", isinstance(d.get("blocks"), list))
    for c in classes:
        check(f"class {c}: at least one book", any(r["class"] == c for r in rows))

    # ══ language resolution validated against ground truth ════════════════
    section("language resolution, validated")
    def sample_text(bid, n=20000):
        t, size = [], 0
        for r in con.execute("""SELECT b.text FROM pl_blocks b
                                JOIN pl_pages p ON p.id=b.page_id
                                WHERE p.book_id=? AND b.text!='' LIMIT 800""", (bid,)):
            t.append(r[0]); size += len(r[0])
            if size > n:
                break
        return " ".join(t)
    ok = wrong = abstain = 0
    for r in rows:
        if not r["language"]:
            continue
        txt = sample_text(r["id"])
        if len(txt) < 200:
            continue
        got = blocks.infer_from_text(txt)["language"]
        if got == r["language"]:
            ok += 1
        elif got is None:
            abstain += 1
        else:
            wrong += 1
            print(f"      mismatch: {r['book'][:24]} is {r['language']}, read as {got}")
    print(f"   {ok} correct · {abstain} abstained · {wrong} wrong")
    check("text-based language resolution is never wrong", wrong == 0, f"{wrong} wrong")
    check("text-based resolution succeeds on most books", ok > abstain,
          f"{ok} vs {abstain}")
    # the discriminator must separate the two that share Devanagari
    hi = [r for r in rows if r["language"] == "Hindi"]
    mr = [r for r in rows if r["language"] == "Marathi"]
    if hi and mr:
        check("Hindi is not read as Marathi",
              blocks.infer_from_text(sample_text(hi[0]["id"]))["language"] in ("Hindi", None))
        check("Marathi is not read as Hindi",
              blocks.infer_from_text(sample_text(mr[0]["id"]))["language"] in ("Marathi", None))

    # ══ geometry, everywhere ══════════════════════════════════════════════
    section("geometry")
    for name, q in (
            ("no block falls outside its page",
             "SELECT COUNT(*) FROM pl_blocks WHERE fx0<-0.01 OR fy0<-0.01 OR fx1>1.01 OR fy1>1.01"),
            ("no block has inverted coordinates",
             "SELECT COUNT(*) FROM pl_blocks WHERE fx1<fx0 OR fy1<fy0"),
            ("no page has a zero or negative size",
             "SELECT COUNT(*) FROM pl_pages WHERE width<=0 OR height<=0"),
            ("no block has a null fraction",
             "SELECT COUNT(*) FROM pl_blocks WHERE fx0 IS NULL OR fy1 IS NULL")):
        n = con.execute(q).fetchone()[0]
        check(name, n == 0, f"{n} do")
    degenerate = con.execute(
        "SELECT COUNT(*) FROM pl_blocks WHERE (fx1-fx0)<=0 OR (fy1-fy0)<=0").fetchone()[0]
    check("degenerate blocks are rare enough to be noise",
          degenerate < s["blocks"] * 0.01, f"{degenerate} of {s['blocks']}")

    # ══ the PDF mapping ═══════════════════════════════════════════════════
    section("mapping onto the original PDFs")
    m = blocks.mapping_report(con, config.DATA_DIR)
    print(f"   {m['mapped']} of {m['books']} mapped · {len(m['missing'])} missing · "
          f"worst aspect delta {m['worst_aspect_delta_pct']}%")
    check("the mapping report accounts for every book",
          m["mapped"] + len(m["missing"]) == m["books"])
    check("every missing PDF is named with a reason",
          all(x.get("reason") and x.get("fix") for x in m["missing"]))
    check("nothing is badly enough skewed to misplace boxes", not m["skewed"],
          str([x["book"] for x in m["skewed"]][:3]))
    if m["mapped"]:
        # boxes must land inside the real page, at any DPI
        from pdflib import fitz
        sampled = 0
        for d in m["detail"][:8]:
            pdf = blocks._find_pdf(config.DATA_DIR, d["relpath"])
            if not pdf:
                continue
            pg = min(3, (d.get("pdf_pages") or 1) - 1)
            bl = blocks.page_blocks(con, d["id"], pg)
            if not bl["blocks"]:
                continue
            with fitz.open(pdf) as doc:
                rect = doc[pg].rect
            for dpi in (72, 150):
                W, H = rect.width * dpi / 72, rect.height * dpi / 72
                out = [b for b in bl["blocks"]
                       if b["fx1"] * W > W + 1 or b["fy1"] * H > H + 1]
                check(f"{d['book'][:18]} at {dpi} dpi: boxes stay on the page",
                      not out, f"{len(out)} escape")
            sampled += 1
        check("box placement sampled across books", sampled >= 3, f"{sampled} books")

    # ══ selection, including the awkward cases ════════════════════════════
    section("selection")
    check("an empty selection is handled",
          blocks.selection_text(con, [])["n_blocks"] == 0)
    check("unknown ids are ignored, not fatal",
          blocks.selection_text(con, [10**9, -1, 0])["n_blocks"] == 0)
    check("duplicate ids do not double-count",
          blocks.selection_text(con, [1, 1, 1])["n_blocks"] <= 1)
    ids = [r[0] for r in con.execute(
        "SELECT id FROM pl_blocks WHERE text!='' LIMIT 5")]
    if len(ids) >= 3:
        a = blocks.selection_text(con, ids)
        check("selection returns every chosen block", a["n_blocks"] == len(ids))
        check("selection is in reading order",
              [b["ord"] for b in a["blocks"]] == sorted(b["ord"] for b in a["blocks"]))
        check("selection does not depend on click order",
              blocks.selection_text(con, ids[::-1])["text"] == a["text"])
        check("selection text is non-empty when the blocks have text", a["n_chars"] > 0)
    big = [r[0] for r in con.execute("SELECT id FROM pl_blocks LIMIT 5000")]
    t0 = time.time()
    r = blocks.selection_text(con, big)
    dt = time.time() - t0
    check("a 5000-block selection works", r["n_blocks"] == len(big), f"{r['n_blocks']}")
    check("a large selection stays responsive", dt < 15, f"{dt:.2f}s")

    # ══ pages: first, last, beyond, negative ══════════════════════════════
    section("page edges")
    bk = rows[0]
    n = bk["num_pages"]
    check("page 0 serves", blocks.page_blocks(con, bk["id"], 0)["exists"] is not None)
    check("the last page serves",
          isinstance(blocks.page_blocks(con, bk["id"], n - 1).get("blocks"), list))
    beyond = blocks.page_blocks(con, bk["id"], n + 500)
    check("a page beyond the end says so rather than failing",
          beyond["exists"] is False and beyond["blocks"] == [])
    neg = blocks.page_blocks(con, bk["id"], -5)
    check("a negative page is handled", neg["exists"] is False)
    try:
        blocks.page_blocks(con, 10**9, 0)
        check("an unknown book raises", False)
    except ValueError:
        check("an unknown book raises cleanly", True)

    # ══ malformed input ═══════════════════════════════════════════════════
    section("malformed input")
    tmp = Path(tempfile.mkdtemp())
    (tmp / "notjson.json").write_text("{ this is not json", encoding="utf-8")
    (tmp / "wrongshape.json").write_text(json.dumps({"hello": "world"}), encoding="utf-8")
    (tmp / "emptypages.json").write_text(json.dumps(
        {"book": "EMPTY", "relpath": "CLASS-9/EMPTY_EN_9.pdf", "num_pages": 0,
         "pages": []}), encoding="utf-8")
    (tmp / "nastyblocks.json").write_text(json.dumps(
        {"book": "NASTY", "relpath": "CLASS-9/NASTY_EN_9.pdf", "num_pages": 1,
         "pages": [{"page": 0, "width": 0, "height": 0, "blocks": [
             {"order": 0, "label": "Paragraph", "bbox_xyxy": [10, 10, 5, 5],
              "conf": 2.0, "text": "inverted"},
             {"order": 1, "label": "Paragraph", "bbox_xyxy": ["x", "y", 1, 2],
              "text": "bad types"},
             {"order": 2, "label": None, "bbox_xyxy": [0, 0, 10, 10],
              "text": "\\u0000null byte and \ud83d\ude00 emoji"},
         ]}]}), encoding="utf-8")
    try:
        r2 = blocks.ingest(con, corpus=tmp, data_dir=config.DATA_DIR, log=lambda m: None)
        check("malformed JSON does not stop ingestion", True, f"{r2['books']} imported")
        check("unreadable files are reported", any("not readable" in p for p in r2["problems"])
              or r2["books"] < 4)
    except Exception as e:
        check("malformed JSON does not stop ingestion", False, str(e)[:80])
    check("a zero-size page did not poison the geometry",
          con.execute("SELECT COUNT(*) FROM pl_blocks WHERE fx0 IS NULL").fetchone()[0] == 0)
    shutil.rmtree(tmp, ignore_errors=True)

    # ══ unicode ═══════════════════════════════════════════════════════════
    section("unicode")
    for lang, probe in (("Bengali", "\u0997"), ("Devanagari", "\u0915"),
                        ("Tamil", "\u0b95"), ("Telugu", "\u0c15"),
                        ("Kannada", "\u0c95"), ("Malayalam", "\u0d15"),
                        ("Gurmukhi", "\u0a15"), ("Gujarati", "\u0a95"),
                        ("Odia", "\u0b15"), ("Perso-Arabic", "\u0627")):
        got, share = blocks.detect_script(probe * 60)
        check(f"{lang} script is detected", got == lang, f"got {got}")
    check("empty text detects nothing", blocks.detect_script("")[0] is None)
    check("digits alone detect nothing or Latin",
          blocks.detect_script("12345")[0] in (None, "Latin"))
    check("an emoji does not crash detection", blocks.detect_script("\U0001f600" * 20)[0] in (None, "Latin"))
    check("mixed Latin and Indic prefers the Indic script",
          blocks.detect_script("Hello world " * 5 + "\u0997" * 30)[0] == "Bengali")

    # ══ idempotency and re-entry ══════════════════════════════════════════
    section("re-running")
    # Count before and after the *same* corpus is re-read. Comparing against the
    # corpus total would be wrong: the malformed-input section above deliberately
    # added a book, and that is not a duplicate.
    base = con.execute("SELECT COUNT(*) FROM pl_blocks").fetchone()[0]
    base_books = con.execute("SELECT COUNT(*) FROM pl_books").fetchone()[0]
    again = blocks.ingest(con, data_dir=config.DATA_DIR, log=lambda m: None)
    now = con.execute("SELECT COUNT(*) FROM pl_blocks").fetchone()[0]
    check("re-ingesting gives the same book count", again["books"] == res["books"],
          f"{again['books']} vs {res['books']}")
    check("re-ingesting adds no rows", now == base, f"{base} -> {now}")
    check("re-ingesting adds no books",
          con.execute("SELECT COUNT(*) FROM pl_books").fetchone()[0] == base_books)
    check("relpath stays unique",
          con.execute("""SELECT COUNT(*) FROM (SELECT relpath FROM pl_books
                         GROUP BY relpath HAVING COUNT(*)>1)""").fetchone()[0] == 0)
    after2 = fingerprint(con)
    check("the pre-existing tables are still untouched after re-ingest",
          all(before[t] == after2[t] for t in before),
          str([t for t in before if before[t] != after2[t]]))

    # ══ pairing ═══════════════════════════════════════════════════════════
    section("pairing")
    pl = blocks.pairable(con)
    check("pairable combinations found", len(pl) > 0, f"{len(pl)}")
    for c in pl:
        eng = blocks.editions(con, c["board"], c["class"], c["subject"], "English")
        check(f"{c['label'][:38]} has both sides",
              bool(eng) and bool(c["target_languages"]))
    check("no combination is offered with only English",
          all(c["target_languages"] for c in pl))

    # ══ a future board and language ═══════════════════════════════════════
    section("extensibility")
    fut = Path(tempfile.mkdtemp())
    (fut / "future.json").write_text(json.dumps(
        {"book": "OD_OR_8", "relpath": "Odisha/Class 8/OD_OR_8.pdf", "num_pages": 1,
         "pages": [{"page": 0, "width": 1000, "height": 1400, "blocks": [
             {"order": 0, "label": "Paragraph", "bbox_xyxy": [10, 10, 900, 200],
              "conf": 0.9, "text": "\u0b13\u0b21\u0b3f\u0b06 " * 40}]}]}),
        encoding="utf-8")
    blocks.ingest(con, corpus=fut, data_dir=config.DATA_DIR, log=lambda m: None)
    nb = con.execute("SELECT * FROM pl_books WHERE book='OD_OR_8'").fetchone()
    check("a board added in future resolves", nb and nb["board"] == "OD",
          nb["board"] if nb else "not ingested")
    check("its language resolves", nb and nb["language"] == "Odia",
          nb["language"] if nb else "-")
    check("its script resolves", nb and nb["script"] == "Odia",
          nb["script"] if nb else "-")
    check("its class resolves", nb and nb["class"] == 8, str(nb["class"]) if nb else "-")
    shutil.rmtree(fut, ignore_errors=True)

    con.close()
    print(f"\n===== {passed} passed, {failed} failed =====")
    return failed


if __name__ == "__main__":
    sys.exit(main())
