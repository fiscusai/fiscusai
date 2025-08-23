
import { test, expect, request } from '@playwright/test';

test('ETag If-None-Match returns 304', async ({}) => {
  const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
  const api = await request.newContext({ baseURL });
  const res1 = await api.get('/v2/invoices/?page=1&page_size=5', {
    headers: { 'X-Org': 'ORG-ALPHA', 'X-User-Role': 'user' }
  });
  expect(res1.ok()).toBeTruthy();
  const etag = res1.headers()['x-etag'] || res1.headers()['X-ETag'];
  expect(etag).toBeTruthy();
  const res2 = await api.get('/v2/invoices/?page=1&page_size=5', {
    headers: { 'X-Org': 'ORG-ALPHA', 'X-User-Role': 'user', 'If-None-Match': etag as string }
  });
  expect(res2.status()).toBe(304);
});
