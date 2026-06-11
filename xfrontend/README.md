# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run (list all commands)
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

## Run Unit Tests with [Vitest](https://vitest.dev/)

- Run tests (dependent on the config in package.json)

```sh
npm run test:watch (watch-mode)                             # all tests
npm run test:once
npm run test:watch -- src/stores/__tests__                  # a folder
npm run test:once -- src/stores/__tests__
npm run test:watch -- src/stores/__tests__/counter.test.ts  # a test file
npm run test:once -- src/stores/__tests__/counter.test.ts
```

- Run a specific test (3 ways)

```sh
npm run test:watch -- src/stores/__tests__/counter.test.ts -t "checks the default count to be 0"
npx vitest run src/stores/__tests__/counter.test.ts:29
npx vitest run -t "checks the default count to be 0"
```

## Run End-to-End Tests with [Playwright](https://playwright.dev)

```sh
# Install browsers for the first run
npx playwright install

# When testing on CI, must build the project first
npm run build

# Runs the end-to-end tests
npm run test:e2e
# Runs the tests only on Chromium
npm run test:e2e -- --project=chromium
# Runs the tests of a specific file
npm run test:e2e -- tests/example.spec.ts
# Runs the tests in debug mode
npm run test:e2e -- --debug
```
