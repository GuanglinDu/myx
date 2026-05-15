import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import LoginView from '@/views/LoginView.vue';
import { setActivePinia, createPinia } from 'pinia';

// Mock axios
vi.mock('axios', () => ({
  default: {
    post: vi.fn().mockResolvedValue({ data: { access: 'token', refresh: 'refresh' } }),
    get: vi.fn().mockResolvedValue({ data: { id: '1', name: 'Test', email: 'test@example.com' } }),
    defaults: { headers: { common: {} } },
  },
}));

describe('LoginView', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('renders login form correctly', () => {
    const wrapper = mount(LoginView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    expect(wrapper.find('h1').text()).toBe('Log in');
    expect(wrapper.find('input[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find('button').text()).toBe('Log in');
  });

  it('has link to signup page', () => {
    const wrapper = mount(LoginView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    expect(wrapper.html()).toContain("Don't have an account");
  });

  it('form fields are interactive', async () => {
    const wrapper = mount(LoginView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    const emailInput = wrapper.find('input[type="email"]');
    await emailInput.setValue('test@example.com');
    expect((emailInput.element as HTMLInputElement).value).toBe('test@example.com');

    const passwordInput = wrapper.find('input[type="password"]');
    await passwordInput.setValue('password123');
    expect((passwordInput.element as HTMLInputElement).value).toBe('password123');
  });

  it('validates email is not empty on submit', async () => {
    const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    const wrapper = mount(LoginView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    await wrapper.find('input[type="password"]').setValue('password123');
    await wrapper.find('form').trigger('submit.prevent');

    // In LoginView, validation errors go to console.log, not the template
    expect(consoleSpy).toHaveBeenCalledWith(
      expect.arrayContaining(['Your e-mail is missing'])
    );
    consoleSpy.mockRestore();
  });

  it('validates password is not empty on submit', async () => {
    const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    const wrapper = mount(LoginView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    await wrapper.find('input[type="email"]').setValue('test@example.com');
    await wrapper.find('form').trigger('submit.prevent');

    // In LoginView, validation errors go to console.log, not the template
    expect(consoleSpy).toHaveBeenCalledWith(
      expect.arrayContaining(['Your password is missing'])
    );
    consoleSpy.mockRestore();
  });

  it('submits form to API when fields are valid', async () => {
    const wrapper = mount(LoginView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    await wrapper.find('input[type="email"]').setValue('test@example.com');
    await wrapper.find('input[type="password"]').setValue('password123');
    await wrapper.find('form').trigger('submit.prevent');

    // Wait for the async axios calls
    await new Promise((resolve) => setTimeout(resolve, 50));

    // Verify API was called
    const axios = await import('axios');
    expect(axios.default.post).toHaveBeenCalled();
    expect(axios.default.post).toHaveBeenCalledWith('/api/login/', expect.any(Object));
  });
});