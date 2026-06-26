<script setup lang="ts">
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";

const userStore = useUserStore();
const toastStore = useToastStore();
const $router = useRouter();

// Lightweight client-side check. The backend enforces the same shape.
// This regular expression supports an unlimited number of dots (.). While it
// explicitly requires at least one literal dot after the @ symbol, it does
// not cap the maximum number of dots allowed anywhere in the string.
const EMAIL_RE: RegExp = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

// Form fields are kept in sync with the user store. The store is the
// single source of truth, so typing in the form updates the store and
// vice versa.
const name = ref<string>(userStore.user.name);
const email = ref<string>(userStore.user.email);

watch(name, (value: string) => {
  userStore.user.name = value;
});

watch(email, (value: string) => {
  userStore.user.email = value;
});

// If the active user changes (e.g. after a re-login), pull the latest
// values back into the form.
watch(
  () => userStore.user.id,
  () => {
    name.value = userStore.user.name;
    email.value = userStore.user.email;
  },
);

async function submitForm(): Promise<void> {
  if (!name.value.trim()) {
    toastStore.showToast(5000, "Your name is missing", "bg-red-300");
    return;
  }

  if (!EMAIL_RE.test(email.value.trim())) {
    toastStore.showToast(5000, "Enter a valid e-mail address", "bg-red-300");
    return;
  }

  try {
    const response = await axios.post("/api/editprofile/", {
      name: name.value.trim(),
      email: email.value.trim(),
    });

    userStore.setUserInfo({
      ...userStore.user,
      name: response.data.name,
      email: response.data.email,
    });

    toastStore.showToast(5000, "Profile updated", "bg-emerald-500");
    // Navigate to the profile page to show the updated info. This also serves
    // as a confirmation that the update was successful.
    $router.push({ name: "profile", params: { id: userStore.user.id } });
  } catch (error: unknown) {
    // Avoid relying on axios.isAxiosError so this also works under mocks
    // and in any caller that throws a plain object.
    const responseError: string | undefined = (
      error as { response?: { data?: { error?: string } } }
    )?.response?.data?.error;
    const message: string =
      responseError ?? "Could not update profile. Please try again.";
    toastStore.showToast(5000, message, "bg-red-300");
  }
}
</script>

<template>
  <div class="mx-auto grid max-w-7xl grid-cols-2 gap-4">
    <div class="main-left">
      <div class="rounded-lg border border-gray-200 bg-white p-12">
        <h1 class="mb-6 text-2xl">Edit profile</h1>
        <p class="mb-6 text-gray-500">
          Update your name and e-mail address. Changes are saved immediately.
        </p>

        <RouterLink to="/profile/editpassword" class="underline">
          Edit Password
        </RouterLink>
      </div>
    </div>

    <div class="main-right">
      <div class="rounded-lg border border-gray-200 bg-white p-12">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>Name</label><br />
            <input
              type="text"
              name="name"
              v-model="name"
              placeholder="Enter your full name"
              class="mt-2 w-full rounded-lg border-gray-200 px-6 py-4"
            />
          </div>

          <div>
            <label>E-mail</label><br />
            <input
              type="email"
              name="email"
              v-model="email"
              placeholder="Enter your e-mail address"
              class="mt-2 w-full rounded-lg border-gray-200 px-6 py-4"
            />
          </div>

          <button class="rounded-lg bg-purple-600 px-6 py-4 text-white">
            Save
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
