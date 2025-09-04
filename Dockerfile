# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# OpenCV/PyTorch ve benzeri için gerekli kütüphaneler
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 libgl1 build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python bağımlılıkları
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY . .

# FastAPI app'inin statiklerini nerede arayacağını belirt (main.py bunu okuyor)
# Senin repo yapına göre bu varsayılan doğru: /app/apps/api/web/public
ENV FRONTEND_ROOT=/app/apps/api/web/public

# (İsteğe bağlı) PYTHONPATH: genellikle gerekmez; istersen aç.
# ENV PYTHONPATH=/app

# -------------------------------------------------------------------
# (Opsiyonel) Frontend build gerekiyorsa multi-stage tercih et:
# 
# FROM node:20 as webbuild
# WORKDIR /src
# COPY apps/api/web/package.json apps/api/web/package-lock.json ./ 
# RUN npm ci
# COPY apps/api/web ./ 
# RUN npm run build
# 
# # Üstteki Python imajına dönüp build çıktısını kopyalarsın:
# COPY --from=webbuild /src/dist /app/apps/api/web/public
# -------------------------------------------------------------------

# Render, konteynere PORT verir; gunicorn bunu dinlemeli.
# JSON formunda env değişkenleri genişlemez; bu yüzden sh -c kullanıyoruz.
CMD ["sh", "-c", "gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:${PORT:-10000} --timeout 120"]
