import { test, expect } from '@playwright/test';

test('landing loads and navigate to pricing', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText(/FISCUS AI/i)).toBeVisible();
  await page.goto('/pricing');
  await expect(page.getByText(/Planlar/i)).toBeVisible();
});

test('status page shows version', async ({ page }) => {
  await page.goto('/status');
  await expect(page.getByText(/Sistem Durumu/i)).toBeVisible();
});

test('invoices v2 page renders', async ({ page }) => {
  await page.goto('/invoices_v2');
  await expect(page.getByText(/Faturalar/i)).toBeVisible();
});
