from pathlib import Path


def extract_text(path: Path) -> str:
    path = Path(path)
    ext = path.suffix.lower()
    if ext in (".txt", ".md"):
        return path.read_text("utf-8", errors="ignore")
    if ext == ".pdf":
        import fitz  # PyMuPDF
        with fitz.open(path) as doc:
            return "\n".join(p.get_text() for p in doc)
    if ext == ".docx":
        import docx
        return "\n".join(p.text for p in docx.Document(str(path)).paragraphs)
    if ext in (".xlsx", ".csv"):
        import pandas as pd
        df = pd.read_excel(path) if ext == ".xlsx" else pd.read_csv(path)
        return df.to_string(index=False)
    return ""
