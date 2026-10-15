import json
from pathlib import Path
from app.config import settings


class MockGmail:
    def search_emails(self, addresses: list[str], company_names: list[str]) -> list[dict]:
        threads = json.loads((Path(settings.data_dir) / "sample_emails/threads.json").read_text("utf-8"))
        addrs = {a.lower() for a in addresses}
        out = []
        for t in threads:
            for m in t["messages"]:
                people = {m["from"].lower(), *[x.lower() for x in m["to"]]}
                if people & addrs:
                    out.append({"thread_id": t["thread_id"], "subject": t["subject"], "sender": m["from"],
                                "to": m["to"], "date": m["date"], "body": m["body"]})
        return sorted(out, key=lambda x: x["date"])
