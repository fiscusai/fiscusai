# Güvenlik Sertleştirme Kontrol Listesi

- [x] Güvenlik başlıkları (CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy)
- [x] Rate limiting (in-memory, prod'da redis tabanlı önerilir)
- [x] JWT'den role/org claim çekip istek bağlamına ekleyen middleware
- [ ] HSTS (prod'da reverse proxy/Nginx ile etkin)
- [ ] CSRF koruması (cookie-based oturumlarda zorunlu)
- [ ] Parola politikası ve ihlal edilmiş parola kontrolü (HIBP k-anonim API)
- [ ] Secrets yönetimi (Vault/SSM), .env üretimden izole
- [ ] E-posta güvenliği (SPF/DKIM/DMARC) yapılandırması
