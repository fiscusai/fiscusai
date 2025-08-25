# gunicorn.conf.py
import os

# Render'ın otomatik sağladığı PORT
port = os.environ.get("PORT", 10000)
bind = f"0.0.0.0:{port}"

# FastAPI için optimize worker ayarları
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 2

# Loglama
loglevel = "info"
accesslog = "-"
errorlog = "-"
capture_output = True

# Performans ve stabilite
max_requests = 1000
max_requests_jitter = 200
preload_app = True

# FastAPI için özel ayarlar
proxy_protocol = True
forwarded_allow_ips = "*"