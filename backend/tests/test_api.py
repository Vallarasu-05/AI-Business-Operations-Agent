import time
from fastapi.testclient import TestClient
from app.config import settings
from app.main import app


def test_api_run_and_approve(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "output_dir", str(tmp_path))
    monkeypatch.setattr(settings, "api_key", "")
    c = TestClient(app)
    assert c.get("/health").json()["status"] == "ok"
    eid = c.post("/api/agent/run", json={"request": "Prepare tomorrow's sales meeting with ABC Corporation"}).json()["execution_id"]

    def wait(status):
        for _ in range(100):
            ex = c.get(f"/api/executions/{eid}").json()
            if ex["status"] == status:
                return ex
            time.sleep(0.1)
        raise AssertionError(ex["status"])

    ex = wait("waiting_approval")
    assert ex["interrupt"]["action"] == "send_email"
    assert c.post(f"/api/approval/{eid}", json={"status": "approved"}).status_code == 200
    ex = wait("completed")
    assert ex["state"]["delivery"]["email"]["status"] == "simulated"
    assert c.get(f"/api/briefings/{eid}/pdf").status_code == 200


def test_api_key_enforced(monkeypatch):
    monkeypatch.setattr(settings, "api_key", "secret")
    c = TestClient(app)
    assert c.get("/api/meetings/tomorrow").status_code == 401
    assert c.get("/api/meetings/tomorrow", headers={"X-API-Key": "secret"}).status_code == 200
