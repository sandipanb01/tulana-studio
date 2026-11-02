# Selecting and cropping

There are two tools, and they answer different questions.

**Click blocks** takes what the parser found, and brings its text with it.
**Drag to crop** takes what *you* decide, as a rectangle, and cuts exactly that.

A figure with its caption and the line beneath may be one passage to a reader
and three blocks to the parser. A hand-drawn diagram or a margin note was never
a block at all, so no amount of clicking would reach it. Both tools work across
pages, both are kept automatically, and both are cut from the original PDF as
parallel images.

Use them together in one pair if that is what the passage needs.

## Drag to crop

Switch the tool, then drag a rectangle over the passage. Drag inside a crop to
move it, the corner grip to resize, the **×** to remove it. Every crop is listed
in the sidebar with the page it is on; **go** jumps back to it.

Draw as many as you need, on as many pages as you need. A tap without a drag
does not create one.

## Clicking blocks

A **block** is a region the document parser found on a page — a paragraph, a
table, an equation, a heading — with the text it read inside it. Each carries
its reading-order number and a colour for its type.

## Selecting

**Click** a block to select it. Click again to deselect.

**Shift-click** takes everything between the last block you clicked and this
one, *in reading order* — not in the order you clicked them. Selecting a worked
example out of sequence still reads the way the page does.

**All on page** takes every block on the current page, honouring the type filter
if you have one set.

**Clear** empties both sides. So does `Esc`.

## Across pages

This is the part worth understanding.

**Your selection survives turning the page.** Translated text is longer, so a
passage that fits on one English page often runs onto the next in Marathi or
Malayalam. A selection confined to a single page could not express that
alignment at all.

So: select what you need on page 12, turn to page 13, carry on selecting. The
panel tells you when blocks are selected on pages you are not looking at —
*"4 target block(s) selected on other pages"* — so nothing is ever silently
included.

A pair that spans pages is marked **spans pages** in Saved pairs.

## The cropped images

While you select, the panel shows the region that will be cut from each page —
the box around everything you have picked there. That is what gets saved as an
image, cut from the original PDF at 300 DPI.

**One image per page each side touches.** A pair spanning two pages has two
images on that side. A single image cannot span a page break, and one image that
silently showed only the first page would be worse than two honest ones.

If the PDF is not on disk there is no image, and the pair says so rather than
showing an empty box. Once the PDF arrives, **Try again** on the pair cuts them.

## Reading the selection

The text of everything selected appears beneath the pages, both languages side
by side, assembled in reading order across every page involved. This is what
gets saved.

Some blocks have no text. A diagram carries none, and a page without a usable
text layer yields none either. Empty means *the parser recovered nothing here*,
not *the page is blank*. Select such a block if it belongs to the passage — its
position is recorded even when its text is not.

## Narrowing what you see

**Show only** limits the overlay to one block type — every Table, say — which
helps on a dense page. **Dim unselected** fades everything you have not picked.
**Reading order** turns the numbers and the order path on and off.

## Zoom

Each pane zooms independently, and the two need not match: an English page at
100% next to a Malayalam page at 150% is often exactly what you want. `+` and
`−` zoom both together. **⤢** fits the page again.

Drag the divider between the panes to give one side more room.

## Keyboard

| key | does |
|---|---|
| `←` `→` | previous and next page |
| `+` `−` | zoom both panes |
| `Esc` | clear the selection |
| shift-click | select a range in reading order |
