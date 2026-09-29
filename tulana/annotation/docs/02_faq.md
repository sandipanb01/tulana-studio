# Common questions

These are the questions a newcomer is most likely to have, grouped by topic. The manual explains each area at length. These answers are short and point you back to it. Where the honest answer is "we do not know yet" or "ask your supervisor", the answer says so.

## Getting started

**Do I need to install anything, and which browser should I use?**
You need nothing installed. Open the link you were given in a browser on a laptop or desktop computer. This guide was checked in Chrome. Firefox and Safari have not been checked, so if something looks wrong in one of them, switch to Chrome.

**The link will not open, or it opens a page that is not Setu. What now?**
The link is temporary. It stops working when whoever started Setu closes it, and this kind of link expires after about a week. If the page opens but looks like a different tool, add `/work/` to the end of the address. Otherwise ask whoever gave you the link for the current one. Your work is not affected, because it is kept on their computer.

**A box is empty, or the book I was asked to check is not in the list.**
The boxes list only books that have been added to this copy of Setu, and each box depends on the one above it, so work from the top down. A board that has only one language sits at the bottom of the first box under "only one language — cannot be paired", and it cannot be opened. If your book is not there, tell your supervisor the board, class, subject and language.

**What does "No scan of this book on this machine" mean? Is something wrong?**
Nothing is wrong. A scan is a picture of a printed page. In the Text view this box appears at the top of each column every time, whether or not the scans exist, and it only says that you are reading text and not a picture. Everything you need for checking translations works without scans.

## Losing work, and coming back

**Will I lose my work if I close the tab or my laptop dies?**
No. Answers are saved the moment you press them, and corrections the moment you click out of the box. They are saved on the computer that runs Setu, not on yours. The one thing at risk is text you have typed and not yet clicked away from, so click away from the box and wait for the green flash, or for "Saved." beside the note box, before you close anything.

**Do I have to press Save?**
There is no save button. An answer is saved the moment you press it: the button turns solid teal and "Saved." appears beside the note box. A correction is saved when you click outside its box, and the card flashes green. If a red message appears at the bottom of the screen, that save did not happen.

**I stopped yesterday. How do I get back to where I was?**
Open the same two books with the same book on the left. Then open **Saved work**, choose "Not checked yet" and click the first card, and Setu takes you to that pair's pages. Setu does not remember the page you were on, and pairs you skipped earlier are listed first, so scroll down to find where you stopped. Section 3 of the manual has the details, including a shortcut with the `n` key.

**What happens if the internet drops while I work?**
Nothing you have already saved is lost. Anything you try while the connection is down fails, with a red message at the bottom of the screen. In Chrome the message reads "Failed to fetch", and other browsers word it differently. An answer that fails does not light up its button and is not saved, so press it again when you are back online. A correction that fails stays in its box until you turn the page, so once you are back online, click into the box and click away again to save it.

**A page would not turn and a red message appeared, such as "Failed to fetch". Can I keep pressing ›?**
No. The screen stays on the old page, but Setu has already counted the turn, so the next press that works skips a page. Type the page number you want into the page box and press Enter instead.

**A message flashed at the bottom of the screen and vanished. What did it say?**
Messages there disappear on their own, after about three seconds for an ordinary one and about seven for a red one. If something did not work and you missed the message, do it again and read it. A failed answer or correction also leaves its message beside the note box.

## The two columns

**What is the "machine-read text"?**
The text in both columns was read off scanned pictures of the printed pages by a computer program. Setu's buttons call it the parser. A person did not type the text, so it contains mistakes: wrong letters, missing words, scrambled formulas. Checking it is your job. Which passage goes with which was also suggested by a program, and it is only a suggestion until you have looked at it.

**What do the coloured boxes and outlines mean?**
The colour of a card's left edge is the kind of passage (paragraph, equation and so on), and the key is the row of small coloured labels at the bottom of the left panel. A dashed outline means the pair has not been answered, a solid one means it has, and a grey card with a dotted outline belongs to no pair. A tinted card with a ring is the one you have selected. The colours are handed out as Setu goes, so read the word on the card's top line and do not learn the colours.

**The left side shows Chapter 3 and the right side shows Chapter 5. Is something broken?**
No. Two editions of a book rarely start their chapters on the same page, so each side has its own chapter and page controls. Untick **Turn both pages together**, choose the chapter you want on each side, find the pages that match, and press **⇄ These two pages match**. Section 5 of the manual walks through it.

**The page number does not match my printed book. Why?**
The number on screen is the page's place in the book's scanned file, counting from 1. If the file starts with a cover or a blank page, that counts as page 1, so the number printed on the paper can differ. Files you download count from 0, so page 1 on screen is page 0 in the file.

**Why do some passages have no partner?**
The matching program pairs passages by looking for things that read the same in every language, such as formulas and numbers like 1.2, and by keeping the two books in order. A passage with no such anchor, or one that one edition cut differently, can be left without a partner, and some passages exist in only one edition. In the one pair of books that was measured, 29 pairs in every hundred had a passage on one side only. Setu leaves these for a person and does not invent a partner. Record them as Missing or incomplete, or as Structural mismatch if you can find the words elsewhere on the other side.

