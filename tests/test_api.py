from fastapi.testclient import TestClient
from orchestrator.api import app

client = TestClient(app)


def test_start_and_fetch_run():
    resp = client.post("/runs", json={"task": "hello"})
    assert resp.status_code == 200
    run_id = resp.json()["run_id"]

    result = client.get(f"/runs/{run_id}").json()
    assert result["status"] == "passed"
    assert len(result["events"]) > 0


def test_unknown_run_returns_404():
    assert client.get("/runs/doesnotexist").status_code == 404