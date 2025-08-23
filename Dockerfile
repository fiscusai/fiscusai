# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1

# OpenCV/torch vs. için sistem paketleri
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 libgl1 build-essential && \
    rm -rf /var/lib/apt/lists/*

# ... (üst kısım aynı)
WORKDIR /app
# ...
COPY . .

# *** BURAYI GÜNCELLE ***
# Hem kökü (/app), hem proje kökünü, hem de apps/api'yi ekliyoruz
ENV PYTHONPATH=/app:/app/FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48:/app/FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api

CMD ["sh","-c","gunicorn -k uvicorn.workers.UvicornWorker server:app --bind 0.0.0.0:${PORT:-8000} --log-level info"]

