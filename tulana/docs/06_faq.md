# Questions

**A textbook is not in the dropdown.**
It needs a layout JSON *and* a board, class and subject that match an edition in
another language. Call `GET /api/blocks/mapping` — it names every book as
mapped, missing or worth a look. The commonest cause is not the file name: the
**subject must match too**. A Malayalam *Science* book beside an English
*Mathematics* book will never pair.

**The page is blank but the blocks are there.**
The layout covers that page and the PDF does not — a truncated copy, or a
different edition of the same book. The blocks and their text are still usable;
only the picture is missing.

**Everything is blank and there are no page images at all.**
The PDFs are probably Git LFS pointers. Run `git lfs install && git lfs pull`.

**A block has no text.**
Diagrams carry none, and a page without a usable text layer yields none. Empty
means the parser recovered nothing there, not that the page is empty. Select it
anyway if it belongs to the passage — its position is recorded.

**I turned the page and my selection is still highlighted.**
That is deliberate. A passage that fits one English page often runs onto the
next in the target language, so the selection is kept until you clear it. The
panel tells you how many blocks are selected on pages you are not looking at.

**A pair has no image.**
The PDF was not on disk when it was saved. Fetch it — usually `git lfs pull` —
then press **Try again** on the pair.

**Why two images on one side?**
The selection spans two pages. One image per page: a single image cannot cross a
page break.

**I closed the tab by mistake.**
Your selection was kept. Reopen the same two editions and it is there.

**Two of us edited the same pair.**
The last save wins, and both are recorded in the audit log. Agree who owns a
textbook before you start; the studio does not lock.

**I deleted a pair I needed.**
Deletion is permanent — that is what *exclude* is for. If you have an export
from before, the pair is in it.

**Can I export only the pairs I have checked?**
Yes. Approve them, then choose *Approved only* in Export.

**Which format for training a translation model?**
JSONL, or Moses if your pipeline wants two aligned files. Hugging Face if you
are pushing to the Hub.

**Which format for a human translator?**
TMX. It opens in OmegaT, memoQ and Trados.

**The link stopped working.**
A `gradio.live` link lasts about a week and changes on restart. Nothing is lost
— the work is on the host, not in the link. For a permanent address, put the
studio behind nginx.

**Can I use this on a phone?**
Yes. The panes stack and the controls move behind the menu button. Selecting
small blocks is fiddly; zoom in first.
