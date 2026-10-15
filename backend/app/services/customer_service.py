from app.config import settings
from app.tools import crm_tools


def resolve_customer_identity(meeting: dict) -> dict:
    """attendee email -> CRM contact -> company; falls back to domain / title matching."""
    internal = "@" + settings.internal_domain.lower()
    external = [a for a in meeting.get("attendees", []) if not a["email"].lower().endswith(internal)]
    emails = [a["email"] for a in external]
    if not external:
        return {}

    company, via, conf = None, "", 0.0
    for a in external:
        company = crm_tools.find_company(email=a["email"])
        if company:
            via, conf = f"attendee_email:{a['email']}", 0.97
            break
    if not company:
        company = crm_tools.find_company(name=meeting.get("title", ""))
        if company:
            via, conf = "meeting_title", 0.75
    if company:
        return {**company, "company_id": company["id"], "emails": emails,
                "contacts_attending": [a["name"] for a in external],
                "matched_via": via, "confidence": conf}

    domain = emails[0].split("@")[1]
    return {"company_id": None, "name": domain.split(".")[0].title(), "domain": domain,
            "emails": emails, "contacts_attending": [a["name"] for a in external],
            "aliases": [], "matched_via": "attendee_domain_fallback", "confidence": 0.4}
