# The annotator's manual

This manual is for you if you have been asked to check translations in **सेतु Setu** and you have never used a tool like it. You do not need to know anything about databases or programming, and nothing here assumes you do. If you can read English and one Indian language, you can do this work.

Read sections 1 and 2 first, and try each step in Setu as you read it. Sections 4 to 7 come next, because they cover what you will meet every day. Sections 3 and 8 to 13 are for coming back to when you need them. You can switch to the **Guide** tab and back at any time, and your place in **Annotate** stays as it was. Sections 2 and 6 are the ones you will look at most often.

Setu is a new tool and it has some rough edges. Where one of them affects your work, this manual says so plainly, so that you never have to wonder whether something odd was your fault.

## 1. What this work is, and why it matters

School textbooks in India are printed in English and in many other languages. The English edition of a maths book and its Marathi edition are meant to say the same thing, but they were made separately, by different people, and they are laid out differently on the page.

Someone who wants to use the two editions together, for example to build translation tools or to study how an idea is worded in different languages, needs them matched up passage against passage, with every match checked by a person. A collection of matched passages is called a **parallel corpus**. (A corpus is a large body of text. Parallel means two languages side by side.) The files you can download from Setu are in the formats that translation software and researchers expect.

Two computer programs have already done a first pass. One, which the tool calls **the parser**, looked at scanned pictures of the printed pages, found the separate pieces of text on each page and read the letters in them. The other suggested which piece of text in the English book goes with which piece in the other book. Both are useful and neither is reliable. The parser misreads letters, drops words and scrambles formulas. The matcher sometimes pairs the wrong things, and sometimes finds no partner at all.

You are the check. For each pair Setu shows you, you say whether the two sides really say the same thing. If something in the text is wrong, you say so and, where you can, you fix it. If the matcher paired the wrong passages, or missed a pair, you can put that right too (section 5). That is the whole job. You are not translating anything, rewriting anything or improving the textbook. (The word for this kind of work is **annotating**: attaching your judgement to each piece of data. It is the name of the first tab.)

It matters because whatever is wrong in this text gets copied into everything built from it. A wrong number or a missing sentence does not announce itself later. Only a person who reads both languages can catch it now.

It is also patient work. Most pairs are fine and take seconds. A few need real thought. Some cannot be settled at all, and for those the right answer is **Unclear**, which is a useful answer and not a failure.

## 2. Your first ten minutes

This walks you through opening two textbooks and answering your first pair. While you are only reading and clicking cards, you cannot damage anything. Only a few things change the saved work: the answer buttons (and the number keys that press them), the note box, typing into a passage while **Correct it** is switched on (and the button that puts the original back), the buttons and the `p` key that pair or unpair passages, the buttons that save or remove a page match, and two buttons on the **Saved work** tab. Each is explained where it comes up.

**Step 1. Open the link you were given.** You will see सेतु Setu at the top left and four tabs: **Annotate**, **Saved work**, **Download** and **Guide**. These are Setu's own tabs, not the tabs of your browser. You start on **Annotate**, where the work is done. **Guide** holds this manual and the list of common questions. You do not need to install anything. Use a laptop or desktop computer, because the screen does not work properly on a phone (the common questions say why).

**Step 2. Type your name.** Use the box at the top right that says "Your name", then press Enter. Setu attaches the name to every answer, note, correction and pairing you make, so that someone can ask you about them later, and it uses the name to remember where you were (section 3). Type it the same way each time. The name is remembered in this browser, so you type it once. If you use another browser or another computer, type it again.

**Step 3. Choose the two books.** On the left is a panel headed **Textbook** with seven dropdown boxes. Setu fills them in for you, so you may only need to change a few. (If you have worked in Setu before, the group above it, **Continue where you left off**, can reopen your books for you. Section 3 explains it.) In order from the top:

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

**Step 4. Press Open side by side.** The button says "Opening…" for a moment. The first time anyone opens a particular pair of books, Setu sets up the pairing for them, and that can take longer. When it finishes, more controls appear in the left panel (Chapter, Page, View, Tool, Text and Show only), two columns fill the screen, and two things appear at the top right: a counter, for example "0 / 21 answered", and a small message about saving, which starts as "Nothing to save" (section 8 explains it). The counter is the number of pairs answered out of all the pairs in these two books.

**Step 5. Look at what appeared.** Each column is headed with its language and the book's title, and a line such as "page 1 of 6 · 4 blocks". That means you are on page 1 of a six-page book and there are four pieces of text on this page. (The tool calls a piece of text a **block**: a heading, a paragraph, an equation, a caption. This manual mostly says passage or card.) If the scanned picture of the page is not on this computer, the line also ends with "· no scan on disk". You can ignore that. Each passage is a card, and the cards are in reading order. The top line of a card says what kind of passage it is, which page it is on and which pair it belongs to, for example "pair #2 ↔ p1". Section 4 explains each part.

**Step 6. Click the first card in the left column.** The card gets a tinted background and a ring. The panel under the columns fills in. It shows the left text and its partner's text in two boxes, a thin strip under them that says the two are paired, the question "Do these two say the same thing?", six answer buttons and a box for a note. A line above the two boxes names the pair, for example "pair #2".

**Step 7. Read both boxes and decide.** Do the two say the same thing? Look at numbers and symbols first, because they read the same in every language. Then read the words.

**Step 8. Give your answer.** Click one of the six buttons, or press its number on the keyboard (1 to 6). The button you chose turns solid teal, the word "Saved." appears beside the note box, the answer's name appears as a teal label on the top line of the card, and the counter at the top right goes up by one. The card's outline changes from dashed to solid the next time the page is drawn, for instance when you turn the page and come back, so do not wait for it. If you want to leave a note, type it in the note box. It saves by itself, whether you write it before or after you answer (section 6).

**Step 9. Go on.** Click the next card in the left column and repeat. When the page is finished, press the **›** button in the Page group in the left panel to turn both books to their next page. (The right-arrow key turns pages too. It turns both books only if **Turn both pages together** is ticked, which section 5 explains.) Or press `n`, and Setu takes you to the next pair that nobody has answered, whatever page it is on.

That is the loop: pick a card, read, answer, next. Everything else in this manual is about the cases where the loop does not fit.

**One habit to start with.** Select one card at a time. If you click a card in each column, Setu checks that the two cards belong to the same pair. When they do not, an amber bar appears and the answer buttons disappear, so an answer cannot land on the wrong pair. If you did not mean to select the second card, click it again to let it go, or press `Esc` to clear everything. Section 4 explains.

