#!/usr/bin/env python3
"""Naming robustness — every board, every language, every plausible file name.

A textbook that is in the folder but not in the dropdown is the worst kind of
bug: nothing is broken, nothing errors, the work simply cannot be done. This
suite exists so that adding a board or a language in future cannot reintroduce
it silently.

    python3 test_naming.py
"""
import sys
from pathlib import Path

import config
import library

R = Path("/data")
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"FAIL  {name}  {detail}")


def infer(rel):
    return library.infer(R / rel, R)


def main():
    # ── every language, in the short-code convention already in use ─────────
    codes = {"en": "English", "hi": "Hindi", "bn": "Bengali", "mr": "Marathi",
             "ta": "Tamil", "te": "Telugu", "kn": "Kannada", "ml": "Malayalam",
             "gu": "Gujarati", "pa": "Punjabi", "or": "Odia", "as": "Assamese",
             "ur": "Urdu", "sa": "Sanskrit"}
    for code, name in codes.items():
        for board in ("KER", "PUN", "MH", "TM", "GUJ", "KT", "AP", "BA"):
            m = infer(f"board_pdfs/{board}_{code}_10.pdf")
            check(f"{board}_{code}_10 resolves language",
                  m["language"] == name, f"got {m['language']}")
            check(f"{board}_{code}_10 resolves board and class",
                  m["board"] and m["class"] == 10,
                  f"board={m['board']} class={m['class']}")

    # ── full language names, which people use at least as often ─────────────
    for word, name in (("malayalam", "Malayalam"), ("punjabi", "Punjabi"),
                       ("bengali", "Bengali"), ("assamese", "Assamese"),
                       ("odia", "Odia"), ("kannada", "Kannada"),
                       ("telugu", "Telugu"), ("tamil", "Tamil"),
                       ("gujarati", "Gujarati"), ("marathi", "Marathi"),
                       ("hindi", "Hindi"), ("urdu", "Urdu")):
        m = infer(f"board_pdfs/Kerala_Class10_{word}_Maths.pdf")
        check(f"full language name '{word}'", m["language"] == name, str(m["language"]))

    # ── the ways people write a class ───────────────────────────────────────
    for rel, want in (
            ("board_pdfs/Kerala_Class10_Malayalam.pdf", 10),
            ("board_pdfs/Kerala_Class_10_Malayalam.pdf", 10),
            ("board_pdfs/Kerala-class-9-malayalam.pdf", 9),
            ("board_pdfs/SCERT_Kerala_Std10_Malayalam.pdf", 10),
            ("board_pdfs/Kerala_Grade7_Malayalam.pdf", 7),
            ("board_pdfs/Kerala_Class_X_Malayalam.pdf", 10),
            ("board_pdfs/kerala_XII_malayalam.pdf", 12),
            ("board_pdfs/KER_ML_10_1.pdf", 10),
            ("board_pdfs/Kerala/Class 10/Malayalam/maths.pdf", 10),
            ("board_pdfs/Punjab/Grade 7/Punjabi/science.pdf", 7)):
        check(f"class from {Path(rel).name}", infer(rel)["class"] == want,
              f"got {infer(rel)['class']}")

    # ── board and language codes that collide ───────────────────────────────
    for rel, board, lang in (
            ("board_pdfs/GUJ_EN_10.pdf", "GJ", "English"),
            ("board_pdfs/GUJ_GJ_10.pdf", "GJ", "Gujarati"),
            ("board_pdfs/PUN_EN_10.pdf", "PB", "English"),
            ("board_pdfs/PUN_PU_10.pdf", "PB", "Punjabi"),
            ("board_pdfs/KER_EN_10.pdf", "KL", "English"),
            ("board_pdfs/KER_ML_10.pdf", "KL", "Malayalam")):
        m = infer(rel)
        check(f"{Path(rel).name} keeps board and language apart",
              m["board"] == board and m["language"] == lang,
              f"board={m['board']} lang={m['language']}")

    # ── subjects ────────────────────────────────────────────────────────────
    for word, want in (("maths", "Mathematics"), ("mathematics", "Mathematics"),
                       ("science", "Science"), ("physics", "Physics"),
                       ("chemistry", "Chemistry"), ("biology", "Biology"),
                       ("history", "History"), ("geography", "Geography")):
        m = infer(f"board_pdfs/Kerala_Class10_Malayalam_{word}.pdf")
        check(f"subject '{word}'", m["subject"] == want, m["subject"])

    # ── existing names must not regress ─────────────────────────────────────
    for rel, board, cls, lang in (
            ("Boardwise_PDF_class10_Maths/CLASS-10/MH_MR_9_1.pdf", "MH", 9, "Marathi"),
            ("Boardwise_PDF_class10_Maths/CLASS-10/AP_EN-TEL_10_SEM1.pdf", "AP", 10, "English"),
            ("input/eng/10/1001.pdf", "NCERT", 10, "English"),
            ("input/hin/12/1205.pdf", "NCERT", 12, "Hindi")):
        m = infer(rel)
        check(f"existing name {Path(rel).name} still resolves",
              m["board"] == board and m["class"] == cls and m["language"] == lang,
              f"{m['board']} {m['class']} {m['language']}")

    # ── a name with nothing usable must be reported, not silently dropped ───
    m = infer("board_pdfs/random_textbook.pdf")
    check("an unnameable file yields no false board or class",
          not (m["board"] and m["class"] and m["language"]),
          f"{m['board']} {m['class']} {m['language']}")

    print(f"\n===== {passed} passed, {failed} failed =====")
    return failed


if __name__ == "__main__":
    sys.exit(main())
