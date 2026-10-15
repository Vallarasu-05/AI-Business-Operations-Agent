import httpx
from app.config import settings


def call_webhook(path: str, payload: dict, timeout: float = 60) -> dict:
    """POST to an n8n webhook (production URL). Protected by a shared-secret header."""
    r = httpx.post(f"{settings.n8n_base_url}/webhook/{path}", json=payload, timeout=timeout,
                   headers={"X-Webhook-Secret": settings.n8n_webhook_secret})
    r.raise_for_status()
    try:
        return r.json()
    except ValueError:
        return {"raw": r.text}
