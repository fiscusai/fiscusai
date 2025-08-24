from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from importlib import import_module
import pkgutil
import os

# --- App içi relative importlar (absolute 'from app...' yerine) ---
from .metrics import PrometheusMiddleware, metrics, instrument, router as metrics_router
from .security.middleware import AuthContextMiddleware
from .security.headers import SecurityHeadersMiddleware

# İsteğe bağlı rate limit middleware (varsa)
try:
    from .security.rate_limit import RateLimitMiddleware  # type: ignore
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

# === FastAPI app ===
app = FastAPI(title="FISCUS AI API", version=os.getenv("APP_VERSION", "0.1.0"))

# --- Middlewares ---
# Güvenlik başlıkları
app.add_middleware(SecurityHeadersMiddleware)

# Rate limit (varsa)
if RateLimitMiddleware:
    app.add_middleware(RateLimitMiddleware)

# Auth context
app.add_middleware(AuthContextMiddleware)

# Prometheus
app.add_middleware(PrometheusMiddleware)

# CORS (ENV üzerinden liste al)
allow_origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allow_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health endpoints ---
@app.get("/health")
def health():
    return {"ok": True}

@app.get("/live")
def live():
    return {"ok": True}

@app.get("/ready")
def ready():
    try:
        from .utils_health import health_snapshot  # relative import
        snap = health_snapshot()
        is_ready = (snap.get("db") == "up" and snap.get("s3") in ("up", "unknown"))
        return {"ready": is_ready, **snap}
    except Exception:
        # utils_health yoksa en azından "up" ver
        return {"ready": True}

# --- Prometheus metrics ---
@app.get("/metrics")
async def metrics_route(request):
    return await metrics(request)

# --- (Opsiyonel) debug sentry ---
@app.get("/debug-sentry")
def debug_sentry():
    raise RuntimeError("Sentry test: deliberate error")

# --- Router auto-discovery: .routers altındaki tüm modülleri tara ---
def _include_all_routers():
    pkg_name = __package__ + ".routers"  # "app.routers"
    try:
        pkg = import_module(pkg_name)
    except Exception:
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
            # Router importu patlarsa API boot etmeye devam etsin
            continue

_include_all_routers()

# --- Metrics helper (opsiyonel) ---
try:
    instrument(app)
    app.include_router(metrics_router)
except Exception:
    pass

# Root
@app.get("/")
def root():
    return {"service": "FISCUS AI API"}
