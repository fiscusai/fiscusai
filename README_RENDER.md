# Render Deploy - FISCUS AI

Bu paket Render'a hazır hale getirilmiştir.

## İçerik
- `runtime.txt` → Python sürümü (3.11.9)
- `requirements.txt` → Gerekli paketler
- `Procfile` → Uygulama başlangıç komutu
- `render.yaml` → Web servisi + Redis servis tanımları
- (Varsa) mevcut FastAPI giriş noktası: FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api/app/main.py

## Render'da Deploy
1. Bu zip'i GitHub'a yükleyin.
2. Render'da **New +** → **Blueprint** → repo'yu seçin. (Yoksa Web Service de olur.)
3. Ortam değişkenlerini ayarlayın (SECRET_KEY, DATABASE_URL, vb.).
4. Deploy.
5. Health check: `/healthz`

> Not: Eğer kendi uygulama dosyanız farklıysa (örn. `app/main.py`), Procfile otomatik olarak FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48/apps/api/app/main.py'a ayarlanmıştır.


## Ortam Değişkenleri (Environment Variables)
Render üzerinde **Settings → Environment** kısmına eklenmelidir:

- `ALLOW_IPS`
- `APP_VERSION`
- `AV_ENABLED`
- `AV_REQUIRED`
- `CLAMD_HOST`
- `CLAMD_PORT`
- `CORS_ALLOW_ORIGINS`
- `DATABASE_URL`
- `FF_AI_PANEL`
- `FF_BILLING`
- `FF_RECON_RULES`
- `IYZICO_WEBHOOK_SECRET`
- `JWT_ALG`
- `JWT_EXPIRES`
- `JWT_EXPIRE_SECONDS`
- `JWT_REFRESH_EXPIRES`
- `JWT_SECRET`
- `LOG_DIR`
- `MAIL_FROM`
- `MAIL_OUT_DIR`
- `MAIL_PROVIDER`
- `PAYMENT_WEBHOOK_SECRET`
- `POSTMARK_TOKEN`
- `REDIS_RL`
- `REDIS_URL`
- `S3_ACCESS_KEY`
- `S3_BUCKET`
- `S3_ENDPOINT`
- `S3_PUBLIC_BASE_URL`
- `S3_REGION`
- `S3_SECRET_KEY`
- `SENTRY_DSN`
- `SENTRY_TRACES`
- `SES_REGION`
- `SMTP_HOST`
- `SMTP_PASS`
- `SMTP_PORT`
- `SMTP_SENDER`
- `SMTP_TLS`
- `SMTP_USER`
- `STRIPE_WEBHOOK_SECRET`
- `WEBHOOK_SECRET`
- `WORKER_HEARTBEAT`
