#!/usr/bin/env python3
"""Publish Tulana Studio on a public link.

    python3 share_gradio.py

Prints an https://….gradio.live address serving the studio itself. The link is
a tunnel, not a copy: everything is still stored in this machine's `state/`
folder, so restarting — and getting a new link — never loses a clipping.
"""
import os
import sys
import time
import webbrowser
from urllib.parse import urljoin

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config  # noqa: E402

try:
    import gradio as gr
except ImportError:
    sys.exit("Gradio is not installed. Run:  pip install gradio")

from app import app as studio_app  # noqa: E402

MOUNT = "/studio"
PORT = config.free_port(int(os.environ.get("TULANA_PORT", "7862")))

LANDING = """
<div style="max-width:640px;margin:9vh auto;text-align:center;
            font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;line-height:1.6">
  <div style="font-size:44px;font-weight:700">तुलना <span style="color:#0e7a72">Studio</span></div>
  <p style="color:#556;font-size:17px">Clip parallel passages from textbooks,
     side by side, in any Indian language.</p>
  <a href="./studio/" target="_blank" style="display:inline-block;margin-top:18px;
     background:#0e7a72;color:#fff;text-decoration:none;font-size:18px;font-weight:600;
     padding:14px 34px;border-radius:10px">Open the clipping workspace →</a>
  <p style="color:#889;font-size:13px;margin-top:26px">
     Works on a phone or tablet as well as a laptop. Every pair you save is
     written to the studio's database immediately.</p>
</div>
"""

with gr.Blocks(title="Tulana Studio") as demo:
    gr.HTML(LANDING)

server_app, local_url, share_url = demo.launch(
    server_name="0.0.0.0", server_port=PORT, share=True,
    prevent_thread_lock=True, inbrowser=False)

# A sub-application mounted onto a server that has already started never
# receives startup events, so index explicitly — otherwise the studio comes up
# with an empty textbook list and an interface waiting for data that never
# arrives.
try:
    from app import initialise
    initialise()
except ImportError:
    pass

server_app.mount(MOUNT, studio_app)


def at(base: str) -> str:
    """Join a base URL to the mount point.

    Gradio returns the share URL without a trailing slash and the local URL
    with one, depending on version. Concatenating blindly produced
    `https://xxxx.gradio.livestudio/` — a dead link printed as the headline
    instruction."""
    if not base:
        return ""
    return urljoin(base if base.endswith("/") else base + "/", MOUNT.lstrip("/") + "/")


public_url = at(share_url)
machine_url = at(local_url)

print(f"""
{'=' * 70}
  Tulana Studio is live.

  Public link (share this):
      {public_url or '(tunnel unavailable — see note below)'}

  On this machine:
      {machine_url}

  Textbooks: {config.DATA_DIR}
  Your work: {config.STATE_DIR}
{'=' * 70}
""")
if not share_url:
    print("  The gradio.live tunnel could not be created — this machine may have\n"
          "  no route to Gradio's tunnel service. The studio still works locally.\n")
else:
    try:
        webbrowser.open(public_url)
    except Exception:
        pass

try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    print("Shutting down.")
