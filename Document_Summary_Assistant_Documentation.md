
# 📚 Document Summary Assistant – Project Documentation

## ✅ Project Description

The **Document Summary Assistant** is a Python-based desktop application that allows users to:
- Extract text from PDF or image files.
- Summarize the extracted text using multiple methods:
    1. OpenAI GPT-3.5 API (optional).
    2. Hugging Face Transformers summarization pipeline.
    3. Simple fallback summarization when neither service is available.

It features a simple graphical interface (GUI) built using **Tkinter**, allowing non-technical users to easily load files and generate summaries.

## ✅ How the Project Works

1. **Text Extraction**
   - From PDF: Uses **PyMuPDF (fitz)** to extract text.
   - From Image: Uses **pytesseract OCR** and **PIL (Pillow)** to extract text.

2. **Text Summarization**
   - First tries OpenAI API if an API key is provided.
   - If OpenAI is unavailable, it tries Hugging Face summarization.
   - If both fail, applies a fallback heuristic by returning the first few sentences.

3. **Graphical Interface**
   - Load a PDF or image file.
   - Show the extracted text in an input pane.
   - Allow setting max summary length (50–1000 words).
   - Optionally provide OpenAI API key.
   - Display the generated summary in a second pane.
   - Show status messages (like "Ready", "Summarizing...", etc.).

## ✅ Python Modules Used

| Module | Purpose |
|--------|---------|
| os | File path handling (standard library) |
| tkinter | GUI components (standard library) |
| threading | Run tasks in background threads (standard library) |
| platform | Check OS platform (standard library) |
| shutil | System utilities, check for tesseract command (standard library) |
| fitz (PyMuPDF) | Extract text from PDF files |
| pytesseract | OCR engine for extracting text from images |
| PIL (Pillow) | Image handling for OCR |
| transformers | Hugging Face summarization pipeline |
| openai | OpenAI GPT API client |

## ✅ Required Install Commands

```
pip install pymupdf pytesseract pillow transformers openai
```

⚡ Note:
- Also install **Tesseract OCR Engine** separately:
    - https://github.com/tesseract-ocr/tesseract
    - Add Tesseract executable to system PATH, or specify the path in the code (handled automatically on Windows).

## ✅ Example Usage Steps

1. Run the application:
    ```
    python document_summary_app.py
    ```
2. In the GUI:
    - Click "Load File" and select a PDF or Image.
    - The extracted text appears in the left pane.
    - Optionally enter your OpenAI API key.
    - Set a maximum summary length (e.g., 300 words).
    - Click "Summarize" to generate the summary.
    - The summary appears in the right pane.

## ✅ Fallback Mechanism

- If neither OpenAI nor Hugging Face are available, the application will gracefully fallback to simply returning the first few sentences of the text.

## ✅ Why This Project is Useful

- Ideal for summarizing large documents quickly.
- Helps extract text from scanned PDFs or images.
- Useful for knowledge workers, researchers, or students.
- Works offline for OCR & fallback summarization.
- Simple user-friendly GUI.
