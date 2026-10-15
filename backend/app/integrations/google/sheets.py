from app.config import settings
from app.integrations.google.auth import service


class GoogleSheets:
    def get_pipeline(self, names: list[str]) -> list[dict]:
        vals = service("sheets", "v4").spreadsheets().values().get(
            spreadsheetId=settings.google_sheet_id, range="A1:Z1000").execute().get("values", [])
        if not vals:
            return []
        header, keys = vals[0], [n.lower() for n in names if n]
        rows = []
        for i, r in enumerate(vals[1:], start=2):
            d = dict(zip(header, r))
            c = str(d.get("Customer", "")).lower()
            if any(k in c or c in k for k in keys):
                rows.append({"row": i, **d})
        return rows
