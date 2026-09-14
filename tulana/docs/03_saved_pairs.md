# Saved pairs

Everything you have saved, newest first.

Each card shows the pair's number, its name, its status, the pages each side
came from, **the cropped images side by side**, and the first part of both
texts. A pair drawn from more than one page is marked **spans pages** and has
one image per page on each side.

The images are the point: reading Devanagari against English in two columns of
plain text tells you little, while the two passages as they appear in the books
tell you immediately whether the alignment is right.

## Statuses

**draft** — kept automatically while you were working, never saved by hand.
Drafts are hidden unless you tick *show drafts*, and they are excluded from
every export.

**saved** — you pressed Save pair. In the corpus.

**approved** — someone has checked it. Use this when a second pair of eyes has
confirmed the alignment; you can then export approved pairs only.

**excluded** — kept but left out. For a pair you no longer trust but do not want
to lose. Restore it at any time.

## What you can do

**Rename** — give the passage a name that means something later. *Practice set
1.1* beats *pair 47*.

**Open in Blocks** — puts the selection back on the pages it came from, so a
correction is an adjustment rather than starting again. Change what is selected
and press Save pair; the same pair is updated, not duplicated.

**Approve**, **Exclude**, **Restore** — move the pair between statuses.

**Delete** — removes it permanently. There is no undo, which is why exclude
exists. The image files are left alone, because they are named by content and
another pair over the same passage may share one; an administrator clears
unreferenced files deliberately with `POST /api/pairs/crops/prune?apply=true`.

**Try again** — appears when a pair has no image because the PDF was missing
when it was saved. Cuts them now.

## Finding a pair

Filter by textbook, language or status, or search the text itself — the search
looks in both languages and in the pair's name.

## What a pair remembers

Each pair keeps its own copy of the text, not just a reference to the blocks.
Re-running the document parser renumbers blocks; a pair you approved must not
quietly change what it says because the corpus was reloaded underneath it.

It also keeps every block's box and page, so the pair can be exported as layout
training data, not only as text — and so a pair whose block ids were renumbered
by a corpus reload can still be reopened, matched by page and reading position.
