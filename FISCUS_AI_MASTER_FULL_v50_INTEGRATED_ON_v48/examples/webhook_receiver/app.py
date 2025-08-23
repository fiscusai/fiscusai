from fastapi import FastAPI, Request, HTTPException
import hmac, hashlib, os, json

app = FastAPI()

def verify(body: bytes, signature: str) -> bool:
    secret = os.getenv("WEBHOOK_SECRET","").encode("utf-8")
    if not secret:
        return True  # dev mode
    mac = hmac.new(secret, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature)

@app.post("/webhook/fiscus")
async def fiscus_hook(request: Request):
    body = await request.body()
    sig = request.headers.get("X-Webhook-Signature","")
    if not verify(body, sig):
        raise HTTPException(status_code=401, detail="invalid signature")
    data = json.loads(body.decode("utf-8"))
    print("event:", data.get("event"), "key:", data.get("key"), "ok:", data.get("ok"), "av:", data.get("av"))
    return {"received": True}