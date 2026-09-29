# The annotator's manual

This manual is for you if you have been asked to check translations in **सेतु Setu** and you have never used a tool like it. You do not need to know anything about databases or programming, and nothing here assumes you do. If you can read English and one Indian language, you can do this work.

Read sections 1 and 2 first, and try each step in Setu as you read it. Sections 4 to 7 come next, because they cover what you will meet every day. Sections 3 and 8 to 13 are for coming back to when you need them. You can switch to the **Guide** tab and back at any time, and your place in **Annotate** stays as it was. Sections 2 and 6 are the ones you will look at most often.

Setu is a new tool and it has some rough edges. Where one of them affects your work, this manual says so plainly, so that you never have to wonder whether something odd was your fault.

## 1. What this work is, and why it matters

School textbooks in India are printed in English and in many other languages. The English edition of a maths book and its Marathi edition are meant to say the same thing, but they were made separately, by different people, and they are laid out differently on the page.

Someone who wants to use the two editions together, for example to build translation tools or to study how an idea is worded in different languages, needs them matched up passage against passage, with every match checked by a person. A collection of matched passages is called a **parallel corpus**. (A corpus is a large body of text. Parallel means two languages side by side.) The files you can download from Setu are in the formats that translation software and researchers expect.

Two computer programs have already done a first pass. One, which the tool calls **the parser**, looked at scanned pictures of the printed pages, found the separate pieces of text on each page and read the letters in them. The other suggested which piece of text in the English book goes with which piece in the other book. Both are useful and neither is reliable. The parser misreads letters, drops words and scrambles formulas. The matcher sometimes pairs the wrong things, and sometimes finds no partner at all.

You are the check. For each pair Setu shows you, you say whether the two sides really say the same thing. If something in the text is wrong, you say so and, where you can, you fix it. That is the whole job. You are not translating anything, rewriting anything or improving the textbook. (The word for this kind of work is **annotating**: attaching your judgement to each piece of data. It is the name of the first tab.)

It matters because whatever is wrong in this text gets copied into everything built from it. A wrong number or a missing sentence does not announce itself later. Only a person who reads both languages can catch it now.

It is also patient work. Most pairs are fine and take seconds. A few need real thought. Some cannot be settled at all, and for those the right answer is **Unclear**, which is a useful answer and not a failure.

## 2. Your first ten minutes

This walks you through opening two textbooks and answering your first pair. While you are only reading and clicking, you cannot damage anything. Only a few things change the saved work: the answer buttons, typing into a passage while **Correct it** is switched on (and the button that puts the original back), and the buttons that save or remove a page match. Each is explained where it comes up.

**Step 1. Open the link you were given.** You will see सेतु Setu at the top left and four tabs: **Annotate**, **Saved work**, **Download** and **Guide**. These are Setu's own tabs, not the tabs of your browser. You start on **Annotate**, where the work is done. **Guide** holds this manual and the list of common questions. You do not need to install anything. Use a laptop or desktop computer, because the screen does not work properly on a phone (the common questions say why).

**Step 2. Type your name.** Use the box at the top right that says "Your name", then press Enter. Setu attaches the name to every answer and correction you make, so that someone can ask you about them later. The name is remembered in this browser, so you type it once. If you use another browser or another computer, type it again.

**Step 3. Choose the two books.** On the left is a panel headed **Textbook** with seven dropdown boxes. Setu fills them in for you, so you may only need to change a few. In order from the top:

| **Box** | **What it chooses** | **For example** |
|---|---|---|
| **1** The top box | The education board that published the books | Maharashtra State Board |
| **2** The next box | The class | Class 9 · 2 books |
| **3** The next box | The subject | Mathematics · 2 languages |
| **4** Under "Left — usually English", top | The language of the left-hand book | English · 1 |
| **5** Under "Left — usually English", bottom | Which book in that language | Mathematics Part 1 — 6pp · 23 pieces of text |
| **6** Under "Right — the language you check", top | The language of the right-hand book | Marathi · 1 |
| **7** Under "Right — the language you check", bottom | Which book in that language | Mathematics Part 1 — 6pp · 20 pieces of text |

Work from the top down: when you change a box, the boxes below it refill. Keep English (or whichever book you are checking against) on the left and the language you were asked to check on the right. The numbers after the names are counts: how many books a class or a language has, how many languages a subject has, and, for a book, its pages ("pp") and how many pieces of text it holds. A board that has only one language cannot be paired, so such boards are listed at the bottom of the first box under the heading "only one language — cannot be paired".

