from src.extractor.ingest import extract_file_to_markdown_or_text

def test_txt_extraction():
    content = "Hello\n\nWorld!".encode("utf-8")
    out = extract_file_to_markdown_or_text("demo.txt", content, prefer_format="md")
    assert out["text"].strip() == "Hello\n\nWorld!"
    assert isinstance(out["markdown"], str)
    assert isinstance(out["warnings"], list)