from app.services.customer_service import resolve_customer_identity
from app.tools import crm_tools


def test_find_by_contact_email():
    assert crm_tools.find_company(email="john.smith@abcmfg.com")["id"] == "12345"


def test_resolve_identity_from_meeting():
    m = {"title": "x", "attendees": [{"name": "J", "email": "john.smith@abcmfg.com"},
                                      {"name": "V", "email": "v@mycompany.com"}]}
    c = resolve_customer_identity(m)
    assert c["company_id"] == "12345" and c["confidence"] > 0.9


def test_unknown_domain_falls_back():
    c = resolve_customer_identity({"title": "x", "attendees": [{"name": "Z", "email": "z@nowhere.org"}]})
    assert c["company_id"] is None and c["matched_via"] == "attendee_domain_fallback"
