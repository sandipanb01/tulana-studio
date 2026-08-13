# Tulana Studio

Tulana Studio is a document-processing and ground-truth management platform for multilingual textbook, OCR, document-alignment, PDF verification, and translation-quality workflows.

This repository contains:

- the complete Tulana application code
- the complete board textbook PDF corpus
- installation and deployment instructions
- validation and troubleshooting instructions

The application code and board PDF corpus are kept in separate directories while remaining part of the same repository.

---

# 1. Repository Structure

```text
tulana-studio/
│
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
│   │
│   ├── docs/
│   ├── static/
│   └── ...
│
└── board_pdfs/
    ├── board textbook PDFs
    └── ...
