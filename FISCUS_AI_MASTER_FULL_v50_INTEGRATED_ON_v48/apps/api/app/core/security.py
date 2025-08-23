from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Header
from sqlmodel import Session, select
from .config import settings
from ..models.user import User
from ..models.company import Company, UserCompany

def create_token(subject: str, expires_delta: timedelta):
    to_encode = {"sub": subject, "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str) -> Optional[str]:
    try:
        data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        return data.get("sub")
    except Exception:
        return None

def current_user(session: Session, authorization: Optional[str]) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Unauthorized")
    token = authorization.split(" ",1)[1]
    sub = decode_token(token)
    if not sub:
        raise HTTPException(401, "Invalid token")
    user = session.get(User, int(sub))
    if not user or not user.is_active:
        raise HTTPException(401, "User not active")
    return user

def require_company(session: Session, user: User, x_company_id: Optional[int]):
    if not x_company_id:
        raise HTTPException(400, "X-Company-Id header is required")
    rel = session.exec(select(UserCompany).where(UserCompany.user_id==user.id, UserCompany.company_id==x_company_id)).first()
    if not rel:
        raise HTTPException(403, "User has no access to this company")
    return session.get(Company, x_company_id), rel.role
