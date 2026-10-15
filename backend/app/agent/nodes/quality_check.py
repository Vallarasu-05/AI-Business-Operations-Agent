import re
from app.services.money import parse_amounts


def quality_check(state):
    """Deterministic grounding check. Every figure must exist in evidence; conflicts and sources must surface."""
    b, md, ev = state["briefing"], state["briefing_markdown"], state["validated_evidence"]
    issues = []

    known = {round(v) for e in ev for v in parse_amounts(e["claim"])}
    known |= {round(e["value"]) for e in ev if isinstance(e.get("value"), (int, float))}
    amounts = [round(v) for v in parse_amounts(md)]
    unsupported = [v for v in amounts if v not in known]
    if unsupported:
        issues.append(f"Unsupported figures: {sorted(set(unsupported))}")

    valid_ids = {e["id"] for e in ev}
    cited = set(re.findall(r"\[(E\d+)\]", md))
    bad = cited - valid_ids
    if bad:
        issues.append(f"Citations to unknown evidence: {sorted(bad)}")

    for t in b["recommended_topics"]:
        if not t["evidence_ids"]:
            issues.append(f"Topic without evidence: {t['topic']}")
    for c in state.get("conflicts", []):
        if c["topic"] not in md:
            issues.append(f"Conflict not surfaced: {c['topic']}")
    if not b["customer"].get("name"):
        issues.append("Customer identity missing")

    available = {e["source"] for e in ev}
    coverage = len(available & set(b["sources"])) / max(1, len(available))
    total_claims = max(1, len(amounts) + len(b["recommended_topics"]))
    halluc = len(unsupported) / total_claims
    quality = {"factual_accuracy": round(1 - halluc, 2), "source_coverage": round(coverage, 2),
               "hallucination_risk": round(halluc, 2), "passed": not issues, "issues": issues}
    return {"quality": quality}
