// Minimal PWA Service Worker
const CACHE = 'fiscus-cache-v1';
const OFFLINE_URL = '/offline.html';

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.addAll([OFFLINE_URL, '/', '/favicon.ico']);
  })());
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  event.respondWith((async () => {
    try {
      const response = await fetch(request);
      return response;
    } catch (err) {
      const cache = await caches.open(CACHE);
      const cached = await cache.match(request);
      return cached || cache.match(OFFLINE_URL);
    }
  })());
});