**Step 4. Press Open side by side.** The button says "Opening…" for a moment. The first time anyone opens a particular pair of books, Setu sets up the pairing for them, and that can take longer. When it finishes, more controls appear in the left panel (Chapter, Page, View, Tool, Text and Show only), two columns fill the screen, and a counter appears at the top right, for example "0 / 21 answered". The counter is the number of pairs answered out of all the pairs in these two books.

**Step 5. Look at what appeared.** Each column is headed with its language and the book's title, and a line such as "page 1 of 6 · 4 blocks". That means you are on page 1 of a six-page book and there are four pieces of text on this page. (The tool calls a piece of text a **block**: a heading, a paragraph, an equation, a caption. This manual mostly says passage or card.) Each passage is a card, and the cards are in reading order. Above the cards is a box that says "No scan of this book on this machine — showing the text." It appears every time in this view, and you can ignore it.

**Step 6. Click the first card in the left column.** The card gets a tinted background and a ring. The panel under the columns fills in. It shows the left text and its partner's text in two boxes, the question "Do these two say the same thing?", six answer buttons and a box for a note. A line above the two boxes names the pair, for example pair #2.

**Step 7. Read both boxes and decide.** Do the two say the same thing? Look at numbers and symbols first, because they read the same in every language. Then read the words.

**Step 8. Give your answer.** Click one of the six buttons, or press its number on the keyboard (1 to 6). The button you chose turns solid teal, the word "Saved." appears beside the note box, and the counter at the top right goes up by one. The card in the column does not change straight away. Its answer label appears the next time the page is drawn, for instance when you turn the page and come back. The solid button and the counter are your confirmation. If you want to leave a note, type it before you press the answer (section 6).

**Step 9. Go on.** Click the next card in the left column and repeat. When the page is finished, press the **›** button in the Page group in the left panel, or press the right-arrow key, to turn to the next page of both books.

That is the loop: pick a card, read, answer, next. Everything else in this manual is about the cases where the loop does not fit.

**One habit to start with.** Have only one card selected at a time, and choose cards by clicking in the left column. If you have selected something on the left and want to click in the right column, press `Esc` first. Section 4 explains why.

## 3. Picking up where you left off

Your answers and corrections are saved the moment you make them, on the computer that runs Setu. There is nothing to save before you stop and nothing to restore when you come back. What Setu does not do is remember which page you were on. This is how you find your place again.

**Open the same two books, with the same book on the left.** Choose the same board, class, subject, languages and books as before, in the same left and right order, and press **Open side by side**. You are back in the same piece of work, and the counter shows how much has been answered. If you swap the sides, with the other language on the left, Setu treats that as a different piece of work with nothing answered in it. So keep English on the left every time.

**Where you land.** You land on the first page of each book, unless somebody has pressed **⇄ These two pages match** for these two books. If they have, both sides open on the pages that were matched (section 5) and **Turn both pages together** is already ticked.

**Find the first pair nobody has answered.** Open **Saved work** and choose **Not checked yet** in the dropdown. The list is in book order, so the first card is the earliest pair that nobody has answered. Click it. Setu takes you back to **Annotate** with both sides on that pair's pages. Then click the card you want. Three things to know. A pair that has a passage on only one side shows a dash for the other side's page, and clicking it moves only the side that has a passage. The list shows the first 60 matches, and the number beside the dropdown is the full total. And if you skipped some pairs earlier (passages that exist only on the right are the usual ones), they sit at the top of the list, so scroll down to find where you stopped.

**Or jump with the n key.** On the first page, tick **Turn both pages together** and press `n`. It selects the first left-hand passage on the page that nobody has answered. (It skips the one you have selected.) If there is none on that page, it turns to the next page of the left book and looks there, and when it reaches the end of the book a message says "Nothing left unanswered on this side of the book." It only looks at the left column, and it only moves the right side if that box is ticked, so use it once the two sides are matched (section 5).

**If other people work in the same books.** Their answers count too. The counter and the Saved work list show everybody's answers, not only yours. Agree with them in advance who takes which chapter, so that you do not answer the same pairs twice.

## 4. Reading the two columns

