# Document Summary Assistant

A small Tkinter GUI app to extract text from PDFs/images and generate summaries using OpenAI, Hugging Face, or a simple fallback. The main application is implemented in [main.py](main.py).

Key components (in [main.py](main.py)):
- Text extraction: [`main.extract_text_from_pdf`](main.py), [`main.extract_text_from_image`](main.py)
- Summarization: [`main.summarize_text`](main.py)
- GUI: [`main.DocumentSummaryApp`](main.py)

Features
- Load PDF or image files (PDF, PNG, JPG, JPEG, BMP).
- OCR via Tesseract (if installed) for images.
- PDF text extraction via PyMuPDF (fitz).
- Summarization preference order:
  1. OpenAI API (if an API key is provided in the UI)
  2. Hugging Face transformer pipeline (if installed)
  3. Simple fallback sentence-based summary

Requirements
- Python 3.8+
- Optional packages (for full functionality):
  - pytesseract, pillow
  - pymupdf
  - transformers (for Hugging Face summarization)
  - openai (for OpenAI summarization)

Install (recommended)
```sh
python -m pip install --upgrade pip
pip install pytesseract pillow pymupdf transformers openai# Document_Summary_Assistant
