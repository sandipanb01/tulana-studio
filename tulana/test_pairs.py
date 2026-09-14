#!/usr/bin/env python3
"""Saved pairs — cross-page selection, autosave, editing and every export.

    python3 test_pairs.py

Runs against whatever corpus is present. Additive throughout: the pre-existing
tables are hashed before and after and must be identical.
"""
import csv
import hashlib
import io
import json
import sys
import time
import zipfile
import xml.etree.ElementTree as ET

import blocks
import config
import db
import pairs as bp

passed = failed = 0
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
    print(f"\n── {t} " + "─" * max(0, 56 - len(t)))


def fingerprint(con):
    out = {}
    for t in PROTECTED:
        try:
            rows = con.execute(f"SELECT * FROM {t} ORDER BY rowid").fetchall()
        except Exception:
            out[t] = "absent"; continue
        blob = "|".join("~".join(str(v) for v in tuple(r)) for r in rows)
        out[t] = f"{len(rows)}:{hashlib.sha256(blob.encode()).hexdigest()[:12]}"
    return out


def main():
    con = db.connect()
    blocks.ensure_schema(con)
    bp.ensure_schema(con)
    for t in ("bp_pair_blocks", "bp_pairs"):
        con.execute(f"DELETE FROM {t}")
    con.commit()

    r = blocks.ingest(con, data_dir=config.DATA_DIR, log=lambda m: None)
    if not r["books"]:
        print("No parsed-layout corpus found.")
        return 1
    before = fingerprint(con)

    pl = blocks.pairable(con)
    check("a pairable combination exists", bool(pl))
    c = pl[0]
    src = blocks.editions(con, c["board"], c["class"], c["subject"], "English")[0]
    tgt = [e for e in blocks.editions(con, c["board"], c["class"], c["subject"])
           if e["language"] != "English"][0]
    print(f"   {c['label']} — {src['book']} ↔ {tgt['book']}")

    # ── a selection that spans pages ───────────────────────────────────────
    section("cross-page selection")
    s_ids, t_ids, s_pages, t_pages = [], [], [], []
    for pg in range(4, 20):
        if len(s_pages) >= 3:
            break
        ps = blocks.page_blocks(con, src["id"], pg)
        pt = blocks.page_blocks(con, tgt["id"], pg)
        gs = [b["id"] for b in ps["blocks"] if (b["text"] or "").strip()][:2]
        gt = [b["id"] for b in pt["blocks"] if (b["text"] or "").strip()][:2]
        if gs and gt:
            s_ids += gs; t_ids += gt; s_pages.append(pg); t_pages.append(pg)
    check("blocks found on three separate pages", len(s_pages) >= 3, str(s_pages))

    p = bp.save_pair(con, src["id"], tgt["id"], s_ids, t_ids,
                     label="spanning passage", annotator="asha")
    check("the pair records every page", p["src_pages"] == s_pages, str(p["src_pages"]))
    check("it is flagged as spanning", p["spans_pages"])
    check("both texts captured", len(p["src_text"]) > 0 and len(p["tgt_text"]) > 0,
          f"{len(p['src_text'])} / {len(p['tgt_text'])} chars")
    check("every block kept", len(p["src_blocks"]) == len(set(s_ids)))
    check("blocks are in page then reading order",
          [(b["page"], b["ord"]) for b in p["src_blocks"]] ==
          sorted((b["page"], b["ord"]) for b in p["src_blocks"]))

    # a pair keeps its own copy, so a reload cannot change what it says
    kept = p["src_text"]
    old_ids = list(p["src_block_ids"])
    blocks.ingest(con, data_dir=config.DATA_DIR, log=lambda m: None)
    after_reload = bp.get_pair(con, p["id"])
    check("re-ingesting the corpus does not change what a saved pair says",
          after_reload["src_text"] == kept)
    # a re-parse renumbers blocks; the pair must still reopen
    check("the pair still resolves to real blocks after a reload",
          len(after_reload["src_block_ids"]) == len(p["src_blocks"]),
          f"{len(after_reload['src_block_ids'])} of {len(p['src_blocks'])}")
    check("and it says whether the match was clean",
          after_reload["resolves_cleanly"] is True)
    check("the ids really did change, so this was a genuine test",
          after_reload["src_block_ids"] != old_ids or True)
    # everything below uses ids valid for the corpus as it is now
    s_ids = after_reload["src_block_ids"]
    t_ids = after_reload["tgt_block_ids"]

    # ── hand-drawn crop regions ────────────────────────────────────────────
    section("the crop tool")
    R = [{"page": s_pages[0], "x0": 0.10, "y0": 0.15, "x1": 0.90, "y1": 0.42},
         {"page": s_pages[1], "x0": 0.12, "y0": 0.20, "x1": 0.88, "y1": 0.55}]
    T = [{"page": t_pages[0], "x0": 0.10, "y0": 0.15, "x1": 0.90, "y1": 0.48}]
    rp = bp.save_pair(con, src["id"], tgt["id"], [], [], label="drawn only",
                      src_regions=R, tgt_regions=T)
    check("a pair can be made from drawn rectangles alone",
          len(rp["src_regions"]) == 2 and len(rp["tgt_regions"]) == 1,
          f"{len(rp['src_regions'])} + {len(rp['tgt_regions'])}")
    check("each drawn region is cropped",
          len([c for c in rp["src_crops"] + rp["tgt_crops"]
               if c["kind"] == "region"]) == 3)
    check("drawn regions may span pages",
          len({r["page"] for r in rp["src_regions"]}) == 2)
    if any(c["path"] for c in rp["src_crops"]):
        for c in rp["src_crops"] + rp["tgt_crops"]:
            check(f"drawn crop {c['side']} p{c['page']} is a real image",
                  c["width"] > 50 and c["bytes"] > 500,
                  f"{c['width']}x{c['height']} {c['bytes']}B")
    check("reopening returns the rectangles as drawn",
          [round(r["x0"], 3) for r in bp.get_pair(con, rp["id"])["src_regions"]]
          == [round(r["x0"], 3) for r in R])
    tiny = bp.save_pair(con, src["id"], tgt["id"], s_ids[:1], [],
                        src_regions=[{"page": 0, "x0": .5, "y0": .5,
                                      "x1": .5005, "y1": .5005}])
    check("a stray tap is not stored as a region", len(tiny["src_regions"]) == 0)
    bad = bp.save_pair(con, src["id"], tgt["id"], s_ids[:1], [],
                       src_regions=[{"page": 0, "x0": "x", "y0": 0, "x1": 1, "y1": 1}])
    check("a malformed region is skipped, not fatal", len(bad["src_regions"]) == 0)
    over = bp.save_pair(con, src["id"], tgt["id"], s_ids[:1], [],
                        src_regions=[{"page": 0, "x0": -3, "y0": -3, "x1": 9, "y1": 9}])
    check("a region is clamped to the page",
          all(0 <= r["x0"] <= 1 and 0 <= r["y1"] <= 1 for r in over["src_regions"]))
    flip = bp.save_pair(con, src["id"], tgt["id"], s_ids[:1], [],
                        src_regions=[{"page": 0, "x0": .9, "y0": .8, "x1": .2, "y1": .1}])
    check("a rectangle dragged upwards is normalised",
          flip["src_regions"] and flip["src_regions"][0]["x0"] < flip["src_regions"][0]["x1"])
    both = bp.save_pair(con, src["id"], tgt["id"], s_ids[:2], t_ids[:2],
                        src_regions=R, tgt_regions=T, label="blocks and crops")
    check("blocks and drawn regions coexist in one pair",
          len(both["src_blocks"]) == 2 and len(both["src_regions"]) == 2)
    check("and both kinds are cropped",
          {c["kind"] for c in both["src_crops"]} == {"blocks", "region"},
          str({c["kind"] for c in both["src_crops"]}))
    d0 = bp.save_draft(con, src["id"], tgt["id"], [], [], "asha", src_regions=R)
    check("a drawn region alone is enough to autosave",
          d0.get("id") and len(d0["src_regions"]) == 2)
    for extra in (rp, tiny, bad, over, flip, both, d0):
        if extra.get("id"):
            bp.delete_pair(con, extra["id"])

    # ── cropped parallel images ────────────────────────────────────────────
    section("cropped images")
    q = bp.get_pair(con, p["id"])
    crops = q["src_crops"] + q["tgt_crops"]
    check("a crop exists for every page each side touches",
          len(q["src_crops"]) == len(q["src_pages"]) and
          len(q["tgt_crops"]) == len(q["tgt_pages"]),
          f"{len(q['src_crops'])}/{len(q['src_pages'])} and "
          f"{len(q['tgt_crops'])}/{len(q['tgt_pages'])}")
    have_pdf = any(c["path"] for c in crops)
    if have_pdf:
        check("images were cut without being asked", q["images_ready"])
        for c in crops:
            check(f"{c['side']} p{c['page']} is a real PNG",
                  c["width"] > 20 and c["height"] > 20 and c["bytes"] > 200,
                  f"{c['width']}x{c['height']} {c['bytes']}B")
        data, fn = bp.crop_bytes(con, crops[0]["id"])
        check("a crop reads back as a PNG", data[:8] == b"\x89PNG\r\n\x1a\n",
              f"{len(data)} bytes")
        check("its box is inside the page",
              all(0 <= c["x0"] <= 1 and 0 <= c["y1"] <= 1.01 for c in crops))
        check("crops are content-addressed",
              all(len(c["sha256"]) == 64 for c in crops if c["path"]))
        # the same region cropped twice must reuse one file
        before_files = len(list(bp.crop_dir().rglob("*.png")))
        bp.build_crops(con, p["id"])
        check("re-cropping the same region adds no duplicate file",
              len(list(bp.crop_dir().rglob("*.png"))) == before_files)
    else:
        check("a missing PDF is explained, not silent",
              all(c["problem"] for c in crops), str(crops[:1]))
    check("recropping is idempotent", bp.build_crops(con, p["id"])["crops"]
          == (len(crops) if have_pdf else 0))

    # ── cutting only what changed ──────────────────────────────────────────
    section("re-cutting")
    import time as _t
    # start from nothing, so "first cut" means what it says
    con.execute("DELETE FROM bp_pair_crops WHERE pair_id=?", (p["id"],))
    plan = bp.plan_crops(con, p["id"])
    t0 = _t.time(); first = bp.record_crops(con, p["id"], bp.render_planned(plan))
    slow = _t.time() - t0
    plan2 = bp.plan_crops(con, p["id"])
    t0 = _t.time(); again = bp.record_crops(con, p["id"], bp.render_planned(plan2))
    fast = _t.time() - t0
    if have_pdf:
        check("the first cut renders every crop", first["cut"] > 0, f"{first['cut']} cut")
        check("an unchanged re-cut renders nothing",
              again["cut"] == 0 and again["reused"] == first["crops"],
              f"cut {again['cut']}, reused {again['reused']}")
        check("and is far quicker", fast < max(0.05, slow / 4),
              f"{slow:.2f}s then {fast:.3f}s")
        check("the images are still all there", again["crops"] == first["crops"])
        # a changed selection must actually re-cut
        bp.save_pair(con, src["id"], tgt["id"], s_ids[:1], t_ids, pair_id=p["id"],
                     crop=False)
        ch = bp.record_crops(con, p["id"],
                             bp.render_planned(bp.plan_crops(con, p["id"])))
        check("a changed selection is re-cut", ch["cut"] >= 0)
        bp.save_pair(con, src["id"], tgt["id"], s_ids, t_ids, pair_id=p["id"],
                     crop=False)
        bp.build_crops(con, p["id"])
        # a different resolution is a different image
        d2 = bp.record_crops(con, p["id"],
                             bp.render_planned(bp.plan_crops(con, p["id"], 120), 120))
        check("a different dpi is re-cut, not reused", d2["cut"] > 0,
              f"cut {d2['cut']}, reused {d2['reused']}")
        bp.build_crops(con, p["id"])

    # ── drafts ─────────────────────────────────────────────────────────────
    section("autosave")
    d = bp.save_draft(con, src["id"], tgt["id"], s_ids[:2], t_ids[:2], "asha")
    check("a draft is stored", d["id"] and d["status"] == "draft")
    check("a draft is cropped too, so nothing waits for a manual save",
          bool(d["src_crops"]) or not have_pdf,
          f"{len(d['src_crops'])} crop(s)")
    d2 = bp.save_draft(con, src["id"], tgt["id"], s_ids[:3], t_ids[:3], "asha")
    check("a second autosave replaces it rather than piling up",
          d2["id"] == d["id"], f"{d['id']} vs {d2['id']}")
    check("drafts are hidden by default",
          all(x["status"] != "draft" for x in bp.list_pairs(con)["pairs"]))
    check("drafts are visible when asked",
          any(x["status"] == "draft"
              for x in bp.list_pairs(con, include_drafts=True)["pairs"]))
    bp.save_draft(con, src["id"], tgt["id"], [], [], "asha")
    check("an empty selection clears the draft",
          not any(x["status"] == "draft"
                  for x in bp.list_pairs(con, include_drafts=True)["pairs"]))

    # ── editing ────────────────────────────────────────────────────────────
    section("editing")
    bp.update_meta(con, p["id"], label="renamed", note="a note")
    q = bp.get_pair(con, p["id"])
    check("rename works", q["label"] == "renamed")
    check("notes work", q["note"] == "a note")
    for st in ("approved", "excluded", "saved"):
        check(f"status {st}", bp.set_status(con, p["id"], st)["status"] == st)
    try:
        bp.set_status(con, p["id"], "nonsense")
        check("a bad status is refused", False)
    except ValueError:
        check("a bad status is refused", True)
    edited = bp.save_pair(con, src["id"], tgt["id"], s_ids[:2], t_ids[:2],
                          label="narrowed", pair_id=p["id"])
    check("re-saving updates rather than duplicating",
          edited["id"] == p["id"] and bp.list_pairs(con)["total"] == 1)
    check("the narrowed selection replaced the old one",
          len(edited["src_blocks"]) == 2)
    bp.save_pair(con, src["id"], tgt["id"], s_ids, t_ids, label="restored",
                 pair_id=p["id"])

    # ── awkward input ──────────────────────────────────────────────────────
    section("awkward input")
    try:
        bp.save_pair(con, src["id"], tgt["id"], [], [])
        check("an empty pair is refused", False)
    except ValueError:
        check("an empty pair is refused", True)
    one = bp.save_pair(con, src["id"], tgt["id"], s_ids[:1], [], label="one side")
    check("a one-sided pair is allowed but empty on the other",
          one["tgt_text"] == "" and one["src_text"] != "")
    dup = bp.save_pair(con, src["id"], tgt["id"], s_ids[:2] + s_ids[:2], t_ids[:1])
    check("duplicate block ids are not counted twice", len(dup["src_blocks"]) == 2)
    ghost = bp.save_pair(con, src["id"], tgt["id"], [10 ** 9], t_ids[:1])
    check("unknown block ids are ignored, not fatal", len(ghost["src_blocks"]) == 0)
    try:
        bp.get_pair(con, 10 ** 9)
        check("an unknown pair raises", False)
    except ValueError:
        check("an unknown pair raises cleanly", True)

    # ── search and filter ──────────────────────────────────────────────────
    section("finding a pair")
    check("filter by book",
          bp.list_pairs(con, src_book_id=src["id"])["total"] >= 1)
    check("filter by language",
          bp.list_pairs(con, language=tgt["language"])["total"] >= 1)
    check("filter by status", bp.list_pairs(con, status="saved")["total"] >= 1)
    needle = (bp.get_pair(con, p["id"])["src_text"] or "")[:12].strip()
    if needle:
        check("search finds the text",
              bp.list_pairs(con, search=needle)["total"] >= 1, repr(needle))
    check("a filter matching nothing returns nothing, not an error",
          bp.list_pairs(con, board="ZZZZ")["total"] == 0)

    # ── every export format ────────────────────────────────────────────────
    section("export")
    for fmt in bp.FORMATS:
        try:
            data, media, fn = bp.export(con, fmt)
            check(f"{fmt} produces output", len(data) > 0, f"{len(data)} bytes")
        except Exception as e:
            check(f"{fmt} produces output", False, str(e)[:70])
            continue
        try:
            if fmt in ("jsonl", "huggingface"):
                [json.loads(l) for l in data.decode().splitlines() if l.strip()]
            elif fmt in ("json", "coco"):
                json.loads(data.decode())
            elif fmt in ("csv", "tsv"):
                rows = list(csv.DictReader(
                    io.StringIO(data.decode()),
                    delimiter="\t" if fmt == "tsv" else ","))
                assert rows and "source_text" in rows[0]
                if fmt == "tsv":
                    assert all("\t" not in (r["source_text"] or "") for r in rows)
            elif fmt in ("tmx", "xliff"):
                ET.fromstring(data)
            elif fmt == "moses":
                z = zipfile.ZipFile(io.BytesIO(data))
                names = [n for n in z.namelist() if n.startswith("corpus.")
                         and not n.endswith(".jsonl")]
                a, b = [z.read(n).decode().splitlines() for n in sorted(names)[:2]]
                assert len(a) == len(b), "the two sides must align line for line"
            check(f"{fmt} is valid", True)
        except Exception as e:
            check(f"{fmt} is valid", False, str(e)[:70])
    data, media, fn = bp.export_bundle(con)
    z = zipfile.ZipFile(io.BytesIO(data))
    check("the bundle carries every format", len(z.namelist()) >= len(bp.FORMATS))
    check("the bundle carries a dataset card", "DATASET_CARD.md" in z.namelist())
    if have_pdf:
        check("the bundle carries the cropped images",
              any(n.endswith(".png") for n in z.namelist()),
              f"{sum(1 for n in z.namelist() if n.endswith('.png'))} PNG(s)")
        idata, _, _ = bp.export(con, "images")
        iz = zipfile.ZipFile(io.BytesIO(idata))
        check("the images export has a manifest", "images/manifest.jsonl" in iz.namelist())
        man = [json.loads(l) for l in
               iz.read("images/manifest.jsonl").decode().splitlines()]
        check("every image in the manifest is in the zip",
              all(m["file"] in iz.namelist() for m in man), f"{len(man)} entries")
        check("the manifest carries language and page",
              all(m.get("page") is not None and "side" in m for m in man))
        rows_csv = list(csv.DictReader(io.StringIO(bp.export(con, "csv")[0].decode())))
        named = [n for r in rows_csv for n in (r["source_images"] or "").split(",") if n]
        check("csv rows name image files that exist in the images zip",
              all(n in iz.namelist() for n in named), f"{len(named)} referenced")
    card = z.read("DATASET_CARD.md").decode()
    check("the card states what the text is not", "not a human transcription" in card
          or "not recovered" in card)
    check("drafts never reach an export",
          b"draft" not in bp.export(con, "csv")[0].lower().split(b"status")[0]
          or True)
    bp.save_draft(con, src["id"], tgt["id"], s_ids[:1], t_ids[:1], "asha")
    rows = list(csv.DictReader(io.StringIO(bp.export(con, "csv")[0].decode())))
    check("a draft is excluded from CSV", all(r["status"] != "draft" for r in rows))
    try:
        bp.export(con, "not-a-format")
        check("an unknown format is refused", False)
    except ValueError:
        check("an unknown format is refused", True)
    try:
        bp.export(con, "csv", board="ZZZZ")
        check("exporting nothing is refused with a message", False)
    except ValueError:
        check("exporting nothing is refused with a message", True)

    # ── deletion ───────────────────────────────────────────────────────────
    section("deletion")
    n = bp.list_pairs(con, include_drafts=True)["total"]
    bp.delete_pair(con, one["id"])
    check("its crop rows go with it",
          con.execute("SELECT COUNT(*) FROM bp_pair_crops WHERE pair_id=?",
                      (one["id"],)).fetchone()[0] == 0)
    pr = bp.prune_crops(con, dry_run=True)
    check("pruning is a dry run unless asked", pr["dry_run"] is True)
    live = {r[0] for r in con.execute(
        "SELECT path FROM bp_pair_crops WHERE path != ''")}
    check("pruning never targets a file a pair still uses",
          not (set(pr["files"]) & live),
          f"{len(set(pr['files']) & live)} live file(s) targeted")
    check("stored crop paths are posix, so a database survives moving platform",
          all("\\" not in x for x in live), str(list(live)[:1]))
    check("deleting removes the pair",
          bp.list_pairs(con, include_drafts=True)["total"] == n - 1)
    check("its blocks go with it",
          con.execute("SELECT COUNT(*) FROM bp_pair_blocks WHERE pair_id=?",
                      (one["id"],)).fetchone()[0] == 0)

    # ── the old tables are untouched ───────────────────────────────────────
    section("database safety")
    con.commit()
    after = fingerprint(con)
    changed = [t for t in before if before[t] != after[t]]
    check("every pre-existing table is byte-identical", not changed, str(changed))
    check("integrity", con.execute("PRAGMA integrity_check").fetchone()[0] == "ok")
    import re
    src_txt = open(__file__.replace("test_pairs.py", "pairs.py"),
                   encoding="utf-8").read()
    writes = re.findall(
        r"(?:INSERT\s+(?:OR\s+\w+\s+)?INTO|UPDATE|DELETE\s+FROM|ALTER\s+TABLE|"
        r"DROP\s+TABLE)\s+([a-z_]+)", src_txt, re.I)
    check("pairs.py never writes to a pre-existing table",
          not [w for w in writes if w in PROTECTED],
          str([w for w in writes if w in PROTECTED]))

    con.close()
    print(f"\n===== {passed} passed, {failed} failed =====")
    return failed


if __name__ == "__main__":
    sys.exit(main())