**What is in a column.** The heading gives the language and the book's title, the page you are on, and how many blocks are on it. The buttons − and + and ⤢ next to the percentage are zoom controls for the page picture (see View, below). In the Text view they change the percentage and nothing else. If the writing is too small, use your browser's own zoom (hold Ctrl and press +).

Each card has a small line on top, then the text.

- The first word on the line is the kind of passage: Chapter, Section, Paragraph, Example, Question, Equation, Table, Caption and so on.
- "page 1" is the page of that passage in its own book.
- "pair #2" is the pair's number. Both columns carry the same number for the two halves of a pair, starting from #0. To find the partner of a card, look for the same number in the other column.
- If the pair has been answered, a teal label gives the answer. If the text has been corrected by hand, a blue label says "corrected".
- If the card has no pair at all, the line says "no counterpart".

The text under the line is what the parser read. It is the machine's reading, so expect mistakes, and expect a few oddities. A formula is written between dollar signs as code, for example `$A = \{1, 3, 5, 7, 9\}$`. That is normal: it is how a formula is typed in plain text, and you check it by comparing the numbers and symbols on the two sides. A table appears as a run of tags, which are short codes in angle brackets that describe the table's shape, such as `<table><tr><td>`. Read the words between the tags and compare the cells in order. An empty card says "the parser found no text here".

**What the outlines and colours mean.**

| **You see** | **It means** |
|---|---|
| A dashed outline | This pair has not been answered yet |
| A solid outline and a teal answer label | This pair has been answered |
| A grey background, a dotted outline and the tag "no counterpart" | This piece of text belongs to no pair. You only see these if you tick **Include headers and page numbers** (headers, footers, page numbers and pictures). They cannot be answered |
| A tinted background with a ring | The card you have selected |
| A green flash and the word "saved" | A correction has been saved a moment ago |
| A blue tag, "corrected" | The pair's text has been changed by hand |
| The colour of the left edge | The kind of passage. The key is the row of small coloured labels at the bottom of the left panel. The tool hands the colours out as it goes, so read the word on the card's top line rather than remembering a colour |

**The panel under the columns.** When you select a card, this panel shows the two texts side by side, each with a label such as "English · page 1 · Paragraph · pair #2 · as the parser read it" (or "corrected by hand" once somebody has changed it). Under them are the question, the six answer buttons and the note box. If you select nothing, the panel is empty and the buttons are hidden.

**Select one card at a time.** Click a card in the left column and its partner appears in the box under the right column. If you then click a card in the right column while the left one is still selected, both stay selected. Setu shows you two different pairs, one in each box, and records your answer against the left one. The labels above the two boxes each carry a pair number. If the two numbers differ, press `Esc` and start again. The safest habit is to press `Esc` before you click in the other column.

Do not Ctrl-click or Shift-click cards. Those select several at once, and with more than one card selected the answer buttons disappear. After you turn a page the old selection is gone from the screen even though the line above the boxes may still say "selected: 1 on the left". Click a card again before you answer.

**Passages with no partner.** Expect a fair number of pairs to have a passage on one side only. In the one pair of books that was measured, 29 pairs in every hundred were like that. Such a passage shows up in one column with a pair number, and the other column has nothing with that number. Select it and the box on the other side says "Nothing on this side — the machine found no counterpart here." That is expected. Section 5 explains one case where it is misleading, and section 6 says what to record.

**The View switch: Text or Page + blocks.** **Text** is the default and it is the view for checking translations. **Page + blocks** shows the picture of the printed page with the parser's boxes drawn on it. It needs the scanned pages to be on the computer that runs Setu, and often they are not, because the scans are very large files. When they are missing, this view shows the text again. Setu's authors have only tested Page + blocks on specially made test pages and not on real textbook scans, so if the boxes look misplaced, go back to Text. The **Tool** switch (Click a block, Drag to crop) belongs to this view. Drag to crop lets you cut a picture of part of the page and shows it under the columns. It records nothing about your answers. You do not need either switch to do your work. If clicking cards suddenly does nothing, the Tool switch has been set to Drag to crop by accident (press `c`).

**The Show only box.** This box, with **Dim the rest**, **Include headers and page numbers** and **Reading order**, sits at the bottom of the left panel. Leave **Show only** on "All kinds of block". In the Text view a change there does not show until the next time a page is drawn (turn the page), so a filter you set by accident can make passages seem to vanish. **Include headers and page numbers** takes effect at once.

**Scrolling and space.** Each column scrolls on its own. The thin vertical bar between the columns can be dragged left or right to give one side more room.

