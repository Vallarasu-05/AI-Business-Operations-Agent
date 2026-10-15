from app.config import settings
from app.security.sanitizer import sanitize_text
from app.services.research_service import EMAIL_TOPICS, extract_signals
from app.tools.gmail_tools import search_emails


def research_email(state):
    c = state["customer"]
    try:
        msgs = search_emails(c["emails"], [c["name"], *c.get("aliases", [])])
    except Exception as e:  # tool failure -> degrade gracefully (retry/fallback hook)
        return {"errors": [{"node": "research_email", "msg": f"Gmail failed: {e}"}]}
    internal = "@" + settings.internal_domain.lower()
    ev, cleaned = [], []
    for m in msgs:
        body = sanitize_text(m["body"])
        cleaned.append({**m, "body": body})
        topics = EMAIL_TOPICS if not m["sender"].lower().endswith(internal) else {"commitment"}
        e, flags = extract_signals(body, "gmail", m["thread_id"], m["date"], 0.85, topics)
        ev += e + flags
    return {"email_data": cleaned, "evidence": ev}
