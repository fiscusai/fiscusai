import { test, expect } from '@playwright/test';

test('audit page filters render', async ({ page }) => {
  await page.goto('/(main)/audit');
  await expect(page.getByText(/Audit Log/i)).toBeVisible();
  await expect(page.getByText(/Otomatik yenile/i)).toBeVisible();
});
