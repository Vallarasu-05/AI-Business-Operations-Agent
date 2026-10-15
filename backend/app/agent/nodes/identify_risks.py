import re


def identify_risks(state):
    ev, a = state["validated_evidence"], state["analysis"]
    risks = []

    comp = [e for e in ev if e["topic"] == "competitor"]
    if comp:
        risks.append({"risk": "Competitive evaluation", "severity": "high",
                      "rationale": "Customer says another vendor is being evaluated.",
                      "evidence_ids": [e["id"] for e in comp]})
    obj = [e for e in ev if e["topic"] == "objection"]
    if obj:
        pct = next((m.group(1) for e in obj for m in [re.search(r"(\d+)\s?%", e["claim"])] if m), None)
        risks.append({"risk": "Pricing pressure", "severity": "medium",
                      "rationale": f"Customer expects a {pct}% discount." if pct else "Customer raised pricing concerns.",
                      "evidence_ids": [e["id"] for e in obj]})
    hi = [e for e in ev if e["topic"] == "open_ticket" and str(e.get("value")).lower() == "high"]
    if hi:
        risks.append({"risk": "Unresolved high-priority ticket", "severity": "high",
                      "rationale": "A high-priority CRM ticket is still open before negotiation closes.",
                      "evidence_ids": [e["id"] for e in hi]})
    dl = [e for e in ev if e["topic"] == "decision_deadline"]
    if dl:
        risks.append({"risk": "Customer decision deadline", "severity": "medium",
                      "rationale": "Customer set a decision date; slippage could lose the deal.",
                      "evidence_ids": [e["id"] for e in dl]})
    for c in state.get("conflicts", []):
        risks.append({"risk": f"Conflicting data: {c['topic']}", "severity": "medium",
                      "rationale": "Sources disagree; confirm the correct value with the customer before negotiating.",
                      "evidence_ids": [i for g in c["groups"] for i in g["evidence_ids"][:2]]})
    sec = [e for e in ev if e["topic"] == "security_flag"]
    if sec:
        risks.append({"risk": "Possible prompt-injection in external content", "severity": "high",
                      "rationale": "Instruction-like text was found in customer content. It was ignored and not executed.",
                      "evidence_ids": [e["id"] for e in sec]})
    order = {"high": 0, "medium": 1, "low": 2}
    return {"risks": sorted(risks, key=lambda r: order[r["severity"]])}
