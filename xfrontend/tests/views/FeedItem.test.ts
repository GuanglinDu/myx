import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import FeedItem from '@/views/FeedItem.vue';
import type { Post } from '@/types/custom_types';

// Mock axios
vi.mock('axios', async () => {
  const actual = await vi.importActual('axios');
  return {
    default: {
      ...actual.default,
      post: vi.fn().mockResolvedValue({ data: { liked: true,
                                                like_count: 1 } }),
    },
  };
});

describe('FeedItem', () => {
  const mockPost: Post = {
    id: '123',
    body: 'Test post content',
    attachments: [],
    like_count: 0,
    liked: false,
    comments: [],
    comments_count: 5,
    created_at: '2024-01-01T00:00:00Z',
    created_by: {
      id: 'user-1',
      name: 'Test User',
      email: 'test@example.com',
      avatar: '',
      friend_count: 0,
      post_count: 0,
      is_active: true,
      is_superuser: false,
      is_staff: false,
    },
    created_at_formatted: '1 hour',
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders post body', () => {
    const wrapper = mount(FeedItem, {
      props: { post: mockPost },
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    expect(wrapper.text()).toContain('Test post content');
  });

  it('renders author name', () => {
    const wrapper = mount(FeedItem, {
      props: { post: mockPost },
      global: {
        stubs: {
          RouterLink: { template: '<a><strong><slot /></strong></a>' },
        },
      },
    });

    expect(wrapper.html()).toContain('Test User');
  });

  it('renders like button', () => {
    const wrapper = mount(FeedItem, {
      props: { post: mockPost },
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    const likeButton = wrapper.find('button');
    expect(likeButton.exists()).toBe(true);
  });

  it('renders comments count', () => {
    const wrapper = mount(FeedItem, {
      props: { post: mockPost },
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
        },
      },
    });

    expect(wrapper.html()).toContain('5 comments');
  });

  it('renders avatar image', () => {
    const wrapper = mount(FeedItem, {
      props: { post: mockPost },
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    const avatar = wrapper.find('img');
    expect(avatar.exists()).toBe(true);
  });

  it('toggles like when button clicked', async () => {
    const wrapper = mount(FeedItem, {
      props: { post: mockPost },
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    await wrapper.find('button').trigger('click');

    const axios = await import('axios');
    expect(axios.default.post).toHaveBeenCalledWith('/api/posts/123/like/');
  });

  it('renders attachment image when post has attachments', () => {
    const postWithImage: Post = {
      ...mockPost,
      attachments: [
        { id: 'att-1', image: '/media/post_attachments/test.png' },
      ],
    };

    const wrapper = mount(FeedItem, {
      props: { post: postWithImage },
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    const images = wrapper.findAll('img');
    // One for avatar + one for attachment
    expect(images.length).toBeGreaterThanOrEqual(2);
    const postImage = images.find(
      img => img.attributes('src') === '/media/post_attachments/test.png',
    );
    expect(postImage).toBeTruthy();
  });

  it('does not render attachment image when post has no attachments', () => {
    const wrapper = mount(FeedItem, {
      props: { post: mockPost },
      global: {
        stubs: {
          RouterLink: true,
        },
      },
    });

    const images = wrapper.findAll('img');
    // Only the avatar image -- no attachment image
    expect(images.length).toBe(1);
  });
});