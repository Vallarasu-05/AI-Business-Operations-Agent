from app.integrations.hubspot import client

PROPS = ["name", "domain", "industry", "numberofemployees"]


def find(name: str | None = None, domain: str | None = None) -> dict | None:
    if domain:
        res = client.search("companies", [{"propertyName": "domain", "operator": "EQ", "value": domain}], PROPS)
    elif name:
        token = name.split("-")[0].strip().split()[0]
        res = client.search("companies", [{"propertyName": "name", "operator": "CONTAINS_TOKEN", "value": token}], PROPS)
    else:
        return None
    if not res:
        return None
    p = res[0]["properties"]
    return {"id": res[0]["id"], "name": p.get("name"), "domain": p.get("domain"), "industry": p.get("industry"),
            "employees": int(p["numberofemployees"]) if p.get("numberofemployees") else None, "aliases": []}
