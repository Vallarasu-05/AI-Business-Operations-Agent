import base64
from app.integrations.google.auth import service


def _body(payload: dict) -> str:
    if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", "ignore")
    for part in payload.get("parts", []) or []:
        b = _body(part)
        if b:
            return b
    return ""


class GoogleGmail:
    def search_emails(self, addresses: list[str], company_names: list[str], limit: int = 20) -> list[dict]:
        gm = service("gmail", "v1")
        q = " OR ".join(f"from:{a} OR to:{a}" for a in addresses)
        ids = gm.users().messages().list(userId="me", q=q, maxResults=limit).execute().get("messages", [])
        out = []
        for m in ids:
            msg = gm.users().messages().get(userId="me", id=m["id"], format="full").execute()
            h = {x["name"].lower(): x["value"] for x in msg["payload"]["headers"]}
            out.append({"thread_id": msg["threadId"], "subject": h.get("subject", ""),
                        "sender": h.get("from", ""), "to": [h.get("to", "")], "date": h.get("date", "")[:16],
                        "body": _body(msg["payload"])})
        return out
