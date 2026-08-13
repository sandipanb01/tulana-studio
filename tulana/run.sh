#!/usr/bin/env bash
# Tulana Studio — start the clipping workspace.
set -euo pipefail
cd "$(dirname "$0")"
export TULANA_DATA_DIR="${TULANA_DATA_DIR:-$PWD/data}"
python3 -m pip install -q -r requirements.txt
exec python3 app.py            # http://localhost:7862