## 5. When the two sides do not line up

Two editions of a book are printed separately, so the same material rarely sits on the same page number. In the books measured for this project, one translation ran more than a hundred pages away from its English original, and two share no chapter start page at all with theirs. Chapter counts differ too, for example 13 in one edition against 16 in the other. None of that is a fault. It is what happens when two teams make two editions, so Setu does not assume that the two books move together. Each side has its own controls, and you match them up yourself.

**The controls, in the left panel.**

- **Chapter.** Two dropdowns, one for each book. Each lists "Whole book" and then the chapters with the page each starts on, such as "Chapter 2 Relations · from page 4". The two lists rarely agree, so choose a chapter on each side. Choosing a chapter takes that side to the chapter's first page. Choosing "Whole book" does nothing.
- **Page.** Two page boxes, the left book's on the left and the right book's on the right. Type a number and press Enter. A number past the end takes you to the last page, and a number below 1 takes you to page 1. The **‹** and **›** buttons at either end turn both books back or forward together.
- **Turn both pages together.** A tick box. When it is ticked, moving one side moves the other by the same number of pages, keeping whatever gap there is. That includes typing a page number and choosing a chapter.
- **⇄ These two pages match.** This tells Setu that the two pages on screen hold the same material. It records the gap between them, ticks **Turn both pages together**, and saves the link for everyone who works on these two books. A message confirms it: "Saved for everyone working on these two books." Anyone who opens these two books later starts on those pages.
- **Unlink.** This button appears once a link exists. It removes the saved link. It does not untick **Turn both pages together**, so untick that yourself if you want the sides to move separately.

**The line under the tick box** always tells you where you stand. It reads "Both on page 4." when the two are level. It reads "English page 4 is beside page 5. If those two really say the same thing, press the button below." when they are not. After you press the button it reads something like "Linked — the English edition runs 1 page behind the other." That means the same material is on a page number one lower in the left book than in the right. If you then move the sides apart, it adds "You have moved them +1 further apart." (In that line, "the English edition" always means the left-hand book, even when it is not English.)

**Matching two chapters, step by step.** Suppose Chapter 2 starts on page 4 of the English book and on page 5 of the Marathi one.

**1.** Untick **Turn both pages together** if it is ticked. With it ticked, choosing a chapter on one side drags the other side along with it.

**2.** In the left Chapter box choose Chapter 2. In the right Chapter box choose the same chapter. Match them by number and title, because the wording differs.

**3.** Look at the two columns. If the material does not match, type a page number into either page box until the same material is on both sides.

**4.** Press **⇄ These two pages match**. From now on the two sides turn together, with the arrow keys or the **‹** and **›** buttons.

**Match again at every chapter.** The gap usually changes from chapter to chapter, because the two editions are set out differently. When the columns stop lining up, find the pages that match again and press the button again. The new link replaces the old one. Because the link is shared, do not press the button unless the pages really do match, and expect that the next person to open these two books will start where you last pressed it.

**When the box under the right column says "Nothing on this side".** When you select a card on the left, Setu looks for its partner among the cards on the page the right column is showing. If the partner is on a different page, the right-hand box says "Nothing on this side — the machine found no counterpart here." even though a partner exists. Before you record a passage as having no partner, check that the right column is on the right page. Look for the same pair number: pair #14 on the left goes with pair #14 on the right. If you cannot see that number on the right, step the right side to the page before or after.

**Finding a partner quickly.** Open **Saved work**. Each card shows the page of the left passage and the page of the right one, for example p4 and p5. Click a card and both sides jump to those pages.

## 6. The seven answers

A pair has one of seven states. Six are answers you choose. The seventh is where every pair starts. Under the two text boxes is the question "Do these two say the same thing?" and six buttons, each with a number on it. The number is the key you can press instead of clicking. You can change your mind at any time by pressing a different button. The newer answer replaces the older one, and the older one stays in a log, which is a written record of what was done and when. You cannot see the log on screen.

**Notes.** The box under the buttons says "Note (optional) — why did you choose that?". Write a note when you choose Needs correction (what was wrong, if it is not obvious), Structural mismatch (where the rest of the text is) or Unclear (what you could not tell). Type the note first, then press the answer, because a note is saved together with the answer. After you press the answer, the note box empties on your screen even though the note was saved. Pressing Enter in the note box does nothing. A note typed after you have answered is not saved until you press an answer again. To add or change a note later, type the whole note again and press the same answer again, because an empty note box replaces the saved note with nothing.

