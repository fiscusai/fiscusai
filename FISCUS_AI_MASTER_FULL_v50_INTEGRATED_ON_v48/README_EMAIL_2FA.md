
# E-posta Altyapısı ve 2FA (TOTP)

## E-posta
- Varsayılan olarak geliştirme modunda `apps/api/app/utils/mailer.py` gönderimleri `/tmp/mail_out` klasörüne `.eml` dosyası olarak yazar.
- Gerçek gönderim için Postmark/AWS SES/SMTP eklenecek alanlar hazır.

### Yapılandırma
- `MAIL_OUT_DIR=/tmp/mail_out`
- (Opsiyonel) Postmark/SES anahtarları eklenecekse ENV ile tanımlayın ve `mailer.py` içinde gerekli kodu açın.

### SPF/DKIM/DMARC
- **SPF**: DNS TXT kaydı ile yetkili gönderici IP/servis sağlayıcısını tanımlayın.
- **DKIM**: E-posta sağlayıcısının verdiği public key’i DNS'e TXT kaydı olarak ekleyin.
- **DMARC**: `v=DMARC1; p=quarantine; rua=mailto:dmarc@domain.com` gibi bir TXT kaydı ekleyin.
- Üretime çıkmadan önce `mail-tester.com` benzeri araçlarla puanınızı kontrol edin.

## 2FA (TOTP)
- `POST /auth/2fa/setup` kullanıcı için secret üretir ve provisioning URI döner (Google Authenticator uyumlu).
- `POST /auth/2fa/verify` 6 haneli kodu doğrular ve kullanıcıda `twofa_enabled=true` yapar.

## Şifre Sıfırlama
- `POST /auth/reset/request` e-posta'ya token gönderir (dev modda yanıtta `dev_token` döner).
- `POST /auth/reset/confirm` token ve yeni şifre ile sıfırlar.
