from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from typing import Optional
import os, jwt

JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")

def _parse_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except Exception:
        return {}

class AuthContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Defaults
        role: Optional[str] = None
        org: Optional[str] = None

        # Try Bearer token
        auth = request.headers.get("authorization") or request.headers.get("Authorization")
        if auth and auth.lower().startswith("bearer "):
            token = auth.split(" ", 1)[1].strip()
            claims = _parse_jwt(token)
            role = claims.get("role") or role
            org = claims.get("org") or org

        # Fallback headers
        role = role or request.headers.get("X-User-Role")
        org = org or request.headers.get("X-Org")

        # Attach to request.state
        request.state.role = role
        request.state.org = org

        response = await call_next(request)
        return response
