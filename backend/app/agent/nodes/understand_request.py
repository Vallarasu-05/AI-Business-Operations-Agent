import re
from datetime import date, timedelta
from app.agent.llm import llm_parse_intent


def understand_request(state):
    req = state["user_request"]
    intent = llm_parse_intent(req)
    if not intent:  # deterministic fallback
        low, today = req.lower(), date.today()
        d = today + timedelta(days=1)
        if "today" in low:
            d = today
        iso = re.search(r"\d{4}-\d{2}-\d{2}", req)
        if iso:
            d = date.fromisoformat(iso.group())
        hint = re.search(r"\bwith\s+(.+?)[.?!]*$", req, re.I)
        intent = {"task": "meeting_preparation", "date": d.isoformat(), "meeting_type": "sales",
                  "output": "briefing", "customer_hint": hint.group(1).strip() if hint else None}
    return {"intent": intent, "retries": 0}
