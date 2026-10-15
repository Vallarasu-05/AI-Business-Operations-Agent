from app.rag.chunking import chunk_text
from app.rag.vectorstore import get_store


def index_documents(customer_id: str, docs: list[dict]) -> int:
    store, n = get_store(), 0
    for d in docs:
        for i, ch in enumerate(chunk_text(d["text"])):
            store.add(customer_id, d["name"], i, ch)
            n += 1
    return n


def retrieve(customer_id: str, queries: list[str], k: int = 5) -> list[dict]:
    seen, out = set(), []
    for q in queries:
        for hit in get_store().search(customer_id, q, k):
            key = (hit["filename"], hit["chunk"])
            if key not in seen:
                seen.add(key)
                out.append(hit)
    return out
