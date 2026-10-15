from app.schemas.evidence import Evidence
from app.security.injection_guard import is_suspicious
from app.security.sanitizer import sanitize_text
from app.tools.web_search_tools import search_company


def research_web(state):
    c = state["customer"]
    try:
        results = search_company(c["name"], c.get("company_id"))
    except Exception as e:
        return {"errors": [{"node": "research_web", "msg": f"Web search failed: {e}"}]}
    ev = []
    for r in results:
        text = sanitize_text(f"{r['title']}: {r['snippet']}", 400)
        if is_suspicious(text):
            continue
        ev.append(Evidence(claim=text, source="web_search", source_id=r.get("url", r["title"]),
                           date=r.get("date"), confidence=0.6, topic="news").model_dump())
    return {"web_data": results, "evidence": ev}
