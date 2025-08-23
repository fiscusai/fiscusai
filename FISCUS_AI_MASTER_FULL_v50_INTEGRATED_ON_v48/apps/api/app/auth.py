import os, time
from typing import Optional
from passlib.context import CryptContext
import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_EXPIRE = int(os.getenv("JWT_EXPIRE_SECONDS", "86400"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(sub: str) -> str:
    payload = {"sub": sub, "iat": int(time.time()), "exp": int(time.time()) + JWT_EXPIRE}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return str(payload.get("sub"))
    except Exception:
        return None
