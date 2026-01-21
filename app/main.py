

import os
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()


def _push_secret() -> str:
    return os.getenv("PUSH_SECRET", "")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/gmail/push")
async def gmail_push(req: Request, x_push_secret: str | None = Header(default=None)):
    secret = _push_secret()
    if secret and x_push_secret != secret:
        raise HTTPException(status_code=401, detail="bad secret")

    # Por ahora solo logeamos el payload; luego aquí conectaremos Gmail API.
    try:
        payload = await req.json()
    except Exception:
        payload = {"raw": (await req.body()).decode("utf-8", errors="ignore")}

    print("PUBSUB PUSH RECEIVED:", payload)
    return {"ok": True}
