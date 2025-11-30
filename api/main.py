from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List

from src.extractor.ingest import extract_file_to_markdown_or_text

app = FastAPI(title="DocScribe API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "DocScribe API is running. POST /extract with files=... to extract Markdown."}

@app.post("/extract")
async def extract(files: List[UploadFile] = File(...)):
    results = []
    for uf in files:
        content = await uf.read()
        try:
            result = extract_file_to_markdown_or_text(uf.filename, content, prefer_format="md")
            results.append({
                "filename": uf.filename,
                "media_type": uf.content_type,
                "text_len": len(result.get("text", "")),
                "format": "md",
                "warnings": result.get("warnings", []),
                "markdown": result.get("markdown", ""),
            })
        except Exception as e:
            results.append({
                "filename": uf.filename,
                "media_type": uf.content_type,
                "error": str(e),
            })
    return JSONResponse({"results": results})