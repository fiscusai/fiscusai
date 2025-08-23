from fastapi import FastAPI
from app.routers import reports_export
from app.routers import auth_lifecycle
from fastapi.middleware.cors import CORSMiddleware
from importlib import import_module
from app.metrics import PrometheusMiddleware, metrics
import pkgutil
import os
from app.security.middleware import AuthContextMiddleware
from app.security.headers import SecurityHeadersMiddleware

# Optional middlewares
try:
    from app.security.rate_limit import RateLimitMiddleware  # type: ignore
except Exception:  # pragma: no cover
    RateLimitMiddleware = None  # type: ignore

# --- Sentry (opsiyonel) ---
try:
    import sentry_sdk  # type: ignore
    dsn = os.getenv("SENTRY_DSN", "")
    if dsn:
        sentry_sdk.init(dsn=dsn, traces_sample_rate=float(os.getenv("SENTRY_TRACES", "0.1")))
except Exception:
    pass

app = FastAPI
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:3000','http://127.0.0.1:3000'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])(title="FISCUS AI API", version=os.getenv("APP_VERSION", "0.1.0"))
app.add_middleware(SecurityHeadersMiddleware)
if RateLimitMiddleware:
    app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthContextMiddleware)
app.add_middleware(PrometheusMiddleware)

# CORS
allow_origins = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limit (if available)
if RateLimitMiddleware:
    app.add_middleware(RateLimitMiddleware)

# Health endpoint
@app.get("/health")
def health():
    return {"ok": True}

# Auto-discover and register routers from app.routers.* modules
def _include_all_routers():
    pkg_name = "app.routers"
    try:
        pkg = import_module(pkg_name)
    except Exception as e:  # pragma: no cover
        return

    for modinfo in pkgutil.iter_modules(pkg.__path__):  # type: ignore[attr-defined]
        name = modinfo.name
        if name.startswith("_"):
            continue
        try:
            mod = import_module(f"{pkg_name}.{name}")
            router = getattr(mod, "router", None)
            if router is not None:
                app.include_router(router)
        except Exception:
            # If a router fails to import, skip it to keep API booting
            continue

_include_all_routers()

# Root
@app.get("/")
def root():
    return {"service": "FISCUS AI API"}

@app.get("/live")
def live():
    return {"ok": True}

@app.get("/ready")
def ready():
    from app.utils_health import health_snapshot
    snap = health_snapshot()
    ready = (snap.get("db") == "up" and snap.get("s3") in ("up","unknown"))
    return {"ready": ready, **snap}


@app.get('/metrics')
async def metrics_route(request):
    return await metrics(request)


@app.get("/debug-sentry")
def debug_sentry():
    # Bu endpoint, Sentry yakalamasını test etmek için kasıtlı bir hata fırlatır.
    raise RuntimeError("Sentry test: deliberate error")

app.include_router(admin.router)

app.include_router(admin_audit.router)

app.include_router(admin_users.router)

app.include_router(auth_lifecycle.router)

app.include_router(reports_export.router)

from app.routers import auth
app.include_router(auth.router)


from fastapi.middleware.cors import CORSMiddleware
from app.metrics import instrument, router as metrics_router

try:
    app
except NameError:
    from fastapi import FastAPI
    app = FastAPI(title="FISCUS AI API")

# CORS for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:3000","http://localhost:8080","http://localhost:5500","http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers (basic)
@app.middleware("http")
async def security_headers(request, call_next):
    resp = await call_next(request)
    resp.headers.setdefault("X-Content-Type-Options","nosniff")
    resp.headers.setdefault("X-Frame-Options","DENY")
    resp.headers.setdefault("Referrer-Policy","strict-origin-when-cross-origin")
    resp.headers.setdefault("X-XSS-Protection","1; mode=block")
    # CSP is tricky in APIs; omit or tune per route as needed
    return resp

instrument(app)
app.include_router(metrics_router)