**The box under the right column says "Nothing on this side". What does that mean?**
Either the passage really has no partner, or its partner is on a page that the right column is not showing. Setu only looks for the partner on the page on screen. Check that the right column is on the matching page, by looking for the same pair number, before you record the passage as missing.

**A passage is empty and says "the parser found no text here". What do I do?**
Empty means the machine could not read anything there. It does not mean the page is blank. Choose Missing or incomplete, which covers "one side is empty". In Correct it mode the empty box can be typed into, but typing a whole passage in from the page is transcribing and not checking, so ask your supervisor before you do it.

**What is a "block", and what is "pair #7"?**
A block is Setu's word for one piece of text on a page: a heading, a paragraph, an equation, a caption. A pair is a passage on the left together with its partner on the right, and "#7" is its number in these two books. Both cards of a pair carry the same number, so the partner of pair #7 on the left is pair #7 on the right.

## Text that looks wrong

**My text is full of dollar signs, backslashes and angle brackets. Is it broken?**
No. A formula is written between dollar signs as code, for example `$A = \{1, 3, 5, 7, 9\}$`, and a table is written as a run of tags, which are short codes in angle brackets, such as `<table><tr><td>`. That is how the parser stores them. Compare the numbers and symbols on the two sides, and read the words inside the tags.

**The words look wrong: letters swapped, a word missing, a formula scrambled. What do I do?**
That is what this work is for. Switch to **Correct it**, fix what is wrong, click away, and choose Needs correction. You will often have no picture of the printed page, so correct only what you can be sure of from the two texts. If you cannot tell what the text should say, choose Unclear and put in a note what stopped you.

**The printed book itself has a spelling mistake. Do I fix it?**
No. Fix what the machine got wrong so that the text matches the printed page, and leave the book's own mistakes as they are, because the corpus should record what is printed. Put a note on your answer saying that the mistake is in the book. If you cannot tell whether an error is the book's or the machine's, choose Unclear. Setu does not enforce this rule, so if your supervisor gives you a different one, follow theirs.

**Where are the pictures, and what do I do about tables?**
Setu shows text only. A picture has no text, so it does not appear at all unless you tick **Include headers and page numbers**, when it shows as a grey "Figure" card that belongs to no pair and cannot be answered. A caption under a picture is text and appears as an ordinary pair. The project's wording puts picture captions under Not applicable, so ask your supervisor whether you should check them. A table appears as a run of tags with the cell contents in between, so compare the contents cell by cell, in order.

**I do not understand the passage, or I cannot read the script well. Do I have to answer it?**
Do not guess. Choose Unclear and write a note that says what you could not judge, so that a reviewer can pick it up. If a whole chapter or more is beyond you, stop and tell your supervisor.

## Choosing answers

**Needs correction or Structural mismatch?**
Ask whether the two passages are the same piece of the book. If they are, and the text has a mistake in it such as a wrong number, a typo or a garbled formula, choose Needs correction. If they are not the same piece, or one side has cut in two what the other keeps together, choose Structural mismatch and say in a note where the rest is.

**Missing or incomplete, or Not applicable?**
Ask whether something should be there. If text that belongs in the book is absent or empty on one side, choose Missing or incomplete. If nothing was meant to be there, because the passage is a page header, a decoration or a label that needs no translation, choose Not applicable.

**I pressed the wrong number. Can I undo it?**
Press the right number. The new answer replaces the old one, and the old one stays in a record that you cannot see on screen. If you had also written a note, type it again, because an empty note box replaces the saved note with nothing.

**I think my answer went to a different pair from the one I meant.**
Look at the line above the two boxes: it names the pair your answer goes to, for example pair #2. If you selected a card on the left and then clicked one on the right, both stay selected and the answer goes to the left one. Press `Esc`, select the pair you meant, and answer it. Then select the pair that got the wrong answer and answer it properly. If you cannot check it now, choose Unclear and write "answered by mistake, not checked" in the note, because there is no way to set a pair back to Not checked yet.

**The note I typed has vanished.**
A note is saved together with the answer, and only then. After you press an answer the note box empties on screen although the note was saved, and a note typed after you answered is lost unless you press an answer again. Type the note first, then press the answer. To change a note, type all of it again and press the same answer again.

**Do I have to answer every passage, and in order?**
Setu does not force you to do either. You can work in any order, and a pair you leave stays "Not checked yet", which tells the next person that nobody has looked at it. The aim of the work is that every pair gets an answer, so ask your supervisor which chapters are yours. The counter at the top right counts every pair in the two books, including passages that exist on one side only.

**What does the counter "12 / 21 answered" count?**
The first number is the pairs that have an answer, and the second is all the pairs in the two books you have open. It counts everybody's answers, and it includes passages that have no partner. It goes up by one each time a pair gets its first answer.

## When the screen does something odd

**The answer buttons have disappeared.**
The buttons show only when exactly one pair is selected. You may have selected nothing, several cards (with Ctrl-click or Shift-click), or a header or page number that belongs to no pair, or you may have turned the page since you selected. Press `Esc` and click one card in the left column.

