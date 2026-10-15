from app.schemas.evidence import Evidence
from app.tools.sheets_tools import get_pipeline


def research_sheets(state):
    c = state["customer"]
    try:
        rows = get_pipeline([c["name"], *c.get("aliases", [])])
    except Exception as e:
        return {"errors": [{"node": "research_sheets", "msg": f"Sheets failed: {e}"}]}
    ev = []
    for r in rows:
        sid = f"pipeline_row_{r['row']}"
        ev += [Evidence(claim=f"Pipeline sheet lists '{r['Deal']}' value {float(r['Value']):.0f}",
                        source="sheets", source_id=sid, confidence=0.95, topic="deal_value",
                        value=float(r["Value"])),
               Evidence(claim=f"Pipeline sheet lists stage {r['Stage']} (probability {r['Probability']})",
                        source="sheets", source_id=sid, confidence=0.95, topic="deal_stage",
                        value=str(r["Stage"]).lower()),
               Evidence(claim=f"Pipeline sheet lists close date {r['Close Date']}", source="sheets",
                        source_id=sid, confidence=0.95, topic="close_date", value=str(r["Close Date"]))]
    return {"sheet_data": rows, "evidence": [e.model_dump() for e in ev]}
