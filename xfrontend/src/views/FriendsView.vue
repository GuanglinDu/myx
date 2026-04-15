<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import TrendsComponent from '@/components/TrendsComponent.vue';
import { useUserStore } from '@/stores/user';
import type { Post, User } from '@/types/custom_types';

const userStore = useUserStore();
const $route = useRoute();

const user = ref<User>({} as User);
const friends = ref<User[]>([]);
const friendshipRequests = ref<User[]>([]);

async function getFriends(): Promise<void> {
  await axios
    .get(`/api/friends/${$route.params.id}/`)
    .then((response: AxiosResponse) => {
      console.log('data', response.data);

      friendshipRequests.value = response.data.requests;
      friends.value = response.data.friends;
      user.value = response.data.user;
    })
    .catch((error: any) => {
      console.error('Error fetching feed:', error);
    });
}

onMounted(() => {
  getFriends();
});
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- (1/3) The main-left profile column: avatar, name, & statistics -->
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200
                  text-center rounded-lg">
        <img
          src="@/assets/Brian-200x200px.png"
          alt="avatar"
          class="rounded-full"
        />
        
        <!-- the logged-in user's name vs any user's name
          <p><strong>{{ userStore.user.name }}</strong></p>
        -->
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

    <RouterLink :to="{name: 'search', params: {text:'abc' }}" >Search</RouterLink>
    
    The preceding params attribute will be rendered as a URI with the
      ?text=abc query string (HTTP request URL query string).
    
    As we mentioned, if the route has the props attribute active and the
    receiving component has defined a prop of the same name, the value will
    be automatically assigned.
    -->
    <div class="main-center col-span-2 space-y-4">
      <!-- Ignores empty users array -->
      <div
        v-if="friendshipRequests.length"
        class="p-4 bg-white border border-gray-200 rounded-lg
               grid grid-cols-4 gap-4"
      >
        <div
          class="p-4 text-center bg-gray-100 rounded-lg"
          v-for="user in friendshipRequests"
          :key="user.id"
        >
          <img
            src="@/assets/Brian-200x200px.png"
            alt="avatar"
            class="rounded-full"
          />
          
          <p>
            <strong>
              <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
                {{ user.name }}
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
