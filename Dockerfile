# syntax=docker/dockerfile:1

############################
# Stage 1: Frontend build #
############################
FROM node:20-alpine AS fe
WORKDIR /fe

# Frontend paketlerini önce kopyala (cache için)
# (Path'i kendi repo yapına göre ayarladım)
COPY FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api/frontend/package*.json ./
RUN npm ci

# Kaynakları kopyala ve build et
COPY FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api/frontend/ ./
RUN npm run build
# Vite/React çıktısı: /fe/dist
# (CRA kullanıyorsan çıktı /fe/build olur; altta kopyalama satırını değiştirirsin)

#########################
# Stage 2: Python back  #
#########################
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

# Gunicorn konfigürasyon dosyasını da kopyala
COPY gunicorn.conf.py ./gunicorn.conf.py

# Frontend build çıktısını backend'in beklediği yere koy
# (main.py, '.../apps/api/frontend/dist' klasörünü serve ediyor)
COPY --from=fe /fe/dist \
  /app/FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api/frontend/dist
# CRA kullanıyorsan bunun yerine:
# COPY --from=fe /fe/build \
#   /app/FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api/frontend/build

# import yolları için paket köklerini PYTHONPATH'e ekle
ENV PYTHONPATH=/app:/app/FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48:/app/FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api

# Render, PORT env'i atar; gunicorn.conf.py dosyanda bind= "0.0.0.0:$PORT" olduğundan emin ol.
# UvicornWorker kullanarak FastAPI app'ini çalıştır:
CMD ["sh","-c","gunicorn --config gunicorn.conf.py app.main:app"]
