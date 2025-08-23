from fastapi import APIRouter, Request, HTTPException
import hmac, hashlib, json, os, time

router = APIRouter(prefix="/payments/stripe", tags=["payments"])

# Minimal Stripe-like signature: t=<ts>, v1=<hex>
def _parse_sig(sig_header: str):
    parts = [p.strip() for p in (sig_header or "").split(",")]
    data = {}
    for p in parts:
        if "=" in p:
            k,v = p.split("=",1)
            data[k]=v
    return data

def _compute_signature(secret: str, ts: str, payload: bytes):
    signed = f"{ts}.{payload.decode('utf-8')}"
    return hmac.new(secret.encode(), signed.encode(), hashlib.sha256).hexdigest()

@router.post("/webhook")
async def stripe_webhook(request: Request):
    secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_dev")
    sig = request.headers.get("Stripe-Signature")
    if not sig:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature")
    data = _parse_sig(sig)
    ts = data.get("t")
    v1 = data.get("v1")
    if not ts or not v1:
        raise HTTPException(status_code=400, detail="Invalid signature header")
    try:
        ts_i = int(ts)
        # 5 dk tolerans
        if abs(time.time() - ts_i) > 300:
            raise HTTPException(status_code=400, detail="Timestamp too old")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timestamp")

    body = await request.body()
    expected = _compute_signature(secret, ts, body)
    if not hmac.compare_digest(expected, v1):
        raise HTTPException(status_code=400, detail="Invalid signature")

    event = json.loads(body.decode("utf-8"))
    # TODO: handle event['type'] like checkout.session.completed
    return {"ok": True, "received": event.get("type")}
