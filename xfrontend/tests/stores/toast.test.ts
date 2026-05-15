import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useToastStore } from '@/stores/toast';

describe('useToastStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('has correct initial state', () => {
    const toastStore = useToastStore();
    expect(toastStore.milliseconds).toBe(0);
    expect(toastStore.message).toBe('');
    expect(toastStore.classes).toBe('');
    expect(toastStore.isVisible).toBe(false);
  });

  it('showToast sets state correctly', () => {
    const toastStore = useToastStore();
    toastStore.showToast(5000, 'Test message', 'bg-emerald-500');

    expect(toastStore.milliseconds).toBe(5000);
    expect(toastStore.message).toBe('Test message');
    expect(toastStore.classes).toContain('bg-emerald-500');
    expect(toastStore.isVisible).toBe(true);
  });

  it('showToast adds translate class after 10ms', async () => {
    const toastStore = useToastStore();
    toastStore.showToast(5000, 'Test message', 'bg-emerald-500');

    // Before animation delay
    expect(toastStore.classes).not.toContain('-translate-y-28');

    // After animation delay
    await new Promise((resolve) => setTimeout(resolve, 20));
    expect(toastStore.classes).toContain('-translate-y-28');
  });
});