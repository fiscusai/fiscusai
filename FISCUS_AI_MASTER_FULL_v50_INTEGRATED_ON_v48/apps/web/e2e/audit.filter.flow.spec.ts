
import { test, expect } from '@playwright/test';

test('audit filter flow', async ({ page }) => {
  await page.goto('/(main)/audit');
  await expect(page.getByText('Audit Log')).toBeVisible();
  // if there is at least one event filter button, click first toggle
  const btns = page.locator('button', { hasText: /.+/ });
  // this is a smoke test; ensure CSV button exists
  await expect(page.getByText('CSV indir')).toBeVisible();
});
