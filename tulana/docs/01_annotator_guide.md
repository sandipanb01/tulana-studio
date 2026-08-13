# Tulana Studio — Guide for Annotators and Linguists

This guide assumes no technical knowledge. It explains what you are doing, how
to do it, and what happens to your work.

## 1. What this tool is for

You are building a **parallel corpus**: pairs of passages that say the same
thing in two languages, taken from the same textbook published in both.

On the left you see the English edition of a textbook. On the right, the same
textbook in Hindi, Marathi, Tamil, or whichever language you chose. Your job is
to find matching passages — a worked example, a definition, an exercise — and
clip both, so the pair can be used as training and evaluation data.

You are not typing anything out. You are drawing rectangles.

## 2. Getting started in four steps

1. **Type your name** in the box at the top right. It is attached to everything
   you save, so your work is attributable.
2. **Choose the textbook.** On the left panel pick the board and class, then the
   target language, then which volume of each edition. Press
   **Open side by side**.
3. **Find a passage.** Scroll either pane. Use *Go to page* to jump, or click a
   chapter in the bookmark list. Tick **Scroll both together** if the two
   editions run roughly in step.
4. **Clip the pair.** Drag a rectangle around the passage on the English page,
   then drag around the same passage on the target page. Press **Save pair**.

That is the whole loop. Repeat until the book is done.

## 3. Drawing a good clipping

It behaves like a desktop snipping tool.

- **Drag, do not click.** A tap does nothing; press and drag to draw a box. A
  live readout shows the size as you go.
- **Adjust it afterwards.** Once you let go, eight small squares appear on the
  edges and corners. Drag any of them to resize. Drag the middle of the box to
  move the whole thing without changing its size.
- Nothing is committed until you press **Save pair**, so take your time.
- Include the whole passage — the heading if it has one, and every line of it.
  Do not include the page number, the running header, or the next passage.
- The two boxes do not have to be the same shape. Translations run longer or
  shorter, and pages break differently. What matters is that both boxes contain
  *the same content*.
- If you draw badly, just draw again — the newest box on that page replaces the
  previous one. **Clear** removes both.
- Zoom with **+** and **−** if the text is small. Zoom does not affect quality:
  the clipping is always re-cut from the original PDF at print resolution, not
  from what is on your screen.

## 3b. Giving the chunk a category

Under the label box is a row of categories — Definition, Theorem, Example,
Exercise, Activity, Table, Figure caption, Summary. Each has a number on it:
press that number and the category is selected, press it again to unselect.
Click them if you prefer.

Categories are optional but worth doing: they travel into the export, so
whoever uses the corpus later can pull out just the worked examples, or just
the definitions, without looking at a single image. Your project lead can add
categories of their own.

## 4. What to skip

**Geometry and conics are excluded from this corpus.** That includes circles,
triangles, quadrilaterals, similarity, congruence, coordinate geometry,
constructions, mensuration and trigonometry. Those chapters are diagram-led, so
a clipped text region rarely carries the meaning and the pair would mislead.

The studio helps: when a page looks like an excluded topic, the page is marked
in the corner, a warning appears in the panel, and if you save anyway the pair
is recorded as **excluded** rather than silently included. Excluded pairs are
left out of exports unless someone deliberately asks for them.

Also skip: pages that are purely a figure, tables of contents, answer keys, and
anything where you cannot tell that the two sides match.

## 5. Working on a phone or tablet

Everything works with a finger. The two editions stack vertically instead of
side by side, and the ☰ button opens the controls. Drag on a page exactly as you
would with a mouse. Pinch-zoom works as usual for reading; use **+** and **−**
when you want the clipping box to be easier to place.

## 6. Where your work goes

Every pair is saved immediately to the studio's database — there is no separate
"save the project" step and nothing is held in the browser. Each clipping is
stored twice over: as an image cut from the PDF at 300 DPI, and as the exact
page and rectangle it came from, so it can always be re-cut.

Open the **Saved pairs** tab to see everything clipped so far, side by side.
From there you can mark a pair excluded, put it back, or delete it.

## 7. What comes out at the end

The **Export** tab produces a single ZIP, a folder named for the textbook:

```
NCERT_class9_math/
    eng_ncert_math_1.png   .jpg   .pdf
    hin_ncert_math_1.png   .jpg   .pdf
    eng_ncert_math_2.png   …
    hin_ncert_math_2.png   …
    manifest.json     every chunk with pages, coordinates and extracted text
    pairs.jsonl       one chunk per line, for data pipelines
    pairs.csv         the same, for a spreadsheet
    parallel.tsv      just the two texts, tab separated
    README.md         a readable summary
```

The name says everything: `eng_ncert_math_7` and `hin_ncert_math_7` are the same
passage, chunk 7, from the NCERT mathematics textbook. Each clipping is written
as PNG, JPG and a one-page PDF, all cut from the original at 300 DPI.

## 8. Keyboard shortcuts

| Key | Action |
|---|---|
| <kbd>Ctrl</kbd>+<kbd>S</kbd> | save the current pair |
| <kbd>Esc</kbd> | clear the current selection |
| <kbd>L</kbd> | scroll both panes together |
| <kbd>+</kbd> <kbd>−</kbd> | zoom |
| <kbd>1</kbd>–<kbd>8</kbd> | apply a category to the chunk |
| <kbd>?</kbd> | this shortcut list |

## 9. Frequently asked questions

**The two editions are not on the same page number.**
That is normal — translations paginate differently. Scroll each pane to the
right place independently, and untick *Scroll both together*.

**A passage runs across two pages.**
Clip the part on the first page as one pair, and the continuation as the next
pair. Give them the same label with "(1)" and "(2)" so the relationship is clear.

**I cannot find the matching passage.**
Use the chapter bookmarks to get to the same chapter, then look for the same
example number or figure. If the translated edition genuinely omits it, skip it.

**I clipped something wrong and already saved.**
Go to **Saved pairs** and delete it. Nothing is permanent against your wishes.

**Does the image quality depend on my screen?**
No. The clipping is re-cut from the original PDF at 300 DPI regardless of your
zoom or device.

**Is my work lost if the browser closes?**
No. Each pair is saved to the server the moment you press **Save pair**.
