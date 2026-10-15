import httpx
from app.config import settings

BASE = "https://api.hubapi.com"


def _client() -> httpx.Client:
    return httpx.Client(base_url=BASE, timeout=20,
                        headers={"Authorization": f"Bearer {settings.hubspot_access_token}"})


def search(object_type: str, filters: list[dict], properties: list[str], limit: int = 10) -> list[dict]:
    with _client() as c:
        r = c.post(f"/crm/v3/objects/{object_type}/search",
                   json={"filterGroups": [{"filters": filters}], "properties": properties, "limit": limit})
        r.raise_for_status()
        return r.json().get("results", [])


def associated(from_type: str, from_id: str, to_type: str, properties: list[str]) -> list[dict]:
    with _client() as c:
        r = c.get(f"/crm/v4/objects/{from_type}/{from_id}/associations/{to_type}")
        r.raise_for_status()
        ids = [x["toObjectId"] for x in r.json().get("results", [])]
        if not ids:
            return []
        r = c.post(f"/crm/v3/objects/{to_type}/batch/read",
                   json={"properties": properties, "inputs": [{"id": str(i)} for i in ids]})
        r.raise_for_status()
        return r.json().get("results", [])
