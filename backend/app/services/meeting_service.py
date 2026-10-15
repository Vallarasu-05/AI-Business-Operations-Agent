from datetime import date, timedelta
from app.tools import calendar_tools


def tomorrow() -> str:
    return (date.today() + timedelta(days=1)).isoformat()


def meetings_for(day: str) -> list[dict]:
    return calendar_tools.get_meetings(day)


def find_meeting(event_id: str) -> dict | None:
    for offset in range(0, 8):
        d = (date.today() + timedelta(days=offset)).isoformat()
        for m in calendar_tools.get_meetings(d):
            if m["event_id"] == event_id:
                return m
    return None
