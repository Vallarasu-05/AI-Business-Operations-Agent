from app.rag.retriever import index_documents, retrieve
from app.security.sanitizer import sanitize_text
from app.services.research_service import DOC_TOPICS, extract_signals
from app.tools.drive_tools import search_documents

QUERIES = ["pricing total price payment", "technical requirements API integration",
           "timeline deployment go-live", "meeting notes action items decision"]


def research_documents(state):
    c = state["customer"]
    try:
        docs = search_documents([c["name"], *c.get("aliases", [])])
    except Exception as e:
        return {"errors": [{"node": "research_documents", "msg": f"Drive failed: {e}"}]}
    key = c.get("company_id") or c["domain"]
    index_documents(key, [{**d, "text": sanitize_text(d["text"], 20000)} for d in docs])
    hits = retrieve(key, QUERIES, k=5)
    ev = []
    for h in hits:
        e, flags = extract_signals(h["text"], "internal_document", f"{h['filename']}#{h['chunk']}", None,
                                   0.9, DOC_TOPICS)
        ev += e + flags
    return {"document_data": [{"name": d["name"]} for d in docs], "evidence": ev}
