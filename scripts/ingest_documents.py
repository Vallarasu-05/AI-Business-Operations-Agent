"""Index the mock documents and run a sample query.  Run from /backend:  python ../scripts/ingest_documents.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.rag.retriever import index_documents, retrieve  # noqa: E402
from app.tools.drive_tools import search_documents  # noqa: E402

docs = search_documents(["ABC"])
print("chunks indexed:", index_documents("12345", docs))
for h in retrieve("12345", ["What pricing was discussed?"], k=5):
    print(f"[{h['score']}] {h['filename']}#{h['chunk']}: {h['text'][:90]}...")
