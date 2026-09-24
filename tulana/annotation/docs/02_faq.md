# Questions people actually ask

## Getting started

**Do I need to install anything?**
No. Setu runs in the browser. There is nothing to set up and no password.

**Do I need to know the Indian language?**
Ideally yes for the language you are checking. If you do not, you can still
correct obvious machine errors on the English side and mark the rest *Unclear*.

**Which side do I work on?**
Both. Either side can be wrong, because the same machine read both books.

**Where do I start?**
Choose a board, class and the language you are checking, press **Open these two
books**, and you are on the first pair. After that, **Next unchecked** — or the
<kbd>n</kbd> key — is the quickest way through.

**What is Tulana?**
The wider project this belongs to: a workspace for building parallel corpora
from Indian school textbooks. Setu is its annotation tool. The rest of Tulana —
page images, block selection, saved clippings — is at the `/studio` link the
server prints when it starts.

## Saving

**Do I have to save?**
No. Setu saves about half a second after you stop typing.

**How do I know it saved?**
The line to the right of the note box. Green "All changes saved" means your work
is on disk. It also saves whenever you click out of a box, whenever you set an
answer, whenever you move to another pair, and every few seconds while you type.

**What if I close the tab by accident?**
Anything the line said was saved is safe. Setu saves when you leave a box, when
you set an answer, when you move on, and on a timer while you type — so the most
you can lose is the last few seconds of typing in a box you never left.

**Setu says "Unsaved changes" and I need to leave right now.**
Press **Save changes**, or <kbd>Ctrl</kbd>+<kbd>S</kbd>, and wait for the line to
turn green.

**What if the power goes out mid-save?**
Setu asks the database to flush each save to disk before reporting success. A
save that said "saved" is on disk.

**What if the wifi drops?**
The bar turns yellow. Keep working — your edits are stored on this computer and
sent when the connection returns.

**I reloaded the page. Where is my workbook?**
Reloading starts a fresh session — choose the same two books again and you are
back where the work is. Everything you saved is there; the tool does not
remember which pair you were on across a reload.

## Editing

**Can I break something by typing in the wrong box?**
No. Every version is kept and the machine's original is never overwritten.
**Original** above any box puts it back.

**I deleted everything in a box.**
Click **Original**. It comes straight back.

**Should I fix spelling in the printed book?**
No. You are correcting what the machine *read*, not the book. If the page has a
mistake, the text should have the same mistake.

**The formula looks wrong. Do I fix it?**
Fix it if the machine misread it — a `2` that should be a `z`, a missing
brace. Leave it if the printed book prints it that way.

**Should I translate the missing side?**
No, never. An empty side means the text was not found, not that it needs
writing. Mark it *Missing or incomplete*.

**Can I add a pair that does not exist?**
Not directly. Use **Split** on an existing pair, then **Attach** the correct
text to each half.

## Statuses

**What is the difference between "Missing or incomplete" and "Structural mismatch"?**
Missing means text is absent. Mismatch means text is present on both sides but
they are not the same piece of the book.

**I clicked the wrong status.**
Click the correct one, or click the same one again to go back to unchecked.

**Does "Unclear" count as finished?**
Yes for progress, no for the corpus. It is a flag for a reviewer, and using it
honestly is better than guessing.

**Should I mark headers and page numbers?**
*Not applicable*, if they appear at all. Most are filtered out when the
workspace is created.

## Pairs and alignment

**How did Setu decide which texts go together?**
Mostly mathematics. A formula like `$2 \times 3 \times 7$` is written the same
way in Marathi as in English, so it anchors the two books to each other.
Secondly, numbers such as "1.2" in "Practice set 1.2". Everything between two
anchors is matched in reading order.

**How often is it right?**
On the page-parallel state-board editions, the anchored pairs land on the
correct page 99–100% of the time. The "in order" fills are less certain. About a
third of pairs get an anchor; the rest are filled.

**Why is everything one pair out?**
One edition merged two blocks the other kept separate. Use **Split** and
**Attach**, or mark it *Structural mismatch* and move on.

**Why are the same two texts in two different pairs?**
They should not be. Setu refuses to attach one segment to two rows in a
workspace. If you see it, report it.

**Can I rebuild the alignment?**
An administrator can, but it discards every answer in the workspace and will
refuse unless they explicitly force it. It is almost never the right move.

## Reading and the view

**The two boxes are too short / the text is too small.**
Use the grey bar above them: **+ Height** makes the boxes taller, **A+** makes
the text bigger. Both are remembered for next time.

**Why do both sides scroll when I scroll one?**
They are linked by default so the two stay together through a long passage.
Press **Scrolling: linked** to unlink them.

**The two sides drift apart when linked.**
They scroll by proportion, not line by line, because the two languages are
different lengths. On a very uneven pair, unlink them.

**Can I see just the two texts?**
**Compact** hides everything else; **Focus** hides the side panel too.

**How do I see the actual page from the book?**
**Check the printed page**, under either side.

## Browsing the two books apart

**The two textbooks do not line up at all. Page 2 on the left is nothing like
page 2 on the right.**
That is normal, and more common than you would think. The two editions were
printed by different teams; several pairs in this corpus run more than a hundred
pages apart, and some share no chapter starting page at all. Go to **Browse both
books**, where each side moves independently, and put the two pages next to each
other yourself.

**How do I move one side without moving the other?**
In **Browse both books**, each side has its own page box and its own
**◀ Previous page** / **Next page ▶**. They are independent unless you have
linked them.

