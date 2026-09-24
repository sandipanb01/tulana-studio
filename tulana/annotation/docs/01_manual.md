# The annotator's manual

You do not need to have annotated anything before, and you do not need to know
what a database or a parser is. If you can read English and one Indian
language, you can do this work. Everything below is written for somebody
sitting down at Setu for the first time.

Read sections 1 to 6. The rest is there for when you hit something.

---

## 1. What you are being asked to do

A school textbook is published twice — once in English, once in an Indian
language. In principle the two books say the same thing on the same page. In
practice they were typeset by different teams, printed at different times, and
then read by a machine that got some of the words wrong.

Your job has two halves:

1. **Say whether the two sides really say the same thing.**
2. **Correct what the machine misread**, on either side.

That is all. You are not translating, not rewriting, not improving the
textbook. You are checking a machine's work against the printed page.

---

## 2. The screen

One screen, three parts, top to bottom.

**Step 1 — choose two textbooks.** Four dropdowns and a button. Once you press
**Open these two books** this folds itself away; click its title to bring it
back.

**The middle strip** holds three switches and, under them, where you are in
each book:

* *Let me correct the text* — off to begin with. Leave it off while you read;
  turn it on when you want to fix something.
* *Show me the printed page* — puts the real scanned page above the text.
* *Hide running heads, footers and page numbers* — on to begin with. These are
  furniture, not text, and nobody needs to check them.

**The two columns.** English on the left, the other language on the right. Each
column shows the pieces of text the machine found on one page of that book, in
reading order. Each column scrolls on its own.

Above each column: which chapter you are in, which page you are on, and
**◀ Previous page** / **Next page ▶** for that side alone.

---

## 3. Your first ten minutes

1. Type your name in **Your name**. It goes on the work you do.
2. Pick a board, a class and a subject. Pick a language on each side. Pick the
   two books.
3. Press **Open these two books**.
4. Read the first page on both sides. Do they say the same thing?
5. Under each piece of English text there is one question: **Do these two say
   the same thing?** Answer it.
6. Press **Next page ▶** under both columns, or **Both forward ▶▶** to move
   them together.

That is the whole loop. Everything else is for when it is not that simple.

---

## 4. The six answers

Under each piece of English text, pick one:

| Answer | Use it when |
|---|---|
| **Exact** | The two sides say the same thing. Small differences in punctuation or spacing do not matter. |
| **Needs correction** | They are meant to be the same, and one side has been misread — a wrong letter, a missing word, a mangled number. Fix it, then choose this. |
| **Missing or incomplete** | One side genuinely does not have this text. Some editions drop an exercise, or add one. |
| **Structural mismatch** | The text exists on both sides but has been cut up differently — one edition made one paragraph of what the other made two. |
| **Unclear** | You cannot tell. Say why in a note. |
| **Not applicable** | Neither side is really text — a stray mark, or a page number the machine mistook for a sentence. |

The question is asked once, on the English side, because English is the
reference. Answering it records the answer for both halves.

You may change an answer at any time. Nothing is final.

---

## 5. Correcting the text

Turn on **Let me correct the text**. Every piece of text becomes a box you can
type in.

Fix only what the machine got wrong. Do not:

* translate anything
* improve the wording
* correct the textbook's own mistakes
* add anything that is not printed on the page

If the printed page says something wrong, that is what the corpus should
record. You are matching the paper, not fixing the book.

**It saves itself.** When you click out of a box, it is saved, and a short line
under the switches says so. You never press a save button, and there is no
moment where your work is at risk.

**The machine's reading is never thrown away.** What the parser originally read
is kept separately, for ever. If you change something and want it back, press
**Put back what the parser read**, which appears under any box you have
changed.

---

## 6. When the two books do not line up

This is the part that surprises people, so it has its own section.

The two editions were printed separately. Measured across this corpus:

* Karnataka class 10 Kannada runs between 3 pages behind and 8 pages ahead,
  depending on the chapter.
* Punjab class 10 Punjabi drifts from level to 26 pages apart.
* Gujarat class 10 Gujarati is about 111 pages out from end to end.
* NCERT class 11 Hindi and Tamil Nadu class 10 Tamil share **no** chapter
  starting page at all with their English editions.

Chapter counts differ too — 13 against 16, 43 against 48, 27 against 20.

**None of that is a fault.** It is what happens when two teams produce two
editions. So Setu does not assume the two books march together.

### Moving the two sides apart

Each side has its own chapter list, its own page box and its own
**◀ Previous page** / **Next page ▶**. Moving one does not move the other.

