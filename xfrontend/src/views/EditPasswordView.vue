<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";

const userStore = useUserStore();
const toastStore = useToastStore();
const $router = useRouter();

const currentPassword = ref<string>("");
const newPassword = ref<string>("");
const confirmNewPassword = ref<string>("");

// Client-side checks mirror the backend's password rules so the user gets
// immediate feedback. The backend re-validates and is the source of truth.
const MIN_PASSWORD_LENGTH = 8;

async function submitForm(): Promise<void> {
  if (newPassword.value.length < MIN_PASSWORD_LENGTH) {
    toastStore.showToast(
      5000,
      "New password must be at least 8 characters",
      "bg-red-300",
    );
    return;
  }

  if (newPassword.value !== confirmNewPassword.value) {
    toastStore.showToast(
      5000,
      "New passwords do not match",
      "bg-red-300",
    );
    return;
  }

  if (newPassword.value === currentPassword.value) {
    toastStore.showToast(
      5000,
      "New password must differ from the current password",
      "bg-red-300",
    );
    return;
  }

  try {
    await axios.post("/api/editpassword/", {
      currentPassword: currentPassword.value,
      newPassword: newPassword.value,
      confirmNewPassword: confirmNewPassword.value,
    });

    toastStore.showToast(5000, "Password updated", "bg-emerald-500");
    // Redirect to the profile page to confirm the change took effect.
    $router.push({ name: "profile", params: { id: userStore.user.id } });
  } catch (error: unknown) {
    // Avoid relying on axios.isAxiosError so this also works under mocks
    // and in any caller that throws a plain object.
    const responseError: string | undefined = (
      error as { response?: { data?: { error?: string } } }
    )?.response?.data?.error;
    const message: string =
      responseError ?? "Could not update password. Please try again.";
    toastStore.showToast(5000, message, "bg-red-300");
  }
}
</script>

<template>
  <div class="mx-auto max-w-2xl rounded-lg border border-gray-200 bg-white p-4">
    <h2 class="mb-4 text-xl font-bold">Edit Password</h2>

    <form @submit.prevent="submitForm" class="space-y-4">
      <div>
        <label
          for="currentPassword"
          class="block text-sm font-medium text-gray-700"
        >
          Current Password
        </label>
        <input
          id="currentPassword"
          type="password"
          v-model="currentPassword"
          required
          class="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        />
      </div>

      <div>
        <label
          for="newPassword"
          class="block text-sm font-medium text-gray-700"
        >
          New Password
        </label>
        <input
          id="newPassword"
          type="password"
          v-model="newPassword"
          required
          class="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        />
      </div>

      <div>
        <label
          for="confirmNewPassword"
          class="block text-sm font-medium text-gray-700"
        >
          Confirm New Password
        </label>
        <input
          id="confirmNewPassword"
          type="password"
          v-model="confirmNewPassword"
          required
          class="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        />
      </div>

      <button
        type="submit"
        class="w-full rounded-lg bg-purple-600 py-3 text-sm text-white hover:bg-purple-700"
      >
        Update Password
      </button>
    </form>
  </div>
</template>
