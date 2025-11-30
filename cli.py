import os
from pathlib import Path
from typing import Optional

import typer

from src.extractor.ingest import extract_file_to_markdown_or_text
app = typer.Typer(help="DocScribe CLI: Convert documents to Markdown or text")

def _iter_files(path: Path):
    if path.is_file():
        yield path
    else:
        for p in path.rglob("*"):
            if p.is_file():
                yield p

@app.command()
def extract(
    input_path: str = typer.Argument(..., help="File or directory to process"),
    out: str = typer.Option("./out", "--out", "-o", help="Output directory"),
    format: str = typer.Option("md", "--format", "-f", help="md or txt", case_sensitive=False),
):
    """
    Convert file(s) to Markdown (default) or plain text.
    """
    fmt = format.lower()
    if fmt not in {"md", "txt"}:
        typer.echo("Format must be 'md' or 'txt'")
        raise typer.Exit(code=1)

    in_path = Path(input_path)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    processed = 0
    for file_path in _iter_files(in_path):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            result = extract_file_to_markdown_or_text(file_path.name, content, prefer_format=fmt)
            ext = "md" if fmt == "md" else "txt"
            out_file = out_dir / f"{file_path.stem}.{ext}"
            with open(out_file, "w", encoding="utf-8") as wf:
                wf.write(result["markdown"] if fmt == "md" else result["text"])
            typer.echo(f"OK  -> {file_path}  =>  {out_file}")
            processed += 1
        except Exception as e:
            typer.echo(f"FAIL -> {file_path}: {e}")

    typer.echo(f"Done. Processed {processed} file(s).")

if __name__ == "__main__":
    app()