So when English page 2 and the other edition's page 2 are plainly not the same
material, step the English side forward until you find the page that *is* the
same. Four clicks, and the two passages are side by side.

### Linking them

Once you have found two pages that answer each other, press
**⇄ These two pages match**.

Setu works out the distance between them — *the English edition runs 3 pages
ahead* — and from then on moving either side moves the other by exactly that
much. The line under the buttons always tells you where you stand, whether or
not you have linked anything.

**The link is saved**, and it belongs to the two books rather than to you. The
next person to open them starts where you left off instead of working it out
again. **Unlink** removes it.

### Moving both at once

**◀◀ Both back** and **Both forward ▶▶** move the two sides together, keeping
whatever distance you have put between them — linked or not.

---

## 7. The small grey line above each piece of text

It says three or four things:

* **What kind of thing it is** — paragraph, worked example, table, section
  title, and so on. There are 23 kinds. This is often the whole explanation for
  why two sides look different: a caption on one side and a paragraph on the
  other will never match.
* **Which page it is on** — the number printed on that page of that book.
* **How it stands** — either your answer, or *as the parser read it*, meaning
  nobody has touched it yet, or *corrected by hand* if somebody has.
* **no counterpart found** — this piece of text was never paired with anything.
  See section 8.

---

## 8. Text with no counterpart

About a quarter of the text in a typical pair of books has nothing opposite it.
Those pieces are shaded and marked **no counterpart found**.

This is usually not missing text. It is text that was *cut differently*: a
paragraph whole on one side is two pieces on the other, so the machine could
not line them up one to one.

When you see one, look at the other column for the same words. Nine times out
of ten they are there, a little above or below. That is a **Structural
mismatch**, not **Missing or incomplete** — and saying so is more useful,
because it records that the text exists and is merely in a different place.

---

## 9. Checking against the printed page

Turn on **Show me the printed page**. The real scanned page appears above the
text of each column, so you can read the machine's version against the paper.

The page number above each column is the number printed on that page of that
book, so it matches what you would turn to.

If Setu says the page is not on this machine, that is normal — the scans are
large and are often not downloaded. **The text does not depend on them.**
Everything else works exactly as before.

---

## 10. Several people at once

Everybody uses the same link and everybody gets their own session. What you are
reading, where you are in the book and what you have typed are invisible to
everyone else.

If two people correct the same piece of text at the same time, the second one
is told rather than silently overwritten, and nothing is lost — every version
is kept.

---

## 11. Notes

A note is worth writing whenever you choose **Unclear** or **Structural
mismatch**, because the next person to look at it has no idea what you saw.
Notes travel with the pair into every export.

---

## 12. What is never changed

* **The original PDFs.** Setu only reads them.
* **What the parser first read.** Kept for ever, separately from your
  corrections.
* **Every version of every correction.** Nothing is ever pruned.
* **Tulana's own earlier work** — the saved pairs and clippings from the block
  tool. Setu adds its own tables and writes to nothing that existed before it.

---

## 13. Saved work, and downloading it

**Saved work** lists everything judged so far in the open books. Click a row to
go to the page it sits on.

**Download** writes the annotations out in eleven formats — JSON Lines, JSON,
CSV, TSV, XML, plain text, Moses, TMX, Excel, Parquet and a Hugging Face
dataset — filtered by answer or by completeness, or all of them at once as a
zip.

Formats that can only hold true pairs say so, and report what they left out.

---

## 14. Pacing

This is reading work, and reading work does not go faster by hurrying. A page
where both sides agree takes a few seconds. A page where they do not can take
several minutes of hunting, and that hunting is the valuable part — it is what
nobody else can do.

Take breaks. Nothing is lost when you stop, because nothing was ever waiting to
be saved.

---

## 15. When to stop and ask

* A whole book that looks like a different subject on the two sides.
* Two editions where nothing lines up at any distance you try.
* Text in a script you do not read.
* Anything that makes you think *this cannot be right*.

Say so rather than guessing. A guess recorded as an answer is worse than a gap.

---

## 16. If something goes wrong

Setu tells you in a sentence what happened and what it means for your work. It
will not show you an error message full of code.

The one thing worth knowing: **your saved work is on the machine running Setu,
not in your browser.** Closing the tab, losing your connection or your laptop
going to sleep loses nothing.

If a page will not load, turn to another page and back. If that does not help,
tell whoever runs the server — and say which two books and which page, because
that is what lets them find it.