## 3. Picking up where you left off

Your answers, notes, corrections and pairings are saved as you make them, on the computer that runs Setu. There is nothing to save before you stop and nothing to restore when you come back. Setu also remembers which pages you were on, so that you can walk back into the same place. This is how.

**Use "Continue where you left off".** It is the first group in the left panel, above **Textbook**. It appears once any pair of books has been opened on this copy of Setu.

**1.** Look at the **Your name** box at the top right. Your browser remembers the name you typed last time, so it is usually already there. If the box is empty, or you are on another browser or computer, type your name and press Enter. Setu keeps a separate place for each name, so type it the same way each time (capital letters do not matter).

**2.** Choose your books in the dropdown of **Continue where you left off**. It lists the pairs of books where anybody has answered something, or where Setu remembers you being, with the most recently changed first. (If nothing has been answered anywhere yet, it lists every pair of books that has been opened.) Each entry is a short name: the board, the class and the two languages, for example "MH · Class 9 · English ⇄ Marathi". It does not name the subject, so two subjects of the same class and languages look alike. If two entries read the same, the first is the one changed most recently, and the message that appears when you open one names the subject.

**3.** Read the small print under the button. It says how far the work has got, for example "212 of 1,826 answered · 1,614 left · 9 corrected · you were on page 41 ↔ 43 · 3 hours ago". The counts include everybody's answers. "You were on page 41 ↔ 43" gives the page of the left book and of the right book where you last were, and it appears only when Setu remembers a place for your name. The time at the end is when anybody last changed anything in these two books, which may not be you. All of this was worked out when Setu opened.

**4.** Press **Open it again**. Setu opens the two books with the same book on the left, puts each book on the page you were on, and brings back the view you were using (Text or Page + blocks). A message at the bottom names the books and the page. If somebody has saved a page match for these two books (section 5), **Turn both pages together** is ticked, as it was before.

**What Setu remembers, and what it does not.** It remembers the pages of the two books and the view. It saves them about a second after you stop moving: when you turn a page, type a page number, choose a chapter, press `n`, or open a pair from **Saved work**. It does not remember which card you had selected, and it always starts in Read mode, so switch **Correct it** on again if you need it. If you leave the **Your name** box empty, your place goes into one shared place that everybody who left the box empty uses, so type your name. Two people who type the same name share a place.

**If you would rather open the books by hand.** Choose the same board, class, subject, languages and books as before, in the same left and right order, and press **Open side by side**. You are back in the same piece of work, and the counter shows how much has been answered. You land on the first page of each book, unless somebody has pressed **⇄ These two pages match** for these two books, in which case both sides open on the pages that were matched and **Turn both pages together** is already ticked (section 5). If you swap the sides, with the other language on the left, Setu treats that as a different piece of work with nothing answered in it. So keep English on the left every time.

**Find the first pair nobody has answered.** There are two ways.

With the `n` key: press `Esc` so that nothing is selected, then press `n`. Setu finds the first pair in the book that nobody has answered, turns the books to the pages where its passages are, and selects it. Pairs that have a passage on one side only are included, and for those only the book that has the passage turns. When something is already selected, `n` finds the next unanswered pair after that one instead. When there are none left, a message says "Nothing left unanswered after this point in the book."

With **Saved work**: open the tab, choose your textbook and **Not checked yet** (section 9). The list starts with the pairs that somebody changed most recently, even if they are still unanswered, and then follows the book's order, so the first card is not always the earliest. The number at the start of each card is its pair number, and a smaller number is earlier in the book. Click a card and Setu takes you to **Annotate** with both books on that pair's pages and the pair selected. Only 25 cards are shown at a time, and **Older ›** shows the next 25.

**If other people work in the same books.** Their answers count too. The counter and the Saved work list show everybody's answers, not only yours. Pairings are shared as well: when somebody pairs or unpairs passages, you see the change the next time a page is drawn. Agree with them in advance who takes which chapter, so that you do not answer the same pairs twice.

## 4. Reading the two columns

**What is in a column.** The heading gives the language and the book's title, the page you are on, and how many blocks are on it, for example "page 5 of 148 · 8 blocks". When the picture of the page is not on this computer, the line ends with "· no scan on disk". That only says the picture is missing. The text you check is there. The buttons − and + and ⤢ next to the percentage are zoom controls for the page picture (see View, below). In the Text view they change the percentage and nothing else. If the writing is too small, use your browser's own zoom (hold Ctrl and press +).

Each card has a small line on top, then the text.

- The first word on the line is the kind of passage: Chapter, Section, Paragraph, Example, Question, Equation, Table, Caption and so on.
- "page 5" is the page of that passage in its own book.
- "pair #26 ↔ p5" says which pair the passage belongs to and where its partner is. "#26" is the pair's number, and both halves of a pair carry the same number. "↔ p5" is the page of the partner in the other book, so you can see at once when the partner is on a different page, for example "pair #26 ↔ p108". The numbers start from #0 and run through the pairs of these two books in order. They are positions in that list, not names, and they change when pairs are added or taken away (section 5).
- If the pair has a passage on this side only, the line says "pair #26" followed by an orange tag that names the other language, for example "no Marathi paired", and the card has an orange left edge. Section 5 explains what to do.
- If the card belongs to no pair at all, the line says "not in any pair".
- If the pair has been answered, a teal label gives the answer. If the text of this card has been corrected by hand, a blue label says "corrected". Each side has its own label: correcting the Marathi does not put one on the English card.

The text under the line is what the parser read. It is the machine's reading, so expect mistakes, and expect a few oddities. A formula is written between dollar signs as code, for example `$A = \{1, 3, 5, 7, 9\}$`. That is normal: it is how a formula is typed in plain text, and you check it by comparing the numbers and symbols on the two sides. A table appears as a run of tags, which are short codes in angle brackets that describe the table's shape, such as `<table><tr><td>`. Read the words between the tags and compare the cells in order. An empty card says "the parser found no text here".

**What the outlines and colours mean.**

| **You see** | **It means** |
|---|---|
| A dashed outline | This pair has not been answered yet. A card you answered a moment ago stays dashed until the page is drawn again |
| A solid outline and a teal answer label | This pair has been answered |
| An orange left edge and an orange tag such as "no Marathi paired" | The pair has a passage on this side only. Select the card to see what to do (section 5) |
| A grey background, a dotted outline and the tag "not in any pair" | This piece of text belongs to no pair. You only see these if you tick **Include headers and page numbers** (headers, footers, page numbers and pictures). They cannot be answered. If one is really a passage that the parser mislabelled, ask your supervisor before you pair it with a passage on the other side |
| A tinted background with a ring | A card you have selected |
| A green flash and the word "saved" | A correction has been saved a moment ago |
| A blue tag, "corrected" | The text of this card, and of this side only, has been changed by hand |
| The colour of the left edge | The kind of passage. The key is the row of small coloured labels at the bottom of the left panel. The tool hands the colours out as it goes, so read the word on the card's top line rather than remembering a colour. Orange is the exception: it marks a pair with only one side |