**How do I move both at once?**
**◀◀ Both back** and **Both forward ▶▶**, under the two sides. They keep
whatever gap the two sides are currently sitting at.

**I found the two pages that match. How do I keep them together?**
Press **⇄ Link these two pages**. From then on moving either side moves the
other by the same amount.

**Does the link survive me closing the tab?**
Yes. It is saved to the workspace, so the next person to open those two books
starts where you left off. **Unlink** removes it, for everyone.

**How do I know how far apart they are?**
The line under the controls always says: *English p64 is sitting beside p76 — an
offset of −12.*

**The chapter lists on the two sides are different lengths.**
They often are. One edition may carry a chapter the other does not, or number
them differently. Both lists are shown exactly as each book has them; that is
the point.

**Can I work on chapter 3 on the left and something else on the right?**
Yes. The chapter is chosen per side.

**Why is a block marked "not paired"?**
The aligner found nothing opposite it. About a quarter of this corpus is like
that, because the two editions break their paragraphs in different places. It is
information, not an error — and it is the thing this view exists to let you find.

**One of the columns will not scroll.**
Both columns scroll independently; if one appears stuck it is because that page
is short enough to fit. Try a page with more text on it, or turn on **Show the
whole chapter at once**.

**The page I am on is blank.**
Some pages are a single full-page illustration, and Setu holds only text. Step
to the next page.

## Navigation and search

**How do I get to a specific page?**
Type `page 42` into the search box and press Enter.

**How do I find a pair a colleague mentioned?**
Type `#450` and press Enter, then click the row in the results.

**Search finds nothing, but I can see the word.**
Check **Only show** and **Jump to a chapter** on the left — one of them may be
narrowing the search. Set both back to "Everything".

**Nothing happens when I type in the search box.**
Press Enter. Search runs when you submit, not on every keystroke, so that a
long word does not fire a query per letter.

**The contents list shows English chapters but I am reading Marathi.**
That is deliberate. Both sides share the left book's table of contents, so the
sidebar is a single map of one book rather than two competing ones.

## Working with other people

**Can two of us work on the same book?**
Yes. Work on different chapters and you will never collide.

**What if we edit the same pair?**
Whoever saves second is shown both versions and chooses. Nothing is overwritten
and both stay in the history.

**Two tabs of my own browser?**
Treated as two people, for safety. You will get the same choice.

**Does anyone else see what I am typing before I save?**
No. Your session is your own; nothing you type is visible to anybody until it
is saved, and then only when they load that pair.

**Can I see who did what?**
**What changed on this pair** → **Show the history** lists every edit with a
name and a time. Put your name in the box at the top left so your work is
attributed.

## Exporting

**Which format should I use?**
JSON Lines for machine learning, Excel for review by a person, Moses or TMX for
a translation toolchain.

**Why does my Moses file have fewer pairs than the workspace?**
Moses is two line-aligned files, so a pair with one empty side cannot be
represented — a blank line would shift every later line and ruin the alignment.
Those pairs are left out and the download tells you how many.

**Can I export only what I have finished?**
Yes: choose "Everything you have checked", or "Only Exact" for the cleanest set.

**Can I export one chapter?**
Click the chapter in the sidebar first. The export follows the filter.

**Does the export contain the machine's original text?**
Yes, in `source_original` and `target_original`, beside your corrected text.

**A format says it needs an extra package.**
Parquet needs `pyarrow` and Excel needs `openpyxl` on the server. The name of
the package is in the list; ask whoever runs the server to install it.

## Data and safety

**Can I lose my work?**
The design says no: saves are flushed to disk, every version is kept, nothing is
overwritten, and edits are mirrored on your own computer until the server
confirms them.

**Does Setu change the original textbook files?**
No. It never writes to the PDFs or to the parsed files, and it never modifies
the text the parser extracted.

**Does it touch the rest of Tulana Studio's data?**
No. Setu's tables all begin with `setu_`, and it only ever reads the others.

**Where is my work stored?**
In the SQLite database on the server, plus a copy of anything unsent in your own
browser.

**Is my name a login?**
No. It is a label attached to your changes so work can be attributed. There are
no passwords.

## Display

**The text is boxes instead of letters.**
A font for that script is missing on your computer. Install Noto Sans for that
language.

**The text is too small.**
<kbd>Ctrl</kbd> + <kbd>+</kbd>, or the **A+** button. Your choice is remembered.

**Is there an undo?**
<kbd>Ctrl</kbd>+<kbd>Z</kbd> inside a text box, like anywhere else. To go
further back, use the history on that pair.

**Can I use it on a tablet?**
Yes. Below about 900 pixels the two sides stack one above the other.

**Is there a dark mode?**
It follows your system setting.

## When things break

**The page will not load.**
Reload. If it stays blank the server is probably not running.

**A red bar says a save failed.**
It retries by itself. Your text is safe locally meanwhile. If it persists, tell
whoever runs the server.

**Setu says "Something went wrong at our end".**
An unexpected error. The details are in the server log, not on your screen —
that is deliberate, so nothing internal leaks into a browser. Report roughly
when it happened.

**The workspace says it has no pairs.**
The filters on the left are excluding everything. Set **Only show** and **Jump
to a chapter** back to "Everything".

**How do I report a problem?**
Note the pair number — the `#30` at the top — and what you expected. If it is
about one pair, put it in that pair's note as well, so it travels with the data.
