from fastapi import APIRouter, HTTPException
from pathlib import Path
import json, base64
import pyotp

router = APIRouter(prefix="/2fa", tags=["2fa"])
DATA = Path(__file__).resolve().parents[1] / "data" / "twofa.json"

def _load():
    if DATA.exists():
        return json.loads(DATA.read_text(encoding="utf-8"))
    return {}

def _save(obj):
    DATA.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return obj

@router.post("/enable")
def enable_2fa(user_id: str = "admin"):
    db = _load()
    secret = pyotp.random_base32()
    db[user_id] = {"secret": secret, "enabled": False}
    _save(db)
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=user_id, issuer_name="FISCUS AI")
    return {"secret": secret, "otpauth_uri": uri}

@router.post("/verify")
def verify_2fa(code: str, user_id: str = "admin"):
    db = _load()
    rec = db.get(user_id)
    if not rec:
        raise HTTPException(status_code=404, detail="2FA not initialized")
    totp = pyotp.TOTP(rec["secret"])
    ok = totp.verify(code)
    if ok:
        rec["enabled"] = True
        _save(db)
    return {"ok": ok}

@router.get("/status")
def status_2fa(user_id: str = "admin"):
    db = _load()
    rec = db.get(user_id)
    return {"enabled": bool(rec and rec.get("enabled")), "has_secret": bool(rec)}
