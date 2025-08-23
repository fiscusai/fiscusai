# syntax=docker/dockerfile:1
FROM python:3.11-alpine AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apk add --no-cache build-base
WORKDIR /app

# Install deps
COPY ../../requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy app
COPY ./app /app/app

# Create non-root user
RUN addgroup -S app && adduser -S app -G app
USER app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
