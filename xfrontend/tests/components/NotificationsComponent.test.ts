import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import NotificationsComponent from '@/components/NotificationsComponent.vue';
import { setActivePinia, createPinia } from 'pinia';

// Mock axios
vi.mock('axios', async () => {
  const actual = await vi.importActual('axios');
  return {
    default: {
      ...actual.default,
      get: vi.fn().mockResolvedValue({ data: [] }),
      post: vi.fn().mockResolvedValue({ data: {} }),
    },
  };
});

describe('NotificationsComponent', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('renders notification bell button', () => {
    const wrapper = mount(NotificationsComponent, {
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    // Check bell button exists
    const button = wrapper.find('button');
    expect(button.exists()).toBe(true);
    expect(button.find('svg').exists()).toBe(true);
  });

  it('hides badge when no requests', () => {
    const wrapper = mount(NotificationsComponent, {
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    const badge = wrapper.find('.absolute');
    expect(badge.exists()).toBe(false);
  });

  it('toggles dropdown when bell is clicked', async () => {
    const wrapper = mount(NotificationsComponent, {
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    // Dropdown should not be visible initially
    expect(wrapper.find('.absolute.right-0').exists()).toBe(false);

    // Click the bell
    await wrapper.find('button').trigger('click');

    // Now dropdown should be visible
    expect(wrapper.find('.absolute.right-0').exists()).toBe(true);
  });

  it('shows loading state initially', async () => {
    const axios = await import('axios');
    vi.mocked(axios.default.get).mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve({ data: [] }), 100))
    );

    const wrapper = mount(NotificationsComponent, {
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    await wrapper.find('button').trigger('click');

    // Should show loading text
    expect(wrapper.text()).toContain('Loading...');
  });

  it('shows no pending requests message when empty', async () => {
    const axios = await import('axios');
    vi.mocked(axios.default.get).mockResolvedValue({ data: [] });

    const wrapper = mount(NotificationsComponent, {
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    await wrapper.find('button').trigger('click');

    expect(wrapper.text()).toContain('No pending requests');
  });
});