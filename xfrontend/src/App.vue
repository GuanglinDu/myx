<script setup lang="ts">
import { computed } from 'vue';
import axios from 'axios';
import { createAvatar } from '@dicebear/core';
import { adventurer } from '@dicebear/collection';
import ToastComponent from '@/components/ToastComponent.vue';
import NotificationsComponent from '@/components/NotificationsComponent.vue';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();

userStore.initStore();

const avatarDataUri = computed(() =>
  createAvatar(adventurer, {
    seed: userStore.user.id,
    size: 40,
  }).toDataUri()
);

// Makes the login persistent
const token: string = userStore.user.access;
if (token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
} else {
  axios.defaults.headers.common["Authorization"] = "";
}
</script>

<template>
  <nav class="py-10 px-8 border-b border-gray-200">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">
        <div class="menu-left">
          <a href="#" class="text-xl">xfrontend</a>
        </div>

        <!-- The home menu. The SVG source: http://heroicons.com -->         
        <div
          class="menu-center flex space-x-12"
          v-if="userStore.user.isAuthenticated"
        >
          <a href="#" class="text-purple-700">
            <svg xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-6"
            >
              <path stroke-linecap="round"
                stroke-linejoin="round"
                d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
            </svg>
          </a>

          <!-- The chat menu -->
          <a href="#" class="text-black">
            <svg xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-6"
            >
              <path stroke-linecap="round"
                stroke-linejoin="round"
                d="M2.25 12.76c0 1.6 1.123 2.994 2.707 3.227 1.068.157 2.148.279 3.238.364.466.037.893.281 1.153.671L12 21l2.652-3.978c.26-.39.687-.634 1.153-.67 1.09-.086 2.17-.208 3.238-.365 1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
            </svg>
          </a>

          <!-- The notification menu -->
          <NotificationsComponent />

          <!-- The search menu -->
          <RouterLink to="/search" class="text-black">
            <svg xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-6"
            >
              <path stroke-linecap="round"
                stroke-linejoin="round"
                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
          </RouterLink>
        </div>

        <!-- https://i.pravatar.cc/40?img=70 is blocked! -->
        <div class="menu-right">
          <template v-if="userStore.user.isAuthenticated">
            <RouterLink
              :to="{'name': 'profile', params: { id: userStore.user.id }}"
              class="flex items-center space-x-2">
              <img
                :src="avatarDataUri"
                alt="avatar"
                class="rounded-full"
              />
            </RouterLink>
          </template>
          <template v-else>
            <RouterLink
              to="/login" 
              class="py-4 px-6 bg-gray-600 text-white rounded-lg"
            >
              Log in
            </RouterLink>
            <RouterLink
              to="/signup" 
              class="py-4 px-6 bg-purple-600 text-white rounded-lg ml-4"
            >
              Sign up
            </RouterLink>
          </template>
        </div>

      </div>
    </div>
  </nav>

  <main class="px-8 py-6 bg-gray-100">
    <RouterView />
  </main>

  <ToastComponent />
</template>
