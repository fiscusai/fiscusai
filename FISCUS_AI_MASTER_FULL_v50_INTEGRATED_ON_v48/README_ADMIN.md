# Admin / Audit / Roles

## Roller
- `uploader`: dosya yükleme ve `notify-upload`
- `admin`: son yüklemeleri görme, silme, yeniden tarama

## JWT Örneği
```python
import jwt, time
print(jwt.encode({"sub":"admin","role":"admin","exp":int(time.time())+3600}, "change-me", algorithm="HS256"))
```

## Audit Log
- Model: `apps/api/app/models/audit.py` (`AuditLog`)
- Migration: `0002_audit_log`
- Kayıt: `notify-upload` içinde otomatik eklenir

## Admin Web
- URL: `/admin/uploads` (localStorage'da `api_token` varsa çağrılar yetkili olur)

## Webhook İmzalama
- Env: `WEBHOOK_SECRET`
- Bildirimlerde `X-Webhook-Signature` başlığı (HMAC-SHA256) ile imzalı JSON gövdesi gönderilir.
- Doğrulama için aynı sırla `hex` HMAC üretip karşılaştırın.

## Admin • Users (UI)
- Sayfa: `/admin/users`
- İşlevler: listele, rol ataması (admin/uploader), sil
