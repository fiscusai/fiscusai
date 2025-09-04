import os
import pkgutil
from importlib import import_module
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

# --- App içi RELATIVE importlar (absolute `from app...` KULLANMA) ---
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

# === FastAPI APP (doğru initialization) ===
app = FastAPI(title="FISCUS AI API", version=os.getenv("APP_VERSION", "0.1.0"))

# --- Middlewares ---
# Güvenlik başlıkları
app.add_middleware(SecurityHeadersMiddleware)

# Auth context
app.add_middleware(AuthContextMiddleware)

# Prometheus
app.add_middleware(PrometheusMiddleware)

# Rate limit (varsa)
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

# -------------------------------------------------------------------
# Frontend discovery & static serve (EKLENDİ)
# -------------------------------------------------------------------
def _first_existing(paths):
    for p in paths:
        if isinstance(p, Path) and p.exists():
            return p
    return None

# Bu dosyanın konumu: .../apps/api/app/main.py
_API_DIR = Path(__file__).resolve().parent.parent  # .../apps/api
# ENV ile frontend kökü override edilebilir
_env_frontend = os.getenv("FRONTEND_ROOT", "").strip()
_candidates = [
    Path(_env_frontend).resolve() if _env_frontend else None,
    _API_DIR / "web" / "public",
    _API_DIR / "web" / "dist",
    _API_DIR / "web" / "build",
    _API_DIR / "web" / "out",
]
_FRONTEND_ROOT = _first_existing([c for c in _candidates if c])

# Statik klasörleri (varsa) mount et
if _FRONTEND_ROOT:
    # Vite/Next export’ların çoğu /assets veya /_next/static benzeri üretir
    assets_candidates = [
        _FRONTEND_ROOT / "assets",
        _FRONTEND_ROOT / "_next" / "static",
        _FRONTEND_ROOT / "static",
    ]
    _ASSETS_DIR = _first_existing(assets_candidates)
    if _ASSETS_DIR:
        # /assets veya /static altında servis et
        if _ASSETS_DIR.name == "assets":
            app.mount("/assets", StaticFiles(directory=str(_ASSETS_DIR)), name="assets")
        elif _ASSETS_DIR.name == "static":
            app.mount("/static", StaticFiles(directory=str(_ASSETS_DIR)), name="static")
        else:
            # NextJS _next/static
            app.mount("/_next/static", StaticFiles(directory=str(_ASSETS_DIR)), name="_next_static")

    # public içindeki diğer dosyalar için gerekirse ek mount
    # Örn: /images, /fonts vb. (otomatik değil; ihtiyaç olursa ekle)

# Favicon
_FAVICON_CANDIDATES = [
    (_FRONTEND_ROOT / "favicon.ico") if _FRONTEND_ROOT else None,
    _API_DIR / "web" / "public" / "favicon.ico",
    _API_DIR.parent / "favicon.ico",  # .../apps/favicon.ico (yedek)
]
_FAVICON = _first_existing([p for p in _FAVICON_CANDIDATES if p])

@app.get("/favicon.ico")
def favicon():
    if _FAVICON:
        return FileResponse(str(_FAVICON))
    return JSONResponse({"detail": "favicon not found"}, status_code=404)

# -------------------------------------------------------------------
# Health endpoints
# -------------------------------------------------------------------
@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"ok": True}

@app.api_route("/live", methods=["GET", "HEAD"])
def live():
    return {"ok": True}

@app.api_route("/ready", methods=["GET", "HEAD"])
def ready():
    try:
        from .utils_health import health_snapshot  # relative import
        snap = health_snapshot()
        is_ready = (snap.get("db") == "up" and snap.get("s3") in ("up", "unknown"))
        return {"ready": is_ready, **snap}
    except Exception:
        # utils_health yoksa en azından "up" dön
        return {"ready": True}

# Render/monitor’lar için kısa healthz
@app.api_route("/healthz", methods=["GET", "HEAD"])
def healthz():
    return {"status": "ok"}

# --- Prometheus metrics ---
@app.get("/metrics")
async def metrics_route(request):
    return await metrics(request)

# --- (Opsiyonel) Sentry test endpoint'i ---
@app.get("/debug-sentry")
def debug_sentry():
    raise RuntimeError("Sentry test: deliberate error")

# --- Router auto-discovery: .routers altındaki tüm modülleri tara ve ekle ---
def _include_all_routers():
    # Bu dosya 'app' paketinde olduğundan __package__ -> "app"
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
            # Bir router importu patlarsa uygulama yine de boot etsin
            continue

_include_all_routers()

# --- Metrics helper (varsa) ---
try:
    instrument(app)
    app.include_router(metrics_router)
except Exception:
    pass

# -------------------------------------------------------------------
# Root (index.html varsa UI’ı döner; yoksa eski JSON cevabı döner)
# -------------------------------------------------------------------
def _find_index_html():
    if not _FRONTEND_ROOT:
        return None
    # En olası isimler: index.html kökte ya da out/dist/build altında
    candidates = [
        _FRONTEND_ROOT / "index.html",
        _FRONTEND_ROOT,  # direkt klasör path’i verilmiş olabilir (örn. out)
    ]
    for p in candidates:
        if p.is_file() and p.name.endswith(".html"):
            return p
        if p.is_dir() and (p / "index.html").exists():
            return p / "index.html"
    return None

_INDEX_HTML = _find_index_html()

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    # index.html bulunmuşsa UI’ı döndür
    if _INDEX_HTML and _INDEX_HTML.exists():
        return HTMLResponse(_INDEX_HTML.read_text(encoding="utf-8"))
    # Aksi halde mevcut davranışı koru (JSON)
    return {"service": "FISCUS AI API"}
