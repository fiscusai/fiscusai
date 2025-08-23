from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

SEC_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        resp: Response = await call_next(request)
        for k, v in SEC_HEADERS.items():
            resp.headers.setdefault(k, v)
        return resp

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import os
from datetime import datetime, timezone

bearer_scheme = HTTPBearer(auto_error=False)

def require_role(*roles):
    def _dep(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")
        token = credentials.credentials
        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRET","dev-secret"), algorithms=["HS256"])
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        role = payload.get("role","user")
        if roles and role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return payload
    return _dep



from fastapi import Request
import os

async def ip_allowlist_middleware(request: Request, call_next):
    allow = os.getenv("ALLOW_IPS", "")
    if not allow:
        return await call_next(request)
    allowed = {ip.strip() for ip in allow.split(",") if ip.strip()}
    client_ip = request.client.host if request.client else ""
    if client_ip and client_ip not in allowed:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=403, content={"detail":"IP not allowed"})
    return await call_next(request)


def is_2fa_verified(user: dict) -> bool:
    return bool(user.get('twofa_verified', False))
