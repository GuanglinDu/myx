<script setup lang="ts">
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { createAvatar } from '@dicebear/core';
import { adventurer } from '@dicebear/collection';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import TrendsComponent from '@/components/TrendsComponent.vue';
import type { User, FriendshipRequest } from '@/types/custom_types';

const $route = useRoute();

const user = ref<User>({} as User);
const friends = ref<User[]>([]);
const friendshipRequests = ref<FriendshipRequest[]>([]);

function getAvatarUri(userId: string): string {
  return createAvatar(adventurer, {
    seed: userId,
    size: 128,
  }).toDataUri();
}

async function getFriends(): Promise<void> {
  try {
    const response = await axios.get(`/api/friends/${$route.params.id}/`);
    console.log('data', response.data);
    friendshipRequests.value = response.data.friendshipRequests;
    friends.value = response.data.friends;
    user.value = response.data.user;
  } catch (error) {
    console.error('Error fetching friends:', error);
  }
}

async function acceptRequest(requestId: string): Promise<void> {
  try {
    await axios.post(`/api/friends/accept/${requestId}/`);
    friendshipRequests.value = friendshipRequests.value.filter(
      r => r.id !== requestId
    );
  } catch (error) {
    console.error('Error accepting request:', error);
  }
}

async function rejectRequest(requestId: string): Promise<void> {
  try {
    await axios.post(`/api/friends/reject/${requestId}/`);
    friendshipRequests.value = friendshipRequests.value.filter(
      r => r.id !== requestId
    );
  } catch (error) {
    console.error('Error rejecting request:', error);
  }
}

onMounted(() => {
  getFriends();
});
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- (1/3) The main-left profile column.
         The logged-in user: avatar, name, & statistics -->
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200
                  text-center rounded-lg">
        <img
          :src="getAvatarUri(user.id)"
          alt="avatar"
          class="rounded-full"
        />
        
        <p><strong>{{ user.name }}</strong></p>

        <div class="mt-6 flex space-x-8 justify-around">
          <p class="text-xs text-gray-500">
            {{ user.friends_count || 0 }} friends
          </p>
          <p class="text-xs text-gray-500">
            {{ user.posts_count || 0 }} posts
          </p>
        </div>

      </div>
    </div>

    <!-- Friend list
    Page 116/287, 5.3.4 Router template components, Vue.js 3 Design Patterns
    and Best Practices, Pablo David Garaguso, 2023

    <RouterLink :to="{name:'search', params:{text:'abc' }}">Search</RouterLink>
    
    The preceding params attribute will be rendered as a URI with the
    ?text=abc query string (HTTP request URL query string).
    
    As we mentioned, if the route has the props attribute active and the
    receiving component has defined a prop of the same name, the value will
    be automatically assigned.
    -->
    <div class="main-center col-span-2 space-y-4">
      <!-- Pending friendship requests -->
      <div
        v-if="friendshipRequests.length"
        class="p-4 bg-white border border-gray-200 rounded-lg"
      >
        <h2 class="text-lg font-semibold mb-4">Pending Requests</h2>
        <div
          v-for="request in friendshipRequests"
          :key="request.id"
          class="p-4 border-b border-gray-100 last:border-0 flex items-center
                 justify-between"
        >
          <div class="flex items-center space-x-3">
            <img
              :src="getAvatarUri(request.created_by.id)"
              alt="avatar"
              class="w-12 h-12 rounded-full"
            />
            <div>
              <RouterLink
                :to="{ name: 'profile', params: { id: request.created_by.id } }"
                class="font-medium hover:underline"
              >
                {{ request.created_by.name }}
              </RouterLink>
              <p class="text-xs text-gray-500">wants to be your friend</p>
            </div>
          </div>
          <div class="flex space-x-2">
            <button
              @click="acceptRequest(request.id)"
              class="px-3 py-1 bg-green-600 text-white text-xs rounded-lg
                   hover:bg-green-700"
            >
              Accept
            </button>
            <button
              @click="rejectRequest(request.id)"
              class="px-3 py-1 bg-red-500 text-white text-xs rounded-lg hover:bg-red-600"
            >
              Reject
            </button>
          </div>
        </div>
      </div>

      <!-- Friends list -->
      <div
        v-if="friends.length"
        class="p-4 bg-white border border-gray-200 rounded-lg
               grid grid-cols-4 gap-4"
      >
        <div
          class="p-4 text-center bg-gray-100 rounded-lg"
          v-for="friend in friends"
          :key="friend.id"
        >
          <img
            :src="getAvatarUri(friend.id)"
            alt="avatar"
            class="rounded-full"
          />

          <p>
            <strong>
              <RouterLink :to="{ name: 'profile', params: { id: friend.id } }">
                {{ friend.name }}
              </RouterLink>
            </strong>
          </p>
        </div>
      </div>
    </div>

    <!-- (3/3) The main-right column: PeopleYouMayKnow & Trends --> 
    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <TrendsComponent />
    </div>
  </div>
</template>
