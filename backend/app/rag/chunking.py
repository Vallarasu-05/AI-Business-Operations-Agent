def chunk_text(text: str, size: int = 120, overlap: int = 20) -> list[str]:
    """Word-based chunks (~size words, overlapping)."""
    words = text.split()
    if not words:
        return []
    step = max(1, size - overlap)
    return [" ".join(words[i:i + size]) for i in range(0, len(words), step) if words[i:i + size]]
