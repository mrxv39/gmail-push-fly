
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_gmail_push_requires_authorization():
    r = client.post("/gmail/push", json={"hello": "world"})
    assert r.status_code == 401


def test_gmail_push_accepts_valid_oidc(monkeypatch):
    from app import main as main_mod

    def fake_verify(token, request_obj, audience):
        assert token == "fake-token"
        assert audience == main_mod.EXPECTED_AUDIENCE
        return {"email": main_mod.EXPECTED_EMAIL, "aud": audience}

    monkeypatch.setattr(main_mod.id_token, "verify_oauth2_token", fake_verify)

    r = client.post(
        "/gmail/push",
        json={"hello": "world"},
        headers={"Authorization": "Bearer fake-token"},
    )
    assert r.status_code == 200
    assert r.json() == {"ok": True}


def test_gmail_push_rejects_wrong_email(monkeypatch):
    from app import main as main_mod

    def fake_verify(token, request_obj, audience):
        return {"email": "someone-else@gserviceaccount.com", "aud": audience}

    monkeypatch.setattr(main_mod.id_token, "verify_oauth2_token", fake_verify)

    r = client.post(
        "/gmail/push",
        json={"hello": "world"},
        headers={"Authorization": "Bearer fake-token"},
    )
    assert r.status_code == 401
