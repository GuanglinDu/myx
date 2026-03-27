<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios, { AxiosResponse } from 'axios';

interface FriendshipRequest {
  id: string;
  created_by: string;
  created_by_user: {
    id: string;
    name: string;
    email: string;
  };
  created_at: string;
}

const requests = ref<FriendshipRequest[]>([]);
const isLoading = ref<boolean>(false);
const showDropdown = ref<boolean>(false);

async function fetchRequests(): Promise<void> {
  isLoading.value = true;
  await axios
    .get('/api/friends/requests/')
    .then((response: AxiosResponse) => {
      requests.value = response.data;
    })
    .catch((error: any) => {
      console.error('Error fetching requests:', error);
    })
    .finally(() => {
      isLoading.value = false;
    });
}

async function acceptRequest(requestId: string): Promise<void> {
  await axios
    .post(`/api/friends/accept/${requestId}/`)
    .then((response: AxiosResponse) => {
      console.log('Request accepted:', response.data);
      // Remove from list
      requests.value = requests.value.filter(r => r.id !== requestId);
    })
    .catch((error: any) => {
      console.error('Error accepting request:', error);
    });
}

async function rejectRequest(requestId: string): Promise<void> {
  await axios
    .post(`/api/friends/reject/${requestId}/`)
    .then((response: AxiosResponse) => {
      console.log('Request rejected:', response.data);
      // Remove from list
      requests.value = requests.value.filter(r => r.id !== requestId);
    })
    .catch((error: any) => {
      console.error('Error rejecting request:', error);
    });
}

function toggleDropdown(): void {
  showDropdown.value = !showDropdown.value;
  if (showDropdown.value && requests.value.length === 0) {
    fetchRequests();
  }
}

onMounted(() => {
  fetchRequests();
});
</script>

<template>
  <div class="relative">
    <!-- Notification bell icon -->
    <button
      @click="toggleDropdown"
      class="relative text-black hover:text-purple-600"
    >
      <svg xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-6"
      >
        <path stroke-linecap="round"
          stroke-linejoin="round"
          d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0M3.124 7.5A8.969 8.969 0 0 1 5.292 3m13.416 0a8.969 8.969 0 0 1 2.168 4.5" />
      </svg>

      <!-- Badge showing number of pending requests -->
      <span
        v-if="requests.length > 0"
        class="absolute -top-1 -right-1 bg-red-500 text-white text-xs
               rounded-full w-4 h-4 flex items-center justify-center"
      >
        {{ requests.length }}
      </span>
    </button>

    <!-- Dropdown -->
    <div
      v-if="showDropdown"
      class="absolute right-0 mt-2 w-80 bg-white border border-gray-200
             rounded-lg shadow-lg z-50"
    >
      <div class="p-3 border-b border-gray-200">
        <h3 class="font-semibold">Friend Requests</h3>
      </div>

      <div v-if="isLoading" class="p-4 text-center text-gray-500">
        Loading...
      </div>

      <div v-else-if="requests.length === 0" class="p-4 text-center text-gray-500">
        No pending requests
      </div>

      <div v-else class="max-h-96 overflow-y-auto">
        <div
          v-for="request in requests"
          :key="request.id"
          class="p-3 border-b border-gray-100 flex items-center justify-between"
        >
          <div class="flex items-center space-x-3">
            <img
              src="@/assets/Brian-40x40px.png"
              alt="avatar"
              class="w-10 h-10 rounded-full"
            />
            <div>
              <p class="text-sm font-medium">
                {{ request.created_by_user.name }}
              </p>
              <p class="text-xs text-gray-500">
                wants to be your friend
              </p>
            </div>
          </div>
          <div class="flex space-x-2">
            <button
              @click="acceptRequest(request.id)"
              class="px-3 py-1 bg-green-600 text-white text-xs
                     rounded-lg hover:bg-green-700"
            >
              Accept
            </button>
            <button
              @click="rejectRequest(request.id)"
              class="px-3 py-1 bg-red-500 text-white text-xs
                     rounded-lg hover:bg-red-600"
            >
              Reject
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
