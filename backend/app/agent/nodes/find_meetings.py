from app.tools.calendar_tools import get_meetings


def find_meetings(state):
    intent = state["intent"]
    meetings = get_meetings(intent["date"])
    if not meetings:
        return {"meetings": [], "errors": [{"node": "find_meetings", "msg": f"No meetings on {intent['date']}"}]}
    hint = (intent.get("customer_hint") or "").lower()
    chosen = next((m for m in meetings if hint and any(w in m["title"].lower() for w in hint.split()
                                                       if len(w) > 2)), meetings[0])
    return {"meetings": meetings, "selected_meeting": chosen}
