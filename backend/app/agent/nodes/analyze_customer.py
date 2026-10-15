from app.agent.llm import llm_summary
from app.services.money import fmt_inr


def _ids(ev, topic):
    return [e for e in ev if e["topic"] == topic]


def _item(e):
    return {"text": e["claim"], "evidence_ids": [e["id"]]}


def analyze_customer(state):
    ev, c = state["validated_evidence"], state["customer"]
    crm_ctx = state.get("crm_data") or {}
    deal = (crm_ctx.get("deals") or [None])[0]

    deal_ev = next((e for e in ev if e["topic"] == "deal_value" and e["source"] == "crm"), None)
    stage_ev = next((e for e in ev if e["topic"] == "deal_stage" and e["source"] == "crm"), None)
    close_ev = next((e for e in ev if e["topic"] == "close_date" and e["source"] == "crm"), None)

    open_issues = [_item(e) for e in _ids(ev, "open_ticket")]
    open_issues += [_item(e) for e in _ids(ev, "requirement") if e["source"] == "internal_document"
                    and "pending" in e["claim"].lower()]
    pending = [_item(e) for e in _ids(ev, "pending_decision")]
    if _ids(ev, "objection"):
        pending.append({"text": "Final pricing / discount", "evidence_ids": [e["id"] for e in _ids(ev, "objection")]})
    if _ids(ev, "timeline"):
        pending.append({"text": "Implementation date / go-live timeline",
                        "evidence_ids": [e["id"] for e in _ids(ev, "timeline")][:3]})

    prev = [_item(e) for e in _ids(ev, "history")]
    prev += [_item(e) for e in _ids(ev, "commitment")]
    prev += [{"text": f"Email ({e['date']}): {e['claim']}", "evidence_ids": [e["id"]]}
             for e in ev if e["source"] == "gmail" and e["topic"] in ("requirement", "preference")]

    analysis = {
        "requirements": [_item(e) for e in _ids(ev, "requirement")],
        "open_issues": open_issues,
        "objections": [_item(e) for e in _ids(ev, "objection")] + [_item(e) for e in _ids(ev, "competitor")],
        "pending_decisions": pending,
        "previous_discussions": prev,
        "opportunities": [_item(e) for e in _ids(ev, "news")],
        "deal": None,
    }
    if deal and deal_ev:
        analysis["deal"] = {"name": deal["name"], "value": deal["amount"], "stage": deal["stage"],
                            "close_date": deal.get("close_date"),
                            "evidence_ids": [x["id"] for x in (deal_ev, stage_ev, close_ev) if x]}

    base = (f"{c['name']} ({c.get('industry') or 'industry n/a'}) "
            + (f"is in the {deal['stage']} stage for '{deal['name']}' valued at {fmt_inr(deal['amount'])}. "
               if deal else "has no CRM deal on record. ")
            + f"{len(open_issues)} open issue(s), {len(analysis['objections'])} customer concern(s) and "
              f"{len(state.get('conflicts', []))} data conflict(s) were found.")
    refs = [x["id"] for x in (deal_ev, stage_ev) if x]
    summary = llm_summary(c["name"], ev) or base
    analysis["summary"] = summary
    analysis["summary_refs"] = refs
    return {"analysis": analysis}
