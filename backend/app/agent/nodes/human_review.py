from langgraph.types import interrupt


def human_review(state):
    """Pauses the graph. Resume with Command(resume={'status': 'approved|edited|rejected', 'email_body': ...})."""
    b = state["briefing"]
    to = [a["email"] for a in b["meeting"]["attendees"] if a["email"] in state["customer"].get("emails", [])]
    draft = {"to": to, "subject": f"Meeting brief: {b['customer']['name']} ({b['meeting']['date']})",
             "body": f"Hi,\n\nAhead of our meeting on {b['meeting']['date']} at {b['meeting']['start']}:\n\n"
                     f"{b['executive_summary']}\n\nI'll bring the full agenda.\n\nBest regards"}
    decision = interrupt({"action": "send_email", "draft": draft, "quality": state["quality"]})
    if decision.get("email_body"):
        draft["body"] = decision["email_body"]
    return {"approval_status": decision.get("status", "rejected"), "email_draft": draft}
