import { test, expect } from '@playwright/test';

test('V2 invoices create/list flow', async ({ page }) => {
  // Demo auth
  await page.addInitScript(() => {
    localStorage.setItem('fiscus_auth', JSON.stringify({ role:'accountant', org:'ORG-ALPHA' }));
  });
  await page.goto('/(main)/invoices_v2/client');
  await expect(page.getByText('Faturalar')).toBeVisible();
  // Search toggle
  await page.getByPlaceholder('Ara...').fill('Aurea');
  // Just verify table renders (demo)
  await expect(page.locator('table')).toBeVisible();
});
