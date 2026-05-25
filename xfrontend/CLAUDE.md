# Coding Standards

All Vue code in this project must adhere strictly to the Vue.js 3 Compostional API style. Key rules include:

- Use 2 spaces for indentation.
- Limit lines to a maximum of 79 characters wherever possible.
- Use camelCase for function and variable names.
- Use one blank line between functions.

## Testing

### Unit Tests (Vitest)
```bash
npm run test        # Run all unit tests
```

### E2E Tests (Playwright)
```bash
npm run e2e         # Run Playwright e2e tests
npx playwright test # Same as above
```

E2e tests are in the `e2e/` directory. Config is in `playwright.config.ts`.
