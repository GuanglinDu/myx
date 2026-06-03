import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import axios from 'axios';
import TrendsComponent from '@/components/TrendsComponent.vue';

vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}));

// Mock Vue Router to resolve RouterLink
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: { template: '<div />' } },
    {
      path: '/trends/:id',
      name: 'trendview',
      component: { template: '<div />' }
    }
  ]
});

describe('TrendsComponent', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the trends title', async () => {
    (axios.get as ReturnType<typeof vi.fn>).mockResolvedValue({
      data: []
    });
    const wrapper = mount(TrendsComponent, {
      global: {
        plugins: [router]
      }
    });
    await flushPromises();
    expect(wrapper.find('h3').text()).toBe('Trends');
  });

  it('displays trends from API', async () => {
    const mockTrends = [
      { id: '1', hashtag: 'coding', occurences: 100 },
      { id: '2', hashtag: 'python', occurences: 50 },
      { id: '3', hashtag: 'django', occurences: 200 },
      { id: '4', hashtag: 'vue', occurences: 30 }
    ];
    (axios.get as ReturnType<typeof vi.fn>).mockResolvedValue({
      data: mockTrends
    });

    const wrapper = mount(TrendsComponent, {
      global: {
        plugins: [router]
      }
    });
    await flushPromises();

    expect(axios.get).toHaveBeenCalledWith('/api/posts/trends/');
    const hashtags = wrapper.findAll('strong');
    expect(hashtags.length).toBe(4);
    expect(hashtags[0].text()).toBe('#coding');
    expect(hashtags[1].text()).toBe('#python');
    expect(hashtags[2].text()).toBe('#django');
    expect(hashtags[3].text()).toBe('#vue');
  });

  it('displays occurrence count for each trend', async () => {
    const mockTrends = [
      { id: '1', hashtag: 'coding', occurences: 100 }
    ];
    (axios.get as ReturnType<typeof vi.fn>).mockResolvedValue({
      data: mockTrends
    });

    const wrapper = mount(TrendsComponent, {
      global: {
        plugins: [router]
      }
    });
    await flushPromises();
    expect(wrapper.text()).toContain('100 posts');
  });

  it('has explore buttons for each trend', async () => {
    const mockTrends = [
      { id: '1', hashtag: 'coding', occurences: 100 },
      { id: '2', hashtag: 'python', occurences: 50 }
    ];
    (axios.get as ReturnType<typeof vi.fn>).mockResolvedValue({
      data: mockTrends
    });

    const wrapper = mount(TrendsComponent, {
      global: {
        plugins: [router]
      }
    });
    await flushPromises();

    const buttons = wrapper.findAll('a');
    expect(buttons.length).toBe(2);
    buttons.forEach((btn) => {
      expect(btn.text()).toBe('Explore');
    });
  });
});