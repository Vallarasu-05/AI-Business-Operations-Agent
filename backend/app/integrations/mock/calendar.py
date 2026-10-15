import json
from datetime import date, timedelta
from pathlib import Path
from app.config import settings


class MockCalendar:
    def get_meetings(self, day: str) -> list[dict]:
        events = json.loads((Path(settings.data_dir) / "sample_customers/calendar.json").read_text("utf-8"))
        out = []
        for e in events:
            d = (date.today() + timedelta(days=e.get("offset_days", 1))).isoformat()
            if d == day:
                out.append({k: v for k, v in e.items() if k != "offset_days"} | {"date": d})
        return out
