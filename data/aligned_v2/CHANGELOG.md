# Changelog: aligned_v2 (built 2026-10-29 from data/aligned)

## Summary

- **Pages dropped:** 359 English pages (map_wrong 225, alignment_failed 113, nothing_matched 19, unparseable 2).
- **Units unlinked** because an English part is on a dropped page: 1375 units, 2950 blocks (both sides).
- **Markup restored:** 3302 translation blocks.
- Markup run: 3790 requests (one per English page), 10074 candidate blocks: 3302 accepted, 4407 rejected by the guard (the model changed content, so the original was kept), 2365 with no change proposed; 2012 proposed edits could not be placed (text not found exactly once).
- The guard was re-applied when building v2 (`scripts/markup_restore.py`, md5 `27d305f05ab23c4a0de213ee2cf49fd7`); 71 verdicts differ from those stored by the run, because the guard was tightened afterwards: it now also protects currency and other symbols (₹, □), and it no longer reads math such as `72 < 125 ... >` as an HTML tag (which had hidden an inserted word), and it requires image references (`<img src=...>`) to stay identical.
- Model `gemini-3.5-flash`, thinking `low`, prompt `prompts/markup_restore_v1.txt` (md5 `6ef1b286c51db33c3e50f959106381e1`); measured cost $32.50 (online price, not batch).

## Per pair

| pair | pages dropped | units unlinked | blocks with markup restored |
|---|---|---|---|
| AP10_sem1_en-te | 0 | 0 | 143 |
| AP10_sem2_en-te | 0 | 0 | 108 |
| GUJ10_en-gu | 24 | 68 | 155 |
| KER10_1_en-ml | 0 | 0 | 99 |
| KER10_2_en-ml | 0 | 0 | 90 |
| KT10_1_en-kn | 34 | 131 | 101 |
| KT10_2_en-kn | 25 | 92 | 89 |
| MH10_1_en-gu | 0 | 0 | 121 |
| MH10_1_en-hi | 0 | 0 | 103 |
| MH10_1_en-ka | 0 | 0 | 99 |
| MH10_1_en-mr | 0 | 0 | 115 |
| MH10_1_en-te | 0 | 0 | 115 |
| MH10_2_en-mr | 0 | 0 | 160 |
| MH9_1_en-gu | 0 | 0 | 98 |
| MH9_1_en-hi | 0 | 0 | 125 |
| MH9_1_en-ka | 0 | 0 | 106 |
| MH9_1_en-mr | 0 | 0 | 123 |
| MH9_1_en-te | 0 | 0 | 112 |
| PUN10_en-pa | 60 | 279 | 224 |
| PUN12_1_en-pa | 44 | 154 | 126 |
| TM10_en-ta | 51 | 248 | 227 |
| NCERT_1001_en-hi | 0 | 0 | 10 |
| NCERT_1002_en-hi | 0 | 0 | 10 |
| NCERT_1003_en-hi | 5 | 13 | 6 |
| NCERT_1004_en-hi | 1 | 0 | 10 |
| NCERT_1005_en-hi | 4 | 24 | 32 |
| NCERT_1006_en-hi | 6 | 26 | 16 |
| NCERT_1007_en-hi | 4 | 30 | 9 |
| NCERT_1008_en-hi | 3 | 19 | 16 |
| NCERT_1009_en-hi | 0 | 0 | 14 |
| NCERT_1010_en-hi | 1 | 8 | 14 |
| NCERT_1011_en-hi | 1 | 0 | 2 |
| NCERT_1012_en-hi | 1 | 5 | 14 |
| NCERT_1013_en-hi | 2 | 15 | 26 |
| NCERT_1014_en-hi | 1 | 3 | 22 |
| NCERT_1101_en-hi | 5 | 12 | 14 |
| NCERT_1102_en-hi | 5 | 19 | 18 |
| NCERT_1103_en-hi | 1 | 0 | 16 |
| NCERT_1104_en-hi | 3 | 10 | 3 |
| NCERT_1105_en-hi | 4 | 15 | 6 |
| NCERT_1106_en-hi | 3 | 0 | 11 |
| NCERT_1107_en-hi | 3 | 24 | 1 |
| NCERT_1108_en-hi | 3 | 4 | 10 |
| NCERT_1109_en-hi | 2 | 2 | 19 |
| NCERT_1110_en-hi | 0 | 0 | 20 |
| NCERT_1111_en-hi | 0 | 0 | 8 |
| NCERT_1112_en-hi | 7 | 22 | 18 |
| NCERT_1113_en-hi | 3 | 13 | 22 |
| NCERT_1114_en-hi | 4 | 21 | 25 |
| NCERT_1201_en-hi | 2 | 0 | 16 |
| NCERT_1202_en-hi | 3 | 8 | 5 |
| NCERT_1203_en-hi | 7 | 21 | 31 |
| NCERT_1204_en-hi | 2 | 11 | 13 |
| NCERT_1205_en-hi | 4 | 6 | 27 |
| NCERT_1206_en-hi | 4 | 9 | 29 |
| NCERT_1211_en-hi | 8 | 19 | 29 |
| NCERT_1212_en-hi | 0 | 0 | 7 |
| NCERT_1213_en-hi | 3 | 7 | 23 |
| NCERT_1214_en-hi | 8 | 21 | 22 |
| NCERT_1215_en-hi | 5 | 8 | 19 |
| NCERT_1216_en-hi | 1 | 0 | 18 |
| NCERT_1217_en-hi | 2 | 8 | 32 |

## changelog.jsonl

One JSON record per change:

- `page_dropped`: pair, file, page, reason, mapped_page, matched_pages, align_status_before, align_ids_removed
- `unit_removed`: pair, file, page, block_order, align_id, reason (one per block that lost its link)
- `markup_restored`: pair, file, page, block_order, align_id, before, after
