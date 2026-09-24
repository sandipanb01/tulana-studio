# The annotator's manual

Everything you need, in the order you will need it. You do not have to read it
all before you start — sections 1 to 6 are enough for your first hour.

---

## 1. What Setu is for

Setu shows you the same textbook twice: the English edition on the left, and
the same book in an Indian language on the right.

A machine has already read both books and pulled the text off the pages. It did
a good job most of the time and a poor job some of the time. Your work is to:

1. **Fix the text** where the machine misread the page.
2. **Say whether the two sides match** — whether the right-hand text really is
   the same piece of the book as the left-hand text.

That is the whole job. There is nothing to install, nothing to configure, and
nothing you can break.

## 2. What you are looking at

The screen is a list of **pairs**. Each pair is one box with two halves:

- **Left** — the source, usually English.
- **Right** — the target, the Indian-language edition.

Both halves can be typed in. Below each pair is a row of buttons for saying
what you think of it, and a box for a note.

The little label at the top of each pair tells you where it came from:

| Label | What it means |
|---|---|
| **suggested** | Setu found strong evidence these two go together — usually a formula that appears in both. |
| **in order** | Setu placed these together because of where they sit between two suggested pairs. Less certain. |
| **one side only** | Setu could not find a partner. One half is empty. |
| **yours** | You changed this pair yourself. |

Treat "suggested" as a good guess and "in order" as a guess. Neither is a fact
until you have looked.

## 3. Your first pair

1. Read the left text. Read the right text.
2. If either one has an obvious mistake — a missing word, a broken formula, a
   letter that should be a number — click into the box and fix it.
3. Click the button that describes the pair. That is it; move to the next one.

You do not need to save. Setu saves while you type.

## 4. The six answers

These are the only six things you can say about a pair. Pick the first one that
fits.

**Exact** — the two sides say the same thing. Nothing needs changing.

**Needs correction** — they match, but something in the text is wrong: a typo, a
wrong digit, a garbled formula. Use this *after* you have fixed the text, so
that somebody reviewing knows the pair was repaired rather than born perfect.

**Missing or incomplete** — part of the text is missing on one side, or one side
is empty and you could not find what belongs there.

**Structural mismatch** — both sides have real text, but they are not the same
piece of the book. Sometimes one edition puts a question and its answer in one
block while the other splits them in two; that is a structural mismatch.

**Unclear** — you cannot tell. Perhaps the scan is unreadable, perhaps you do
not know the language well enough. Leave a note and move on. Somebody will come
back to it. Using this is not a failure; guessing is.

**Not applicable** — this does not need annotating at all. Page headers, picture
captions, decoration, publisher addresses.

To undo an answer, press the same button again. It goes back to unchecked.

## 5. Fixing text

Click into either box and type. Some rules:

- **Keep the mathematics exactly as it is.** Text like `$x^2 + 3x = 0$` is a
  formula. The dollar signs and backslashes matter. If a formula is wrong, fix
  what is wrong inside it and leave the rest alone.
- **Keep the table markup.** Text starting with `<table>` is a table. Change the
  words inside the cells, not the tags.
- **Do not translate.** You are correcting what the machine read off the page,
  not producing a better translation. If the printed book says something odd,
  the text should say the same odd thing.
- **Do not tidy.** Extra line breaks, odd spacing and strange punctuation are
  usually on the page too.

If you make a mess of a box, click **Original** above it. That puts back
exactly what the machine read, however many times you have edited since.

## 6. Moving around

**Previous** and **Next** step one pair at a time. **Next unchecked** skips
everything anybody has already answered — it is the fastest way through a book.

From the keyboard:

| Key | What it does |
|---|---|
| <kbd>Alt</kbd>+<kbd>→</kbd> / <kbd>Alt</kbd>+<kbd>←</kbd> | next / previous pair |
| <kbd>j</kbd> / <kbd>k</kbd> | the same, one hand |
| <kbd>n</kbd> | next pair nobody has checked |
| <kbd>1</kbd>…<kbd>6</kbd> | set the answer — the number is printed on each button |
| <kbd>Ctrl</kbd>+<kbd>S</kbd> | save right now |
| <kbd>Ctrl</kbd>+<kbd>+</kbd> / <kbd>Ctrl</kbd>+<kbd>−</kbd> | bigger / smaller text |
| <kbd>Ctrl</kbd>+<kbd>0</kbd> | back to the normal view |

