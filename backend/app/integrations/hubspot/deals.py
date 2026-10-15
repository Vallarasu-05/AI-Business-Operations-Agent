from app.integrations.hubspot import client


def for_company(company_id: str) -> list[dict]:
    rows = client.associated("companies", company_id, "deals",
                             ["dealname", "amount", "dealstage", "closedate", "hs_deal_stage_probability"])
    return [{"id": r["id"], "name": r["properties"].get("dealname"),
             "amount": float(r["properties"].get("amount") or 0), "currency": "INR",
             "stage": r["properties"].get("dealstage"), "close_date": (r["properties"].get("closedate") or "")[:10],
             "probability": r["properties"].get("hs_deal_stage_probability")} for r in rows]
