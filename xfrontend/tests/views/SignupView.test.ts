import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import SignupView from '@/views/SignupView.vue';
import { setActivePinia, createPinia } from 'pinia';
import { createApp } from 'vue';

// Mock axios
vi.mock('axios', () => ({
  default: {
    post: vi.fn().mockResolvedValue({ data: { message: 'success' } }),
    get: vi.fn(),
    defaults: { headers: { common: {} } },
  },
}));

describe('SignupView', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('renders signup form correctly', () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    expect(wrapper.find('h1').text()).toBe('Sign up');
    expect(wrapper.find('input[name="name"]').exists()).toBe(true);
    expect(wrapper.find('input[name="email"]').exists()).toBe(true);
    expect(wrapper.find('input[name="password1"]').exists()).toBe(true);
    expect(wrapper.find('input[name="password2"]').exists()).toBe(true);
    expect(wrapper.find('button').text()).toBe('Sign up');
  });

  it('has link to login page', () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    expect(wrapper.html()).toContain('Already have an account');
  });

  it('form fields are interactive', async () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    const nameInput = wrapper.find('input[name="name"]');
    await nameInput.setValue('Test User');
    expect((nameInput.element as HTMLInputElement).value).toBe('Test User');

    const emailInput = wrapper.find('input[name="email"]');
    await emailInput.setValue('test@example.com');
    expect((emailInput.element as HTMLInputElement).value).toBe('test@example.com');
  });

  it('calls toastStore.showToast when name is missing', async () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    // Fill other fields but not name
    await wrapper.find('input[name="email"]').setValue('test@example.com');
    await wrapper.find('input[name="password1"]').setValue('password123');
    await wrapper.find('input[name="password2"]').setValue('password123');

    // Spy on showToast
    const toastStoreModule = await import('@/stores/toast');
    const showToastSpy = vi.spyOn(toastStoreModule.useToastStore(), 'showToast');

    await wrapper.find('form').trigger('submit.prevent');

    // Verify showToast was called with expected args
    expect(showToastSpy).toHaveBeenCalledWith(
      5000,
      'Your name is missing',
      'bg-red-300'
    );
  });

  it('calls toastStore.showToast when passwords do not match', async () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    await wrapper.find('input[name="name"]').setValue('Test User');
    await wrapper.find('input[name="email"]').setValue('test@example.com');
    await wrapper.find('input[name="password1"]').setValue('password123');
    await wrapper.find('input[name="password2"]').setValue('differentpassword');

    const toastStoreModule = await import('@/stores/toast');
    const showToastSpy = vi.spyOn(toastStoreModule.useToastStore(), 'showToast');

    await wrapper.find('form').trigger('submit.prevent');

    expect(showToastSpy).toHaveBeenCalledWith(
      5000,
      'The password does not match',
      'bg-red-300'
    );
  });

  it('submits form to API when all fields are valid', async () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    await wrapper.find('input[name="name"]').setValue('Test User');
    await wrapper.find('input[name="email"]').setValue('test@example.com');
    await wrapper.find('input[name="password1"]').setValue('password123');
    await wrapper.find('input[name="password2"]').setValue('password123');
    await wrapper.find('form').trigger('submit.prevent');

    // Wait for the async axios call
    await new Promise((resolve) => setTimeout(resolve, 50));

    // Verify API was called
    const axios = await import('axios');
    expect(axios.default.post).toHaveBeenCalled();
    expect(axios.default.post).toHaveBeenCalledWith('/api/signup/', expect.any(Object));
  });
});