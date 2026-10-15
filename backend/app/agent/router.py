from langgraph.graph import END

RESEARCH_NODES = ["research_crm", "research_email", "research_documents", "research_sheets", "research_web"]
MAX_RETRIES = 2


def route_after_meetings(state) -> str:
    return "identify_customer" if state.get("selected_meeting") else END


def route_after_customer(state):
    """Fan out to all research nodes in parallel, or stop if no customer could be resolved."""
    return RESEARCH_NODES if state.get("customer") else END


def route_after_quality(state) -> str:
    if state["quality"]["passed"] or state.get("retries", 0) > MAX_RETRIES:
        return "human_review"
    return "generate_briefing"
