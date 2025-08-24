# FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api/app/main.py

import os
import pkgutil
from importlib import import_module
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- App içi RELATIVE importlar ---
from .metrics import PrometheusMiddleware, metrics, instrument, router as metrics_router
from .security.middleware import AuthContextMiddleware
from .security.headers import SecurityHeadersMiddleware

# İsteğe bağlı rate limit (yoksa app yine boot eder)
try:
    from .security.rate_limit import RateLimitMiddleware  # type: ignore
except Exception:  # pragma: no cover
    RateLimitMiddleware = None  # type: ignore

# --- Sentry (opsiyonel) ---
try:
    import sentry_sdk  # type: ignore
    _dsn = os.getenv("SENTRY_DSN", "")
    if _dsn:
        sentry_sdk.init(dsn=_dsn, traces_sample_rate=float(os.getenv("SENTRY_TRACES", "0.1")))
except Exception:
    pass

# === Ana FastAPI (statik + /api sub-app) ===
app = FastAPI(title="FISCUS AI", version=os.getenv("APP_VERSION", "0.1.0"))

# --- Middlewares (ana app'e ekliyoruz; sub-app de bunlardan faydalanır) ---
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuthContextMiddleware)
app.add_middleware(PrometheusMiddleware)
if RateLimitMiddleware:
    app.add_middleware(RateLimitMiddleware)

# CORS (ENV'den liste al; virgülle ayrılmış)
_allow_origins = os.getenv(
    "CORS_ALLOW_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _allow_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === API için ayrı bir sub-app oluştur (tüm API /api altında) ===
api_app = FastAPI(title="FISCUS AI API", version=os.getenv("APP_VERSION", "0.1.0"))

# --- Health endpoints (/api/health, /api/live, /api/ready) ---
@api_app.get("/health")
def health():
    return {"ok": True}

@api_app.get("/live")
def live():
    return {"ok": True}

@api_app.get("/ready")
def ready():
    try:
        from .utils_health import health_snapshot  # relative import
        snap = health_snapshot()
        is_ready = (snap.get("db") == "up" and snap.get("s3") in ("up", "unknown"))
        return {"ready": is_ready, **snap}
    except Exception:
        return {"ready": True}

# --- Prometheus metrics (/api/metrics) ---
@api_app.get("/metrics")
async def metrics_route(request):
    return await metrics(request)

# --- (Opsiyonel) Sentry test ---
@api_app.get("/debug-sentry")
def debug_sentry():
    raise RuntimeError("Sentry test: deliberate error")

# --- Router auto-discovery: .routers altındaki tüm modülleri /api'ye ekle ---
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
                api_app.include_router(router)  # <-- sub-app'e ekliyoruz
        except Exception:
            continue

_include_all_routers()

# --- Metrics helper (varsa) ---
try:
    instrument(api_app)                # <-- sub-app'i enstrümanla
    api_app.include_router(metrics_router)
except Exception:
    pass

# --- Frontend build'ini kökten servis et ---
# Vite/React için "frontend/dist", CRA için "frontend/build"
FRONTEND_DIR = (
    Path(__file__).resolve().parent.parent / "frontend" / "dist"
)
if not FRONTEND_DIR.exists():
    # CRA alternatifi:
    alt = Path(__file__).resolve().parent.parent / "frontend" / "build"
    if alt.exists():
        FRONTEND_DIR = alt

if FRONTEND_DIR.exists():
    # html=True => SPA yönlendirmeleri index.html'e düşer
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    # Frontend yoksa kökte kısa bir bilgi döndür
    @app.get("/")
    def root_info():
        return {
            "service": "FISCUS AI",
            "info": f"Frontend build bulunamadı: {FRONTEND_DIR}"
        }

# --- API sub-app'i mount et ---
app.mount("/api", api_app)
