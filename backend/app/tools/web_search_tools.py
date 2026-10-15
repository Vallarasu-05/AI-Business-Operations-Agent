import json
from pathlib import Path
import httpx
from app.config import settings


def search_company(name: str, company_id: str | None) -> list[dict]:
    """External info. Mock mode (or no key) reads data/sample_web; live mode uses Tavily."""
    if settings.is_mock or not settings.web_search_api_key:
        f = Path(settings.data_dir) / "sample_web/web_news.json"
        return json.loads(f.read_text("utf-8")).get(company_id or "", [])
    r = httpx.post("https://api.tavily.com/search", timeout=20, json={
        "api_key": settings.web_search_api_key, "query": f"{name} latest news", "max_results": 5})
    r.raise_for_status()
    return [{"title": x["title"], "snippet": x.get("content", "")[:300], "url": x["url"],
             "date": x.get("published_date", "")} for x in r.json().get("results", [])]