The number keys only work when you are **not** typing in a text box, so typing
"1" into a paragraph can never change your answer by accident.

<kbd>Ctrl</kbd>+<kbd>Z</kbd> undoes your typing, exactly as in any other text
box. Setu deliberately does not take that key over: your browser's own undo
knows every keystroke you made, which is finer-grained than anything the tool
could offer.

## 6a. Making the text comfortable to read

The grey bar above the two panes controls how they look. None of it changes
your work — it is yours, it is remembered, and nobody else sees it.

**Scrolling: linked / separate.** Linked is the default: scrolling one side
scrolls the other to the same relative place, so the two stay together through
a long passage. Press it to unlink them when the two sides are very different
lengths and you want to read one on its own.

**A−  A+  Reset** make the text smaller and larger. **− Height** and
**+ Height** make the two boxes shorter and taller — useful on a small screen,
or when you want to see a whole exercise at once.

**Compact** hides everything except the two texts. **Focus** hides the side
panel as well. Both are good for long stretches of work; press again to bring
things back.

## 7. The sidebar

**Show** — the coloured chips filter the list. Click "Not checked yet" to see
only the pairs nobody has looked at. Click it again to turn the filter off. The
number on each chip is how many pairs have that answer.

**Contents** — the book's chapters and sections. Click a chapter to work through
only that chapter. The `12/340` beside each chapter is how many of its pairs
have been checked.

The contents follow the **left-hand** book. When the right-hand edition
organises things differently, the sidebar still shows the left book's chapters,
so the two of you are always looking at the same map.

## 8. Searching

The search box takes more than words:

| What you type | What you get |
|---|---|
| `quadratic` | every pair containing that word, on either side |
| `"perfect square"` | that exact phrase |
| `संच` | works in any script — type in the language you are reading |
| `page 42` | everything on page 42 of either book |
| `chapter 3` | everything in chapter 3 |
| `1.2` | section, exercise or practice set 1.2 |
| `#450` | pair number 450 |

Search looks at both the original text and your corrections, so a typo you have
already fixed is still findable by its new spelling.

## 8a. Checking the printed page

Sometimes the text alone cannot answer the question: is that a 5 or an S? Does
that table really have four columns? Under each pane there is **Check the
printed page**. It shows you the piece of the scanned book that the text came
from, with a little of the page around it so you can see where you are.

It opens below the two panes and does not touch your text — you can leave it
open while you keep typing.

If it says the PDF has not been downloaded, that is normal on a new
installation: the scanned books are large and are fetched separately. Tell
whoever set up the server; the text side of your work is unaffected.

## 9. When a pair has the wrong partner

This happens. The aligner is a guess, and on about one pair in twenty it guesses
wrong.

When that happens, mark it **Structural mismatch** and write a short note
saying what you saw. The pairing itself is fixed by whoever maintains the
corpus, using the tools in the rest of Tulana Studio; your note is what tells
them where to look.

## 10. When one side is empty

An empty side means Setu could not find a partner. It does not mean the text
does not exist.

Before you mark it *Missing or incomplete*, press **Next** and **Previous**
once each. Very often the partner is sitting in the neighbouring pair, one step
away, and what you are really looking at is a **Structural mismatch** between
the two — which is a more useful answer, because it says the text exists and is
merely in the wrong place.

If the text genuinely is not in the other edition — some books drop an exercise,
or add one — then *Missing or incomplete* is right.

## 10a. When the two editions are pages apart

Sometimes the problem is not one pair. It is that the whole book has slipped.

The two editions were printed separately. They were typeset separately, they
number their chapters differently, and several of them carry chapters the other
does not have at all. Measured across this corpus: the Karnataka class 10 pair
runs between three pages behind and eight pages ahead depending on the chapter;
the Punjab pair drifts from level to twenty-six pages apart; the Gujarat pair is
about a hundred and eleven pages out from end to end. The NCERT class 11 and
Tamil Nadu class 10 pairs share no chapter starting page at all. Chapter counts
differ too — thirteen against sixteen, forty-three against forty-eight.

None of that is a fault in the books. It is what happens when two editions are
produced by two teams.

**Browse both books** is the tab for it. It shows the two editions as two
separate documents rather than as matched pairs:

* Each side has **its own chapter list**, in that edition's own language and
  numbering. You will sometimes see a chapter on one side that simply is not on
  the other; that is real, and worth a note.
