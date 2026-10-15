from app.integrations.hubspot import client


def for_company(company_id: str) -> list[dict]:
    rows = client.associated("companies", company_id, "tickets",
                             ["subject", "hs_ticket_priority", "hs_pipeline_stage"])
    return [{"id": r["id"], "title": r["properties"].get("subject"),
             "priority": (r["properties"].get("hs_ticket_priority") or "").title(),
             "status": r["properties"].get("hs_pipeline_stage")} for r in rows]
