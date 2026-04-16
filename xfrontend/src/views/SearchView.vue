<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { createAvatar } from '@dicebear/core';
import { adventurer } from '@dicebear/collection';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import TrendsComponent from '@/components/TrendsComponent.vue';
import FeedItem from './FeedItem.vue';
import type { Post, User } from '@/types/custom_types';

function getAvatarUri(userId: string): string {
  return createAvatar(adventurer, {
    seed: userId,
    size: 128,
  }).toDataUri();
}

const query = ref<string>('');
const users = ref<Array<User>>([]);
const posts = ref<Array<Post>>([]);

async function submitForm(): Promise<void> {
  console.log('submitForm:', query.value);

  try {
    const response = await axios.post('/api/search/', { query: query.value });
    console.log('Search results:', response.data);
    users.value = response.data.users;
    posts.value = response.data.posts;
  } catch (error) {
    console.error('Error:', error);
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4 ">
    <!-- The main left columns -->
    <div class="main-left col-span-3 space-y-4">
    
      <!-- The search div -->
      <div class="bg-white border border-gray-200 rounded-lg">
        <form @submit.prevent="submitForm" class="p-4 flex space-x-4">
          <input
            type="search"
            v-model="query"
            class="p-4 w-full bg-gray-100 rounded-lg"
            placeholder="What are you looking for?"
          />
          <button
            class="inline-block py-4 px-6 bg-purple-600 text-white
                   rounded-lg"
            type="submit"
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
                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
          </button>
        </form>
      </div>

      <!-- Users found -->
      <div
        v-if="users.length"
        class="p-4 bg-white border border-gray-200 rounded-lg
               grid grid-cols-4 gap-4"
      >
        <div
          class="p-4 text-center bg-gray-100 rounded-lg"
          v-for="user in users"
          :key="user.id"
        >
          <img
            :src="getAvatarUri(user.id)"
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

          <div class="mt-6 flex space-x-8 justify-around">
            <p class="text-xs text-gray-500">182 friends</p>
            <p class="text-xs text-gray-500">120 posts</p>
          </div>
        </div>
      </div>

      <!-- Posts found -->
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        :key="post.id"      
      >
        <FeedItem :post="post" />
      </div>
    </div>

    <!-- (3/3) The main-right column: PeopleYouMayKnow & Trends --> 
    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <TrendsComponent />
    </div>
  </div>
</template>
