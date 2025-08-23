
import { test, expect } from '@playwright/test';

test('customers v2 list page renders', async ({ page }) => {
  // demo auth
  await page.addInitScript(() => {
    localStorage.setItem('fiscus_auth', JSON.stringify({ role:'user', org:'ORG-ALPHA' }));
  });
  await page.goto('/(main)/customers_v2');
  await expect(page.getByText('Müşteriler', { exact: false })).toBeVisible();
});
