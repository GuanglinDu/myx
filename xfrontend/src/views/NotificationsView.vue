<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios, { type AxiosResponse } from "axios";
import { createAvatar } from "@dicebear/core";
import { adventurer } from "@dicebear/collection";
import type { FriendshipRequest, User } from "@/types/custom_types";
import { useUserStore } from "@/stores/user";

interface XNotification {
  id: string;
  body: string;
  is_read: boolean;
  type_of_notification: string;
  post_id: string; // not post
  created_by: User;
  created_for: User;
}

const $router = useRouter();

const userStore = useUserStore();
const requests = ref<FriendshipRequest[]>([]);
const isLoading = ref<boolean>(false);
const showDropdown = ref<boolean>(false);
const notifications = ref<XNotification[]>([]);

function getAvatarUri(userId: string): string {
  return createAvatar(adventurer, {
    seed: userId,
    size: 40,
  }).toDataUri();
}

async function fetchRequests(): Promise<void> {
  isLoading.value = true;
  try {
    const response: AxiosResponse = await axios.get(
      `/api/friends/${userStore.user.id}/requests/`,
    );
    requests.value = response.data;
  } catch (error) {
    console.error("Error fetching requests:", error);
  } finally {
    isLoading.value = false;
  }
}

async function acceptRequest(requestId: string): Promise<void> {
  try {
    await axios.post(`/api/friends/accept/${requestId}/`);
    requests.value = requests.value.filter((r) => r.id !== requestId);
  } catch (error) {
    console.error("Error accepting request:", error);
  }
}

async function rejectRequest(requestId: string): Promise<void> {
  try {
    await axios.post(`/api/friends/reject/${requestId}/`);
    requests.value = requests.value.filter((r) => r.id !== requestId);
  } catch (error) {
    console.error("Error rejecting request:", error);
  }
}

function toggleDropdown(): void {
  showDropdown.value = !showDropdown.value;
  if (showDropdown.value && requests.value.length === 0) {
    fetchRequests();
  }
}

async function getNotifications(): Promise<void> {
  console.log("getNotifications...");

  try {
    const response: AxiosResponse = await axios.get(`/api/notifications/`);

    console.log(response.data);
    notifications.value = response.data;
  } catch (error) {
    console.error("Error getting notifications", error);
  }
}

function extractUserId(createdBy: User | string): string {
  if (typeof createdBy === "string") {
    return createdBy;
  }
  if (createdBy && typeof createdBy.id === "string") {
    return createdBy.id;
  }
  console.error("Invalid created_by:", createdBy);
  return "";
}

async function readNotification(notification: XNotification): Promise<void> {
  console.log("readNotification: ", notification.id);

  try {
    await axios.post(`/api/notifications/read/${notification.id}/`);

    if (
      notification.type_of_notification == "post_like" ||
      notification.type_of_notification == "post_comment"
    ) {
      const postId = notification.post_id;
      if (!postId) {
        console.error("Missing post_id for notification", notification.id);
        return;
      }
      await $router.push({
        name: "postview",
        params: { id: postId },
      });
    } else {
      const userId = extractUserId(notification.created_by);
      if (!userId) {
        console.error(
          "Missing created_by id for notification", notification.id);
        return;
      }
      await $router.push({
        name: "friends",
        params: { id: userId },
      });
    }
  } catch (error) {
    console.error("Error in readNotification:", error);
  }
}

onMounted(() => {
  fetchRequests();
  getNotifications();
});
</script>

<template>
  <div class="relative">
    <!-- Notification bell icon -->
    <button
      @click="toggleDropdown"
      class="relative text-black hover:text-purple-600"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0M3.124 7.5A8.969 8.969 0 0 1 5.292 3m13.416 0a8.969 8.969 0 0 1 2.168 4.5"
        />
      </svg>

      <!-- Badge showing number of pending requests -->
      <span
        v-if="requests.length > 0"
        class="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-xs text-white"
      >
        {{ requests.length }} requests out of
        {{ notifications.length }} notifications.
      </span>
    </button>

    <!-- Dropdown -->
    <div
      v-if="showDropdown"
      class="absolute right-0 z-50 mt-2 w-80 rounded-lg border border-gray-200 bg-white shadow-lg"
    >
      <div class="border-b border-gray-200 p-3">
        <h3 class="font-semibold">Notifications</h3>
      </div>

      <div v-if="isLoading" class="p-4 text-center text-gray-500">
        Loading...
      </div>

      <div
        v-else-if="requests.length === 0 && notifications.length === 0"
        class="p-4 text-center text-gray-500"
      >
        No pending requests
      </div>

      <div v-else class="max-h-96 overflow-y-auto">
        <div
          v-for="request in requests"
          :key="request.id"
          class="flex items-center justify-between border-b border-gray-100 p-3"
        >
          <div class="flex items-center space-x-3">
            <img
              :src="getAvatarUri(request.created_by.id)"
              alt="avatar"
              class="h-10 w-10 rounded-full"
            />
            <div>
              <p class="text-sm font-medium">
                {{ request.created_by.name }}
              </p>
              <p class="text-xs text-gray-500">wants to be your friend</p>
            </div>
          </div>
          <div class="flex space-x-2">
            <button
              @click="acceptRequest(request.id)"
              class="rounded-lg bg-green-600 px-3 py-1 text-xs text-white hover:bg-green-700"
            >
              Accept
            </button>
            <button
              @click="rejectRequest(request.id)"
              class="rounded-lg bg-red-500 px-3 py-1 text-xs text-white hover:bg-red-600"
            >
              Reject
            </button>
          </div>
        </div>
      </div>

      <!-- List all notifications -->
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="flex items-center justify-between p-1"
      >
        <p class="text-xs font-normal">
          {{ notification.body }}
        </p>
        <button class="underline" @click="readNotification(notification)">
          Read more
        </button>
      </div>
    </div>
  </div>
</template>
