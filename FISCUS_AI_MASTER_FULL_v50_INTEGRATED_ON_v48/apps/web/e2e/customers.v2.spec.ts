import { test, expect } from '@playwright/test';

test('customers v2 page loads', async ({ page }) => {
  await page.goto('/(main)/customers_v2/client');
  await expect(page.getByText(/Müşteriler/i)).toBeVisible();
});
