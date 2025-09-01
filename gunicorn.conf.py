import os

port = os.environ.get("PORT", "8000")  # Render verir, local fallback
bind = f"0.0.0.0:{port}"

workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 2

loglevel = "info"
accesslog = "-"
errorlog = "-"
capture_output = True

max_requests = 1000
max_requests_jitter = 200
preload_app = False  # başlangıçta hızlı açsın

# Render'da proxy_protocol gereksiz; kapalı kalsın
# proxy_protocol = True
forwarded_allow_ips = "*"
