from app.agent.source_priority import EXTERNAL_SOURCES
from app.services.briefing_service import render_markdown


def generate_briefing(state):
    a, ev = state["analysis"], state["validated_evidence"]
    retries = state.get("retries", 0)
    sources: dict[str, list[str]] = {}
    for e in ev:
        sources.setdefault(e["source"], []).append(e["id"])

    summary = a["summary"]
    cites = "".join(f"[{i}]" for i in a.get("summary_refs", []))
    if cites and cites not in summary:
        summary = f"{summary} {cites}"

    briefing = {
        "meeting": state["selected_meeting"], "customer": state["customer"],
        "executive_summary": summary, "deal": a.get("deal"),
        "previous_discussions": a["previous_discussions"], "open_issues": a["open_issues"],
        "objections": a["objections"], "pending_decisions": a["pending_decisions"],
        "risks": state["risks"], "conflicts": state.get("conflicts", []),
        "opportunities": a["opportunities"], "recommended_topics": state["recommended_topics"],
        "memory": state.get("memory", {}), "sources": sources,
        "external_sources": sorted(EXTERNAL_SOURCES & set(sources)),
        "revision": retries,
    }
    return {"briefing": briefing, "briefing_markdown": render_markdown(briefing), "retries": retries + 1}
