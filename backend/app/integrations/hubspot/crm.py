from app.integrations.hubspot import activities, companies, contacts, deals, tickets


class HubSpotCRM:
    def find_company(self, name=None, email=None, domain=None):
        if email:
            c = contacts.by_email(email)
            cid = (c or {}).get("properties", {}).get("associatedcompanyid")
            if cid:
                return self._by_id(cid)
            domain = domain or email.split("@")[1]
        return companies.find(name=name, domain=domain)

    def _by_id(self, cid: str):
        from app.integrations.hubspot import client
        res = client.search("companies", [{"propertyName": "hs_object_id", "operator": "EQ", "value": cid}],
                            companies.PROPS)
        if not res:
            return None
        p = res[0]["properties"]
        return {"id": cid, "name": p.get("name"), "domain": p.get("domain"), "industry": p.get("industry"),
                "employees": None, "aliases": []}

    def get_context(self, company_id: str) -> dict:
        return {"company": {"id": company_id}, "contacts": contacts.for_company(company_id),
                "deals": deals.for_company(company_id), "tickets": tickets.for_company(company_id),
                "activities": activities.for_company(company_id)}
