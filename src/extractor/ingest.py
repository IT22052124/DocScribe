from io import BytesIO
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image
import pytesseract
from pypdf import PdfReader
from docx import Document

from .clean import clean_text, to_markdown

SUPPORTED_EXTS = {".pdf", ".docx", ".png", ".jpg", ".jpeg", ".txt"}

def _ext(name: str) -> str:
    return Path(name).suffix.lower()

def extract_pdf(file_bytes: bytes) -> Tuple[str, List[str]]:
    warnings: List[str] = []
    reader = PdfReader(BytesIO(file_bytes))
    texts = []
    for page in reader.pages:
        try:
            t = page.extract_text() or ""
        except Exception:
            t = ""
        if t.strip():
            texts.append(t)
    raw = "\n\n".join(texts)
    if not raw.strip():
        warnings.append("PDF appears to have no embedded text (might be scanned). Consider OCR pipeline.")
    return raw, warnings

def extract_docx(file_bytes: bytes) -> Tuple[str, List[str]]:
    doc = Document(BytesIO(file_bytes))
    paras = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paras), []

def extract_txt(file_bytes: bytes) -> Tuple[str, List[str]]:
    try:
        txt = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        txt = file_bytes.decode("latin-1", errors="replace")
    return txt, []

def extract_image(file_bytes: bytes) -> Tuple[str, List[str]]:
    img = Image.open(BytesIO(file_bytes))
    text = pytesseract.image_to_string(img)
    return text, ["Used OCR via Tesseract"]

def extract_file_to_markdown_or_text(filename: str, file_bytes: bytes, prefer_format: str = "md") -> Dict:
    """
    Returns dict with keys:
    - text: cleaned plain text
    - markdown: markdown rendering (if prefer_format == 'md')
    - warnings: list[str]
    """
    ext = _ext(filename)
    if ext not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported extension '{ext}'. Supported: {sorted(SUPPORTED_EXTS)}")

    if ext == ".pdf":
        raw, warnings = extract_pdf(file_bytes)
    elif ext == ".docx":
        raw, warnings = extract_docx(file_bytes)
    elif ext in {".png", ".jpg", ".jpeg"}:
        raw, warnings = extract_image(file_bytes)
    elif ext == ".txt":
        raw, warnings = extract_txt(file_bytes)
    else:
        raise ValueError(f"Unhandled extension: {ext}")

    cleaned = clean_text(raw)
    md = to_markdown(cleaned) if prefer_format == "md" else ""
    return {"text": cleaned, "markdown": md, "warnings": warnings}