**Choosing when you are unsure.** Ask these in order.

**1.** Does this need checking at all? A header, a page number or a decoration does not. If so, **Not applicable**.

**2.** Is there text on both sides? If one side is empty, or is missing words you cannot find nearby, **Missing or incomplete**.

**3.** Are the two texts the same piece of the book, cut the same way? If not, **Structural mismatch**.

**4.** Do they say the same thing? With nothing to fix, **Exact**. With something wrong that you can point to, **Needs correction**. If you cannot tell, **Unclear**.

### Not checked yet

Every pair starts here. It means nobody has answered the pair, and it is what the counter leaves out: "12 / 21 answered" means twelve pairs have an answer and nine are still Not checked yet. There is no button for it, so you never choose it, and once a pair has an answer you can change the answer but cannot go back to this. It matters for one reason. Not checked yet tells the next person that nobody has been here. If you have looked at a pair and could not decide, do not leave it in this state. Choose Unclear.

### Exact (key 1)

**What it means.** The two sides say the same thing and nothing in either text needs changing. The project's own wording is: "The two sides say the same thing. Nothing needs changing." Different word order, different sentence lengths and small differences in punctuation or spacing are what translation looks like, and they do not stop a pair from being Exact.

**Example.** The left says "The sum of the angles of a triangle is 180 degrees." The right says the same, in its own language, with 180. The words are arranged differently because the languages are, and the number is right. Choose Exact.

**Over its neighbours.** Not Needs correction, because there is nothing to fix. Not Structural mismatch, because both halves are the same piece of the book.

### Needs correction (key 2)

**What it means.** The project's own wording is: "They mostly match, but something in the text is wrong — a typo, a wrong number, a garbled formula." The two passages are the same piece of the book and both are complete, but one side has a mistake in it.

**Example.** The left says "180 degrees" and the right says "108 degrees". Two digits have swapped. The passage is there and it is the right passage, but a number is wrong. Correct the number if you can tell which side is wrong (section 7), then choose Needs correction. Choose it even after you have fixed the text. The answer records what was wrong with the machine's reading, and your fix is saved alongside it.

**Over its neighbours.** Not Exact, because something has to change. Not Missing or incomplete, because nothing is absent: the words are all there and one of them is wrong. If you cannot tell which side is wrong, choose Unclear.

### Missing or incomplete (key 3)

**What it means.** The project's own wording is: "Part of the text is missing on one side, or one side is empty." Something that should be there is not.

**Example.** The left is a paragraph of three sentences and the right has the first two and stops. Or the left passage has a pair number and the right column has nothing with that number, and nothing nearby that says the same. Or the right card reads "the parser found no text here". In each case, text that should exist is absent.

**Over its neighbours.** Not Needs correction, because the text is not wrong, it is absent. Not Structural mismatch, because the missing words are not somewhere else on the other side. Look a little above and below on the other side, and check the page (section 5), before you decide.

### Structural mismatch (key 4)

**What it means.** The project's own wording is: "Both sides have text, but they are not the same piece of the book — or one side splits what the other keeps together."

**Example.** The left keeps two sentences together in one passage, pair #12. The right has cut them into two passages, so the right half of pair #12 holds only the first sentence and the second sentence sits in the next pair. Each half is real text and each says the same as part of its partner, but the passages are not cut the same way. Another example is a worked example on the left that the matcher has set beside an exercise question on the right. Both are real text, but they are not each other's translation. In both cases, write a note saying where the rest is, for example "second sentence is in pair #13".

**Over its neighbours.** Not Missing or incomplete, because you can find the words on the other side. Not Exact, because the two are not the same piece of the book.

### Unclear (key 5)

**What it means.** The project's own wording is: "You cannot tell. Leave it for a reviewer."

**Example.** A formula is so scrambled on both sides that you cannot tell what it should say. Or the subject uses words you do not know well enough to judge. Or you cannot tell whether two passages belong together. Choose Unclear and write a note that says what stopped you, for example "formula garbled on both sides, cannot tell the exponent".

**Over its neighbours.** A guess recorded as an answer is worse than an honest Unclear. And Unclear is better than leaving the pair Not checked yet, because Unclear tells the reviewer that somebody looked.

### Not applicable (key 6)

