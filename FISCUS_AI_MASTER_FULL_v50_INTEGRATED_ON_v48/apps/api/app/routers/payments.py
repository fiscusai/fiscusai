from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime, timedelta
import hmac, hashlib, os

router = APIRouter(prefix="/payments", tags=["payments"])

class CheckoutRequest(BaseModel):
    plan: str  # basic | pro | enterprise
    interval: str = "monthly"  # monthly | yearly
    email: str

@router.post("/checkout")
def checkout(data: CheckoutRequest):
    # Mock checkout: return a fake payment_url and a temp token
    if data.plan not in {"basic","pro","enterprise"}:
        raise HTTPException(status_code=400, detail="Invalid plan")
    token = hashlib.sha256(f"{data.email}:{data.plan}:{datetime.utcnow()}".encode()).hexdigest()[:24]
    return {
        "payment_url": f"https://example-payments.local/checkout/{token}",
        "expires_at": (datetime.utcnow() + timedelta(minutes=30)).isoformat() + "Z"
    }

def _sign(body: bytes, secret: str) -> str:
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

@router.post("/webhook")
async def webhook(request: Request):
    # Very simple webhook signature check
    body = await request.body()
    secret = os.getenv("PAYMENT_WEBHOOK_SECRET", "dev-secret")
    sig = request.headers.get("X-Payment-Signature", "")
    if not hmac.compare_digest(sig, _sign(body, secret)):
        raise HTTPException(status_code=401, detail="Invalid signature")
    # In a real system, update subscription status, record invoice, etc.
    return {"ok": True}
