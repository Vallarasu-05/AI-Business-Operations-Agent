from app.rag.retriever import index_documents, retrieve
from app.tools.drive_tools import search_documents


def test_customer_isolation_and_relevance():
    index_documents("12345", search_documents(["ABC"]))
    index_documents("67890", search_documents(["XYZ"]))
    hits = retrieve("12345", ["total price payment"], k=5)
    names = {h["filename"] for h in hits}
    assert "ABC_Proposal.txt" in names
    assert not any(n.startswith("XYZ") for n in names)
