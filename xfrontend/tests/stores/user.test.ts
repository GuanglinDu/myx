/**
 * Updated at 18:14:51 on 20260520 Wednesday by Guanglin Du
 * 
 * (1/2) What are the unit tests, integration tests, and end-to-end tests in
 * Vue.js 3, respectively? - Google AI Overview
 * 
 * In Vue.js 3, testing is typically categorized by the scope of the code being
 * examined, often following a "testing pyramid" strategy that balances speed
 * and reliability.
 * 
 * (1.1/2) Unit Testing
 * Unit tests verify the smallest, isolated parts of your application in
 * complete isolation. In a Vue context, this usually means testing pure logic
 * rather than the UI. 
 * - Targets: Individual functions, classes, composables, or utility modules.
 * - Focus: Ensuring specific inputs produce the correct outputs or side effects
 * (e.g., a math helper or a data formatter).
 * - Tools: Vitest (native to Vite and highly recommended for Vue 3) or Jest.
 * 
 * (1.2/2) Integration (Component) Testing
 * In Vue development, "Integration Testing" is often synonymous with Component
 * Testing. These tests check how multiple units or components work together as
 * a small system.
 * - Target: Vue components and their interactions with children or shared state.
 * - Focus: Verifying that a component mounts correctly, renders the right UI,
 * handles user events (like clicks), and communicates properly with other
 * modules.
 * - Tools: Vue Test Utils paired with Vitest, or Cypress Component Testing.
 * 
 * (1.3/2) End-to-End (E2E) Testing
 * E2E tests validate the entire application flow from a real user's
 * perspective. They run against a production-like build of your app and often
 * involve a real browser.
 * - Target: Complete user journeys spanning multiple pages and real network
 * requests.
 * - Focus: Checking features like "user login," "shopping cart checkout," or
 * "onboarding flows" to ensure the frontend and backend work together
 * seamlessly.
 * - Tools: Playwright or Cypress.
 * 
 * (2/2) Dependencies
 * npm install -D vitest               (test runners & unit tests)
 * npm install -D @vue/test-utiles     (component tests)
 * npm install -D @testing-library/vue (testing Vue components with a focus on
 * user-centric testing practices, making it easier to test how users interact
 * with your Vue applications)
 * npm install -D @playwright/test     (end-to-end tests), or
 * npm install -D cypress              (end-to-end tests)
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useUserStore } from '@/stores/user';

// Mock the router
vi.mock('vue-router', async () => {
  const actual = await import('vue-router');
  return {
    ...actual,
    useRouter: () => ({
      push: vi.fn(),
    }),
  };
});

// Mock axios with proper Promise returns
vi.mock('axios', () => ({
  default: {
    post: vi.fn().mockResolvedValue({ data: { access: 'mock-access' } }),
    get: vi.fn().mockResolvedValue({ data: {} }),
    defaults: {
      headers: {
        common: {},
      },
    },
  },
}));

describe('useUserStore', () => {
  beforeEach(() => {
    localStorage.clear();
    setActivePinia(createPinia());
  });

  it('has correct initial state', () => {
    const userStore = useUserStore();
    expect(userStore.user.id).toBe('');
    expect(userStore.user.name).toBe('');
    expect(userStore.user.email).toBe('');
    expect(userStore.user.access).toBe('');
    expect(userStore.user.refresh).toBe('');
    expect(userStore.user.avatar).toBe('');
    expect(userStore.user.isAuthenticated).toBe(false);
  });

  it('setToken updates state and localStorage', () => {
    const userStore = useUserStore();
    const tokenData = {
      access: 'test-access-token',
      refresh: 'test-refresh-token',
    };

    userStore.setToken(tokenData);

    expect(userStore.user.access).toBe('test-access-token');
    expect(userStore.user.refresh).toBe('test-refresh-token');
    expect(userStore.user.isAuthenticated).toBe(true);
    expect(localStorage.getItem('user.access')).toBe('test-access-token');
    expect(localStorage.getItem('user.refresh')).toBe('test-refresh-token');
  });

  it('removeToken clears state and localStorage', () => {
    const userStore = useUserStore();
    userStore.setToken({ access: 'token', refresh: 'refresh' });

    userStore.removeToken();

    expect(userStore.user.access).toBe('');
    expect(userStore.user.refresh).toBe('');
    expect(userStore.user.id).toBe('');
    expect(userStore.user.name).toBe('');
    expect(userStore.user.isAuthenticated).toBe(false);
  });

  it('setUserInfo updates user info and localStorage', () => {
    const userStore = useUserStore();
    const userInfo = {
      id: '123',
      name: 'Test User',
      email: 'test@example.com',
      access: '',
      refresh: '',
      avatar: 'avatar.png',
      isAuthenticated: true,
    };

    userStore.setUserInfo(userInfo);

    expect(userStore.user.id).toBe('123');
    expect(userStore.user.name).toBe('Test User');
    expect(userStore.user.email).toBe('test@example.com');
    expect(userStore.user.avatar).toBe('avatar.png');
  });

  it('initStore restores from localStorage when token exists', async () => {
    localStorage.setItem('user.access', 'stored-access');
    localStorage.setItem('user.refresh', 'stored-refresh');
    localStorage.setItem('user.id', 'user-123');
    localStorage.setItem('user.name', 'Stored User');
    localStorage.setItem('user.email', 'stored@example.com');
    localStorage.setItem('user.avatar', 'stored-avatar.png');

    const userStore = useUserStore();
    userStore.initStore();

    // Wait for async refreshToken to complete
    await new Promise((resolve) => setTimeout(resolve, 10));

    // After refreshToken, access should be updated to mock-access
    expect(userStore.user.access).toBe('mock-access');
    expect(userStore.user.refresh).toBe('stored-refresh');
    expect(userStore.user.id).toBe('user-123');
    expect(userStore.user.isAuthenticated).toBe(true);
  });

  it('initStore does nothing when no token exists', () => {
    const userStore = useUserStore();
    userStore.initStore();

    expect(userStore.user.access).toBe('');
    expect(userStore.user.isAuthenticated).toBe(false);
  });
});