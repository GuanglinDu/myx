<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
const $router = useRouter();

const currentPassword = ref<string>("");
const newPassword = ref<string>("");
const confirmNewPassword = ref<string>("");
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
