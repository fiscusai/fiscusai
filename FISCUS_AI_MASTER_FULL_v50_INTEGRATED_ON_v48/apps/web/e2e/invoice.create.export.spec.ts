import { test, expect } from '@playwright/test';

test('login -> create invoice -> export PDF', async ({ page }) => {
  // fake local auth (demo)
  await page.addInitScript(() => {
    localStorage.setItem('fiscus_auth', JSON.stringify({email:'demo@fiscus.ai', role:'admin'}));
  });

  // Go to client invoices page (has form)
  await page.goto('/(main)/invoices/client');
  await expect(page.getByText('Faturalar (Gelişmiş)')).toBeVisible();

  // Click "Yeni Fatura"
  await page.getByRole('button', { name: 'Yeni Fatura' }).click();

  // Fill form fields by label
  await page.getByLabel('Fatura No').fill('INV-E2E-001');
  await page.getByLabel('Müşteri').fill('E2E Test Ltd.');
  await page.getByLabel('Tarih').fill('2025-08-09');
  await page.getByLabel('Tutar').fill('1234');
  await page.getByLabel('KDV').fill('222');

  // Save
  await page.getByRole('button', { name: 'Kaydet' }).click();

  // Expect row appears
  await expect(page.getByText('INV-E2E-001')).toBeVisible();

  // Expect a PDF link is present and clickable
  const pdfLink = page.getByRole('link', { name: /PDF/i }).first();
  await expect(pdfLink).toBeVisible();
});
