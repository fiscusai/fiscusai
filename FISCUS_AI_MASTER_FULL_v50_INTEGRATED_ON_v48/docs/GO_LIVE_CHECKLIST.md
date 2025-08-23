# FISCUS AI — Go‑Live Checklist (v46)
Tarih: 2025-08-09T12:17:50.837032Z

## 1) Ortam & Gizli Anahtarlar
- [ ] `.env.production` dolduruldu (API, Web, DB, S3, Mail, Sentry, Stripe/Iyzi, RateLimit, AV, CSP).
- [ ] Production `DATABASE_URL` (Postgres), `REDIS_URL` ve TLS hazır.
- [ ] `S3_*` + `S3_PUBLIC_BASE_URL` (CDN/CloudFront) aktif.
- [ ] `JWT_SECRET`, `ENCRYPTION_KEY` **env** veya secret store (KMS/SM/HashiCorp) üzerinden.

## 2) Güvenlik
- [ ] CSP **enforce** (gerekli domainler allowlist).
- [ ] Rate limit (webhook/dış uçlar) aktif.
- [ ] RLS etkin ve migrasyonlar `alembic upgrade head` ile işlendi.
- [ ] 2FA (admin zorunlu), parola politikası, şüpheli oturum uyarıları.
- [ ] AV (ClamAV) / S3 event AV Lambda etkin; karantina bucket ve tag'ler.
- [ ] WAF kuralları uygulanmış (IP allowlist opsiyonel).

## 3) Uygulama Sağlığı
- [ ] `/health`, `/health/deep` OK.
- [ ] Worker/Scheduler health, queue depth ve son job başarı oranı ölçülüyor.
- [ ] Log rotasyonu ve Sentry DSN aktif.

## 4) İzleme & Uyarılar
- [ ] Prometheus scrape ⇒ Grafana dashboard (API latency, 5xx, RPS, queue).
- [ ] Alert rules (p95 latency, 5xx oranı, 429 spike, DB bağlantı hatası).
- [ ] CSP raporları panelinde anomali yok.

## 5) Veri & Yedekleme
- [ ] Postgres günlük yedek (full + WAL), şifreli saklama.
- [ ] S3 lifecycle (infrequent access + silme politikaları).
- [ ] Şifreli secrets ve erişim denetimi (least privilege).

## 6) Dağıtım
- [ ] Blue/Green veya Canary planı (checks + otomatik geri dönüş).
- [ ] Smoke testler (aşağıdaki E2E) yeşil.
- [ ] Sürüm etiketi ve RELEASE_NOTES yayınlandı.

## 7) Hukuki & Uyumluluk
- [ ] KVKK/Aydınlatma, KVKK envanteri (kişisel veri, retention, imha politikası).
- [ ] Çerez politikası ve gizlilik metni güncel.
- [ ] Sözleşmeler (KVKK, veri işleyen, tedarikçi).

---

### Smoke Test Senaryoları
- Auth: register → verify → login.
- Invoice: create → list → PDF export.
- Payments: Stripe webhook imza doğrulama.
- Bank import: MT940/CAMT önizleme.
- E‑Fatura: UBL‑TR XML üretimi ve XSD doğrulaması.
- Audit: event düşme ve CSV indir.
- Flags: admin → toggle → persist.