* Each side has **its own page box** and its own **◀ Previous page** /
  **Next page ▶**. Moving one side does not move the other.
* Each side **scrolls on its own**.
* **◀◀ Both back** and **Both forward ▶▶** move the two together, keeping
  whatever gap you have put between them.

So the case that used to be impossible now takes four clicks: you are looking at
English page 2 and the other edition's page 2 and they are plainly not the same
material; you step the English side forward until page 4 shows the passage you
are reading on the right; and there they are, side by side.

### Linking two pages

Once you have found two pages that answer each other, press
**⇄ Link these two pages**.

Setu records the gap between them — "English is 3 pages ahead" — and from then
on moving either side moves the other by exactly that much. The bar under the
controls always tells you where you stand, whether or not you have linked
anything: *English p64 is sitting beside p76 — an offset of −12.*

The link is **saved**, not remembered for the afternoon. It belongs to the
workspace, so the next annotator to open those two books starts where you left
off instead of working it out again. **Unlink** removes it for everyone.

If you move the sides after linking, the bar says so and offers to take the new
offset; press **⇄ Link these two pages** again to keep it.

### What the blocks tell you

Each piece of text carries a small line above it: what kind of block it is
(paragraph, worked example, table, section title — twenty-three kinds), which
page it is on, and which pair it belongs to. A block the aligner never managed
to pair is marked **not paired** and shaded. Those are not errors to report —
about a quarter of this corpus is one-sided, because the two editions cut their
paragraphs in different places — but they are exactly what you are hunting for
when a passage seems to have gone missing.

A block that has been judged shows its answer. A block that has not shows
nothing, and the count above the column — *10 blocks · 3/10 judged* — tells you
how much of the page is done.

**Hide running heads, footers and page numbers** is on by default and strips the
furniture. Turn it off if you are checking whether a running header was parsed
correctly.

**Show the whole chapter at once** turns one side from a single page into the
whole chapter, with page dividers, for when you want to read rather than
compare.

## 11. Notes

The note box takes a sentence about why you chose what you chose. It is worth
writing one whenever you pick *Unclear* or *Structural mismatch*, because the
next person to look has no idea what you saw. Notes travel with the pair into
every export.

## 12. Saving, and why you never have to think about it

Setu saves about half a second after you stop typing. The bar along the bottom
says "Saving…" and then "All changes saved".

Underneath, every save is also written to your own computer the instant you
type it. So:

- **Closing the tab** is safe. Your work is already sent.
- **A crash** is safe. Next time you open Setu it offers to restore anything
  that never reached the server.
- **Losing the network** is safe. The bar turns yellow, your edits keep being
  stored locally, and Setu keeps trying. When the connection comes back
  everything goes out.
- **Turning off the computer mid-save** is safe. Setu asks the database to
  flush every save to disk before it reports success, so "saved" means saved.

## 13. Version history

Every version of every box is kept, for ever. Nothing is overwritten.

Open **What changed on this pair** below the buttons and press **Show the
history**. You get every version with who made it and when, and a comparison
against what the machine originally read.

**Restore the original**, above either pane, puts back exactly what the machine
read — however many times you have edited since. Restoring is itself recorded,
so you can undo an undo.

## 14. When two people edit the same pair

Setu does not stop two people working on the same pair — locking people out
causes more trouble than it prevents. Instead it refuses to let one person
silently overwrite the other.

If somebody saves a pair while you are typing in it, the line at the right says
**Someone else changed this pair**, and both versions appear below the buttons,
side by side. Two buttons let you choose: **Keep what I typed** or **Keep the
saved version**. Nothing is lost either way, and both versions stay in the
history.

If you open the same pair in two tabs of your own browser, the same thing
happens. The two tabs are treated as two people, which is the safe assumption.

## 15. What is never changed

The text the machine originally read is stored separately from your edits and is
never modified, no matter how much you type. Every export carries both, in
`source_original` and `target_original` columns beside your corrected
`source_text` and `target_text`.

This means an experiment can always be re-run against the raw extraction, and a
mistake made in this tool can never destroy the underlying data.

## 16. Progress

The chip at the top right is the whole workspace: how many pairs have an answer,
out of how many.

A pair counts as done once it has any answer, including *Unclear* and *Not
applicable*. Only "Not checked yet" is unfinished.

## 17. Exporting

The **Download** tab. Choose which pairs, then a format.

