from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from passlib.context import CryptContext
from datetime import timedelta, datetime
from ..core.db import get_session
from ..core.security import create_token, decode_token, current_user
from ..core.config import settings
from ..models.user import User
from ..models.company import Company, UserCompany
from ..models.token import ResetToken, InviteToken
from ..schemas.auth import LoginRequest, RegisterRequest, TokenResponse, ResetRequest, DoReset
import secrets, smtplib
from email.message import EmailMessage

router = APIRouter(prefix="/auth", tags=["auth"])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def send_mail(to: str, subject: str, body: str):
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASS: return
    msg = EmailMessage(); msg["From"]=settings.SMTP_FROM; msg["To"]=to; msg["Subject"]=subject; msg.set_content(body)
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
        s.starttls(); s.login(settings.SMTP_USER, settings.SMTP_PASS); s.send_message(msg)

@router.post("/register", response_model=dict)
def register(payload: RegisterRequest, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email == payload.email)).first():
        raise HTTPException(400, "Email already registered")
    u = User(email=payload.email, full_name=payload.full_name or "", hashed_password=pwd.hash(payload.password))
    session.add(u); session.commit(); session.refresh(u)
    c = Company(name=f"{u.full_name or u.email.split('@')[0]}'s Company")
    session.add(c); session.commit(); session.refresh(c)
    session.add(UserCompany(user_id=u.id, company_id=c.id, role="admin")); session.commit()
    return {"ok": True}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not pwd.verify(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    access = create_token(str(user.id), timedelta(minutes=settings.ACCESS_EXPIRE_MIN))
    refresh = create_token(f"r:{user.id}", timedelta(days=settings.REFRESH_EXPIRE_DAYS))
    return TokenResponse(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=TokenResponse)
def refresh(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing refresh token")
    token = authorization.split(" ",1)[1]
    sub = decode_token(token)
    if not sub or not sub.startswith("r:"):
        raise HTTPException(401, "Invalid refresh token")
    uid = sub.split(":",1)[1]
    access = create_token(uid, timedelta(minutes=settings.ACCESS_EXPIRE_MIN))
    new_refresh = create_token(f"r:{uid}", timedelta(days=settings.REFRESH_EXPIRE_DAYS))
    return TokenResponse(access_token=access, refresh_token=new_refresh)

@router.get("/me")
def me(session: Session = Depends(get_session), authorization: str = Header(None)):
    user = current_user(session, authorization)
    companies = session.exec(select(UserCompany).where(UserCompany.user_id==user.id)).all()
    return {"id": user.id, "email": user.email, "full_name": user.full_name,
            "companies":[{"company_id": uc.company_id, "role": uc.role} for uc in companies]}

@router.post("/request-reset")
def request_reset(payload: ResetRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email==payload.email)).first()
    if not user: return {"ok": True}
    token = secrets.token_urlsafe(24)
    rt = ResetToken(user_id=user.id, token=token, expires_at=datetime.utcnow()+timedelta(hours=1))
    session.add(rt); session.commit()
    send_mail(user.email, "Şifre sıfırlama", f"Token: {token}")
    return {"ok": True}

@router.post("/reset")
def do_reset(payload: DoReset, session: Session = Depends(get_session)):
    rt = session.exec(select(ResetToken).where(ResetToken.token==payload.token)).first()
    if not rt or rt.expires_at < datetime.utcnow(): raise HTTPException(400, "Invalid token")
    user = session.get(User, rt.user_id); from passlib.context import CryptContext; pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user.hashed_password = pwd.hash(payload.new_password); session.add(user); session.commit()
    return {"ok": True}

@router.post("/invite")
def create_invite(email: str, company_id: int, role: str = "viewer", session: Session = Depends(get_session), authorization: str = Header(None)):
    user = current_user(session, authorization)
    uc = session.exec(select(UserCompany).where(UserCompany.user_id==user.id, UserCompany.company_id==company_id)).first()
    if not uc or uc.role != "admin": raise HTTPException(403, "Only admin can invite")
    token = secrets.token_urlsafe(24)
    it = InviteToken(email=email, company_id=company_id, role=role, token=token, expires_at=datetime.utcnow()+timedelta(days=3))
    session.add(it); session.commit()
    send_mail(email, "FISCUS AI davet", f"Davet token: {token}")
    return {"ok": True}

@router.post("/invite/accept")
def accept_invite(email: str, token: str, session: Session = Depends(get_session)):
    it = session.exec(select(InviteToken).where(InviteToken.email==email, InviteToken.token==token)).first()
    if not it or it.expires_at < datetime.utcnow(): raise HTTPException(400, "Invalid invite")
    user = session.exec(select(User).where(User.email==email)).first()
    if not user: raise HTTPException(400, "Kayıtlı kullanıcı bulunamadı (önce hesap oluşturun)")
    session.add(UserCompany(user_id=user.id, company_id=it.company_id, role=it.role)); session.commit()
    return {"ok": True}
