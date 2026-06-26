import { test, expect } from "@playwright/test";

test.describe("Login Flow", () => {
  test("shows login page correctly", async ({ page }) => {
    await page.goto("/login");

    await expect(page.locator("h1")).toContainText("Log in");
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator("button")).toContainText("Log in");
  });

  test("shows signup link", async ({ page }) => {
    await page.goto("/login");

    await expect(page.getByText("Don't have an account")).toBeVisible();
    await expect(page.locator('a:has-text("Click here")')).toBeVisible();
  });

  test("validates empty email", async ({ page }) => {
    await page.goto("/login");

    await page.waitForLoadState("networkidle");
    await page.locator('input[type="password"]').fill("password123");
    await page.locator('button:has-text("Log in")').click();

    await page.waitForTimeout(500);
  });

  test("validates empty password", async ({ page }) => {
    await page.goto("/login");

    await page.waitForLoadState("networkidle");
    await page.locator('input[type="email"]').fill("test@example.com");
    await page.locator('button:has-text("Log in")').click();

    await page.waitForTimeout(500);
  });

  test("can navigate to signup page", async ({ page }) => {
    await page.goto("/login");

    await page.locator('a:has-text("Click here")').click();

    await expect(page).toHaveURL(/\/signup/);
    await expect(page.locator("h1")).toContainText("Sign up");
  });
});

test.describe("Signup Flow", () => {
  test("shows signup page correctly", async ({ page }) => {
    await page.goto("/signup");

    await expect(page.locator("h1")).toContainText("Sign up");
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[name="password1"]')).toBeVisible();
    await expect(page.locator('input[name="password2"]')).toBeVisible();
  });

  test("can navigate to login page", async ({ page }) => {
    await page.goto("/signup");

    await page.locator('a:has-text("Click here")').click();

    await expect(page).toHaveURL(/\/login/);
  });
});

test.describe("Navigation", () => {
  test("homepage loads", async ({ page }) => {
    await page.goto("/");

    await expect(page.locator("body")).toBeVisible();
  });
});

/** Updated at 18:29:31 on 20260616 Tue by Guanglin Du.

(1/2) What does the Page fixture look like in Playwright Test?
      - Google AI Overview
See screenshot Built-in-fixture-Page-in-Playwright-Test-20260616.png, and
How-is-the-Page-fixture-passed-to-function-test-in-Playwright-Test-20260616.png

In Playwright Test, the page fixture is a built-in, isolated browser tab that
is passed directly into your test function via object destructuring.

Here is exactly what the code looks like:

import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  // The `page` fixture is automatically passed as an argument
  await page.goto('https://playwright.dev/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Playwright/);
});

(2/2) Key Characteristics of the Page Fixture
(2.1/2) Destructured Argument
You request it by wrapping it in curly braces { page } inside the test function
signature.
(2.2/2) Automatic Isolation
Playwright automatically creates a fresh Browser Context (equivalent to an
incognito profile) and a new page for every single test.
(2.3/2) Zero Manual Setup
You do not need to manually write code to launch the browser, create a context,
or close the page—Playwright handles the setup and teardown automatically.

(3/3) How is the Page fixture passed to function test in Playwright Test?
      - Google AI Overview
In Playwright Test, the page fixture is passed into the test function using
dependency injection through object destructuring as the first argument of
the test closure. See ({ page }) =_ {...} vs (page) =_ {...}-20260616.png.
*/
