import uuid
from langgraph.types import Command
from app.agent.graph import build_graph
from app.config import settings


def _run(request, decision=None, tmp=None):
    g = build_graph()
    cfg = {"configurable": {"thread_id": uuid.uuid4().hex}}
    g.invoke({"user_request": request}, cfg)
    snap = g.get_state(cfg)
    if decision:
        g.invoke(Command(resume=decision), cfg)
    return g, cfg, snap


def test_full_flow_pauses_for_human_approval(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "output_dir", str(tmp_path))
    g, cfg, snap = _run("Prepare tomorrow's sales meeting with ABC Corporation")
    assert snap.next == ("human_review",)
    st = snap.values
    assert st["customer"]["company_id"] == "12345"
    assert st["quality"]["passed"], st["quality"]
    # planted conflict (CRM 18L vs email 20L) must be surfaced, not silently resolved
    assert any(c["topic"] == "deal_value" for c in st["conflicts"])
    # planted injection must be flagged, never executed
    assert any(r["risk"].startswith("Possible prompt-injection") for r in st["risks"])
    assert "attacker@evil.com" not in st["briefing_markdown"]
    assert {"crm", "gmail", "internal_document", "sheets", "web_search"} <= set(st["briefing"]["sources"])


def test_approval_sends_email_rejection_does_not(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "output_dir", str(tmp_path))
    g, cfg, _ = _run("Prepare tomorrow's sales meeting with ABC Corporation", {"status": "approved"})
    d = g.get_state(cfg).values["delivery"]
    assert d["email"]["status"] == "simulated"
    g2, cfg2, _ = _run("Prepare tomorrow's sales meeting with ABC Corporation", {"status": "rejected"})
    assert g2.get_state(cfg2).values["delivery"]["email"]["status"] == "skipped"


def test_no_meetings_ends_gracefully():
    g = build_graph()
    cfg = {"configurable": {"thread_id": uuid.uuid4().hex}}
    g.invoke({"user_request": "Prepare the meeting on 2020-01-01"}, cfg)
    st = g.get_state(cfg)
    assert not st.next and st.values["errors"]