**What it means.** The project's own wording is: "This does not need annotating — a page header, a picture caption, a decoration."

**Example.** A line such as "Free distribution", or a running title printed at the top of every page, has slipped through as a passage. Or a label inside a diagram has been paired with a label in the other book's diagram. There is nothing to translate or check. Choose Not applicable.

**Over its neighbours.** Not Exact, because there is no meaning to compare. Not Missing or incomplete, because nothing is missing: nothing was meant to be there. The project's own wording lists picture captions here. If your supervisor asks you to check captions as well, treat them like any other passage.

## 7. Correcting wrong text

Setu starts in **Read** mode, which is safe: nothing you type can change the text. To change text, switch to **Correct it**. The switch is in the left panel under the heading "Text" (not to be confused with the View switch, which also has a button called Text). You can also press `e`, and pressing `e` again switches back.

**How to correct a passage.**

**1.** Switch to **Correct it**. Every card that belongs to a pair becomes a box you can type in.

**2.** Click into the text of the card and change what is wrong. Change only what is wrong.

**3.** Click anywhere outside the box. This is what saves it. There is no save button.

**4.** Look for the confirmation. The card turns green for a second or two and the word "saved" appears on its top line, the blue "corrected" label appears, and "Saved." shows near the note box.

**5.** Now choose your answer, which will usually be Needs correction.

Clicking into the text of a card in Correct it mode does not select the card, so the panel below does not change. To select it, click on the small line at the top of the card, or on the space around the text. While your cursor is in a box, the number keys type numbers and the other shortcuts are off, so a 1 inside a correction is a 1 and not an answer.

**What to correct, and what not to.** Fix what the machine misread, so that the text matches what is printed in the book. Do not translate anything. Do not improve the wording. Do not fix the book's own mistakes, because the corpus should record what the book says. Do not add anything that is not printed on the page. Setu does not enforce these rules, so they are up to you. If you have been given different rules by your supervisor, follow theirs.

You will often be working without a picture of the printed page, because the scans are often not on the machine. Then you correct only what you can be sure of from the two texts and from what you know. A digit that disagrees between the two sides is a candidate, but that alone does not tell you which side is wrong. Sometimes the subject settles it: the angles of a triangle add up to 180 degrees, so 108 is the wrong one. When nothing settles it, do not guess. Choose **Unclear** and put both possibilities in the note.

**Formulas and tables.** Leave the dollar signs, the backslashes and the tags exactly as they are, and fix only the characters inside them. If you delete a dollar sign by accident, put it back or use **Put back what the parser read**.

**Putting the original back.** Select the card (click its top line). Under each of the two boxes at the bottom of the screen, a button appears that says **Put back what the parser read**. Press the one under the side you want to restore. It appears under both boxes, even when you changed only one side. Pressing it under the side you did not change does nothing. The button restores the machine's original text, not your own earlier correction, and it only appears while **Correct it** is switched on.

**The blue "corrected" label** marks a pair, not a side. If either half has been corrected, by you or by anybody else, both halves of the pair show the label once the page is redrawn.

**The two boxes at the bottom are editable too** while Correct it is on and a card is selected. They save when you pause for about a second and a half or click away, and the correction is stored properly. The card in the column above does not update on screen until you turn the page and come back, which looks as if your change was lost. It was not. Correcting in the column itself avoids the confusion.

**What you cannot do here.** You cannot type text into a side that has no passage. The box says "Nothing on this side" and cannot be edited, so record it as Missing or incomplete. You cannot split a passage, join two passages, or move a passage to another pair. If the pairing is wrong, record a Structural mismatch and say so in a note.

**If two people correct the same passage.** A save that would overwrite somebody else's newer correction is refused, so nobody's work is replaced. You see a red message: "Somebody else changed this while you were typing — nothing of yours was lost, it is in the history." Your typing is still in the box on your screen. The other person's version is the one that was kept. The message says yours is in the history. Do not rely on that. Copy your text (select it and press Ctrl+C) before you do anything else, then turn the page and back to see their version, and decide whether your change is still needed.

## 8. What you cannot break

Setu is built so that ordinary mistakes can be undone. Specifically:

