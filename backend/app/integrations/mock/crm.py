import json
from pathlib import Path
from app.config import settings


class MockCRM:
    def _all(self) -> list[dict]:
        return json.loads((Path(settings.data_dir) / "sample_customers/crm.json").read_text("utf-8"))["companies"]

    @staticmethod
    def _basic(c: dict) -> dict:
        return {k: c[k] for k in ("id", "name", "aliases", "domain", "industry", "employees")}

    def find_company(self, name=None, email=None, domain=None):
        for c in self._all():
            if email:
                if any(ct["email"].lower() == email.lower() for ct in c["contacts"]):
                    return self._basic(c)
                if email.lower().endswith("@" + c["domain"]):
                    return self._basic(c)
            if domain and domain.lower() == c["domain"]:
                return self._basic(c)
            if name:
                text = name.lower()
                if any(n.lower() in text for n in [c["name"], *c["aliases"]]):
                    return self._basic(c)
        return None

    def get_context(self, company_id: str) -> dict:
        for c in self._all():
            if c["id"] == company_id:
                return {"company": self._basic(c), "contacts": c["contacts"], "deals": c["deals"],
                        "tickets": c["tickets"], "activities": c["activities"]}
        return {"company": None, "contacts": [], "deals": [], "tickets": [], "activities": []}
