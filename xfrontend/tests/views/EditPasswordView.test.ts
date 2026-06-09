import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { setActivePinia, createPinia } from 'pinia';
import EditPasswordView from '@/views/EditPasswordView.vue';
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
vi.mock('axios', () => ({
  default: {
    post: (...args: unknown[]) => axiosPost(...args),
    defaults: { headers: { common: {} } },
  },
}));

describe('EditPasswordView', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
    vi.clearAllMocks();
    axiosPost.mockReset();
  });

  it('renders the form with three password fields and a submit button',
     () => {
       const wrapper = mount(EditPasswordView);
       const currentInput = wrapper.find('#currentPassword');
       const newInput = wrapper.find('#newPassword');
       const confirmInput = wrapper.find('#confirmNewPassword');
       const button = wrapper.find('button[type="submit"]');

       expect(currentInput.exists()).toBe(true);
       expect(currentInput.attributes('type')).toBe('password');
       expect(newInput.exists()).toBe(true);
       expect(newInput.attributes('type')).toBe('password');
       expect(confirmInput.exists()).toBe(true);
       expect(confirmInput.attributes('type')).toBe('password');
       expect(button.exists()).toBe(true);
       expect(button.text()).toBe('Update Password');
       expect(wrapper.find('h2').text()).toBe('Edit Password');
     });

  it('shows an error toast when new password is too short',
     async () => {
       const toastModule = await import('@/stores/toast');
       const showToastSpy = vi.spyOn(
         toastModule.useToastStore(), 'showToast');

       const wrapper = mount(EditPasswordView);
       await wrapper.find('#currentPassword').setValue('oldpassword1');
       await wrapper.find('#newPassword').setValue('short');
       await wrapper.find('#confirmNewPassword').setValue('short');
       await wrapper.find('form').trigger('submit.prevent');

       expect(showToastSpy).toHaveBeenCalledWith(
         5000,
         'New password must be at least 8 characters',
         'bg-red-300',
       );
       expect(axiosPost).not.toHaveBeenCalled();
     });

  it('shows an error toast when confirmation does not match',
     async () => {
       const toastModule = await import('@/stores/toast');
       const showToastSpy = vi.spyOn(
         toastModule.useToastStore(), 'showToast');

       const wrapper = mount(EditPasswordView);
       await wrapper.find('#currentPassword').setValue('oldpassword1');
       await wrapper.find('#newPassword').setValue('newpassword456');
       await wrapper.find('#confirmNewPassword').setValue('different99');
       await wrapper.find('form').trigger('submit.prevent');

       expect(showToastSpy).toHaveBeenCalledWith(
         5000,
         'New passwords do not match',
         'bg-red-300',
       );
       expect(axiosPost).not.toHaveBeenCalled();
     });

  it('shows an error toast when new password equals current password',
     async () => {
       const toastModule = await import('@/stores/toast');
       const showToastSpy = vi.spyOn(
         toastModule.useToastStore(), 'showToast');

       const wrapper = mount(EditPasswordView);
       await wrapper.find('#currentPassword').setValue('samepassword1');
       await wrapper.find('#newPassword').setValue('samepassword1');
       await wrapper.find('#confirmNewPassword').setValue('samepassword1');
       await wrapper.find('form').trigger('submit.prevent');

       expect(showToastSpy).toHaveBeenCalledWith(
         5000,
         'New password must differ from the current password',
         'bg-red-300',
       );
       expect(axiosPost).not.toHaveBeenCalled();
     });

  it('posts to the editpassword API and redirects on success',
     async () => {
       const userStore = useUserStore();
       userStore.setUserInfo({
         id: 'user-1',
         name: 'Test User',
         email: 'test@example.com',
         access: '',
         refresh: '',
         avatar: '',
         isAuthenticated: true,
       });

       axiosPost.mockResolvedValue({ data: { message: 'Password updated' } });

       const toastModule = await import('@/stores/toast');
       const showToastSpy = vi.spyOn(
         toastModule.useToastStore(), 'showToast');

       const wrapper = mount(EditPasswordView);
       await wrapper.find('#currentPassword').setValue('oldpassword1');
       await wrapper.find('#newPassword').setValue('newpassword456');
       await wrapper.find('#confirmNewPassword').setValue('newpassword456');
       await wrapper.find('form').trigger('submit.prevent');
       await flushPromises();

       expect(axiosPost).toHaveBeenCalledWith('/api/editpassword/', {
         currentPassword: 'oldpassword1',
         newPassword: 'newpassword456',
         confirmNewPassword: 'newpassword456',
       });
       expect(showToastSpy).toHaveBeenCalledWith(
         5000,
         'Password updated',
         'bg-emerald-500',
       );
       expect(routerPush).toHaveBeenCalledWith(
         expect.objectContaining({ name: 'profile' }),
       );
     });

  it('shows an error toast when the API returns an error',
     async () => {
       axiosPost.mockRejectedValue({
         response: {
           status: 400,
           data: { error: 'Current password is incorrect' },
         },
       });

       const toastModule = await import('@/stores/toast');
       const showToastSpy = vi.spyOn(
         toastModule.useToastStore(), 'showToast');

       const wrapper = mount(EditPasswordView);
       await wrapper.find('#currentPassword').setValue('wrongcurrent');
       await wrapper.find('#newPassword').setValue('newpassword456');
       await wrapper.find('#confirmNewPassword').setValue('newpassword456');
       await wrapper.find('form').trigger('submit.prevent');
       await flushPromises();

       expect(showToastSpy).toHaveBeenCalledWith(
         5000,
         'Current password is incorrect',
         'bg-red-300',
       );
       expect(routerPush).not.toHaveBeenCalled();
     });
});
