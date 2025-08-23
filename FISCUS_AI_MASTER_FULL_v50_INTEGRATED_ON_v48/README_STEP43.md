# STEP 43 — User Lifecycle (verify/reset/invite/disable)

## API
- POST /auth/register
- POST /auth/login
- POST /auth/verify/request
- GET  /auth/verify/confirm?token=...
- POST /auth/password/reset/request
- POST /auth/password/reset/confirm { token, new_password }
- POST /auth/invite
- POST /auth/accept-invite { token, password }
- POST /auth/disable { email }
- POST /auth/enable { email }

Outbox: `apps/api/app/data/outbox/` dizinine .eml dosyaları düşer.

## Çalıştırma
```
cd apps/api
uvicorn app.main:app --reload
```

Web davet sayfası:
```
cd apps/web
npm install
npm run dev
# /settings/users/invite
```
