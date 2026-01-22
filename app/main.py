

import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Request
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

app = FastAPI()

EXPECTED_AUDIENCE = os.getenv("PUBSUB_OIDC_AUDIENCE", "https://gmail-push-fly.fly.dev/gmail/push")
EXPECTED_EMAIL = os.getenv(
    "PUBSUB_OIDC_EMAIL",
    "pubsub-push-invoker@gmail-push-fly.iam.gserviceaccount.com",
)


def verify_pubsub_oidc(auth_header: Optional[str]) -> Dict[str, Any]:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization Bearer token")

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty Bearer token")

    try:
        info = id_token.verify_oauth2_token(token, google_requests.Request(), EXPECTED_AUDIENCE)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid OIDC token")

    email = info.get("email")
    if email != EXPECTED_EMAIL:
        raise HTTPException(status_code=401, detail="Invalid token email")

    return info


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/gmail/push")
async def gmail_push(req: Request):
    verify_pubsub_oidc(req.headers.get("authorization"))

    try:
        payload = await req.json()
    except Exception:
        payload = {"raw": (await req.body()).decode("utf-8", errors="ignore")}

    print("PUBSUB PUSH RECEIVED:", payload)
    return {"ok": True}
