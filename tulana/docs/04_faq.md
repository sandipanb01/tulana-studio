# Tulana Studio — Questions and Troubleshooting

## For annotators

**Nothing appears when I press "Open side by side".**
Check all four dropdowns are set: board and class, target language, and a volume
for each edition. If the target list is empty, that board has no translated
edition indexed yet — tell your administrator.

**The pages look blurry.**
The on-screen view is deliberately light so scrolling stays fast. Clippings are
cut from the original PDF at 300 DPI, so the exported image is sharp regardless.
Use **+** if you want a bigger view while working.

**Drag does not draw a box.**
Draw on the page image itself, not the grey margin, and drag at least a
centimetre — a small movement is treated as a tap so that scrolling still works.

**A warning says the page is geometry.**
Geometry and conics are out of scope. You can still save, but the pair is marked
excluded and left out of exports.

**I need to stop and come back tomorrow.**
Just close the tab. Every pair was saved when you pressed **Save pair**.

## For administrators

**A textbook does not appear in the list.**
A board and class is only offered once it has an English edition *and* at least
one other language. Check both PDFs are in the data folder, then `POST
/api/rescan`. If a file is mis-classified, check its name — the first segment is
read as the board.

**A file is classified with the wrong language.**
Board and language codes overlap (`guj`, `pun`). The first segment of the file
name is treated as the board; name files as `BOARD_LANG_CLASS`, for example
`GUJ_EN_10.pdf`, and both are read correctly.

**"PyMuPDF is not installed on the server".**
`pip install PyMuPDF`. The studio imports it in one place and reports the
version at `GET /api/health`.

**Exports are missing pairs.**
Excluded pairs are left out by default. Tick *include excluded pairs*, or clear
the exclusion on the Saved pairs tab.

**Disk usage is growing.**
`state/pages/` is a render cache and can be deleted at any time; it rebuilds on
demand. `state/crops/` is the annotators' work and must be kept.

**Can two people work at once?**
Yes. Each saves to the same database and pairs are numbered per project as they
arrive. Put each annotator on a different textbook to avoid duplicate coverage.

## Known limits, stated plainly

**Extracted text is a bonus, not a guarantee.** Where a PDF has a readable text
layer, the text under each rectangle is stored alongside the image. Many Indian
textbook PDFs are scans, or use fonts whose encoding was never mapped to
Unicode; for those the text field will be empty or unreadable. **The images are
always correct** — they are pictures of the page — and the images are what the
corpus is built from.

**Excluded-topic detection is a keyword match** on the page text. It cannot see
into a scanned page, and it will occasionally flag a page that merely mentions a
circle. It is a prompt for your judgement, not a gate.

**Page alignment between editions is not automatic in Phase I.** You scroll both
editions yourself. *Scroll both together* keeps them proportionally in step,
which helps when the editions run parallel, and can be turned off when they
drift.