**The panel under the columns.** When you select a card, this panel shows the two texts side by side, each with a label such as "English · page 5 · Paragraph · pair #26 · as the parser read it" (or "corrected by hand" once somebody has changed that text). The partner is shown even when it is on a page that is not on screen, and its label gives its page. Under the two texts is a thin strip. On a pair it reads "Paired: English page 5 ↔ Marathi page 5." and has an **Unpair** button. When you have selected two cards that are not a pair, it is an amber bar with **⇄ Pair these two** instead (section 5). Then come the question, the six answer buttons and the note box. The line above the texts says what is selected, for example "pair #26" or "pair #26 — both sides selected". If you select nothing, the panel is empty and the buttons are hidden.

**What you can select.** You can select a card in either column. What happens depends on what is selected.

- **One card.** Click it. Its partner appears in the other box under the columns, even when the partner is on a page that is not on screen, and you can answer. Click the same card again to let it go.
- **One card in each column, from the same pair.** Both boxes show the pair, and you can answer.
- **One card in each column, from different pairs.** Setu does not guess. The line above the boxes says "These two blocks are not paired with each other yet.", an amber bar appears under them, and the answer buttons are hidden, so an answer cannot go to the wrong pair. You can pair the two passages (section 5), or click one of the cards again to let it go, or press `Esc` and start again.
- **Several cards in one column.** Ctrl-click and Shift-click select several cards at once. While more than one is selected the line above the boxes says so, for example "selected: 2 on the left, 0 on the right — pairing and answering work one block per side; click a single block.", and the answer buttons and the pairing button are hidden. Click one card to start again.

**The selection stays when you turn a page.** That is deliberate. A passage that fits on one English page often runs onto the next page in the other language, and the two halves of a pair can sit on different pages. Turn the pages as you need, and the selected card stays selected, with its text still in the panel. `Esc` clears the selection.

**Passages with no partner.** Expect a fair number of pairs to have a passage on one side only. In the one pair of books that was measured, 29 pairs in every hundred were like that. Such a card shows "no Marathi paired" (or the name of whichever language is missing) in orange. Select it and the box on the other side says "No Marathi passage is paired with this one." and tells you what to do: if the passage is on another page, turn that book to it, click it and press "Pair these two"; if the Marathi book really has nothing there, answer "Missing or incomplete". Three of the six answers, Exact, Needs correction and Structural mismatch, compare two passages, so on a pair with only one passage they are greyed out and Setu refuses them. Missing or incomplete, Unclear and Not applicable still work. Section 5 explains how to pair passages and section 6 says which answer to record.

**The View switch: Text or Page + blocks.** **Text** is the default and it is the view for checking translations. **Page + blocks** shows the picture of the printed page with the parser's boxes drawn on it. It needs the scanned pages to be on the computer that runs Setu, and often they are not, because the scans are very large files. When they are missing, this view shows the text again, under a box that says "No scan of this page on this machine — showing the text instead." Setu's authors have only tested Page + blocks on specially made test pages and not on real textbook scans, so if the boxes look misplaced, go back to Text. The **Tool** switch (Click a block, Drag to crop) belongs to this view. Drag to crop lets you cut a picture of part of the page and shows it under the columns. It records nothing about your answers. You do not need either switch to do your work. If clicking cards suddenly does nothing, the Tool switch has been set to Drag to crop by accident (press `c`).

**The Show only box.** This box, with **Dim the rest**, **Include headers and page numbers** and **Reading order**, sits at the bottom of the left panel. Leave **Show only** on "All kinds of block". A choice there takes effect at once: the other kinds of passage disappear from both columns. A kind that is on one page but not on the other leaves the second column with nothing to show, and that column then says "The parser found nothing on page 4. Try the next page.", even though the page has passages. **Dim the rest** fades every card except the ones you have selected, so a page can look washed out if you tick it by accident. While it is ticked, **Show only** hides nothing. **Include headers and page numbers** also takes effect at once. **Reading order** only matters in Page + blocks, where it numbers the boxes. If passages seem to have vanished, look at these boxes first.

**Scrolling and space.** Each column scrolls on its own. The thin vertical bar between the columns can be dragged left or right to give one side more room.

## 5. When the two sides do not line up

Two editions of a book are printed separately, so the same material rarely sits on the same page number. In the books measured for this project, one translation ran more than a hundred pages away from its English original, and two share no chapter start page at all with theirs. Chapter counts differ too, for example 13 in one edition against 16 in the other. None of that is a fault. It is what happens when two teams make two editions, so Setu does not assume that the two books move together. Each side has its own controls, and you match them up yourself.

**The controls, in the left panel.**

- **Chapter.** Two dropdowns, one for each book. Each lists "Whole book" and then the chapters with the page each starts on, such as "Chapter 2 Relations · from page 4". The two lists rarely agree, so choose a chapter on each side. Choosing a chapter takes that side to the chapter's first page. Choosing "Whole book" does nothing.
- **Page.** Two page boxes, the left book's on the left and the right book's on the right. Type a number and press Enter. A number past the end takes you to the last page, and a number below 1 takes you to page 1. The **‹** and **›** buttons at either end turn both books back or forward together, whether or not the box below is ticked.
- **Turn both pages together.** A tick box. When it is ticked, moving one side moves the other by the same number of pages, keeping whatever gap there is. That includes typing a page number, choosing a chapter, and using the arrow keys.
- **⇄ These two pages match.** This tells Setu that the two pages on screen hold the same material. It records the gap between them, ticks **Turn both pages together**, and saves the link for everyone who works on these two books. A message confirms it: "Saved for everyone working on these two books." Anyone who opens these two books later starts on those pages.
- **Unlink.** This button appears once a link exists. It removes the saved link and unticks **Turn both pages together**, so each side moves on its own again. A message says "Unlinked. Each side moves on its own again."

**The line under the tick box** always tells you where you stand. It reads "Both on page 4." when the two are level. It reads "English page 4 is beside page 5. If those two really say the same thing, press the button below." when they are not. After you press the button it reads something like "Linked — the English edition runs 1 page behind the other." That means the same material is on a page number one lower in the left book than in the right. If you then move the sides apart, it adds "You have moved them +1 further apart." (In that line, "the English edition" always means the left-hand book, even when it is not English.)

