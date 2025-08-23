
import { test, expect } from '@playwright/test';

test('audit page loads and filters exist', async ({ page }) => {
  await page.goto('/(main)/audit');
  await expect(page.getByText('Audit Log')).toBeVisible();
  await expect(page.getByText('Otomatik yenile')).toBeVisible();
});
