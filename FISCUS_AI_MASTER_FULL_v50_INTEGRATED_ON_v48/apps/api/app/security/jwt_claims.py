import os
from typing import Optional, Tuple
from fastapi import Request
import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

def extract_role_org_from_jwt(auth_header: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    if not auth_header or not auth_header.lower().startswith("bearer "):
        return None, None
    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return payload.get("role"), payload.get("org")
    except Exception:
        return None, None

async def claims_middleware(request: Request, call_next):
    role = None
    org = None
    # Prefer JWT
    auth = request.headers.get("Authorization")
    role, org = extract_role_org_from_jwt(auth)
    # Fallback to headers for local/dev
    role = role or request.headers.get("X-User-Role")
    org = org or request.headers.get("X-Org")
    request.state.role = role
    request.state.org = org
    response = await call_next(request)
    return response
