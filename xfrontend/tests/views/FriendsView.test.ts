import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import FriendsView from '@/views/FriendsView.vue';
import { setActivePinia, createPinia } from 'pinia';

// Mock axios
vi.mock('axios', async () => {
  const actual = await vi.importActual('axios');
  return {
    default: {
      ...actual.default,
      get: vi.fn().mockResolvedValue({
        data: {
          user: { id: '1', name: 'Test User', friend_count: 10, post_count: 5 },
          friends: [],
          friendshipRequests: [],
        },
      }),
      post: vi.fn().mockResolvedValue({ data: {} }),
    },
  };
});

describe('FriendsView', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('renders friends view', () => {
    const wrapper = mount(FriendsView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
          PeopleYouMayKnow: true,
          TrendsComponent: true,
        },
      },
    });

    expect(wrapper.find('.max-w-7xl').exists()).toBe(true);
  });

  it('renders user profile section', () => {
    const wrapper = mount(FriendsView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
          PeopleYouMayKnow: true,
          TrendsComponent: true,
        },
      },
    });

    expect(wrapper.find('.main-left').exists()).toBe(true);
  });

  it('renders main content area', () => {
    const wrapper = mount(FriendsView, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
          PeopleYouMayKnow: true,
          TrendsComponent: true,
        },
      },
    });

    expect(wrapper.find('.main-center').exists()).toBe(true);
  });
});