from app.schemas.evidence import Evidence
from app.tools.crm_tools import get_context


def research_crm(state):
    cid = state["customer"].get("company_id")
    if not cid:
        return {"errors": [{"node": "research_crm", "msg": "Skipped: customer not in CRM"}]}
    ctx = get_context(cid)
    ev = []
    for d in ctx["deals"]:
        sid = d["id"]
        ev += [Evidence(claim=f"Deal '{d['name']}' value is {d['amount']:.0f} {d.get('currency', 'INR')}",
                        source="crm", source_id=sid, confidence=0.99, topic="deal_value", value=float(d["amount"])),
               Evidence(claim=f"Deal '{d['name']}' stage is {d['stage']}", source="crm", source_id=sid,
                        confidence=0.99, topic="deal_stage", value=str(d["stage"]).lower()),
               Evidence(claim=f"Expected close date is {d.get('close_date')}", source="crm", source_id=sid,
                        confidence=0.95, topic="close_date", value=d.get("close_date"))]
    for t in ctx["tickets"]:
        if str(t.get("status", "")).lower() == "open":
            ev.append(Evidence(claim=f"Open ticket: {t['title']} (priority {t['priority']})", source="crm",
                               source_id=t["id"], confidence=0.99, topic="open_ticket", value=t["priority"]))
    for a in ctx["activities"]:
        ev.append(Evidence(claim=a["note"], source="crm", source_id=a["id"], date=a["date"],
                           confidence=0.95, topic="history"))
    return {"crm_data": ctx, "evidence": [e.model_dump() for e in ev]}
