# Tulana Studio

Tulana Studio is a document-processing, OCR/alignment, PDF-ground-truth, and translation-quality research platform.

The repository contains both the application source code and the board textbook PDF corpus, kept as separate components within the same repository.

## Repository Structure

```text
tulana-studio/
├── README.md
├── .gitignore
├── .gitattributes
│
├── tulana/
│   ├── app.py
│   ├── config.py
│   ├── db.py
│   ├── fetcher.py
│   ├── library.py
│   ├── pdflib.py
│   ├── share_gradio.py
│   ├── requirements.txt
│   ├── selftest.py
│   ├── check_sources.py
│   ├── docs/
│   └── static/
│
└── board_pdfs/
    └── board textbook PDF corpus
```

The application code and PDF corpus are intentionally separated.

---

# Quick Start

## 1. Clone the repository

```bash
git clone https://github.com/sandipanb01/tulana-studio.git
cd tulana-studio
```

## 2. Download the PDF corpus

The board PDFs are stored using Git LFS.

```bash
git lfs install
git lfs pull
```

Verify the corpus.

### Windows

```text
(Get-ChildItem ".\board_pdfs" -Recurse -File -Filter "*.pdf").Count
```

### Linux

```bash
find board_pdfs -type f -iname "*.pdf" | wc -l
```

The current repository contains 144 board PDFs.

---

# Windows

PowerShell is NOT required by Tulana. Any terminal capable of running Python can be used.

## 1. Enter the application

```text
cd tulana
```

## 2. Create the Python environment

```text
python -m venv .venv
```

## 3. Install dependencies

The complete Python dependency list is stored in `requirements.txt`.

```text
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 4. Verify Gradio and PyMuPDF

```text
.venv\Scripts\python.exe -c "import gradio; print('Gradio:', gradio.__version__)"
.venv\Scripts\python.exe -c "import fitz; print('PyMuPDF:', fitz.__version__)"
```

## 5. Connect the PDF corpus

Tulana expects the PDF corpus to be accessible through:

```text
tulana/data
```

Create a Windows directory junction from `tulana/data` to `board_pdfs`.

From a Windows terminal:

```text
mklink /J data ..\board_pdfs
```

Verify:

```text
(Get-ChildItem ".\data" -Recurse -File -Filter "*.pdf").Count
```

Expected:

```text
144
```

## 6. Run the application

```text
.venv\Scripts\python.exe app.py
```

## 7. Run the Gradio interface

```text
.venv\Scripts\python.exe share_gradio.py
```

The terminal will display the local URL and, when sharing is enabled, a temporary `gradio.live` URL.

No PowerShell-specific activation step is required.

---

# Linux / Cluster

## 1. Enter the application

```bash
cd tulana
```

## 2. Create the Python environment

```bash
python3 -m venv .venv
```

## 3. Install dependencies

```bash
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

## 4. Verify Gradio and PyMuPDF

```bash
.venv/bin/python -c "import gradio; print('Gradio:', gradio.__version__)"
.venv/bin/python -c "import fitz; print('PyMuPDF:', fitz.__version__)"
```

## 5. Connect the PDF corpus

From inside `tulana/`:

```bash
ln -s ../board_pdfs data
```

Verify:

```bash
find data -type f -iname "*.pdf" | wc -l
```

Expected:

```text
144
```

## 6. Run the application

```bash
.venv/bin/python app.py
```

## 7. Run the Gradio interface

```bash
.venv/bin/python share_gradio.py
```

For permanent deployment, use the target server or cluster's normal process manager and networking configuration rather than relying on a temporary Gradio share.

---

# Dependencies

All Python dependencies are declared in:

```text
tulana/requirements.txt
```

The environment should be created from this file rather than manually installing individual packages.

Important runtime dependencies include:

* Python
* Gradio
* PyMuPDF
* other packages listed in `requirements.txt`

Install everything with:

```bash
python -m pip install -r requirements.txt
```

---

# Application and PDF Layout

The repository uses the following structure:

```text
tulana/
    application source code

board_pdfs/
    board textbook PDF corpus
```

Tulana accesses the PDF corpus through:

