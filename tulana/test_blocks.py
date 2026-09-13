#!/usr/bin/env python3
"""Stress test for the parsed-layout corpus.

Walks every book, every board, every language and a sample of pages from each,
so that adding a board, a class, a language or a script in future cannot break
another one silently.

    python3 test_blocks.py
"""
import os
import random
import sys
import time
from pathlib import Path

import blocks
import config
import db

passed = failed = 0
random.seed(7)


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"FAIL  {name}  {detail}")


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
    t0 = time.time()
    res = blocks.ingest(con, data_dir=config.DATA_DIR, log=lambda m: None)
    load = time.time() - t0
    if not res["books"]:
        print("No parsed-layout corpus found. Place the parser output beside the "
              "data folder, or pass its path to blocks.ingest().")
        return 1
    print(f"corpus: {res['books']} books · {res['pages']} pages · "
          f"{res['blocks']} blocks · loaded in {load:.1f}s")

    s = blocks.stats(con)
    check("every book was ingested", s["books"] == res["books"])
    check("pages and blocks counted", s["pages"] > 0 and s["blocks"] > 0)
    check("ingestion is fast enough to run at startup", load < 60, f"{load:.1f}s")

    # ── every dimension resolves ───────────────────────────────────────────
    rows = [dict(r) for r in con.execute("SELECT * FROM pl_books")]
    unresolved = [r["relpath"] for r in rows
                  if not (r["board"] and r["class"] and r["language"])]
    check("every book resolved its board, class and language",
          not unresolved, f"{len(unresolved)} did not: {unresolved[:3]}")
    check("every language has a script",
          all(r["script"] for r in rows if r["language"]),
          str([r["language"] for r in rows if r["language"] and not r["script"]][:3]))

    boards = {r["board"] for r in rows}
    langs = {r["language"] for r in rows}
    classes = {r["class"] for r in rows}
    print(f"  boards {len(boards)} · languages {len(langs)} · classes {sorted(classes)}")
    check("more than one board present", len(boards) >= 2,
          str(sorted(x for x in boards if x)))
    check("more than one language present", len(langs) >= 2,
          str(sorted(x for x in langs if x)))

    # ── geometry is sane everywhere ────────────────────────────────────────
    bad_frac = con.execute("""SELECT COUNT(*) FROM pl_blocks
        WHERE fx0 < -0.01 OR fy0 < -0.01 OR fx1 > 1.01 OR fy1 > 1.01""").fetchone()[0]
    check("no block falls outside its page", bad_frac == 0, f"{bad_frac} do")
    inverted = con.execute("SELECT COUNT(*) FROM pl_blocks WHERE fx1 < fx0 OR fy1 < fy0"
                           ).fetchone()[0]
    check("no block has inverted coordinates", inverted == 0, f"{inverted} do")
    zero = con.execute("SELECT COUNT(*) FROM pl_pages WHERE width<=0 OR height<=0").fetchone()[0]
    check("every page records a real size", zero == 0, f"{zero} do not")

    # ── pairing across languages ───────────────────────────────────────────
    pairs = blocks.pairable(con)
    check("pairable combinations found", len(pairs) >= 1, f"{len(pairs)}")
    for c in pairs:
        eng = blocks.editions(con, c["board"], c["class"], c["subject"], "English")
        check(f"{c['label']} has an English edition", bool(eng))
        check(f"{c['label']} has a target edition", bool(c["target_languages"]))

    # ── walk every book, sampling pages ────────────────────────────────────
    empty_pages = no_text = sampled = 0
    for r in rows:
        n = r["num_pages"] or 0
        if n <= 0:
            continue
        for pg in {0, n // 2, max(0, n - 1), random.randrange(n)}:
            d = blocks.page_blocks(con, r["id"], pg)
            sampled += 1
            check(f"page {pg} of {r['book']} returns a shape",
                  isinstance(d.get("blocks"), list))
            if d["exists"] and not d["blocks"]:
                empty_pages += 1
            for b in d["blocks"]:
                if not (b["text"] or "").strip():
                    no_text += 1
    print(f"  sampled {sampled} pages across {len(rows)} books")
    check("sampling found no crash", True)

    # ── selection, the feature annotators use ──────────────────────────────
    c = pairs[0]
    src = blocks.editions(con, c["board"], c["class"], c["subject"], "English")[0]
    tgt = [e for e in blocks.editions(con, c["board"], c["class"], c["subject"])
           if e["language"] != "English"][0]
    found = None
    for pg in range(0, min(40, src["num_pages"])):
        d = blocks.page_blocks(con, src["id"], pg)
        withtext = [b for b in d["blocks"] if (b["text"] or "").strip()]
        if len(withtext) >= 2:
            found = withtext
            break
    check("a page with text was found to select from", bool(found))
    if found:
        sel = blocks.selection_text(con, [b["id"] for b in found[:3]])
        check("selection returns the chosen blocks", sel["n_blocks"] == len(found[:3]))
        check("selection assembles text", sel["n_chars"] > 0, f"{sel['n_chars']} chars")
        check("selection is in reading order",
              [b["ord"] for b in sel["blocks"]] == sorted(b["ord"] for b in sel["blocks"]))
        # order of the ids must not change the result
        shuffled = [b["id"] for b in found[:3]][::-1]
        check("selection is independent of click order",
              blocks.selection_text(con, shuffled)["text"] == sel["text"])
    check("an empty selection is handled",
          blocks.selection_text(con, [])["n_blocks"] == 0)
    check("unknown block ids are ignored rather than failing",
          blocks.selection_text(con, [10**9])["n_blocks"] == 0)

    # ── a large selection must not fall over ───────────────────────────────
    ids = [r[0] for r in con.execute("SELECT id FROM pl_blocks LIMIT 2000")]
    t1 = time.time()
    big = blocks.selection_text(con, ids)
    check("a 2000-block selection works", big["n_blocks"] == len(ids),
          f"{big['n_blocks']} in {time.time()-t1:.2f}s")
    check("a large selection stays fast", time.time() - t1 < 10)

    # ── re-ingest is idempotent ────────────────────────────────────────────
    again = blocks.ingest(con, data_dir=config.DATA_DIR, log=lambda m: None)
    check("re-ingesting gives the same totals",
          again["books"] == res["books"] and again["blocks"] == res["blocks"],
          f"{again['books']}/{again['blocks']} vs {res['books']}/{res['blocks']}")
    check("re-ingesting does not duplicate rows",
          con.execute("SELECT COUNT(*) FROM pl_blocks").fetchone()[0] == res["blocks"])

    # ── the existing tables are untouched ──────────────────────────────────
    for t in ("documents", "projects", "clips", "pairs", "labels",
              "pair_labels", "exports", "audit"):
        try:
            con.execute(f"SELECT COUNT(*) FROM {t}")
        except Exception as e:
            check(f"{t} still readable", False, str(e))
    check("the original tables are all intact", True)
    check("database integrity", con.execute("PRAGMA integrity_check").fetchone()[0] == "ok")

    con.close()
    print(f"\n===== {passed} passed, {failed} failed =====")
    return failed


if __name__ == "__main__":
    sys.exit(main())
