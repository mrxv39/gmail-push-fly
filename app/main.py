

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/gmail/push")
async def gmail_push(req: Request):
    try:
        payload = await req.json()
    except Exception:
        payload = {"raw": (await req.body()).decode("utf-8", errors="ignore")}

    print("PUBSUB PUSH RECEIVED:", payload)
    return {"ok": True}
