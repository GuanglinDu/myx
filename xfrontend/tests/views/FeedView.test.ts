import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
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

// Mock URL.createObjectURL and URL.revokeObjectURL (not available in jsdom)
const mockObjectUrl = 'blob:http://localhost/mock-image-preview';
const createObjectURLSpy = vi.fn(() => mockObjectUrl);
const revokeObjectURLSpy = vi.fn();

function mountFeedView() {
  return mount(FeedView, {
    global: {
      stubs: {
        RouterLink: true,
        PeopleYouMayKnow: true,
        TrendsComponent: true,
        FeedItem: true,
      },
    },
  });
}

function createMockFile(): File {
  return new File(['dummy-image-data'], 'test-image.png', {
    type: 'image/png',
  });
}

async function selectFile(wrapper: ReturnType<typeof mount>, file: File) {
  const input = wrapper.find('input[type="file"]');
  const dt = new DataTransfer();
  dt.items.add(file);
  (input.element as HTMLInputElement).files = dt.files;
  await input.trigger('change');
}

describe('FeedView', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
    URL.createObjectURL = createObjectURLSpy;
    URL.revokeObjectURL = revokeObjectURLSpy;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders the feed view', () => {
    const wrapper = mountFeedView();
    expect(wrapper.find('textarea').exists()).toBe(true);
  });

  it('renders textarea for post content', () => {
    const wrapper = mountFeedView();

    const textarea = wrapper.find('textarea');
    expect(textarea.exists()).toBe(true);
    expect(textarea.attributes('placeholder'))
      .toContain('What are you curious about');
  });

  it('has Post button', () => {
    const wrapper = mountFeedView();

    const buttons = wrapper.findAll('button');
    expect(buttons.some(b => b.text() === 'Post')).toBe(true);
  });

  it('has file input for image upload', () => {
    const wrapper = mountFeedView();

    const fileInput = wrapper.find('input[type="file"]');
    expect(fileInput.exists()).toBe(true);
    expect(fileInput.attributes('accept')).toBe('image/*');
  });

  it('has Attach image label that triggers file input', () => {
    const wrapper = mountFeedView();

    const fileInput = wrapper.find('input[type="file"]');
    expect(fileInput.exists()).toBe(true);
  });

  describe('image preview', () => {
    it('does not show image preview when no file is selected', () => {
      const wrapper = mountFeedView();

      const preview = wrapper.find('img[data-testid="image-preview"]');
      expect(preview.exists()).toBe(false);
    });

    it('shows image preview after a file is selected', async () => {
      const wrapper = mountFeedView();
      const file = createMockFile();

      await selectFile(wrapper, file);

      const preview = wrapper.find('img[data-testid="image-preview"]');
      expect(preview.exists()).toBe(true);
    });

    it('uses URL.createObjectURL for the preview source', async () => {
      const wrapper = mountFeedView();
      const file = createMockFile();

      await selectFile(wrapper, file);

      expect(createObjectURLSpy).toHaveBeenCalledWith(file);
      const preview = wrapper.find('img[data-testid="image-preview"]');
      expect(preview.attributes('src')).toBe(mockObjectUrl);
    });

    it('hides image preview when Remove button is clicked', async () => {
      const wrapper = mountFeedView();
      const file = createMockFile();

      await selectFile(wrapper, file);

      expect(wrapper.find('img[data-testid="image-preview"]').exists())
        .toBe(true);

      const removeButton = wrapper.find('button[type="button"]');
      await removeButton.trigger('click');

      expect(wrapper.find('img[data-testid="image-preview"]').exists())
        .toBe(false);
    });

    it('revokes object URL when Remove button is clicked', async () => {
      const wrapper = mountFeedView();
      const file = createMockFile();

      await selectFile(wrapper, file);

      const removeButton = wrapper.find('button[type="button"]');
      await removeButton.trigger('click');

      expect(revokeObjectURLSpy).toHaveBeenCalledWith(mockObjectUrl);
    });

    it('hides image preview after successful form submission', async () => {
      const axios = (await import('axios')).default;
      const wrapper = mountFeedView();
      const file = createMockFile();

      await selectFile(wrapper, file);

      expect(wrapper.find('img[data-testid="image-preview"]').exists())
        .toBe(true);

      await wrapper.find('form').trigger('submit.prevent');

      // Wait for async submitForm to complete
      await wrapper.vm.$nextTick();

      expect(wrapper.find('img[data-testid="image-preview"]').exists())
        .toBe(false);
    });

    it('shows selected file name after selection', async () => {
      const wrapper = mountFeedView();
      const file = createMockFile();

      await selectFile(wrapper, file);

      expect(wrapper.text()).toContain('test-image.png');
    });
  });
});