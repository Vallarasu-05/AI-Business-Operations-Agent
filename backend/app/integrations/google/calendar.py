from datetime import datetime, timedelta
from app.integrations.google.auth import service


class GoogleCalendar:
    def get_meetings(self, day: str) -> list[dict]:
        start = datetime.fromisoformat(day)
        res = service("calendar", "v3").events().list(
            calendarId="primary", singleEvents=True, orderBy="startTime",
            timeMin=start.astimezone().isoformat(),
            timeMax=(start + timedelta(days=1)).astimezone().isoformat()).execute()
        out = []
        for e in res.get("items", []):
            s, en = e["start"].get("dateTime", ""), e["end"].get("dateTime", "")
            out.append({
                "event_id": e["id"], "title": e.get("summary", "(no title)"), "date": day,
                "start": s[11:16], "end": en[11:16], "location": e.get("location") or e.get("hangoutLink"),
                "attendees": [{"name": a.get("displayName") or a["email"].split("@")[0], "email": a["email"]}
                              for a in e.get("attendees", [])]})
        return out
