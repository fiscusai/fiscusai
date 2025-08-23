import { test, expect } from '@playwright/test';

test('smoke: landing → status → invoices', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText(/FISCUS AI/i)).toBeVisible();
  await page.goto('/status');
  await expect(page.getByText(/Sürüm|Version/i)).toBeVisible();
  // demo auth for invoices
  await page.addInitScript(() => {
    localStorage.setItem('fiscus_auth', JSON.stringify({ role:'accountant', org:'ORG-ALPHA' }));
  });
  await page.goto('/(main)/invoices_v2');
  await expect(page.getByText(/Faturalar V2|Invoices V2/i)).toBeVisible();
});