- **The printed books.** Setu only reads the scanned pages. It cannot change them, and nothing you do touches them.
- **What the machine read.** The parser's original text for every passage is kept separately and is never overwritten. Your corrections are stored next to it, not on top of it. **Put back what the parser read** restores it at any time.
- **Every version of your corrections.** Each time a correction is saved, that version is kept too, and nothing on your screen deletes them. You cannot see the list of versions from this screen. Whoever runs Setu can.
- **Your answers.** You can change an answer at any time by pressing a different button. Every earlier answer stays in a log.
- **Other people's corrections.** If you and somebody else correct the same passage at the same moment, the second save is refused rather than replacing the first (section 7).
- **Deleting.** There is no button anywhere in Setu that deletes a pair, a book or somebody's work.
- **Where your work lives.** Answers and corrections are stored on the computer that runs Setu, as you make them, and not in your browser. Closing the tab, or a laptop that dies, does not lose what was already saved. The one exception is text you have typed into a box and not yet clicked away from. Click away from a box before you leave it.

**What you can affect,** so that you know. Your answer on a pair replaces the previous answer, including one given by somebody else. The saved page link (section 5) is shared, so pressing its button changes where everybody starts. A correction changes the text that goes into downloaded files (the original goes in too). All three can be put right, but you cannot see who to ask from this screen, so if you think you have done one of them wrongly, tell your supervisor.

## 9. The Saved work tab

**Saved work** lists the pairs of the two books you have open in Annotate. If you have not opened two books yet, it says "Open two textbooks first."

Each card shows the pair's number (for example #7), its answer, its chapter, the page of the left passage and the page of the right one (for example p4 and p5), and the first part of each text. The answer label is teal for Exact, blue for Needs correction and grey for everything else, but read the words rather than the colour. A pair that has a passage on one side only shows a dash where the other page would be.

The dropdown at the top filters the list: **Everything**, **Everything I have answered**, **Not checked yet**, **Exact**, **Needs correction**, **Missing or incomplete**, **Structural mismatch**, **Unclear** and **Not applicable**. The number beside it counts all the pairs that match, including any beyond the 60 that the list will show. **Refresh** reloads the list. (Opening the tab reloads it too.)

Two things do not work the way the names suggest. **Everything I have answered** currently lists every pair, answered or not, so use **Not checked yet** to see what is left, or one of the specific answers to see those. And the list is not only yours: it shows everybody's answers, and it does not say who gave them.

Click a card and Setu takes you to **Annotate** with both sides on that pair's pages. It does not select the pair. Click the card in the column yourself.

## 10. The Download tab

An **export** is a copy of your work written into a file, so that you can open it in another program or pass it on. Downloading does not take anything out of Setu. It is a snapshot of the work as it is at that moment, so download again later to get newer work. (Setu also keeps a copy of each file it makes, on the computer that runs it.) The tab covers the two books that are open in Annotate, and includes everybody's answers, not only yours.

**The controls.**

- **Format.** The first choice, "JSON Lines (.jsonl)", is already selected. It is meant for programs, not people. If you do not know which format you need, choose **Excel workbook (.xlsx)**. It is a spreadsheet with one row for each pair, and it opens in Excel, LibreOffice or Google Sheets.
- **Which pairs.** The second dropdown offers "Everything", "Only what has been answered", "Only “Exact”" and "Only “Needs correction”".
- **Download** downloads one file with your choices.
- **Every format, as a zip** downloads all eleven formats at once, packed in a zip file. It ignores the "which pairs" choice and includes everything.

The eleven formats are JSON Lines, JSON, CSV, TSV, XML, Plain text, Moses (two files), TMX (translation memory), Excel workbook, Parquet and Hugging Face dataset. Most people who are not programmers need one of three. **Excel workbook** is the friendly one. **CSV** is the same table as a plain file that a spreadsheet can open. **Plain text** shows the pairs one after another, readable, and is good for proofreading. The others are for other programs. If someone tells you which they need, choose that. A format that cannot be produced on this copy of Setu is greyed out, with a note saying what it needs.

**What is in the spreadsheet.** One row for each pair, with columns for the pair's number (seq), its answer (status_label), your note, the kind of passage, the chapter, the two texts after any corrections (source_text and target_text), the two original machine-read texts (source_original and target_original), whether each side was corrected, the two page numbers, and the name of the person who last changed the pair (updated_by). A second sheet, About, says where the file came from. Page numbers in downloaded files start at 0, so page 1 on screen is page 0 in a file.

**Where the file goes.** Your browser saves it in its usual downloads folder, and Setu shows "The file should appear in your downloads." The name begins with the board, the class and the two languages, and ends with the format and the date and time.

