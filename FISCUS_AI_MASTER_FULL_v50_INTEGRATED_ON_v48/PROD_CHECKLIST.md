# FISCUS AI — Prod Checklist

## Güvenlik
- [ ] `JWT_SECRET` güçlü ve döndürülmüş
- [ ] `CORS_ORIGINS` prod domainleri ile sınırlı
- [ ] `SECURITY_HEADERS` ve `CSP` aktif
- [ ] Rate limiting açık, loglarda PII maskeleme
- [ ] Sentry DSN ayarlı (hata takip)

## Altyapı
- [ ] Web → Vercel (env: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_PLAUSIBLE_DOMAIN`)
- [ ] API → Render/Container (env: DB, S3, Sentry)
- [ ] S3/CloudFront public URL stratejisi ayarlı (`S3_PUBLIC_BASE_URL`)
- [ ] DB yedekleme & geri yükleme planı

## Performans
- [ ] Lighthouse >= 90 (Performance/SEO/Accessibility/Best Practices)
- [ ] ISR revalidate süreleri kontrol
- [ ] Görsel optimizasyonu (AVIF/WebP), font subset

## Gözlemleme
- [ ] Sentry issues panelinde test hata görünür
- [ ] Uptime monitor (ping) ekli
- [ ] Log rotasyonu ve log forward

## Hukuki
- [ ] KVKK/Gizlilik/Çerez sayfaları dolu
- [ ] Çerez izin yöneticisi
- [ ] Kullanım şartları & Mesafeli satış (varsa)

## Dağıtım
- [ ] Alembic `upgrade head` uygulandı
- [ ] Versiyon/Tag ve CHANGELOG güncellendi
- [ ] Ortam değişkenleri .env (secret manager) ile yönetiliyor
