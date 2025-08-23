# FISCUS API - Sağlık ve CI

## Çalıştırma (lokal)
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Sağlık endpoint'leri
- `GET /live` → Uygulama canlılık (her zaman 200/{"ok":true})
- `GET /ready` → Hazırlık: DB ve (varsa) S3/Redis port kontrolü
- `GET /health` → Özet: `{ ok, version, db, s3, redis }`

## Docker healthchecks
`docker-compose.yml` içinde **db**, **minio**, **redis**, **api** için healthcheck eklidir.

## CI
`.github/workflows/api-ci.yml`:
- `pip install -r requirements.txt`
- Import check (app.main)
- FastAPI TestClient ile `/live` smoke testi