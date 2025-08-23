# FISCUS AI Monorepo

Modern + Roma temalı KOBİ muhasebe platformu.

## Uygulamalar
- **apps/web**: Next.js 14 + TailwindCSS
- **apps/api**: FastAPI + SQLAlchemy/SQLModel

## Geliştirme
### Web
```bash
cd apps/web
npm ci
npm run dev
```

### API
```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install -r ../../requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Env Dosyaları
- `apps/web/.env.example`
- `apps/api/.env.example`

## SEO
- `app/robots.ts`, `app/sitemap.ts`, `app/opengraph-image.tsx`

## Hukuki
- `app/legal/*` sayfaları: KVKK, Gizlilik, Çerez, Kullanım Şartları

## i18n
Basit mesaj tabanlı bir sözlük yapısı `apps/web/messages` altında.
`components/LanguageSwitcher.tsx` örneğini inceleyin.

## Lisans
Tüm hakları saklıdır.

## FISCUS AI — Quick Start

### Monorepo yapısı
- `apps/web`: Next.js (Landing, Features, Pricing, Auth sayfaları)
- `apps/api`: FastAPI (health endpoint'leri)

### Geliştirme
```bash
# API
cd apps/api
uvicorn app.main:app --reload

# WEB
cd ../web
npm install
npm run dev
```

Yerel geliştirme için `NEXT_PUBLIC_API_URL` tanımlamazsanız web uygulaması `/api/health-proxy` ile `http://localhost:8000/health`'e proxy eder.

### Deploy
- Render API: `render-api.yaml`
- Render Web: `render-web.yaml`
- Vercel Web: `apps/web/vercel.json`

### Test & CI
- `pytest` ile API smoke test'leri
- `ruff` ve `mypy` Python statik analiz
- `ESLint` ve `Prettier` web tarafı
- GitHub Actions workflow: `.github/workflows/ci.yml`

### Marka
- Renkler: Mermer #F2F2F0, Altın #C9A54A, Kırmızı #7A1F1F, Antrasit #2D2D2D, Zeytin #6E6B5E
- Tipografi: Başlık Cinzel, Metin Inter

## Deploy Rehberi (Kısa)

### Vercel (Web)
1. `apps/web` klasörünü Vercel'e bağla.
2. Build: `npm ci && npm run build`
3. Env: `NEXT_PUBLIC_API_URL=https://<render-api-host>`
4. Güvenlik başlıkları `next.config.js` içinde tanımlıdır (CSP dahil).

### Render (API)
1. Reponu Render'e bağla ve `render-api.yaml` seç.
2. Docker deploy otomatik çalışır (Alpine + non-root).
3. Env:
   - `JWT_SECRET`: oluştur (Render generate)
   - `CORS_ORIGINS`: `https://fiscus.ai,https://www.fiscus.ai` ve Vercel preview alan adların

### Yerel Çalıştırma
- API: `cd apps/api && uvicorn app.main:app --reload`
- Web: `cd apps/web && npm install && npm run dev`
- `.env`: `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`

### Pre-commit
- `npm run prepare` (web) → Husky kurulur.
- Commit öncesi `lint-staged` (web) ve `ruff` (root) otomatik koşar.


## Yüklemeler & Banka Import & AI Tahmin
- Dosya yükleme: POST `/uploads/` (form-data: `file`, ops: `invoice_id`) — Tipler: PDF/PNG/JPEG, limit 10MB.
- Banka import: POST `/bank/import` (CSV/JSON, header: `X-Token: dev-bank-token`).
- AI Forecast: GET `/ai/forecast?months=3` — lineer trend tahmini.
- Web sayfaları: `/bank/import` (banka yükleme), `/invoices` (dosya ekleme butonu), `/ai` (tahmin grafiği).

## Step 10 — Attachments, Reconciliation, AI Anomalies & Forecast

**API**
- `GET /attachments/{invoice_id}` — list invoice attachments
- `POST /attachments/{invoice_id}` — upload attachment (pdf/png/jpeg)
- `GET /attachments/file/{filename}` — download/preview attachment
- `GET /reconcile/preview` — preview heuristic invoice↔bank matches
- `POST /reconcile/apply` — apply matches and mark invoices `paid` (header: `X-Token: dev-bank-token`)
- `GET /ai_adv/anomalies` — outlier & duplicate detection
- `GET /ai_adv/cashflow_forecast?months=3` — simple linear forecast

**Web**
- Invoices: edit modal içinde **Ekler** paneli (yükleme + liste)
- Bank → Reconcile: eşleştirme önizleme & uygulama
- AI Paneli: anomaliler listesi + 3 aylık nakit akışı tahmin grafiği


## Step 13 Updates
- Admin-only **Settings** page (`/(main)/settings`)
- Polished **Invoice PDF** (currency formatting, footer notes, page footer)
- Reconciliation **rule engine**: `/reconcile/rules/preview` and `/reconcile/rules/apply`
- Design tokens (`styles/tokens.css`) and final OG SVGs (`public/images/og-*.svg`)


## Deploy Checklist (Final)

- [ ] Vercel (Web) bağlantısı ve `NEXT_PUBLIC_API_URL` ayarı
- [ ] Render (API) bağlantısı ve `CORS_ORIGINS` allowlist
- [ ] `JWT_SECRET` üretildi ve `.env`'e eklendi
- [ ] S3/MinIO endpoint ve bucket ayarlandı, `POST /s3/upload` test edildi
- [ ] PostgreSQL hazır ve `DATABASE_URL` güncellendi
- [ ] Alembic migration çalıştırıldı (opsiyonel)
- [ ] Plausible domain ayarlandı (opsiyonel)
- [ ] CI: ruff + pytest + eslint + build geçiyor
- [ ] KVKK/Gizlilik sayfaları yayınlandı



## Step 17 — Presigned Uploads + DB (SQLModel) + Reconcile Edit/Delete + Lighthouse

### S3/MinIO Presigned Upload
- API: `GET /s3/presign-upload?filename=FILENAME&content_type=...`
- Web: `/uploads` sayfasındaki demo ile dosyayı direkt S3/MinIO'ya yükleyin.

### DB (SQLModel) V2 Endpoint'leri
- API: `/v2/invoices`, `/v2/customers` (SQLModel + SQLite varsayılan)
- ENV ile `DATABASE_URL=postgresql+psycopg2://...` verdiğinizde otomatik PostgreSQL.
- Web: `/invoices_v2` sayfası V2'yi gösterir.

### Reconcile — Manuel Düzenleme & İptal
- API: `POST/PUT/DELETE /reconcile/manual` uçları
- Web: `/bank/reconcile` sayfası demo butonları

### Lighthouse İyileştirmeleri
- `next/image` kullanımı ve WebP yer tutucular
- `app/head.tsx` preconnect/dns-prefetch


## Production DB (PostgreSQL) Quickstart
1. Create DB and user:
   ```sql
   CREATE DATABASE fiscus;
   CREATE USER fiscus WITH PASSWORD 'your-strong-pass';
   GRANT ALL PRIVILEGES ON DATABASE fiscus TO fiscus;
   ```
2. Set env:
   ```bash
   export DATABASE_URL=postgresql+psycopg2://fiscus:your-strong-pass@your-host:5432/fiscus
   ```
3. Migrate:
   ```bash
   cd apps/api
   alembic -c alembic.ini upgrade head
   ```
4. Run API:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```


## Step 20
- V1 sayfaları V2'ye yönlendirildi (invoices/customers).
- S3 presign demo endpoint eklendi.
- Audit Log UI: /(main)/audit-log.
- Lighthouse için hero görseli next/image ile WebP.

---

## Public Upload URL (S3/CloudFront) Stratejisi

**Amaç:** Yüklenen dosyanın tarayıcıdan doğrudan, kalıcı ve güvenli şekilde görüntülenmesi.

1) **Bucket Politikası (public-read)** yerine **CloudFront** önerilir.  
2) API `GET /s3/presign-upload` yanıtında `public_url` alanı döner. Bu URL şuna göre hesaplanır:
   - `S3_PUBLIC_BASE_URL` env değişkeni **varsa**: `https://cdn.example.com/{key}`
   - Yoksa: `https://{bucket}.s3.{region}.amazonaws.com/{key}` (veya MinIO website endpoint)
3) Saklanacak meta:
   - `Content-Type`, `Content-Disposition` (isteğe bağlı inline/attachment)
4) **Örnek env:**
   ```env
   S3_REGION=eu-central-1
   S3_BUCKET=fiscus-prod
   S3_PUBLIC_BASE_URL=https://cdn.fiscus.ai
   ```
5) **Cache Policy:** CloudFront'ta `Cache-Control: public,max-age=31536000,immutable` (versiyonlama için dosya anahtarında hash kullanın).

### Güvenlik Notları
- Hassas dokümanları **public** yayımlamayın. Presigned GET URL'leri kısa TTL ile kullanın.
- Kişisel veriler için KVKK kapsamını ve erişim yetkisini doğrulayın.


## Production Runbook
Bkz: `PRODUCTION_RUNBOOK.md`


## Step 29 — RBAC, BI Email Job, Status Uptime
- RBAC (demo) header'ları: `X-User-Role: admin|accountant|user`, `X-Org: ORG-ALPHA`
- BI ZIP email job: `POST /bi/export/email?to=ops@fiscus.ai&from_date=2025-07-01&to_date=2025-08-01`
- Status: `/status/uptime`, `/status/worker`
- Web: `/settings/rbac` (izin matrisi), `/reports/bi-email` (zip'i maille)
- Mailhog ile test: SMTP host `localhost`, port `1025`


## Org & Role Enforcement (Step 31)
- V2 CRUD uçları artık X-Org/JWT claim ile zorunlu organizasyon filtresi kullanıyor.
- Yazma işlemleri için roller: admin/accountant; silme yalnızca admin.
- Web client POST/PUT çağrılarında `getAuthHeaders()` otomatik header ekler.


### Step 33 — Org & Role Enforcement (API) + Web Client Standardization
- All `/v2/invoices` and `/v2/customers` endpoints now enforce `organization_id` via `Depends(require_org)`
  and role checks via `Depends(require_role([...]))`.
- Web client POST/PUT/DELETE calls were migrated to `apiFetch()` which automatically injects
  `Authorization`, `X-User-Role`, and `X-Org` headers from `localStorage.fiscus_auth`.
- New tests: `apps/api/app/tests/test_v2_crud.py` verify update/delete and customers flows.


    ## STEP 42 — Payments & Bank Imports

    ### Stripe Webhook
    - Env: `STRIPE_WEBHOOK_SECRET`
    - Test:
      ```bash
      BODY='{"type":"checkout.session.completed"}'
      TS=$(date +%s)
      SIG=$(python - <<'PY'
import hmac,hashlib,os,time
sec=os.getenv("STRIPE_WEBHOOK_SECRET","whsec_dev")
body=b'{"type":"checkout.session.completed"}'
ts=str(int(time.time()))
s=hmac.new(sec.encode(), f"{ts}.{body.decode()}".encode(), hashlib.sha256).hexdigest()
print(f"t={ts}, v1={s}")
PY
)
      curl -X POST -H "Stripe-Signature: $SIG" -d "$BODY" http://127.0.0.1:8000/payments/stripe/webhook
      ```

    ### Iyzico Webhook
    - Env: `IYZICO_WEBHOOK_SECRET`
    - Test:
      ```bash
      BODY='{"status":"success"}'
SIG=$(python - <<'PY'
import hmac,hashlib,os
sec=os.getenv("IYZICO_WEBHOOK_SECRET","iyzi_dev")
body=b'{"status":"success"}'
print(hmac.new(sec.encode(), body, hashlib.sha1).hexdigest())
PY
)
      curl -X POST -H "X-IYZ-Signature: $SIG" -d "$BODY" http://127.0.0.1:8000/payments/iyzico/webhook
      ```

    ### Bank Imports
    - MT940: `POST /bank/import/mt940` (file: .mt940/.sta/.txt)
    - CAMT.053: `POST /bank/import/camt53` (file: .xml/.camt)
    - Web: `/bank/import_mt940` ve `/bank/import_camt53`


## Security Hardening (Step 44)
- **Antivirus (ClamAV):** `clamd` entegrasyonu; `AV_ENABLED=true`, `AV_REQUIRED=false`, `CLAMD_HOST=127.0.0.1`, `CLAMD_PORT=3310`
- **CSP enforce:** Next.js `headers()` ile katı CSP; ihlaller API `POST /csp-report` ile loglanır (`apps/api/app/data/csp_reports.jsonl`).
- **SBOM/Scan (dev):**
  ```bash
  pip install cyclonedx-bom pip-licenses
  cyclonedx-bom -o sbom.json
  pip-licenses --format=json --output-file=thirdparty-licenses.json
  ```
- **Docker Compose:** `clamav` servisi eklendi.


### Step 48 — Auto Reconcile
- API: `POST /reconcile/auto/run` (role: accountant|admin)
- Web: `/bank/auto-reconcile` demo sayfası
