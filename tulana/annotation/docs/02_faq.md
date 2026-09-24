# Questions people actually ask

## Getting started

**Where do I start?**
Type your name, pick a board, class and subject, pick a language and a book on
each side, press **Open these two books**. The chooser folds away and the two
columns appear.

**I opened a board and the other boxes are empty.**
That board has only one language in the corpus, so there is nothing to pair it
with. Boards that can be paired are listed first; the ones that cannot say so.

**The right-hand language list is missing a language.**
Every Indian language is offered. The ones with no textbook in the corpus yet
are marked as such — they are there so the work does not need changing when
those books arrive.

**Do I need to press save?**
No. There is no save button. Clicking out of a box saves it, and a line under
the switches says so.

## The two columns

**Why is there only one screen now?**
There used to be two — one for judging a pair, one for reading the books. They
disagreed constantly about where you were, so they were merged. The page is now
the unit: what you see is what you judge.

**How do I correct text?**
Turn on **Let me correct the text**. Every piece of text becomes a box.

**Can I correct the Indian-language side too?**
Yes. Both sides are editable.

**Where did the answer dropdown go on the right-hand side?**
There is one question per pair, and it is asked on the English side because
English is the reference. Answering it records the answer for both halves.

**A block is shaded and says "no counterpart found".**
The machine could not pair it. About a quarter of a typical pair of books is
like that, because the two editions break their paragraphs in different places.
Look in the other column a little above or below — the text is usually there.

**One of the columns will not scroll.**
Both columns scroll independently. If one seems stuck, that page is short
enough to fit.

## Pages that do not line up

**Page 2 on the left is nothing like page 2 on the right.**
Normal, and more common than you would think. Several pairs in this corpus run
more than a hundred pages apart, and two share no chapter starting page at all.
Move one side until you find the page that matches.

**How do I move one side without moving the other?**
Each side has its own page box and its own **◀ Previous page** /
**Next page ▶**. They are independent unless you have linked them.

**How do I move both at once?**
**◀◀ Both back** and **Both forward ▶▶**. They keep whatever distance the two
sides are sitting at.

**I found the two pages that match. How do I keep them together?**
Press **⇄ These two pages match**. From then on, moving either side moves the
other by the same distance.

**Does that survive me closing the tab?**
Yes. It is saved against the two books, so the next person starts where you
left off. **Unlink** removes it.

**The chapter lists on the two sides are different lengths.**
They often are. One edition may carry a chapter the other does not, or number
them differently. Both lists are shown exactly as each book has them.

**Can I work on chapter 3 on the left and something else on the right?**
Yes. The chapter is chosen per side.

## The printed page

**The page number does not match my book.**
It should — the number above each column is the number printed on that page. If
it is out by one, say so immediately; that is a fault worth stopping for.

**It says the page is not on this machine.**
The scans are large and often are not downloaded. Everything except the picture
works exactly as before. Whoever runs the server can fetch them with
`git lfs pull`.

**The page is blank.**
Some pages are a single full-page illustration and Setu holds only text. Step
to the next page.

## Answers

**What is the difference between "Missing or incomplete" and "Structural
mismatch"?**
*Missing* means the text is genuinely not in the other edition. *Structural
mismatch* means it is there but cut up differently. If you can find the words
in the other column, it is a structural mismatch.

**I chose the wrong answer.**
Choose a different one. Nothing is final, and every change is kept.

**Do I have to answer every block?**
No. Unanswered means "nobody has looked at this yet", which is honest and
useful. A guess is worse than a gap.

## Corrections

**How much should I correct?**
Only what the machine misread. Do not translate, do not improve the wording,
and do not correct the textbook's own mistakes — the corpus should record what
is printed.

**I changed something and want it back.**
Press **Put back what the parser read**, under any box you have changed.

**Is the machine's original reading lost when I correct it?**
Never. It is kept in a separate place, for ever, and every version of every
correction is kept too.

**Somebody else changed the same block while I was typing.**
Setu tells you rather than overwriting either version. Turn the page and back
to see theirs; yours is in the history.

## Working with other people

**Can several of us use the same link?**
Yes. Everybody gets their own session. What you are reading and what you have
typed are invisible to everyone else.

**Will we overwrite each other?**
No. A save that would land on top of somebody else's is refused and both are
kept.

**Whose name goes on the work?**
Whatever you typed in **Your name**.

## Getting the data out

**How do I download what we have done?**
The **Download** tab. Eleven formats, filtered by answer or by completeness, or
all of them at once as a zip.

**Which format should I use?**
JSON Lines for a training pipeline, Excel for somebody who wants to read it,
TMX for a translation tool, Moses for machine-translation training.

**Some pairs were left out of my download.**
Formats that can only hold true pairs leave out the one-sided ones and say how
many — including them would shift every later line out of alignment.

**Are notes exported?**
Yes, with their pair.

## Safety

**Can I break anything?**
No. Setu only reads the PDFs and the parsed text. Your corrections go to a
separate place from the machine's reading, and nothing is ever deleted.

**Where is my work kept?**
On the machine running Setu, not in your browser. Closing the tab, losing your
connection or your laptop sleeping loses nothing.

**Is the earlier Tulana work affected?**
No. The saved pairs and clippings from the block tool are untouched. Setu adds
its own tables and writes to nothing that existed before it.

## When things break

**A page will not load.**
Turn to another page and back. If that does not fix it, tell whoever runs the
server which two books and which page.

**The interface looks unstyled.**
The server needs restarting; the stylesheet is read at start-up.

**Everything is slow.**
Turn off **Show me the printed page**. Rendering a scan is the slowest thing
Setu does, and everything else works without it.
