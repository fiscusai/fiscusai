import os

# Render otomatik bir PORT sağlar, onu al, yoksa localde 8000 kullan
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"

# FastAPI / Starlette için uygun worker
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 2

# Loglar console'a gider (Render'da görünür)
loglevel = "info"
accesslog = "-"
errorlog = "-"
capture_output = True

# Performans ve stabilite
max_requests = 1000
max_requests_jitter = 200
preload_app = True

# Proxy ayarları (Render CDN'den gelen IP'yi algılar)
proxy_protocol = True
forwarded_allow_ips = "*"
