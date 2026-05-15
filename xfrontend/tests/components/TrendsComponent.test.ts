import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import TrendsComponent from '@/components/TrendsComponent.vue';

describe('TrendsComponent', () => {
  it('renders the trends title', () => {
    const wrapper = mount(TrendsComponent);
    expect(wrapper.find('h3').text()).toBe('Trends');
  });

  it('displays four trend items', () => {
    const wrapper = mount(TrendsComponent);
    const trendItems = wrapper.findAll('.space-y-4');
    expect(trendItems.length).toBe(4);
  });

  it('displays the hashtag in each trend', () => {
    const wrapper = mount(TrendsComponent);
    const hashtags = wrapper.findAll('strong');
    hashtags.forEach((el) => {
      expect(el.text()).toContain('#codewithguanglin');
    });
  });

  it('has explore buttons for each trend', () => {
    const wrapper = mount(TrendsComponent);
    const buttons = wrapper.findAll('a');
    expect(buttons.length).toBe(4);
    buttons.forEach((btn) => {
      expect(btn.text()).toBe('Explore');
    });
  });
});