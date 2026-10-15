"""Email delivery. Real sending only happens in live_write mode via n8n; otherwise it's simulated."""
import time
from pathlib import Path
from app.config import settings
from app.integrations.n8n.client import call_webhook


def send_email(to: list[str], subject: str, body: str, attachment: str | None = None) -> dict:
    if settings.data_mode == "live_write":
        res = call_webhook("briefing-delivery", {"to": to, "subject": subject, "body": body,
                                                  "attachment": attachment})
        return {"status": "sent", "via": "n8n", "response": res}
    outbox = Path(settings.output_dir) / "outbox"
    outbox.mkdir(parents=True, exist_ok=True)
    f = outbox / f"email_{int(time.time())}.txt"
    f.write_text(f"TO: {', '.join(to)}\nSUBJECT: {subject}\n\n{body}\n", encoding="utf-8")
    return {"status": "simulated", "via": "outbox", "file": str(f)}
