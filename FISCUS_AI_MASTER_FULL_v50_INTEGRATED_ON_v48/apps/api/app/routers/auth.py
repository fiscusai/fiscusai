from app.security.rate_limit import rate_limit
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from passlib.hash import bcrypt
from datetime import datetime
from typing import Optional

from app.db import get_session
from app.models.user import User
from app.security.auth_jwt import create_token, verify_token
from app.dependencies import auth_bearer

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    org: Optional[str] = "DEFAULT"
    role: Optional[str] = "user"

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenOut)
def register(data: RegisterIn, s: Session = Depends(get_session)):
    # unique email
    exists = s.exec(select(User).where(User.email == str(data.email))).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(
        email=str(data.email),
        password_hash=bcrypt.hash(data.password),
        role=data.role or "user",
        org=data.org or "DEFAULT",
        created_at=datetime.utcnow(),
    )
    s.add(user); s.commit(); s.refresh(user)
    payload = {"sub": user.email, "role": user.role, "org": user.org, "uid": user.id}
    return TokenOut(access_token=create_token(payload), refresh_token=create_token(payload, refresh=True))

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, s: Session = Depends(get_session)):
    user = s.exec(select(User).where(User.email == str(data.email))).first()
    if not user or not bcrypt.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {"sub": user.email, "role": user.role, "org": user.org, "uid": user.id}
    return TokenOut(access_token=create_token(payload), refresh_token=create_token(payload, refresh=True))

class RefreshIn(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=TokenOut)
def refresh(inp: RefreshIn):
    data = verify_token(inp.refresh_token, expect_typ="refresh")
    payload = {"sub": data.get("sub"), "role": data.get("role"), "org": data.get("org"), "uid": data.get("uid")}
    return TokenOut(access_token=create_token(payload), refresh_token=create_token(payload, refresh=True))

@router.get("/me")
def me(user=Depends(auth_bearer)):
    return user