**Matching two chapters, step by step.** Suppose Chapter 2 starts on page 4 of the English book and on page 5 of the Marathi one.

**1.** Untick **Turn both pages together** if it is ticked. With it ticked, choosing a chapter on one side drags the other side along with it.

**2.** In the left Chapter box choose Chapter 2. In the right Chapter box choose the same chapter. Match them by number and title, because the wording differs.

**3.** Look at the two columns. If the material does not match, type a page number into either page box until the same material is on both sides.

**4.** Press **⇄ These two pages match**. From now on the two sides turn together, with the arrow keys or the **‹** and **›** buttons.

**Match again at every chapter.** The gap usually changes from chapter to chapter, because the two editions are set out differently. When the columns stop lining up, find the pages that match again and press the button again. The new link replaces the old one. Because the link is shared, do not press the button unless the pages really do match, and expect that the next person to open these two books will start where you last pressed it.

**Matching pages is not the same as pairing passages.** The page controls only decide which pages you are looking at. Which passage goes with which, the pairs themselves, was suggested by the matching program, and you can correct it passage by passage, as described below.

**When a card says "no Marathi paired".** Select it. The box for the missing side says "No Marathi passage is paired with this one." and under it: "If it is on another page, turn the right-hand page to it, click it, and press “Pair these two”. If the Marathi book really has nothing here, answer “Missing or incomplete”." Setu looks up the partner itself, on whatever page it is, so when a pair does have a passage on the other side you see it in the box without turning any page. When the box says nothing is paired, the matching program found no partner, and the choice is yours: look for the partner in the other book, or accept that there is none. Often the partner does exist and the program left it standing alone too. Look near where you expect it in the other book for a card whose orange tag names the first language, for example "no English paired". That card is the other half of the same passage.

### Pairing two passages that are on different pages

Use this when two passages say the same thing but are not paired with each other: one or both of them stands alone, or each is paired with something else. They can be on any pages. The pages do not have to match, and you do not need to press **⇄ These two pages match**.

**1.** Make sure you are in Read mode (press `e` if **Correct it** is on), so that clicking text selects the card. Click the first passage in its column. The panel under the columns shows it, and the box on the other side says "No Marathi passage is paired with this one." if it stands alone.

**2.** Turn the other book to the page that holds the other passage. Type the page number into that book's page box and press Enter. If **Turn both pages together** is ticked, untick it first, or the first book moves too. The card you selected stays selected while you turn the page.

**3.** Click the other passage in the other column. The panel now shows both texts, and an amber bar appears under them: "These two are not a pair yet. Left is page 106, pair #31; right is page 108, pair #36. If they say the same thing, pair them — pages do not have to match." The answer buttons are hidden while the bar is showing.

**4.** Read both texts. If they do not say the same thing, click one of the two cards again to let it go, or press `Esc`. Nothing has changed.

**5.** If they do say the same thing, press **⇄ Pair these two** (or press the `p` key). A message says "Paired. Now answer: do these two say the same thing?". The bar goes away, the two passages are one pair, both are selected, and the answer buttons appear. Answer as usual.

**If one of the two passages already had a partner.** The amber bar tells you before you press anything, for example "Pairing them means the English passage is now paired with another Marathi passage (page 20), which will be left on its own." That other passage is not deleted. It stays in the book as a pair of its own, with its text and any correction it had. Answers already given to the pairs that change go back to "Not checked yet", and the old answers are kept in the log. Setu never pairs two passages that you did not choose.

**Pairs you make are shared.** Everybody who works on these two books sees the new pairing, and the strip under the texts adds "paired by hand". Before it changes a pairing, Setu sends any text of yours that is still waiting to be saved, so your own correction cannot be left behind.

### Unpairing

Use this when Setu shows two passages as a pair but they do not say the same thing: the matching program paired the wrong ones.

**1.** Select the pair by clicking one of its cards. The strip under the two texts reads "Paired: English page 5 ↔ Marathi page 5. If these are not translations of each other, unpair them." and has an **Unpair** button.

**2.** Press **Unpair**. Your browser asks you to confirm: "Unpair #26? The English and the Marathi will each stand on their own until you pair them with something else. Corrections stay with their text; the answer goes back to “Not checked yet”." Press OK.

**3.** A message says "Unpaired. Now select its real partner on the other side, or answer “Missing or incomplete”." Each passage is now a pair of its own, and its card says "no Marathi paired" or "no English paired". Find each passage's real partner and pair them as above, or answer Missing or incomplete for a passage that really has no partner.

Unpairing does not delete anything. The text and any corrections stay with their passages, and the old answer is kept in the log. A note you wrote stays with the pair that keeps the left-hand passage. If you unpaired by mistake, select the two passages again and press **⇄ Pair these two**. The answer you had is not put back, but you can give it again.

**Pair numbers change.** The number on a card is the pair's place in the list of pairs for these two books, counting from 0. It is a position, not a name. Unpairing adds a pair. Pairing two passages that each stood alone takes one away. Other pairings can do either. Whenever a pair is added or taken away, every pair after it moves up or down by one. So after you pair or unpair something, the numbers after that point are not what they were a moment ago, and that is expected. Somebody else's pairing shows up the same way once your page is drawn again. Do not note a pair number somewhere and trust it tomorrow. Write down the page and the first words of the passage instead.

**Finding a partner quickly.** The top line of a card already names the page of its partner, for example "pair #26 ↔ p108". Select the card and the partner's text appears under the columns at once. To see the partner in its own column, type that page number into the other book's page box. You can also open **Saved work**. Each card there shows the page of the left passage and the page of the right one, for example p4 and p5. Click **Open in Annotate** and both books turn to those pages with the pair selected.

## 6. The seven answers

A pair has one of seven states. Six are answers you choose. The seventh is where every pair starts. Under the two text boxes is the question "Do these two say the same thing?" and six buttons, each with a number on it. The number is the key you can press instead of clicking. You can change your mind at any time by pressing a different button. The newer answer replaces the older one, and the older one stays in a log, which is a written record of what was done and when. You cannot see the log on screen.

**Which answers need two passages.** Exact, Needs correction and Structural mismatch compare the two sides, so they only work on a pair that has a passage on both sides. On a pair with a passage on one side only, those three buttons are greyed out, a note appears when you point at one, and Setu refuses them with a red message if you press one anyway. Missing or incomplete, Unclear and Not applicable work on every pair. If the partner is on another page, pair the two passages first (section 5), and the three buttons come back.

