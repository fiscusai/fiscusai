# FISCUS AI — Geliştirici Rehberi (Local Dev)

## Hızlı Başlangıç (Docker)
```bash
# Servisleri başlat
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d db redis minio clamav

# API'yi başlat
docker compose -f docker-compose.yml -f docker-compose.override.yml up --build api
```

## Hızlı Başlangıç (Python venv)
```bash
make install
make run
```

## Ortam Değişkenleri
`.env.example` içindeki değerleri `.env` veya `.env.dev`'e kopyalayın ve düzenleyin.

## Veritabanı
- İlk kurulumda tablo oluşturmak için:
```bash
make seed   # init_db() çağırır
```
- Alembic ile migrasyon:
```bash
make migrate
make upgrade
```

## Dosya Yükleme (MinIO)
- MinIO Arayüzü: http://localhost:9001
- Access Key / Secret: `minioadmin` / `minioadmin123`
- Bucket: `uploads`

## Güvenlik
- Geliştirme modunda `presign` endpoint'i boto3 yoksa dummy yanıt dönebilir.
- Production'da ClamAV ve imza doğrulaması aktif edilmelidir.
```


## İzleme (opsiyonel)
- SENTRY_DSN ortam değişkeni verilirse Sentry etkinleştirin.
- Prometheus metrics için `prometheus-client` paketini kullanın; `/metrics` route’u zaten projede mevcutsa kablolayın (yoksa kolayca eklenebilir).


## Basit Auth UI (statik)
`apps/web/auth-ui/login.html` dosyasını tarayıcıda açarak (Live Server/VSCode da olur) API’ye istek atabilirsiniz.
- `login.html`, `register.html`, `reset.html`, `twofa.html` mevcut.
- CORS için API `http://localhost:8000` adresinde çalışmalıdır.
