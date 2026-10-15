from app.integrations.hubspot import client


def by_email(email: str) -> dict | None:
    res = client.search("contacts", [{"propertyName": "email", "operator": "EQ", "value": email}],
                        ["firstname", "lastname", "email", "jobtitle", "associatedcompanyid"])
    return res[0] if res else None


def for_company(company_id: str) -> list[dict]:
    rows = client.associated("companies", company_id, "contacts", ["firstname", "lastname", "email", "jobtitle"])
    return [{"id": r["id"], "name": f"{r['properties'].get('firstname', '')} {r['properties'].get('lastname', '')}".strip(),
             "email": r["properties"].get("email"), "role": r["properties"].get("jobtitle")} for r in rows]