**I click on a card and nothing happens.**
The Tool switch in the left panel is probably on Drag to crop, which happens when the `c` key is pressed by accident. Click "Click a block" under Tool, or press `c` again.

**Passages have vanished from the column.**
Look at **Show only** at the bottom of the left panel. If it is not on "All kinds of block", it hides every other kind of passage from the next time a page is drawn. Set it back to "All kinds of block", then turn the page and come back. Also check that **Dim the rest** is not ticked.

**I pressed some keys and things changed: the columns became editable, or clicks stopped working.**
The letters `e`, `c` and `n` are shortcuts. `e` switches Correct it on and off, `c` switches the Tool between Click a block and Drag to crop, and `n` selects the next pair nobody has answered. Press `e` or `c` again to switch either one back. The shortcuts switch off while your cursor is in a box, so click into a box before you type anything.

## Correcting text

**How do I correct text, and how do I know it saved?**
Switch to **Correct it**, click into the text of a card, fix it, and click anywhere outside the box. The card flashes green for a second or two, the word "saved" and a blue "corrected" label appear on its top line, and "Saved." shows near the note box. Then choose your answer. Section 7 of the manual has the full steps.

**The "corrected" label is on a card I did not touch.**
The label marks a pair, not a side. If either half of a pair has been corrected, by you or by anybody else, both halves show the label once the page is redrawn.

**How do I undo a correction?**
Select the card by clicking its top line. With **Correct it** switched on, press "Put back what the parser read" under the box for that side. That restores the machine's original text, not your previous version. The button appears under both boxes, and pressing it under a side you did not change does nothing.

**A red message says "Somebody else changed this while you were typing". What do I do?**
Somebody saved a correction to that passage before you did, and Setu kept theirs instead of overwriting it. Your typing is still in the box, whatever the message says about a history, so copy it (select it and press Ctrl+C) before you do anything else. Then turn the page and come back to see their version, and decide whether your change is still needed.

## Working with other people

**Can two of us use the same link at the same time?**
Yes. Each of you sees your own screen, and answers and corrections go into one shared record as you make them. Your screen does not update when somebody else answers. You see their work the next time a page is drawn. Setu has not been tested with a large group, so agree in advance who takes which chapter.

**What if we both answer the same pair?**
The later answer replaces the earlier one, and neither of you is told. The earlier answer stays in a record that you cannot see. Two people correcting the same passage is different: the second save is refused, as described above.

**Does anyone see my name?**
Setu attaches the name you typed to every answer and correction, but it does not show it on anybody's screen. It does appear in the `updated_by` column of the Excel, CSV, TSV, JSON, JSON Lines and Parquet downloads, where it records the last person to change each pair, and whoever runs Setu can look it up. If you leave the box empty your work is still saved, but it carries no name. Setu has no accounts or passwords, so anyone who has the link can use it under any name. Treat the link like a key, and share it only with people who are annotating.

**Can I see or undo somebody else's answers?**
The Saved work tab lists everybody's answers but does not say who gave each one. You can replace an answer by answering the pair again, but agree with whoever gave it first. If you think somebody else's answer is wrong and you cannot reach them, tell your supervisor.

## Downloading

**Which format should I download?**
Choose **Excel workbook (.xlsx)** if you do not know which you need. It is a spreadsheet with one row for each pair, and it opens in Excel, LibreOffice or Google Sheets. The box starts on JSON Lines, which is meant for programs. If someone tells you which format they need, choose that one.

**Some passages are missing from my download.**
Plain text, Moses, TMX and Hugging Face dataset can only hold pairs where both sides have text, so passages with no partner, or with an empty side, are left out of those four. Setu does not tell you on screen how many were left out. The other seven formats include every pair. The zip contains all eleven, so its four files of that kind leave the same passages out.

**How do I download only the pairs I have answered?**
Choose "Only what has been answered" in the second box before you press **Download**. It includes everybody's answers, not only yours. The **Every format, as a zip** button ignores that choice.

## Practical questions

**How long does a book take?**
We do not know yet, because there is no measured pace for this work. The counter at the top right tells you how many pairs the two books hold, and the one pair of books that was measured held 2,304. Work for an hour, divide the pairs you answered by the hours, and you have your own pace. Ask your supervisor what they expect.

**Can I work on a phone or a tablet?**
Not properly on a phone. On a narrow screen the controls panel covers the columns, the button that hides it cannot be brought back without reloading the page, the panel under the columns overlaps the right column, and the page controls are inside the hidden panel. A tablet has not been tried, and the full layout needs a screen wider than 1,000 pixels. Use a laptop or desktop computer if you can.

**Can I use a dictionary or a translation website to help me?**
Nothing in Setu stops you, and nothing in it needs one. Whether your project allows it is your supervisor's decision, so ask before you rely on one.

**Who do I ask?**
Ask your supervisor about anything to do with the work: what to answer, what to correct, how much to do. Ask whoever gave you the link about anything that stops Setu working, such as a link that will not open. Tell them your name, the two books, the page on each side, the pair number, what you expected and what happened, and copy the words of any red message.
