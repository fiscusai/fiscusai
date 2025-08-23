import { test, expect } from '@playwright/test';

test('home has hero and cta', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText(/FISCUS AI/i)).toBeVisible();
  await expect(page.getByRole('button', { name: /başla|get started/i })).toBeVisible();
});
