import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import ToastComponent from '@/components/ToastComponent.vue';
import { setActivePinia, createPinia } from 'pinia';

describe('ToastComponent', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('is not visible when toastStore.isVisible is false', () => {
    const wrapper = mount(ToastComponent);
    // v-if hides the element when isVisible is false, so find returns empty
    expect(wrapper.find('div').exists()).toBe(false);
  });

  it('displays message when toastStore.isVisible is true', async () => {
    const { useToastStore } = await import('@/stores/toast');
    const toastStore = useToastStore();

    toastStore.showToast(5000, 'Test message', 'bg-emerald-500');

    const wrapper = mount(ToastComponent);
    expect(wrapper.text()).toContain('Test message');
  });

  it('applies CSS classes from toastStore', async () => {
    const { useToastStore } = await import('@/stores/toast');
    const toastStore = useToastStore();

    toastStore.showToast(5000, 'Test', 'bg-emerald-500');

    const wrapper = mount(ToastComponent);
    const div = wrapper.find('div');
    expect(div.classes()).toContain('bg-emerald-500');
  });
});