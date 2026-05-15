import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import FeedView from '@/views/FeedView.vue';
import { setActivePinia, createPinia } from 'pinia';

// Mock axios
vi.mock('axios', async () => {
  const actual = await vi.importActual('axios');
  return {
    default: {
      ...actual.default,
      get: vi.fn().mockResolvedValue({ data: [] }),
      post: vi.fn().mockResolvedValue({ data: { id: '1', body: 'Test' } }),
    },
  };
});

describe('FeedView', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('renders the feed view', () => {
    const wrapper = mount(FeedView, {
      global: {
        stubs: {
          RouterLink: true,
          PeopleYouMayKnow: true,
          TrendsComponent: true,
          FeedItem: true,
        },
      },
    });

    expect(wrapper.find('textarea').exists()).toBe(true);
  });

  it('renders textarea for post content', () => {
    const wrapper = mount(FeedView, {
      global: {
        stubs: {
          RouterLink: true,
          PeopleYouMayKnow: true,
          TrendsComponent: true,
          FeedItem: true,
        },
      },
    });

    const textarea = wrapper.find('textarea');
    expect(textarea.exists()).toBe(true);
    expect(textarea.attributes('placeholder')).toContain('What are you curious about');
  });

  it('has Post button', () => {
    const wrapper = mount(FeedView, {
      global: {
        stubs: {
          RouterLink: true,
          PeopleYouMayKnow: true,
          TrendsComponent: true,
          FeedItem: true,
        },
      },
    });

    const buttons = wrapper.findAll('button');
    expect(buttons.some(b => b.text() === 'Post')).toBe(true);
  });

  it('has Attach image link', () => {
    const wrapper = mount(FeedView, {
      global: {
        stubs: {
          RouterLink: true,
          PeopleYouMayKnow: true,
          TrendsComponent: true,
          FeedItem: true,
        },
      },
    });

    const links = wrapper.findAll('a');
    expect(links.some(l => l.text() === 'Attach image')).toBe(true);
  });
});