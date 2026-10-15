from app.integrations.hubspot import client


def for_company(company_id: str) -> list[dict]:
    rows = client.associated("companies", company_id, "notes", ["hs_note_body", "hs_timestamp"])
    return [{"id": r["id"], "type": "note", "date": (r["properties"].get("hs_timestamp") or "")[:10],
             "note": r["properties"].get("hs_note_body") or ""} for r in rows]
