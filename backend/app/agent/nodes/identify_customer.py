from app.services.customer_service import resolve_customer_identity


def identify_customer(state):
    customer = resolve_customer_identity(state["selected_meeting"])
    if not customer:
        return {"errors": [{"node": "identify_customer", "msg": "No external attendees; cannot resolve customer"}]}
    out = {"customer": customer}
    if not customer.get("company_id"):
        out["errors"] = [{"node": "identify_customer",
                          "msg": f"No CRM record found; fell back to attendee domain ({customer['domain']})"}]
    return out