**Notes.** The box next to the buttons says "Note (optional) — why did you choose that?". Write a note when you choose Needs correction (what was wrong, if it is not obvious), Structural mismatch (where the rest of the text is) or Unclear (what you could not tell). The note saves by itself, about a second after you stop typing and again when you click away, so you can write it before or after you press the answer. It stays in the box after you answer. Each pair has its own note: when you select a different pair, the box shows that pair's note. To change a note, change the words in the box. There is nothing to press, and pressing Enter does nothing. You can write a note on a pair you have not answered, and the pair stays Not checked yet. If a red message says the note could not be saved, the words are still in the box. Click into the box and out again to send them once the problem has passed.

**Choosing when you are unsure.** Ask these in order.

**1.** Does this need checking at all? A header, a page number or a decoration does not. If so, **Not applicable**.

**2.** Is there text on both sides? If one side is empty, or is missing words you cannot find nearby, **Missing or incomplete**. If the card says "no Marathi paired", look for its partner on other pages first (section 5).

**3.** Are the two texts the same piece of the book, cut the same way? If not, **Structural mismatch**.

**4.** Do they say the same thing? With nothing to fix, **Exact**. With something wrong that you can point to, **Needs correction**. If you cannot tell, **Unclear**.

### Not checked yet

Every pair starts here. It means nobody has answered the pair, and it is what the counter leaves out: "12 / 21 answered" means twelve pairs have an answer and nine are still Not checked yet. There is no button for it, so you never choose it. Once a pair has an answer you can change the answer. To put the pair back in this state, open **Saved work**, find the pair and press **Undo my answer** (section 9). Setu also puts a pair back here by itself when its pairing changes (section 5). It matters for one reason. Not checked yet tells the next person that nobody has been here. If you have looked at a pair and could not decide, do not leave it in this state. Choose Unclear.

### Exact (key 1)

**What it means.** The two sides say the same thing and nothing in either text needs changing. The project's own wording is: "The two sides say the same thing. Nothing needs changing." Different word order, different sentence lengths and small differences in punctuation or spacing are what translation looks like, and they do not stop a pair from being Exact. It needs a passage on both sides.

**Example.** The left says "The sum of the angles of a triangle is 180 degrees." The right says the same, in its own language, with 180. The words are arranged differently because the languages are, and the number is right. Choose Exact.

**Over its neighbours.** Not Needs correction, because there is nothing to fix. Not Structural mismatch, because both halves are the same piece of the book.

### Needs correction (key 2)

**What it means.** The project's own wording is: "They mostly match, but something in the text is wrong — a typo, a wrong number, a garbled formula." The two passages are the same piece of the book and both are complete, but one side has a mistake in it. It needs a passage on both sides.

**Example.** The left says "180 degrees" and the right says "108 degrees". Two digits have swapped. The passage is there and it is the right passage, but a number is wrong. Correct the number if you can tell which side is wrong (section 7), then choose Needs correction. Choose it even after you have fixed the text. The answer records what was wrong with the machine's reading, and your fix is saved alongside it.

**Over its neighbours.** Not Exact, because something has to change. Not Missing or incomplete, because nothing is absent: the words are all there and one of them is wrong. If you cannot tell which side is wrong, choose Unclear.

### Missing or incomplete (key 3)

**What it means.** The project's own wording is: "Part of the text is missing on one side, or one side is empty." Something that should be there is not. This answer works on a pair with a passage on one side only.

**Example.** The left is a paragraph of three sentences and the right has the first two and stops. Or the left card says "no Marathi paired", you have looked for its partner on the nearby pages of the other book, and there is none. Or the right card reads "the parser found no text here". In each case, text that should exist is absent.

**Over its neighbours.** Not Needs correction, because the text is not wrong, it is absent. Not Structural mismatch, because the missing words are not somewhere else on the other side. Look a little above and below on the other side, and check the page (section 5), before you decide.

### Structural mismatch (key 4)

**What it means.** The project's own wording is: "Both sides have text, but they are not the same piece of the book — or one side splits what the other keeps together." It needs a passage on both sides.

**Example.** The left keeps two sentences together in one passage. The right has cut them into two passages, so the right half of this pair holds only the first sentence and the second sentence sits in the next pair. Each half is real text and each says the same as part of its partner, but the passages are not cut the same way. Another example is a worked example on the left that the matcher has set beside an exercise question on the right. Both are real text, but they are not each other's translation. In both cases, write a note saying where the rest is, for example "second sentence is in the next right-hand passage, the one that starts Therefore". Describe the place by its words or its page, because pair numbers move.

**Over its neighbours.** Not Missing or incomplete, because you can find the words on the other side. Not Exact, because the two are not the same piece of the book.

### Unclear (key 5)

**What it means.** The project's own wording is: "You cannot tell. Leave it for a reviewer." This answer works on every pair.

**Example.** A formula is so scrambled on both sides that you cannot tell what it should say. Or the subject uses words you do not know well enough to judge. Or you cannot tell whether two passages belong together. Choose Unclear and write a note that says what stopped you, for example "formula garbled on both sides, cannot tell the exponent".

**Over its neighbours.** A guess recorded as an answer is worse than an honest Unclear. And Unclear is better than leaving the pair Not checked yet, because Unclear tells the reviewer that somebody looked.

### Not applicable (key 6)

**What it means.** The project's own wording is: "This does not need annotating — a page header, a picture caption, a decoration." This answer works on every pair.

**Example.** A line such as "Free distribution", or a running title printed at the top of every page, has slipped through as a passage. Or a label inside a diagram has been paired with a label in the other book's diagram. There is nothing to translate or check. Choose Not applicable.

**Over its neighbours.** Not Exact, because there is no meaning to compare. Not Missing or incomplete, because nothing is missing: nothing was meant to be there. The project's own wording lists picture captions here. If your supervisor asks you to check captions as well, treat them like any other passage.

## 7. Correcting wrong text

Setu starts in **Read** mode, which is safe: nothing you type can change the text. To change text, switch to **Correct it**. The switch is in the left panel under the heading "Text" (not to be confused with the View switch, which also has a button called Text). You can also press `e`, and pressing `e` again switches back.

**How to correct a passage.**

**1.** Switch to **Correct it**. Every card that belongs to a pair becomes a box you can type in. A card marked "not in any pair" stays read-only.

**2.** Click into the text of the card and change what is wrong. Change only what is wrong.

