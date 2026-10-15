import math
import re
from app.config import settings
from app.rag.embeddings import get_embedder


def _tok(s: str) -> list[str]:
    return re.findall(r"[a-z0-9₹]+", s.lower())


class MemoryStore:
    """In-process store. Uses embeddings if available, otherwise keyword overlap (BM25-lite)."""

    def __init__(self):
        self.rows: list[dict] = []
        self.embed = get_embedder()

    def add(self, customer_id: str, filename: str, idx: int, text: str):
        key = (customer_id, filename, idx)
        if any(r["key"] == key for r in self.rows):
            return
        vec = self.embed([text])[0] if self.embed else None
        self.rows.append({"key": key, "customer_id": customer_id, "filename": filename,
                          "chunk": idx, "text": text, "vec": vec})

    def search(self, customer_id: str, query: str, k: int = 5) -> list[dict]:
        rows = [r for r in self.rows if r["customer_id"] == customer_id]  # customer isolation
        if self.embed:
            q = self.embed([query])[0]
            scored = [(sum(a * b for a, b in zip(q, r["vec"])), r) for r in rows]
        else:
            qt = set(_tok(query))
            scored = [(len(qt & set(_tok(r["text"]))) / math.sqrt(len(_tok(r["text"])) + 1), r) for r in rows]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{**{k2: v for k2, v in r.items() if k2 != "vec"}, "score": round(s, 4)}
                for s, r in scored[:k] if s > 0]


class QdrantStore:
    """Optional Qdrant backend (requires sentence-transformers + qdrant-client)."""
    COLLECTION = "customer_docs"

    def __init__(self):
        from qdrant_client import QdrantClient, models
        self.models = models
        self.embed = get_embedder()
        if not self.embed:
            raise RuntimeError("Qdrant backend needs sentence-transformers")
        self.client = QdrantClient(url=settings.vector_db_url)
        if not self.client.collection_exists(self.COLLECTION):
            self.client.create_collection(self.COLLECTION, vectors_config=models.VectorParams(
                size=len(self.embed(["x"])[0]), distance=models.Distance.COSINE))

    def add(self, customer_id, filename, idx, text):
        import uuid
        pid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{customer_id}/{filename}/{idx}"))
        self.client.upsert(self.COLLECTION, points=[self.models.PointStruct(
            id=pid, vector=self.embed([text])[0],
            payload={"customer_id": customer_id, "filename": filename, "chunk": idx, "text": text})])

    def search(self, customer_id, query, k=5):
        res = self.client.query_points(
            self.COLLECTION, query=self.embed([query])[0], limit=k,
            query_filter=self.models.Filter(must=[self.models.FieldCondition(
                key="customer_id", match=self.models.MatchValue(value=customer_id))]))
        return [{**p.payload, "score": p.score} for p in res.points]


_store = None


def get_store():
    global _store
    if _store is None:
        _store = QdrantStore() if settings.vector_backend == "qdrant" else MemoryStore()
    return _store
