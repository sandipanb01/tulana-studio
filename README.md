# Tulana Studio

Tulana Studio is a document-processing, OCR/alignment, PDF-ground-truth, and translation-quality research platform.

## Repository

```text
tulana-studio/
├── tulana/        # Application code
└── board_pdfs/    # Board textbook PDF corpus
````

The application and PDF corpus are kept separate inside the same repository.

---

# Quick Start

## 1. Clone

```bash
git clone <REPOSITORY_URL>
cd tulana-studio
```

## 2. Download the PDFs

The board PDFs are stored using Git LFS.

```bash
git lfs install
git lfs pull
```

Verify:

```bash
# Windows
(Get-ChildItem ".\board_pdfs" -Recurse -File -Filter "*.pdf").Count

# Linux
find board_pdfs -type f -iname "*.pdf" | wc -l
```

---

# Windows

Run these commands in PowerShell **from the repository root**:

```powershell
cd tulana
```

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Install all dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify the important dependencies:

```powershell
python -c "import gradio; print('Gradio:', gradio.__version__)"
python -c "import fitz; print('PyMuPDF:', fitz.__version__)"
```

Connect the PDF corpus:

```powershell
New-Item -ItemType Junction -Path ".\data" -Target "..\board_pdfs"
```

Verify that Tulana can see the PDFs:

```powershell
(Get-ChildItem ".\data" -Recurse -File -Filter "*.pdf").Count
```

Run the application:

```powershell
python app.py
```

Or run the Gradio interface:

```powershell
$env:GRADIO_SERVER_PORT="7870"
python share_gradio.py
```

The terminal will print the local URL and, when sharing is enabled, a temporary public `gradio.live` URL.

---

# Linux / Cluster

Run from the repository root:

```bash
cd tulana
```

Create the environment:

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify:

```bash
python -c "import gradio; print('Gradio:', gradio.__version__)"
python -c "import fitz; print('PyMuPDF:', fitz.__version__)"
```

Connect the PDF corpus:

```bash
ln -s ../board_pdfs data
```

Verify:

```bash
find data -type f -iname "*.pdf" | wc -l
```

Run:

```bash
python app.py
```

Or:

```bash
python share_gradio.py
```

For permanent deployment, use the target cluster/server's normal process manager and networking configuration rather than a temporary Gradio share.

---

# Updating the Application

Change files inside:

```text
tulana/
```

Then:

```bash
git add tulana/
git commit -m "Update Tulana"
git push
```

# Updating the PDF Corpus

Add or replace PDFs inside:

```text
board_pdfs/
```

Then:

```bash
git add board_pdfs/
git commit -m "Update board PDF corpus"
git push
```

Pull updated PDFs on another machine:

```bash
git lfs pull
```

---

# Important

The following are intentionally not stored in GitHub:

```text
.venv/
.gradio/
__pycache__/
*.db
*.sqlite
.env
```

They are local/generated/runtime files and are recreated when the application is installed on a new machine.

The application should use relative paths and should not depend on machine-specific paths such as `D:\Tulana`.

---

# Troubleshooting

### PyMuPDF missing

```bash
python -m pip install -r requirements.txt
python -c "import fitz; print(fitz.__version__)"
```

### Gradio missing

```bash
python -m pip install -r requirements.txt
python -c "import gradio; print(gradio.__version__)"
```

### PDFs missing

```bash
git lfs install
git lfs pull
```

### Gradio port busy on Windows

```powershell
$env:GRADIO_SERVER_PORT="7871"
python share_gradio.py
```

---

# Current Repository Layout

```text
tulana-studio/
│
├── tulana/
│   ├── app.py
│   ├── requirements.txt
│   ├── config.py
│   ├── db.py
│   ├── share_gradio.py
│   ├── docs/
│   └── static/
│
└── board_pdfs/
    └── board textbook PDFs
```

The basic workflow is:

```text
Clone
  ↓
git lfs pull
  ↓
cd tulana
  ↓
create .venv
  ↓
activate .venv
  ↓
pip install -r requirements.txt
  ↓
connect data → board_pdfs
  ↓
python app.py
  ↓
or: python share_gradio.py
```

````

Then just update GitHub:

```powershell
cd "D:\Bodhan-Tulana-Studio"
git add README.md
git commit -m "Improve README"
git push
````