**3.** Stop typing. Setu saves by itself about a second after you stop, and straight away when you click outside the box. There is no save button.

**4.** Look for the confirmation. The top bar says "Saving…" and then "All changes saved". The card turns green for a second or two and the word "saved" appears on its top line, and the blue "corrected" label appears. The small line beside the note box may keep showing "…" after a correction. Ignore it, because the top bar is the one to trust (section 8).

**5.** Now choose your answer, which will usually be Needs correction.

Clicking into the text of a card in Correct it mode does not select the card, so the panel below does not change. To select it, click on the small line at the top of the card, or on the space around the text. While your cursor is in a box, the number keys type numbers and the other shortcuts are off, so a 1 inside a correction is a 1 and not an answer.

**You can also correct in the panel under the columns.** The two boxes there are editable while Correct it is on and a pair is selected. They show the same passage as the cards in the columns, so whatever you type in one appears in the other at once. A partner on a page that is not on screen can be corrected there too.

**What to correct, and what not to.** Fix what the machine misread, so that the text matches what is printed in the book. Do not translate anything. Do not improve the wording. Do not fix the book's own mistakes, because the corpus should record what the book says. Do not add anything that is not printed on the page. Setu does not enforce these rules, so they are up to you. If you have been given different rules by your supervisor, follow theirs.

You will often be working without a picture of the printed page, because the scans are often not on the machine. Then you correct only what you can be sure of from the two texts and from what you know. A digit that disagrees between the two sides is a candidate, but that alone does not tell you which side is wrong. Sometimes the subject settles it: the angles of a triangle add up to 180 degrees, so 108 is the wrong one. When nothing settles it, do not guess. Choose **Unclear** and put both possibilities in the note.

**Formulas and tables.** Leave the dollar signs, the backslashes and the tags exactly as they are, and fix only the characters inside them. If you delete a dollar sign by accident, put it back or use **Put back what the parser read**.

**Pasting.** Pasting into a passage pastes plain text only, without fonts, colours or links, so text copied from a web page or a document arrives as plain words.

**Clearing a passage.** Deleting everything in a box so that you can retype it is fine. But an empty passage is never saved. While the box is empty nothing is sent, and the top bar may keep saying "Saving…". If you click away while it is still empty, the earlier text comes back and a red message says: "The passage was left empty, so nothing was saved and the text is back. To mark it as wrong, use an answer instead." If the passage should not be in the book at all, answer Not applicable. If the other book is missing it, answer Missing or incomplete.

**Clicking in and out changes nothing.** Clicking into a box and out again without changing a character is not a correction. No "corrected" label appears and nothing is saved.

**Putting the original back.** Select the card (click its top line). With **Correct it** switched on, a button that says **Put back what the parser read** appears next to the label above the box of each side whose text has been corrected, and only that side: under the English if the English was corrected, under the Marathi if the Marathi was. Press it to restore the machine's original text for that side. The button restores the machine's original text, not your own earlier correction, and your corrected version stays in the history.

**The blue "corrected" label** marks a passage, not a pair. If the English text was corrected, the English card has the label and the Marathi card does not. (The Saved work tab does the reverse: a pair shows "corrected" if either side was, and says which one.)

**What you cannot do here.** You cannot type text into a side that has no passage. The box says "No Marathi passage is paired with this one." and cannot be edited, so pair it with its partner (section 5) or record it as Missing or incomplete. You cannot split a passage or join two passages into one. You can pair and unpair passages (section 5), but if the two editions have cut the text differently, record a Structural mismatch and say so in a note.

**If two people correct the same passage.** A save that would overwrite somebody else's newer correction is stopped, so nobody's work is replaced without being asked. A box opens, headed "Someone else changed this passage while you were typing". It shows two versions side by side: "Theirs — what is saved now" and "Yours — what you typed". While it is open the top bar says "1 change needs you". Choose one.

**Keep mine** saves your text as the newest version. Theirs stays in the history. **Keep theirs** leaves what is saved and throws away what you typed. Nothing of yours is kept anywhere after that, even though the box says that neither version is thrown away. If you might want your words, select them in the "Yours" box and copy them (Ctrl+C) before you press Keep theirs.

## 8. What you cannot break

Setu is built so that ordinary mistakes can be undone. Specifically:

- **The printed books.** Setu only reads the scanned pages. It cannot change them, and nothing you do touches them.
- **What the machine read.** The parser's original text for every passage is kept separately and is never overwritten. Your corrections are stored next to it, not on top of it. **Put back what the parser read** restores it at any time.
- **Every version of your corrections.** Each time a correction is saved, that version is kept too, and nothing on your screen deletes them. You cannot see the list of versions from this screen. Whoever runs Setu can.
- **Your answers.** You can change an answer at any time by pressing a different button, or remove it with **Undo my answer**. Every earlier answer stays in a log.
- **Pairings.** Pairing and unpairing move passages between pairs. They never delete a passage or a correction, and a correction travels with its passage. When a pair changes, its answer goes back to Not checked yet and the old answer stays in the log. You can undo a mistaken pairing by pairing or unpairing again.
- **Other people's corrections.** If you and somebody else correct the same passage at the same moment, you are asked which version to keep (section 7). Only Keep theirs throws your own typing away.
- **Deleting.** There is no button anywhere in Setu that deletes a book, a passage, a correction or somebody's work.
- **Where your work lives.** Answers, notes, pairings and corrections are stored on the computer that runs Setu, as you make them, and not in your browser. Closing the tab, or a laptop that dies, does not lose what was already saved. Text you have typed that has not been confirmed yet is also kept in your browser, as described below.

**How to tell that your work is saved.** Once two books are open, a small message sits to the left of the counter at the top right. It tells the truth about the text you type into passages. It does not cover answers, which show "Saved." beside the note box, or a red message if they fail.

| **The top bar says** | **It means** |
|---|---|
| Nothing to save | You have not corrected anything since this page opened |
| Saving… | Text you typed is waiting to be sent, or is being sent. It usually lasts a second or two |
| All changes saved | Everything you typed has reached the computer that runs Setu |
| Not saved yet — trying again (amber) | The text could not be sent, because the connection or the computer that runs Setu is not answering. Setu keeps the text in your browser and tries again every few seconds, waiting longer each time up to half a minute. Leave the tab open |
| Offline — kept on this computer (amber) | Your browser says you have no connection. It is the same situation. The text is sent by itself when the connection comes back |
| 1 change needs you (red; "2 changes need you" and so on) | Setu cannot save a change without a decision from you. A box is asking which version of a passage to keep, or a red message has said that a change was refused. Deal with the box or the message first |

