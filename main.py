import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import platform
import shutil
import pytesseract
import fitz  # PyMuPDF
# PDF text extraction
from PIL import Image
try:
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

# OCR setup
try:

    from PIL import Image
    HAS_TESSERACT = True

    if platform.system() == "Windows":
        default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if shutil.which("tesseract"):
            pass  # already in PATH
        elif os.path.exists(default_path):
            pytesseract.pytesseract.tesseract_cmd = default_path
        else:
            HAS_TESSERACT = False
    else:
        if not shutil.which("tesseract"):
            HAS_TESSERACT = False
except ImportError:
    HAS_TESSERACT = False

# Summarization
try:
    from transformers import pipeline
    hf_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    HAS_HF = True
except ImportError:
    HAS_HF = False

# OpenAI (optional)
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


# ---------------- TEXT EXTRACTION ----------------
def extract_text_from_pdf(path):
    if not HAS_FITZ:
        raise RuntimeError("PyMuPDF not installed. Run: pip install pymupdf")
    doc = fitz.open(path)
    texts = [page.get_text("text") for page in doc]
    doc.close()
    return "\n".join(texts)


def extract_text_from_image(path):
    if not HAS_TESSERACT:
        return "OCR not available. Please install Tesseract OCR + pytesseract + pillow."
    try:
        text = pytesseract.image_to_string(Image.open(path))
        return text.strip()
    except Exception as e:
        return f"OCR failed: {e}"


# ---------------- SUMMARIZATION ----------------
def summarize_text(text, max_length=300, api_key=None):
    """
    Summarizes text using OpenAI -> HuggingFace -> Fallback
    max_length = target number of tokens/words (approx)
    """
    text = text.strip()
    if not text:
        return "No text to summarize."

    # Try OpenAI
    if HAS_OPENAI and api_key:
        try:
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Summarize the following text in detail."},
                    {"role": "user", "content": text[:8000]}
                ],
                max_tokens=max_length
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI summarization failed: {e}"

    # Try Hugging Face
    if HAS_HF:
        try:
            # Hugging Face models usually support max_length up to ~1024
            result = hf_summarizer(
                text[:2000],
                max_length=min(max_length, 1024),
                min_length=min(100, max_length // 2),
                do_sample=False
            )
            return result[0]["summary_text"]
        except Exception as e:
            return f"Hugging Face summarization failed: {e}"

    # Fallback: return more sentences for longer summaries
    sentences = text.split(".")
    return ".".join(sentences[:max_length // 30]) + "..."


# ---------------- GUI APP ----------------
class DocumentSummaryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Document Summary Assistant")
        self.geometry("1100x650")

        self.api_key = tk.StringVar()
        self.file_path = None

        self._build_ui()

    def _build_ui(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(top_frame, text="Load File", command=self.load_file).pack(side="left", padx=5)
        tk.Label(top_frame, text="Max length (words):").pack(side="left")
        self.max_len_var = tk.IntVar(value=300)
        tk.Entry(top_frame, textvariable=self.max_len_var, width=6).pack(side="left", padx=5)
        tk.Label(top_frame, text="(50–1000)").pack(side="left")

        tk.Label(top_frame, text="OpenAI Key:").pack(side="left")
        tk.Entry(top_frame, textvariable=self.api_key, width=40, show="*").pack(side="left", padx=5)

        tk.Button(top_frame, text="Summarize", command=lambda: self._threaded(self.run_summary)).pack(side="left", padx=5)

        # Text areas
        frame = tk.PanedWindow(self, orient="horizontal")
        frame.pack(side="bottom", expand=True)

        self.text_input = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
        frame.add(self.text_input)

        self.text_summary = scrolledtext.ScrolledText(frame, wrap=tk.WORD, bg="#f4f4f4")
        frame.add(self.text_summary)

        self.status = tk.Label(self, text="Ready", anchor="w")
        self.status.pack(fill="x", side="bottom")

    def set_status(self, msg):
        self.status.config(text=msg)
        self.update_idletasks()

    def _threaded(self, fn):
        threading.Thread(target=fn, daemon=True).start()

    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("PDF or Image", "*.pdf;*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if not path:
            return
        self.file_path = path
        self.set_status(f"Loaded: {os.path.basename(path)}")

        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".pdf":
                text = extract_text_from_pdf(path)
            else:
                text = extract_text_from_image(path)
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Extraction error", str(e))

    def run_summary(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No text", "Please load a document or paste text first.")
            return

        max_len = max(50, min(1000, self.max_len_var.get()))  # clamp between 50–1000
        self.set_status(f"Summarizing (max length {max_len})...")

        summary = summarize_text(
            text,
            max_length=max_len,
            api_key=self.api_key.get().strip()
        )
        self.text_summary.delete("1.0", tk.END)
        self.text_summary.insert(tk.END, summary)
        self.set_status("Summary generated.")


if __name__ == "__main__":
    app = DocumentSummaryApp()
    app.mainloop()
