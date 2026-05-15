import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';

describe('PeopleYouMayKnow', () => {
  it('renders the section title', () => {
    const wrapper = mount(PeopleYouMayKnow);
    expect(wrapper.find('h3').text()).toBe('People you may know');
  });

  it('displays three people items', () => {
    const wrapper = mount(PeopleYouMayKnow);
    const peopleItems = wrapper.findAll('.space-y-4');
    expect(peopleItems.length).toBe(3);
  });

  it('has show buttons for each person', () => {
    const wrapper = mount(PeopleYouMayKnow);
    const buttons = wrapper.findAll('a');
    expect(buttons.length).toBe(3);
    buttons.forEach((btn) => {
      expect(btn.text()).toBe('Show');
    });
  });

  it('displays avatar images', () => {
    const wrapper = mount(PeopleYouMayKnow);
    const images = wrapper.findAll('img');
    expect(images.length).toBe(3);
    images.forEach((img) => {
      expect(img.attributes('alt')).toBe('avatar');
    });
  });
});