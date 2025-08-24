# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# OpenCV/PyTorch için gerekli sistem paketleri
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 libgl1 build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- Bağımlılıkları kur ---
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Uygulama dosyaları ---
COPY . .

# import yolları için paket köklerini PYTHONPATH'e ekle
ENV PYTHONPATH=/app:/app/FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48:/app/FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api

# Render PORT'u env olarak enjekte ediyor; shell expansion için sh -c kullan
CMD ["sh","-c","gunicorn -k uvicorn.workers.UvicornWorker server:app --bind 0.0.0.0:${PORT:-8000} --log-level info"]
