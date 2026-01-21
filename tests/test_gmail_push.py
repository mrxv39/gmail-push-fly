
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_gmail_push_allows_when_no_secret(monkeypatch):
    monkeypatch.delenv("PUSH_SECRET", raising=False)
    r = client.post("/gmail/push", json={"hello": "world"})
    assert r.status_code == 200
    assert r.json() == {"ok": True}


def test_gmail_push_rejects_wrong_secret(monkeypatch):
    monkeypatch.setenv("PUSH_SECRET", "abc")
    r = client.post("/gmail/push", json={"x": 1}, headers={"X-Push-Secret": "wrong"})
    assert r.status_code == 401


def test_gmail_push_accepts_correct_secret(monkeypatch):
    monkeypatch.setenv("PUSH_SECRET", "abc")
    r = client.post("/gmail/push", json={"x": 1}, headers={"X-Push-Secret": "abc"})
    assert r.status_code == 200
    assert r.json() == {"ok": True}
