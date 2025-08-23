# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1

# OpenCV/torch vs. için sistem paketleri
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 libgl1 build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) Gereksinimler
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 2) Uygulama
COPY . .

# 3) (Opsiyonel) import kolaylığı
# ... (üst kısım aynı)
ENV PYTHONPATH=/app

CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker server:app --bind 0.0.0.0:${PORT:-8000} --log-level info"]

