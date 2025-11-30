# DocScribe: Universal Document → Markdown (CLI + API)

Turn PDFs, Word docs (DOCX), images (OCR), and text files into clean Markdown via a simple CLI and REST API.
Great for knowledge bases, RAG ingestion, note-taking, and automation.

Features
- File types: PDF, DOCX, PNG/JPG, TXT
- Outputs: Cleaned Markdown or plain text
- CLI: Convert a single file or an entire folder
- API: FastAPI endpoint for uploading files and getting Markdown back
- Docker: One-command deployment
- Sensible defaults + easy to extend

Quickstart
1) Local install
- Python 3.10+
- Tesseract (for OCR on images):
  - macOS: brew install tesseract
  - Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y tesseract-ocr
  - Windows: Install from https://github.com/UB-Mannheim/tesseract/wiki

Then:
```
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

CLI usage
```
# Convert a single file to Markdown (default)
python cli.py extract ./samples/sample.pdf -o ./out

# Convert a folder recursively
python cli.py extract ./samples -o ./out --format md

# Output as plain text
python cli.py extract ./samples/doc.docx -o ./out --format txt
```

API usage
Start the server:
```
uvicorn api.main:app --reload
```

Then POST files:
```
curl -X POST "http://localhost:8000/extract" \
  -F "files=@samples/sample.pdf" \
  -F "files=@samples/scan.jpg"
```

Response:
```
{
  "results": [
    {
      "filename": "sample.pdf",
      "media_type": "application/pdf",
      "text_len": 12345,
      "format": "md",
      "warnings": [],
      "markdown": "# Extracted content..."
    },
    {
      "filename": "scan.jpg",
      "media_type": "image/jpeg",
      "text_len": 2345,
      "format": "md",
      "warnings": ["Used OCR via Tesseract"],
      "markdown": "Extracted text..."
    }
  ]
}
```

Docker
```
docker build -t docscribe .
docker run -p 8000:8000 docscribe
# API at http://localhost:8000
```

Project structure
```
.
├── api/
│   └── main.py
├── src/extractor/
│   ├── __init__.py
│   ├── ingest.py
│   └── clean.py
├── tests/
│   └── test_basic.py
├── cli.py
├── requirements.txt
├── Dockerfile
├── .github/workflows/ci.yml
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

Extending
- Add new extractors in `src/extractor/ingest.py` (e.g., PPTX, HTML)
- Customize cleaning in `src/extractor/clean.py`
- Adjust API response schema in `api/main.py`

Notes and limitations
- OCR requires Tesseract to be installed on the host or Docker image.
- Some PDFs that are pure images will return little/no text without OCR; adding `pdf2image` to render pages for OCR is a good enhancement.
- Complex layouts (tables, multi-column) may need specialized libraries; this starter prioritizes simplicity and speed.

License
MIT — see LICENSE.

Contributing
PRs welcome! See CONTRIBUTING.md.

Security
See SECURITY.md for how to report vulnerabilities.