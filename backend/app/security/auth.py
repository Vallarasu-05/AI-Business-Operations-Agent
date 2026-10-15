from fastapi import Header, HTTPException
from app.config import settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """If API_KEY is configured, requests must send it in X-API-Key."""
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
