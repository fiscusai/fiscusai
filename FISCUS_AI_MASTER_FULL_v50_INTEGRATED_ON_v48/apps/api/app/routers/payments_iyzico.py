from fastapi import APIRouter, Request, HTTPException
import hmac, hashlib, os, json

router = APIRouter(prefix="/payments/iyzico", tags=["payments"])

@router.post("/webhook")
async def iyzico_webhook(request: Request):
    secret = os.getenv("IYZICO_WEBHOOK_SECRET", "iyzi_dev")
    sig = request.headers.get("X-IYZ-Signature")
    if not sig:
        raise HTTPException(status_code=400, detail="Missing signature")
    body = await request.body()
    expected = hmac.new(secret.encode(), body, hashlib.sha1).hexdigest()
    if not hmac.compare_digest(expected, sig):
        raise HTTPException(status_code=400, detail="Invalid signature")
    try:
        payload = json.loads(body.decode("utf-8"))
    except Exception:
        payload = {"raw": body.decode("utf-8", errors="ignore")}
    return {"ok": True, "status": "accepted", "payload": payload.get("status")}
