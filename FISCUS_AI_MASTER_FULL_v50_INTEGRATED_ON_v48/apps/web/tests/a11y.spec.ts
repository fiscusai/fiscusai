import { test, expect } from '@playwright/test';

test.describe('A11y smoke', () => {
  test('home has title and no console errors', async ({ page }) => {
    const messages: string[] = [];
    page.on('console', msg => {
      const type = msg.type();
      if (type === 'error') messages.push(msg.text());
    });

    await page.goto('/');
    await expect(page).toHaveTitle(/FISCUS AI/i);
    // En az bir H1 veya role="main" alanı olsun
    const h1 = page.locator('h1');
    const main = page.locator('main');
    expect(await h1.count() + await main.count()).toBeGreaterThan(0);
    expect(messages).toEqual([]);
  });
});