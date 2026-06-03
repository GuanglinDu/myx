import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { setActivePinia, createPinia } from 'pinia';
import EditProfileView from '@/views/EditProfileView.vue';
import { useUserStore } from '@/stores/user';

// Mock vue-router so navigation can be observed.
const routerPush = vi.fn();
vi.mock('vue-router', async () => {
  const actual = await vi.importActual('vue-router');
  return {
    ...actual,
    useRouter: () => ({ push: routerPush }),
  };
});

// Mock axios. The post mock is reassignable per test.
const axiosPost = vi.fn();
const axiosGet = vi.fn();
vi.mock('axios', () => ({
  default: {
    post: (...args: unknown[]) => axiosPost(...args),
    get: (...args: unknown[]) => axiosGet(...args),
    defaults: { headers: { common: {} } },
  },
}));

describe('EditProfileView', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
    vi.clearAllMocks();
    axiosPost.mockReset();
    axiosGet.mockReset();
  });

  it('renders the edit profile form with title and fields', () => {
    const wrapper = mount(EditProfileView, {
      global: {
        stubs: { RouterLink: { template: '<a><slot /></a>' } },
      },
    });

    expect(wrapper.find('h1').text()).toBe('Edit profile');
    expect(wrapper.find('input[name="name"]').exists()).toBe(true);
    expect(wrapper.find('input[name="email"]').exists()).toBe(true);
    expect(wrapper.find('button').text()).toBe('Save');
  });

  it('pre-fills name and email from the user store on mount', () => {
    const userStore = useUserStore();
    userStore.setUserInfo({
      id: 'user-1',
      name: 'Stored Name',
      email: 'stored@example.com',
      access: '',
      refresh: '',
      avatar: '',
      isAuthenticated: true,
    });

    const wrapper = mount(EditProfileView, {
      global: {
        stubs: { RouterLink: { template: '<a><slot /></a>' } },
      },
    });

    const nameInput = wrapper.find('input[name="name"]')
      .element as HTMLInputElement;
    const emailInput = wrapper.find('input[name="email"]')
      .element as HTMLInputElement;

    expect(nameInput.value).toBe('Stored Name');
    expect(emailInput.value).toBe('stored@example.com');
  });

  it('keeps the user store values in sync as the user types', async () => {
    const userStore = useUserStore();
    userStore.setUserInfo({
      id: 'user-1',
      name: 'Stored Name',
      email: 'stored@example.com',
      access: '',
      refresh: '',
      avatar: '',
      isAuthenticated: true,
    });

    const wrapper = mount(EditProfileView, {
      global: {
        stubs: { RouterLink: { template: '<a><slot /></a>' } },
      },
    });

    await wrapper.find('input[name="name"]').setValue('New Name');
    await wrapper.find('input[name="email"]')
      .setValue('new@example.com');

    expect(userStore.user.name).toBe('New Name');
    expect(userStore.user.email).toBe('new@example.com');
  });

  it('shows an error toast when name is blank on submit', async () => {
    const userStore = useUserStore();
    userStore.setUserInfo({
      id: 'user-1',
      name: '   ',
      email: 'test@example.com',
      access: '',
      refresh: '',
      avatar: '',
      isAuthenticated: true,
    });

    const toastModule = await import('@/stores/toast');
    const showToastSpy = vi.spyOn(toastModule.useToastStore(), 'showToast');

    const wrapper = mount(EditProfileView, {
      global: {
        stubs: { RouterLink: { template: '<a><slot /></a>' } },
      },
    });

    await wrapper.find('form').trigger('submit.prevent');

    expect(showToastSpy).toHaveBeenCalledWith(
      5000,
      'Your name is missing',
      'bg-red-300',
    );
    expect(axiosPost).not.toHaveBeenCalled();
  });

  it('shows an error toast when email is invalid on submit', async () => {
    const userStore = useUserStore();
    userStore.setUserInfo({
      id: 'user-1',
      name: 'Test User',
      email: 'not-an-email',
      access: '',
      refresh: '',
      avatar: '',
      isAuthenticated: true,
    });

    const toastModule = await import('@/stores/toast');
    const showToastSpy = vi.spyOn(toastModule.useToastStore(), 'showToast');

    const wrapper = mount(EditProfileView, {
      global: {
        stubs: { RouterLink: { template: '<a><slot /></a>' } },
      },
    });

    await wrapper.find('form').trigger('submit.prevent');

    expect(showToastSpy).toHaveBeenCalledWith(
      5000,
      'Enter a valid e-mail address',
      'bg-red-300',
    );
    expect(axiosPost).not.toHaveBeenCalled();
  });

  it('posts to the editme API and updates the store on success',
     async () => {
       const userStore = useUserStore();
       userStore.setUserInfo({
         id: 'user-1',
         name: 'Old Name',
         email: 'old@example.com',
         access: '',
         refresh: '',
         avatar: '',
         isAuthenticated: true,
       });

       axiosPost.mockResolvedValue({
         data: { id: 'user-1', name: 'New Name',
                 email: 'new@example.com' },
       });

       const wrapper = mount(EditProfileView, {
         global: {
           stubs: { RouterLink: { template: '<a><slot /></a>' } },
         },
       });

       await wrapper.find('input[name="name"]').setValue('New Name');
       await wrapper.find('input[name="email"]')
         .setValue('new@example.com');
       await wrapper.find('form').trigger('submit.prevent');
       await flushPromises();

       expect(axiosPost).toHaveBeenCalledWith('/api/editme/', {
         name: 'New Name',
         email: 'new@example.com',
       });

       expect(userStore.user.name).toBe('New Name');
       expect(userStore.user.email).toBe('new@example.com');
       expect(localStorage.getItem('user.name')).toBe('New Name');
       expect(localStorage.getItem('user.email')).toBe('new@example.com');

       expect(routerPush).toHaveBeenCalledWith(
         expect.objectContaining({ name: 'profile' }),
       );
     });

  it('shows an error toast when the API returns an error',
     async () => {
       const userStore = useUserStore();
       userStore.setUserInfo({
         id: 'user-1',
         name: 'Test User',
         email: 'taken@example.com',
         access: '',
         refresh: '',
         avatar: '',
         isAuthenticated: true,
       });

       axiosPost.mockRejectedValue({
         response: {
           status: 400,
           data: { error: 'This e-mail is already in use' },
         },
       });

       const toastModule = await import('@/stores/toast');
       const showToastSpy = vi.spyOn(toastModule.useToastStore(), 'showToast');

       const wrapper = mount(EditProfileView, {
         global: {
           stubs: { RouterLink: { template: '<a><slot /></a>' } },
         },
       });

       await wrapper.find('form').trigger('submit.prevent');
       await flushPromises();

       expect(showToastSpy).toHaveBeenCalledWith(
         5000,
         'This e-mail is already in use',
         'bg-red-300',
       );
       // Store values should not change.
       expect(userStore.user.email).toBe('taken@example.com');
       expect(routerPush).not.toHaveBeenCalled();
     });
});
