import re

def clean_text(text: str) -> str:
    # Normalize line endings
    t = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse excessive blank lines
    t = re.sub(r"\n{3,}", "\n\n", t)
    # Trim trailing spaces on lines
    t = "\n".join(line.rstrip() for line in t.split("\n"))
    # Normalize multiple spaces (but keep in-code spaces)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()

def to_markdown(text: str) -> str:
    # Very light markdown conversion: turn long lines into paragraphs and keep bullets
    lines = text.split("\n")
    md_lines = []
    for line in lines:
        if line.strip().startswith(("-", "*", "•", "·")):
            md_lines.append(f"- {line.strip().lstrip('-*•· ').strip()}")
        else:
            md_lines.append(line)
    return "\n".join(md_lines).strip()