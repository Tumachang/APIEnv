from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"

def test_echo_post():
    payload = {"msg": "hello"}
    r = client.post("/echo", json=payload)
    assert r.status_code == 200
    assert r.json()["received"] == payload
