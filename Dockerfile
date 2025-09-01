# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 libgl1 build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Bağımlılıklar
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Uygulama
COPY . .

# (İsteğe bağlı) PYTHONPATH; gerek yoksa sade bırak
# ENV PYTHONPATH=/app

# Health endpoint'in olduğundan emin ol (/ veya /health)
# Gunicorn’u exec formda çalıştır
CMD ["gunicorn", "-c", "gunicorn.conf.py", "server:app"]
