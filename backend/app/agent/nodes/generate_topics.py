def generate_topics(state):
    ev, a, conflicts = state["validated_evidence"], state["analysis"], state.get("conflicts", [])
    ids = lambda *topics: [e["id"] for e in ev if e["topic"] in topics][:4]  # noqa: E731
    topics = []
    if ids("open_ticket", "requirement"):
        topics.append({"topic": "Resolve API / integration scope",
                       "why": "An integration ticket is open in the CRM and the customer repeatedly raised ERP/API requirements.",
                       "suggested_question": "Can we confirm the remaining integration requirements and the expected resolution timeline?",
                       "evidence_ids": ids("open_ticket", "requirement")})
    if ids("competitor"):
        topics.append({"topic": "Address the competitive evaluation",
                       "why": "The latest customer email says another vendor is being evaluated.",
                       "suggested_question": "What criteria matter most in your vendor comparison, and where do we stand today?",
                       "evidence_ids": ids("competitor")})
    if ids("objection"):
        topics.append({"topic": "Clarify pricing and discount expectations",
                       "why": "The customer asked for a discount and raised pricing concerns.",
                       "suggested_question": "What would a commercially acceptable structure look like for your team?",
                       "evidence_ids": ids("objection")})
    for c in conflicts:
        if c["topic"] == "deal_value":
            vals = " vs ".join(f"{g['display']} ({', '.join(g['sources'])})" for g in c["groups"])
            topics.append({"topic": "Confirm the agreed commercial figure",
                           "why": f"Sources disagree on deal value: {vals}.",
                           "suggested_question": "To avoid confusion, can we confirm the total value including implementation?",
                           "evidence_ids": [i for g in c["groups"] for i in g["evidence_ids"][:2]]})
    if ids("timeline", "decision_deadline"):
        topics.append({"topic": "Confirm implementation timeline and decision process",
                       "why": "Go-live expectations and a customer decision date were mentioned.",
                       "suggested_question": "Who signs off, and what must be true for a decision by your deadline?",
                       "evidence_ids": ids("timeline", "decision_deadline")})
    return {"recommended_topics": topics}