```text
tulana/data
```

which points to:

```text
../board_pdfs
```

The application and corpus therefore remain separate while being distributed together.

---

# Validation

## Verify Python

```bash
python --version
```

## Verify Gradio

Windows:

```text
.venv\Scripts\python.exe -c "import gradio; print(gradio.__version__)"
```

Linux:

```bash
.venv/bin/python -c "import gradio; print(gradio.__version__)"
```

## Verify PyMuPDF

Windows:

```text
.venv\Scripts\python.exe -c "import fitz; print(fitz.__version__)"
```

Linux:

```bash
.venv/bin/python -c "import fitz; print(fitz.__version__)"
```

## Verify the PDF corpus

Windows:

```text
(Get-ChildItem ".\board_pdfs" -Recurse -File -Filter "*.pdf").Count
```

Linux:

```bash
find board_pdfs -type f -iname "*.pdf" | wc -l
```

## Verify Git LFS

```bash
git lfs ls-files
```

## Run repository validation scripts

If present:

```bash
python selftest.py
```

```bash
python check_sources.py
```

---

# Updating the Application

Modify files inside:

```text
tulana/
```

Then:

```bash
git add tulana/
git commit -m "Update Tulana"
git push
```

---

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

To retrieve updated PDFs on another machine:

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
*.pyc
*.db
*.sqlite
.env
```

These are local environments, generated files, runtime state, caches, or secrets.

They are recreated or configured on the target machine.

---

# Portability

Tulana should not depend on developer-specific filesystem paths.

Avoid hard-coded paths such as:

```text
D:\Tulana
D:\Bodhan-Tulana-Studio
C:\Users\...
```

Use repository-relative paths or configuration wherever machine-specific paths are required.

---

# Troubleshooting

## PyMuPDF is missing

Windows:

```text
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -c "import fitz; print(fitz.__version__)"
```

Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -c "import fitz; print(fitz.__version__)"
```

## Gradio is missing

Windows:

```text
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -c "import gradio; print(gradio.__version__)"
```

Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -c "import gradio; print(gradio.__version__)"
```

## PDFs are missing

```bash
git lfs install
git lfs pull
```

## Tulana cannot see the PDFs

Check that:

```text
tulana/data
```

exists and points to:

```text
../board_pdfs
```

Windows:

```text
dir data
```

Linux:

```bash
ls -la data
```

## Gradio port is busy

Choose another port using the mechanism supported by the application environment.

Example:

```text
set GRADIO_SERVER_PORT=7870
```

or use the equivalent environment-variable syntax for the shell being used.

---

# Complete Windows Setup

```text
git clone https://github.com/sandipanb01/tulana-studio.git
cd tulana-studio
git lfs install
git lfs pull
cd tulana
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
mklink /J data ..\board_pdfs
.venv\Scripts\python.exe app.py
```

For Gradio:

```text
.venv\Scripts\python.exe share_gradio.py
```

---

# Complete Linux / Cluster Setup

```bash
git clone https://github.com/sandipanb01/tulana-studio.git
cd tulana-studio
git lfs install
git lfs pull
cd tulana
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
ln -s ../board_pdfs data
.venv/bin/python app.py
```

For Gradio:

```bash
.venv/bin/python share_gradio.py
```

---

# Workflow

```text
Clone repository
      ↓
git lfs pull
      ↓
Create .venv
      ↓
Install requirements.txt
      ↓
Connect tulana/data → board_pdfs
      ↓
Verify the PDF corpus
      ↓
Run app.py
      ↓
Run share_gradio.py when needed
```

---

# Repository Layout

```text
tulana-studio/
│
├── README.md
├── .gitignore
├── .gitattributes
│
├── tulana/
│   ├── app.py
│   ├── requirements.txt
│   ├── config.py
│   ├── db.py
│   ├── fetcher.py
│   ├── library.py
│   ├── pdflib.py
│   ├── share_gradio.py
│   ├── docs/
│   └── static/
│
└── board_pdfs/
    └── board textbook PDFs
```

The repository is designed to run on Windows, Linux, and server/cluster environments without requiring PowerShell or any other specific shell as part of the application itself.
