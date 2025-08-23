# FISCUS Web - Çalıştırma ve Kalite Kontrolleri

## Geliştirme
```bash
cd apps/web
npm install
npm run dev
```

## Üretim
```bash
npm run build
npm start
```

## Testler
- Erişilebilirlik duman testi:
```bash
npm run test:a11y
```

## Lighthouse CI
GitHub Actions `Web CI` workflow'u, build sonrası Lighthouse puanlarını hesaplar ve raporları artifact olarak yükler.

## PWA
- `public/site.webmanifest`, `public/sw.js` ve `public/offline.html` eklendi.
- `ServiceWorker` bileşeni `app/layout.tsx` içinde kaydı otomatik yapar.