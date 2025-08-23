# Incident Runbook (FISCUS AI)

## 1) Trafik Artışı / Hata Oranı
- **Grafana**: FISCUS API Overview dashboard → Error Rate / p95 Latency
- **Prometheus**: son 15dk `sum(rate(http_requests_total{status=~"5.."}[5m]))`
- **Eylem**: Canary weight'i 0'a çek (NGINX annotation `canary-weight: "0"`), sonra rollback: 
  - `kubectl rollout undo deploy/fiscus-api-canary`

## 2) Webhook İmzaları / Replay
- `payments` loglarında `timestamp_skew|bad_signature|replay` hatalarını kontrol et.
- Nonce cache TTL'i yükselt (varsayılan 10dk).

## 3) DB yükü / yavaş sorgular
- `EXPLAIN (ANALYZE, BUFFERS)` → indeks öner
- Gerekirse read replica yönlendirmesi

## 4) Backup Restore
```
infra/backup/pg_restore.sh s3://backups/fiscus.dump "$DATABASE_URL"
```

## 5) Güvenlik Olayı
- Rate-limit'i sıkılaştır (`burst`/`rate_per_minute` düşür) 
- WAF kuralını etkinleştir (ingress-waf.yaml)
- Access log + CSP raporları incele