| Format | Use it for |
|---|---|
| JSON Lines | training data; one object per line |
| JSON | one document with everything |
| CSV | opening in Excel |
| TSV | tab-separated tools |
| XML | tools that want structured markup |
| Plain text | proofreading on paper |
| Moses | the classic two-file parallel corpus |
| TMX | translation tools such as OmegaT |
| Excel | reviewing in a spreadsheet, with wrapped text |
| Parquet | loading into pandas or Spark |
| Hugging Face | pushing a dataset to the Hub |

Formats marked **both sides only** — Moses, TMX, plain text, Hugging Face —
describe *parallel* data and cannot represent a pair with an empty side. Those
pairs are left out, and the download tells you how many. This is deliberate: a
blank line in a Moses file shifts every later line out of alignment and quietly
ruins the corpus.

"Download every format as one zip" gives you all of them at once.

## 18. Filtering an export

Common things people want:

- **Only finished work** — choose "Everything you have checked".
- **Only the clean pairs** — choose "Only Exact".
- **Only usable training data** — "Exact and Needs correction", and tick "Only
  pairs that have text on both sides".
- **One chapter** — pick it in **Jump to a chapter** first, then choose
  "Only this chapter".

## 19. Reading mathematics

Roughly half the text in these books contains mathematics, written in a LaTeX-
like notation.

| You see | It means |
|---|---|
| `$...$` | a formula inside a line |
| `$$...$$` | a formula on its own line |
| `\frac{a}{b}` | a over b |
| `x^2`, `x_1` | superscript, subscript |
| `\times`, `\neq`, `\therefore` | ×, ≠, ∴ |
| `\begin{matrix}...\end{matrix}` | a matrix |

You do not need to understand it to work with it. Compare the two sides
character by character: the mathematics is usually *identical* in both languages,
so any difference is either a genuine difference in the books or a mistake by
the machine.

The ∑ mark in a pair's header means that side contains mathematics; ⊞ means it
contains a table.

## 19a. Reviewing what has been done

The **Saved work** tab lists every pair in the open workbook, with its answer,
when it was last changed and by whom. Filter it by answer, or to just the pairs
somebody has edited, and sort it by most recently changed to see what a
colleague did this morning. Click any row to open that pair back in
**Annotate**.

## 20. Working in your own script

Type in whichever script you are reading. Setu stores everything as Unicode and
normalises it so that the same word typed two different ways compares as the
same word.

For right-to-left scripts — Urdu, for instance — the box switches direction
automatically, and the cursor and alignment go with it. That comes from the
script recorded for the book, not from a list of languages, so a new one works
the day its textbooks are added.

If the text looks like a row of empty boxes, your computer is missing a font for
that script rather than the text being missing. Installing Noto Sans for that
language fixes it.

## 21. Pacing

An experienced annotator does 150–300 pairs an hour on a familiar book. Do not
chase that number on your first day.

Two habits that help:

- Work chapter by chapter rather than roaming. Context carries over.
- Use <kbd>n</kbd> to move to the next unchecked pair rather than scrolling. It
  keeps you from re-reading the same pairs.

## 22. When to stop and ask

- The same kind of mistake appears in dozens of pairs — that is a parser problem
  worth reporting, not dozens of individual fixes.
- Whole pages are missing from one edition.
- You are unsure whether something counts as *structural mismatch* or *missing*
  — pick one, write a note, keep going. Consistency matters more than which one
  you chose.

## 23. Reviewing somebody else's work

Filter by status to see only what you want to review, and use **View changes**
to see what was altered from the machine's original. A reviewer changing a
status is recorded in the history alongside the original annotator's.

## 24. Your name

Type it into the box at the top right. It is stored on this computer and
attached to every change you save, so work can be attributed and questions can
be asked later. It is a label, not a login — Setu has no passwords and no
accounts.

## 25. If something goes wrong

- **"Could not save"** — the save will be retried. Press **Save changes** to
  try immediately. Do not close the tab until it says saved.
- **"Someone else changed this pair"** — see section 14. Nothing is lost.
- **A pair looks wrong after a reload** — open **What changed on this pair**.
  Every version is there and any of them can be put back.
- **The page is blank** — reload it. If it is still blank, the server is
  probably not running; tell whoever started it.
- **The printed page will not show** — usually the scanned PDFs have not been
  downloaded on the server. Your text work is unaffected.
- **You think you lost work** — you almost certainly did not. Check the history
  on that pair first.
