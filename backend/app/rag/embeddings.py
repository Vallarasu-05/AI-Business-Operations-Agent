_model = None


def get_embedder():
    """Return a callable list[str] -> list[list[float]], or None if sentence-transformers isn't installed."""
    global _model
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        return None
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return lambda texts: _model.encode(texts, normalize_embeddings=True).tolist()