**Text kept in your browser.** While a correction is on its way, Setu keeps a copy of it in your browser's own storage until the computer that runs Setu confirms it. If the tab closes, the browser crashes or the connection is lost, the copy survives. The next time you open Setu in the same browser, a message says "Sending 1 change from last time that had not reached the server yet…" and the text goes through. That copy lives in one browser on one computer. It is not there if you open Setu in another browser, on another computer, or in a private window. In a private window, or when the browser's storage is full, Setu says so in a red message. Then do not close the tab while the top bar says anything other than "All changes saved".

**"Leave site?"** If you try to close the tab or the window while text is still unconfirmed, your browser asks whether you really want to leave. The exact words are your browser's own, and "Leave site?" is the usual question. Choose to stay, wait for "All changes saved", and then close the tab. If you leave anyway, Setu tries to send the text as the page closes and keeps the copy in your browser.

**What you can affect,** so that you know. Your answer on a pair replaces the previous answer, including one given by somebody else. The saved page link (section 5) is shared, so pressing its button changes where everybody starts. Pairing and unpairing are shared too: they change the pairs everybody sees, and the numbers of the pairs after them. A correction changes the text that goes into downloaded files (the original goes in too). All of these can be put right, and the Saved work tab shows the name of the last person who changed each pair, so you can ask them. If you think you have done one of them wrongly, tell your supervisor.

## 9. The Saved work tab

**Saved work** lists pairs from every textbook that has been opened on this copy of Setu. You do not need to have two books open to use it. The line under the heading counts the textbook chosen in the first dropdown, for example "212 of 1,826 pairs answered · 9 corrected by hand · 2 need attention · 150 exact · 40 needs correction". If nothing has been answered yet, it says "Nothing here yet."

**The filters.** All of them include everybody's work, not only yours.

- **The first dropdown** chooses the textbook ("Every textbook" or one pair of books).
- **The second dropdown** chooses which pairs: **Every answer** (every pair, answered or not), **Everything I have answered** (every pair that has an answer, whoever gave it), **Needs attention** with a count, **Not checked yet**, and one entry for each of the six answers.
- **The third dropdown** chooses a chapter.
- **The search box**, "Search the text, either language…", finds the pairs whose text contains what you type, in either language, in the corrected text as well as the machine's reading. The list updates a moment after you stop typing.
- **only ones I corrected** keeps the pairs whose text has been corrected by hand. It does not check who corrected them.
- **Refresh** reloads the list. (Opening the tab reloads it too.)

**When nothing matches.** If the filters find no pair, for example a search with no hits or an answer that nobody has given, the list says "Nothing has been answered yet — open two textbooks and start in the Annotate tab." Take that to mean that no pair matches, not that your work has gone.

**The order.** The list starts with the pair changed most recently, whatever the change was: an answer, a note, a correction or a pairing. Pairs that nobody has touched follow in book order. Only 25 cards are shown at a time. **‹ Newer** and **Older ›** under the list move through the rest, and the range between them, for example "1–25 of 1,826", says where you are.

**What a card shows.** The top line has the pair's number (for example #7), its answer, a "corrected" label if either side was corrected, a "one side only" label if the pair has a passage on one side only, its chapter, the page of the left passage and the page of the right one (for example p4 and p5), the kind of passage, and the name of the last person who changed the pair. A pair with a passage on one side only shows a dash for the other page. The answer label has its own colour for each answer, but read the words rather than the colour. Under the top line are the two texts, each headed with its language (and "corrected" if that side was). A side with no passage says "No Marathi passage is paired with this one." (or the name of the language that is missing). A side whose text was saved empty says "Saved empty — open it to put the text back." If the pair has a note, it is shown under the texts.

**Buttons on a card.**

- **Open in Annotate.** Setu takes you to the **Annotate** tab, opens the textbook if it is not already open, turns both books to the pages of that pair and selects it, so the panel under the columns shows it at once. Clicking anywhere else on the card does the same. A side with no passage stays on the page it was on.
- **Undo my answer.** It appears on answered pairs. After you confirm ("Put this pair back to “Not checked yet”? Any text you corrected is kept — only the answer is removed."), the pair goes back to Not checked yet. Despite its name it removes the answer whoever gave it, and the old answer stays in the log.
- **Change to “Missing or incomplete”.** It appears only on the first kind of warning card, described next.

**Needs attention.** This choice in the second dropdown lists the pairs that Setu thinks need another look, and shows how many there are. Each card has an amber edge and a warning at the top. There are two kinds.

"Answered as a pair, but there is nothing on the right. Open it and pair it with its partner, or change the answer to “Missing or incomplete”." means somebody gave Exact, Needs correction or Structural mismatch to a pair that has a passage on one side only. An older version of Setu allowed that. If the other book really has nothing, press **Change to “Missing or incomplete”**. If the partner is somewhere else, press **Open in Annotate**, find it and pair the two passages (section 5). Pairing puts the answer back to Not checked yet so that you can answer properly.

"A side was saved empty. Open it and type the text, or put back what the parser read." means the saved text of a passage is empty, which older versions of Setu allowed. Setu repairs most of these by itself every time it is started, and this list catches any that are left. Press **Open in Annotate**, switch on **Correct it**, and type the text or press **Put back what the parser read**.

A pair leaves the list as soon as the problem is fixed.

## 10. The Download tab

An **export** is a copy of your work written into a file, so that you can open it in another program or pass it on. Downloading does not take anything out of Setu. It is a snapshot of the work as it is at that moment, so download again later to get newer work. (Setu also keeps a copy of each file it makes, on the computer that runs it.) The tab includes everybody's answers, not only yours.

**What to include.** The box at the top has three dropdowns. The first is the textbook, and the pair of books open in Annotate is chosen for you. The second is which pairs: "Everything", "Only what has been answered", "Only “Exact”", "Only “Needs correction”", "Only “Missing or incomplete”" or "Only “Structural mismatch”". The third is the chapter. Under them a line says how many pairs match.

**Choose a format.** Each of the eleven formats is a button with its file ending and a line saying what it is for. Click one and the file downloads at once, with your choices applied. If you do not know which format you need, choose **Excel workbook**. It is a spreadsheet with one row for each pair, and it opens in Excel, LibreOffice or Google Sheets.

**Everything at once.** **Download the full bundle (.zip)** gives one zip file with every format that can be produced on this copy of Setu, each in its own folder. It uses the same choices as the dropdowns above, and a large book can take a minute. The page says the bundle also holds "a dataset card". The only description inside is the short README file in the Hugging Face dataset, so do not look for a separate card at the top of the zip.

