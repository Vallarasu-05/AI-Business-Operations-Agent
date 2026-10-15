"""Long-term customer memory (JSON files; swap for Postgres/Store later)."""
import json
from pathlib import Path
from app.config import settings


def _file(company_id: str) -> Path:
    d = Path(settings.output_dir) / "memory"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{company_id}.json"


def load(company_id: str | None) -> dict:
    if not company_id:
        return {}
    f = _file(company_id)
    return json.loads(f.read_text("utf-8")) if f.exists() else {}


def update_from_briefing(company_id: str | None, briefing: dict) -> dict:
    if not company_id:
        return {}
    mem = load(company_id)
    concerns = set(mem.get("known_concerns", [])) | {o["text"][:140] for o in briefing.get("objections", [])}
    meetings = mem.get("past_meetings", []) + [{"date": briefing["meeting"]["date"],
                                                "summary": briefing["executive_summary"]}]
    mem.update({"known_concerns": sorted(concerns), "past_meetings": meetings[-10:],
                "last_meeting": briefing["meeting"]["date"],
                "open_commitments": [i["text"][:140] for i in briefing.get("open_issues", [])]})
    _file(company_id).write_text(json.dumps(mem, indent=2, ensure_ascii=False), "utf-8")
    return mem
