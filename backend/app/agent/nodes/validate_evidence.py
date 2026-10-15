from app.agent.source_priority import priority
from app.memory import customer_memory
from app.schemas.evidence import Conflict
from app.services.money import fmt_inr

CONFLICT_TOPICS = {"deal_value", "deal_stage", "close_date"}


def _display(topic, v):
    return fmt_inr(v) if topic == "deal_value" and isinstance(v, (int, float)) else str(v)


def validate_evidence(state):
    """Dedupe, assign stable ids, add memory, and detect cross-source conflicts (never silently pick one)."""
    seen, ev = set(), []
    for e in state.get("evidence", []):
        k = (e["topic"], e["claim"], e["source"])  # overlapping chunks repeat claims
        if k not in seen:
            seen.add(k)
            ev.append(e)

    mem = customer_memory.load(state["customer"].get("company_id"))
    for concern in mem.get("known_concerns", []):
        ev.append({"claim": f"Previously recorded concern: {concern}", "source": "memory",
                   "source_id": "customer_memory", "date": mem.get("last_meeting"), "confidence": 0.8,
                   "topic": "memory_concern", "value": None})

    ev.sort(key=lambda e: -priority(e["source"]))
    for i, e in enumerate(ev, 1):
        e["id"] = f"E{i}"

    conflicts = []
    for topic in CONFLICT_TOPICS:
        rows = [e for e in ev if e["topic"] == topic and e.get("value") is not None]
        if len({str(e["value"]) for e in rows}) > 1:
            best = max(rows, key=lambda e: priority(e["source"]))
            groups: dict[str, dict] = {}
            for e in rows:
                g = groups.setdefault(str(e["value"]), {"display": _display(topic, e["value"]),
                                                        "sources": [], "evidence_ids": []})
                if e["source"] not in g["sources"]:
                    g["sources"].append(e["source"])
                g["evidence_ids"].append(e["id"])
            conflicts.append(Conflict(
                topic=topic,
                values=[{"source": e["source"], "source_id": e["source_id"], "value": e["value"],
                         "display": _display(topic, e["value"]), "evidence_id": e["id"]} for e in rows],
                groups=list(groups.values()),
                note="Conflict detected; the latest authoritative value could not be determined automatically.",
                highest_priority_source=best["source"]).model_dump())
    return {"validated_evidence": ev, "conflicts": conflicts, "memory": mem}