The eleven formats are JSON Lines, JSON, CSV, TSV, XML, Plain text, Moses (two files), TMX (translation memory), Excel workbook, Parquet and Hugging Face dataset. Most people who are not programmers need one of three. **Excel workbook** is the friendly one. **CSV** is the same table as a plain file that a spreadsheet can open. **Plain text** shows the pairs one after another, readable, and is good for proofreading. The others are for other programs. If someone tells you which they need, choose that. A format that cannot be produced on this copy of Setu is greyed out, with a note saying what it needs. Tell whoever runs Setu.

**What is in the spreadsheet.** A sheet called Pairs, with one row for each pair and columns for the pair's number (seq), its answer (status_label), the note, the kind of passage, the chapter, the two texts after any corrections (source_text and target_text), the two original machine-read texts (source_original and target_original), whether each side was corrected (yes or no), the two page numbers, and the name of the person who last changed the pair (updated_by). A pair with a passage on one side only has an empty text on the other side. A second sheet, About, says where the file came from. Page numbers in downloaded files start at 0, so page 1 on screen is page 0 in a file.

**Where the file goes.** Your browser saves it in its usual downloads folder, and Setu shows "The file should appear in your downloads in a moment." (for the bundle, "Building the bundle — a large book can take a minute."). The name begins with the board, the class and the two languages, and ends with the format and the date and time.

**What some formats leave out.** Plain text, Moses, TMX and Hugging Face dataset can only hold pairs where both sides have text. Passages with no partner, or with an empty side, are left out of those four files. Setu does not tell you on screen how many were left out. The other formats include every pair.

## 11. Keyboard shortcuts

The **?** button at the top right of the screen opens a list of these, and so does pressing the **?** key. Press **Close**, or click outside the list, to shut it.

| **Key** | **What it does** |
|---|---|
| `1` to `6` | Answer the selected pair: 1 Exact, 2 Needs correction, 3 Missing or incomplete, 4 Structural mismatch, 5 Unclear, 6 Not applicable. On a pair with a passage on one side only, 1, 2 and 4 are refused |
| `←` `→` | Turn the page back or forward. Both books turn if **Turn both pages together** is ticked. If it is not ticked, only the left book turns |
| `Alt` with `←` `→` | Turn the left page only. If **Turn both pages together** is ticked, both turn. (`Option` on a Mac) |
| `Shift` with `←` `→` | Turn the right page only. If **Turn both pages together** is ticked, both turn |
| `n` | Select the next pair after the selected one that nobody has answered, whichever side it is on, and turn the books to the pages of its passages. With nothing selected, it finds the first one in the book |
| `p` | Pair the card selected on the left with the card selected on the right, when the amber bar is showing |
| `e` | Switch between Read and Correct it |
| `c` | Switch between Click a block and Drag to crop |
| `Esc` | Clear the selection |
| `+` `-` | Zoom both pages. This changes the page picture only, and does nothing you can see in the Text view |
| `?` | Open the list of shortcuts |
| `Ctrl` (hold) | Hide the block labels in the Page + blocks view |

**When a key does nothing.** The shortcuts switch themselves off while your cursor is in a box: a text box, the note box, a page-number box, a dropdown or a tick box. After you tick **Turn both pages together** or choose from a dropdown, click a card before you press a number key.

**Stray keys.** Letters you type with nothing in a box can change things. `c` switches the Tool to Drag to crop, and then clicking cards does nothing. `e` switches on Correct it. `n` selects a different pair and turns the pages to it. `p` pairs the two selected cards when they are not already a pair, so look at the amber bar before you press it. Press `c` or `e` again to switch either one back. A number key answers the selected pair, so make sure the right pair is selected.

In Chrome and Edge on Windows and Linux, Alt with the left arrow is also the browser's own shortcut for going back to the previous website, and Setu does not block it. If that happens, use your browser's forward button to return to Setu, and use the **‹** and **›** buttons instead.

## 12. Getting faster

**Keep your hands on the keyboard.** Click a card in the left column, read, press a number, click the next card. Or press `n` to jump to the next unanswered pair. It turns the books to the right pages by itself, so it works even when the pages are not matched.

**Read numbers and symbols first.** They are the same in every language, so a wrong digit or a broken formula shows up faster than a wrong word. Then read the words.

**Match the pages at the start of every chapter.** A minute spent matching (section 5) saves every later page from showing the right column a page out.

**Save notes for where they help.** Write one when you choose Needs correction and the fix is not obvious, Structural mismatch, or Unclear. An Exact needs no note.

**Treat a card with no partner as a decision, not a comparison.** The `n` key visits these pairs as well. When a card says "no Marathi paired", spend half a minute looking for the partner on the nearby pages of the other book. If you find it, pair the two passages (section 5). If you do not, press 3 for Missing or incomplete. Do not leave them for later: the counter will not reach its total without them.

**Make the writing bigger if you need to.** Hold Ctrl and press + in your browser. The zoom buttons in Setu do not help in the Text view.

**Stop and start freely.** Nothing is lost when you stop, because everything is saved as you go. Glance at the top bar first: it should not say that anything is unsaved. Next time, **Continue where you left off** (section 3) puts you back. A page where both sides agree takes seconds. A page where they do not can take several minutes of looking, and that looking is the valuable part, because it is what a program cannot do. Take breaks.

## 13. When to stop and ask a human

Some things are not yours to decide. Stop and tell your supervisor, rather than guessing, when:

- The two books do not seem to be the same book, for example a different subject or a different edition, or nothing lines up at any distance you try.
- A whole chapter or more is in a script or language you cannot read well enough to judge.
- You have answered, paired or unpaired a run of passages and then realised the wrong ones were selected. Answers and pairings can be changed, but tell someone the pages and the first words of the passages if you cannot remember them all, because pair numbers move when pairs change.
- The tool does something this manual does not describe, a red message appears that you do not understand, or the top bar says that a change needs you and you cannot see why.
- You are unsure what the project wants for a case such as a typo in the printed book, or a caption.
- Something makes you think "this cannot be right".

A guess recorded as an answer is worse than a gap. Ask first.

**What to tell them.** Give your name, the two books (as they read in the boxes), the page on each side, the first words of the passage, the pair number as you saw it (it can change when pairs change), what you expected and what happened. If a red message appeared, copy its exact words.

**If Setu itself will not load.** The link may have been replaced or closed. Ask whoever gave it to you. Your work is kept on their machine, so it is not affected.
