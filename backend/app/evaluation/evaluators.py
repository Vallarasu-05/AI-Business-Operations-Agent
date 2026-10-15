"""Run:  python -m app.evaluation.evaluators   (from /backend, mock mode)"""
import json
import time
import uuid

from langgraph.types import Command

from app.agent.graph import build_graph
from app.evaluation import metrics
from app.evaluation.test_cases import CUSTOMER_ID_CASES, RETRIEVAL_CASES
from app.rag.retriever import index_documents, retrieve
from app.services.customer_service import resolve_customer_identity
from app.tools.drive_tools import search_documents


def eval_customer_id() -> float:
    ok = 0
    for c in CUSTOMER_ID_CASES:
        m = {"title": c["title"], "attendees": [{"name": a, "email": a} for a in c["attendees"]]}
        got = resolve_customer_identity(m).get("company_id")
        ok += got == c["expected"]
    return metrics.accuracy(ok, len(CUSTOMER_ID_CASES))


def eval_retrieval() -> dict:
    for name in ("ABC", "XYZ"):
        docs = search_documents([name])
        cid = "12345" if name == "ABC" else "67890"
        index_documents(cid, docs)
    r, p = [], []
    for c in RETRIEVAL_CASES:
        hits = retrieve(c["customer_id"], [c["query"]], k=5)
        files = [h["filename"] for h in hits]
        r.append(metrics.recall_at_k(files, c["relevant"]))
        p.append(metrics.precision_at_k(list(dict.fromkeys(files)), c["relevant"]))
    return {"recall@5": round(sum(r) / len(r), 3), "precision@5": round(sum(p) / len(p), 3)}


def eval_end_to_end() -> dict:
    g, out = build_graph(), []
    for req in ["Prepare tomorrow's sales meeting with ABC Corporation",
                "Prepare tomorrow's sales meeting with XYZ Technologies"]:
        cfg = {"configurable": {"thread_id": uuid.uuid4().hex}}
        t = time.time()
        g.invoke({"user_request": req}, cfg)
        g.invoke(Command(resume={"status": "approved"}), cfg)
        st = g.get_state(cfg).values
        out.append({"request": req, "customer": st["customer"]["name"], "quality": st["quality"],
                    "conflicts": [c["topic"] for c in st["conflicts"]], "seconds": round(time.time() - t, 2)})
    ok = sum(1 for o in out if o["quality"]["passed"])
    return {"success_rate": metrics.accuracy(ok, len(out)), "runs": out}


if __name__ == "__main__":
    report = {"customer_identification_accuracy": eval_customer_id(), "retrieval": eval_retrieval(),
              "end_to_end": eval_end_to_end()}
    print(json.dumps(report, indent=2, ensure_ascii=False))
