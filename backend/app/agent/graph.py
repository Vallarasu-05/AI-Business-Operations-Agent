from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.agent import router
from app.agent.nodes import (analyze_customer, deliver, find_meetings, generate_briefing, generate_topics,
                             human_review, identify_customer, identify_risks, quality_check, research_crm,
                             research_documents, research_email, research_sheets, research_web,
                             understand_request, validate_evidence)
from app.agent.state import AgentState

NODES = {
    "understand_request": understand_request, "find_meetings": find_meetings,
    "identify_customer": identify_customer, "research_crm": research_crm,
    "research_email": research_email, "research_documents": research_documents,
    "research_sheets": research_sheets, "research_web": research_web,
    "validate_evidence": validate_evidence, "analyze_customer": analyze_customer,
    "identify_risks": identify_risks, "generate_topics": generate_topics,
    "generate_briefing": generate_briefing, "quality_check": quality_check,
    "human_review": human_review, "deliver": deliver,
}
NODE_ORDER = list(NODES)


def build_graph(checkpointer=None):
    g = StateGraph(AgentState)
    for name, fn in NODES.items():
        g.add_node(name, fn)

    g.add_edge(START, "understand_request")
    g.add_edge("understand_request", "find_meetings")
    g.add_conditional_edges("find_meetings", router.route_after_meetings, ["identify_customer", END])
    g.add_conditional_edges("identify_customer", router.route_after_customer,
                            router.RESEARCH_NODES + [END])
    g.add_edge(router.RESEARCH_NODES, "validate_evidence")  # join: waits for all five
    g.add_edge("validate_evidence", "analyze_customer")
    g.add_edge("analyze_customer", "identify_risks")
    g.add_edge("identify_risks", "generate_topics")
    g.add_edge("generate_topics", "generate_briefing")
    g.add_edge("generate_briefing", "quality_check")
    g.add_conditional_edges("quality_check", router.route_after_quality, ["human_review", "generate_briefing"])
    g.add_edge("human_review", "deliver")
    g.add_edge("deliver", END)
    return g.compile(checkpointer=checkpointer or MemorySaver())
