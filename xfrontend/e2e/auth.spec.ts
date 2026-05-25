import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test('shows login page correctly', async ({ page }) => {
    await page.goto('/login');

    await expect(page.locator('h1')).toContainText('Log in');
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button')).toContainText('Log in');
  });

  test('shows signup link', async ({ page }) => {
    await page.goto('/login');

    await expect(page.getByText("Don't have an account")).toBeVisible();
    await expect(page.locator('a:has-text("Click here")')).toBeVisible();
  });

  test('validates empty email', async ({ page }) => {
    await page.goto('/login');

    await page.waitForLoadState('networkidle');
    await page.locator('input[type="password"]').fill('password123');
    await page.locator('button:has-text("Log in")').click();

    await page.waitForTimeout(500);
  });

  test('validates empty password', async ({ page }) => {
    await page.goto('/login');

    await page.waitForLoadState('networkidle');
    await page.locator('input[type="email"]').fill('test@example.com');
    await page.locator('button:has-text("Log in")').click();

    await page.waitForTimeout(500);
  });

  test('can navigate to signup page', async ({ page }) => {
    await page.goto('/login');

    await page.locator('a:has-text("Click here")').click();

    await expect(page).toHaveURL(/\/signup/);
    await expect(page.locator('h1')).toContainText('Sign up');
  });
});

test.describe('Signup Flow', () => {
  test('shows signup page correctly', async ({ page }) => {
    await page.goto('/signup');

    await expect(page.locator('h1')).toContainText('Sign up');
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[name="password1"]')).toBeVisible();
    await expect(page.locator('input[name="password2"]')).toBeVisible();
  });

  test('can navigate to login page', async ({ page }) => {
    await page.goto('/signup');

    await page.locator('a:has-text("Click here")').click();

    await expect(page).toHaveURL(/\/login/);
  });
});

test.describe('Navigation', () => {
  test('homepage loads', async ({ page }) => {
    await page.goto('/');

    await expect(page.locator('body')).toBeVisible();
  });
});