**What some formats leave out.** Plain text, Moses, TMX and Hugging Face dataset can only hold pairs where both sides have text. Passages with no partner, or with an empty side, are left out of those four files. Setu does not tell you on screen how many were left out. The other formats include every pair.

## 11. Keyboard shortcuts

The **?** button at the top right of the screen opens a list of these. There is no ? key, only the button. Press **Close** to shut the list.

| **Key** | **What it does** |
|---|---|
| `1` to `6` | Answer the selected pair: 1 Exact, 2 Needs correction, 3 Missing or incomplete, 4 Structural mismatch, 5 Unclear, 6 Not applicable |
| `←` `→` | Turn both pages back or forward, whether or not **Turn both pages together** is ticked |
| `Alt` with `←` `→` | Turn the left page only. If **Turn both pages together** is ticked, both turn. (`Option` on a Mac) |
| `Shift` with `←` `→` | Turn the right page only. If **Turn both pages together** is ticked, both turn |
| `n` | Select the first left-hand passage on this page that nobody has answered, turning the left page forward if there is none |
| `e` | Switch between Read and Correct it |
| `c` | Switch between Click a block and Drag to crop |
| `Esc` | Clear the selection |
| `+` `-` | Zoom both pages. This changes the page picture only, and does nothing you can see in the Text view |
| `Ctrl` (hold) | Hide the block labels in the Page + blocks view |

**When a key does nothing.** The shortcuts switch themselves off while your cursor is in a box: a text box, the note box, a page-number box, a dropdown or a tick box. After you tick **Turn both pages together** or choose from a dropdown, click a card before you press a number key.

**Stray keys.** Letters you type with nothing selected can change things. `c` switches the Tool to Drag to crop, and then clicking cards does nothing. `e` switches on Correct it. `n` selects a different pair. Press `c` or `e` again to switch either one back. A number key answers the selected pair, so make sure the right pair is selected.

In Chrome and Edge on Windows and Linux, Alt with the left arrow is also the browser's own shortcut for going back to the previous website, and Setu does not block it. If that happens, use your browser's forward button to return to Setu, and use the **‹** and **›** buttons instead.

## 12. Getting faster

**Keep your hands on the keyboard.** Click a card in the left column, read, press a number, click the next card. Or press `n` to jump to the next unanswered card, once **Turn both pages together** is ticked and the pages are matched.

**Read numbers and symbols first.** They are the same in every language, so a wrong digit or a broken formula shows up faster than a wrong word. Then read the words.

**Match the pages at the start of every chapter.** A minute spent matching (section 5) saves every later page from showing the right column a page out.

**Save notes for where they help.** Write one when you choose Needs correction and the fix is not obvious, Structural mismatch, or Unclear. An Exact needs no note.

**Do the passages with no partner in a batch.** The `n` key visits only the left column, so passages that exist only on the right are never reached by it. At the end of a chapter, or of the book, open **Saved work**, choose **Not checked yet**, and work through what is left. The counter includes those pairs, and it will not reach its total without them.

**Make the writing bigger if you need to.** Hold Ctrl and press + in your browser. The zoom buttons in Setu do not help in the Text view.

**Stop and start freely.** Nothing is lost when you stop, because everything is saved as you go. A page where both sides agree takes seconds. A page where they do not can take several minutes of looking, and that looking is the valuable part, because it is what a program cannot do. Take breaks.

## 13. When to stop and ask a human

Some things are not yours to decide. Stop and tell your supervisor, rather than guessing, when:

- The two books do not seem to be the same book, for example a different subject or a different edition, or nothing lines up at any distance you try.
- A whole chapter or more is in a script or language you cannot read well enough to judge.
- You have answered a run of pairs and then realised the wrong pair was selected. Answers can be changed, but tell someone the pair numbers if you cannot remember them all.
- The tool does something this manual does not describe, or a red message appears that you do not understand.
- You are unsure what the project wants for a case such as a typo in the printed book, or a caption.
- Something makes you think "this cannot be right".

A guess recorded as an answer is worse than a gap. Ask first.

**What to tell them.** Give your name, the two books (as they read in the boxes), the page on each side, the pair number, what you expected and what happened. If a red message appeared, copy its exact words.

**If Setu itself will not load.** The link may have been replaced or closed. Ask whoever gave it to you. Your work is kept on their machine, so it is not affected.
