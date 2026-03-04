<script setup lang="ts">
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useRoute, onBeforeRouteUpdate } from 'vue-router';
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import TrendsComponent from '@/components/TrendsComponent.vue';
import FeedItem from './FeedItem.vue';
import { useUserStore } from '@/stores/user';
import type { Post, User } from '@/types/custom_types';

const userStore = useUserStore();
const $route = useRoute();

const user = ref<User>({} as User);
const posts = ref<Post[]>([]);
const body = ref<string>('');

async function getFeed(): Promise<void> {
  await axios
    .get(`/api/posts/profile/${$route.params.id}/`)
    .then((response: AxiosResponse) => {
      console.log('data', response.data);

      posts.value = response.data.posts;
      user.value = response.data.user;
    })
    .catch((error: any) => {
      console.error('Error fetching feed:', error);
    });
}

async function submitForm(): Promise<void> {
  console.log('submitForm:', body.value);
  await axios
    .post('/api/posts/create/', { body: body.value })
    .then((response: AxiosResponse) => {
      console.log('Post created:', response.data);

      // posts.value.push(response.data);    // appended to the end
      posts.value.unshift(response.data); // appended to the start
      body.value = '';
      // getFeed();
    })
    .catch((error: any) => {
      console.error('Error creating post:', error);
    });
}

onMounted(() => {
  getFeed();
});

// TODO: Cannot work
onBeforeRouteUpdate(async (to, from) => {
  console.log('Route is changing from', from.name, 'to', to.name);
  if (from.name === to.name) {
    getFeed();
  }
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
          <p class="text-xs text-gray-500">182 friends</p>
          <p class="text-xs text-gray-500">120 posts</p>
        </div>
      </div>
    </div>

    <!-- (2/3) The central two columns for the text area to create posts -->
    <div class="main-center col-span-2 space-y-4">
      <!-- (2.1/3) The text area for images & posts -->
      <div
        v-if="userStore.user.id === user.id"
        class="bg-white border border-gray-200 rounded-lg"
      >
        <!-- (2.1.1/3) The textarea element -->
        <form @submit.prevent="submitForm" method="POST">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What are you curious about?"
            />
          </div>

          <!-- (2.1.2/3) The Attach image and Post buttons -->
          <div class="p-4 border-t border-gray-100 flex justify-between">
            <a href="#"
              class="inline-block py-4 px-6 bg-gray-600 text-white
                      rounded-lg">
              Attach image
            </a>

            <button
              class="inline-block py-4 px-6 bg-purple-600 text-white
                     rounded-lg">
              Post
            </button>
          </div>
        </form>
      </div>

      <!-- 1/2 Start of posts -->
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        :key="post.id"      
      >
        <FeedItem :post="post" />
      </div>
      <!-- 2/2 End of post --> 
    </div>

    <!-- (3/3) The main-right column: PeopleYouMayKnow & Trends --> 
    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <TrendsComponent />
    </div>
  </div>
</template>
