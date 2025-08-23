from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

DEFAULT_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}

# Basit bir CSP (geliştirme için gevşek, üretimde sıkılaştırın)
CSP = "default-src 'self'; img-src 'self' data: blob:; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self' *"

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        resp: Response = await call_next(request)
        for k, v in DEFAULT_HEADERS.items():
            resp.headers.setdefault(k, v)
        resp.headers.setdefault("Content-Security-Policy", CSP)
        return resp
