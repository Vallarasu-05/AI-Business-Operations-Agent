"""Seed ABC Manufacturing into a HubSpot test account (needs HUBSPOT_ACCESS_TOKEN with write scopes
for companies/contacts/deals/tickets).  Run from /backend:  python ../scripts/create_demo_customer.py"""
import json
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from app.config import settings  # noqa: E402

if not settings.hubspot_access_token:
    sys.exit("Set HUBSPOT_ACCESS_TOKEN in .env first")
c = httpx.Client(base_url="https://api.hubapi.com", timeout=20,
                 headers={"Authorization": f"Bearer {settings.hubspot_access_token}"})
abc = json.loads((ROOT / "data/sample_customers/crm.json").read_text("utf-8"))["companies"][0]


def create(obj, props):
    r = c.post(f"/crm/v3/objects/{obj}", json={"properties": props})
    r.raise_for_status()
    return r.json()["id"]


def associate(a, aid, b, bid):
    c.put(f"/crm/v4/objects/{a}/{aid}/associations/default/{b}/{bid}").raise_for_status()


cid = create("companies", {"name": abc["name"], "domain": abc["domain"], "industry": "MANUFACTURING",
                           "numberofemployees": abc["employees"]})
for ct in abc["contacts"]:
    first, last = ct["name"].split(" ", 1)
    pid = create("contacts", {"firstname": first, "lastname": last, "email": ct["email"], "jobtitle": ct["role"]})
    associate("contacts", pid, "companies", cid)
d = abc["deals"][0]
did = create("deals", {"dealname": d["name"], "amount": d["amount"], "closedate": d["close_date"]})
associate("deals", did, "companies", cid)
t = abc["tickets"][0]
tid = create("tickets", {"subject": t["title"], "hs_ticket_priority": "HIGH", "hs_pipeline_stage": "1"})
associate("tickets", tid, "companies", cid)
print("Created company", cid, "- now set DATA_MODE=live_readonly")
