from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel, EmailStr
from typing import Optional
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import pyotp
import os

from app.db import get_session
from sqlmodel import Session, select
from app.models.user import User
from app.dependencies import require_role, auth_bearer
from app.auth import hash_password
from app.utils.mailer import send_email

SECRET = os.getenv("JWT_SECRET", "change-me")
RESET_SALT = "password-reset"
serializer = URLSafeTimedSerializer(SECRET)

router = APIRouter(prefix="/auth", tags=["auth"])

class ResetRequest(BaseModel):
    email: EmailStr

@router.post("/reset/request")
def reset_request(payload: ResetRequest, s: Session = Depends(get_session)):
    user = s.exec(select(User).where(User.email == payload.email)).first()
    if not user:
        # Do not leak existence
        return {"ok": True}
    token = serializer.dumps({"email": user.email}, salt=RESET_SALT)
    # Send email (dev writes to file)
    send_email([user.email], "Password reset", f"<p>Use this token: <code>{token}</code></p>")
    return {"ok": True, "dev_token": token}

class ResetConfirm(BaseModel):
    token: str
    new_password: str

@router.post("/reset/confirm")
def reset_confirm(payload: ResetConfirm, s: Session = Depends(get_session)):
    try:
        data = serializer.loads(payload.token, max_age=3600, salt=RESET_SALT)
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")

    email = data.get("email")
    user = s.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password_hash = hash_password(payload.new_password)
    s.add(user)
    s.commit()
    return {"ok": True}

class TFASetupOut(BaseModel):
    secret: str
    uri: str

@router.post("/2fa/setup", response_model=TFASetupOut)
def tfa_setup(user=Depends(auth_bearer), s: Session = Depends(get_session)):
    # Per-user secret
    email = (user or {}).get("email") or "dev@local"
    account = s.exec(select(User).where(User.email == email)).first()
    if not account:
        raise HTTPException(status_code=404, detail="User not found")

    secret = pyotp.random_base32()
    account.totp_secret = secret
    s.add(account)
    s.commit()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name="FISCUS AI")
    return {"secret": secret, "uri": uri}

class TFAVerifyIn(BaseModel):
    code: str

@router.post("/2fa/verify")
def tfa_verify(payload: TFAVerifyIn, user=Depends(auth_bearer), s: Session = Depends(get_session)):
    email = (user or {}).get("email") or "dev@local"
    account = s.exec(select(User).where(User.email == email)).first()
    if not account or not account.totp_secret:
        raise HTTPException(status_code=400, detail="2FA not initialized")
    totp = pyotp.TOTP(account.totp_secret)
    if not totp.verify(payload.code, valid_window=1):
        raise HTTPException(status_code=400, detail="Invalid code")
    account.twofa_enabled = True
    s.add(account)
    s.commit()
    return {"ok": True}
