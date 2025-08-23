# FISCUS AI — Production Runbook

Bu belge, prod ortamında olay yönetimi, bakım ve rutin operasyonlar için hızlı rehberdir.

## 1) Olay (Incident) Yönetimi
- **Kim bildirir?** Sentry uyarıları, Uptime pingi, müşteri destek bileti.
- **Önceliklendirme:** P1 (kritik), P2 (majör), P3 (minör).
- **İlk müdahale:** Status sayfasına olay gir, log/kibana kontrol et, rollback gerekiyorsa son tag'e dön.
- **İletişim:** Status page + e-posta şablonu (template/email-incident.md).

## 2) Yedekleme & Geri Yükleme
- **PostgreSQL:** Günlük dump (7 gün saklama), haftalık tam yedek.
- **S3:** Versiyonlama + lifecycle (30/90 gün).
- **Tatbikat:** Çeyreklik geri yükleme testi (runbook'a sonuç ekle).

## 3) Güvenlik
- **Rotating secrets:** S3, DB, JWT anahtarları 90 günde bir.
- **Erişim:** En az ayrıcalık (IAM), IP allowlist, 2FA.
- **CSP/CORS:** Production domainleri dışında kapalı.

## 4) Ölçümleme & Gözlemleme
- **Sentry:** Hata trendleri, release tag ile ilişkilendirme.
- **Metrics:** Uptime, latency, 95p response time, error rate.
- **Log rotasyonu:** 5x5MB; kritik olaylar için ayrı index.

## 5) Deploy & Rollback
- **CI/CD:** main → staging → prod; tag ile release.
- **Rollback:** Docker image tag geri al; DB migration rollback planlı.
- **Feature flags:** Riskli özellikleri bayrakla aç/kapat.

## 6) Check‑list (her release)
- [ ] ENV & secrets güncel
- [ ] DB migration'lar uygulandı
- [ ] Sentry DSN aktif
- [ ] CSP/CORS kontrollü
- [ ] Backup planı doğrulandı
- [ ] Status sayfası sürüm notu girdin
