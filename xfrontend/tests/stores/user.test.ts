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