<script setup lang="ts">
import { onMounted, ref } from 'vue';
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import TrendsComponent from '@/components/TrendsComponent.vue';
import FeedItem from './FeedItem.vue';
import type { Post } from '@/types/custom_types';

const posts = ref<Post[]>([]);
const body = ref<string>('');

async function getFeed(): Promise<void> {
  await axios
    .get('/api/posts/')
    .then((response: AxiosResponse) => {
      console.log('data', response.data);

      posts.value = response.data;
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

function handlePostUpdated(updatedPost: Post): void {
  const index = posts.value.findIndex((p) => p.id === updatedPost.id);
  if (index !== -1) {
    posts.value[index] = updatedPost;
  }
}

onMounted(() => {
  getFeed();
});
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- (2/3) The central two columns for the text area to create posts -->
    <div class="main-center col-span-3 space-y-4">
      <!-- (2.1/3) The text area for images & posts -->
      <div class="bg-white border border-gray-200 rounded-lg">
        <!-- (2.1.1/3) The textarea element -->
        <form @submit.prevent="submitForm" method="POST">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What are you curious about? - FeedView.vue"
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

      <!-- @post-updated <=> @postUpdated in template -->
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        :key="post.id"      
      >
        <FeedItem :post="post" @post-updated="handlePostUpdated" />
      </div>

      <!-- (3/3) The main-right column: PeopleYouMayKnow & Trends --> 
      <div class="main-right col-span-1 space-y-4">
        <PeopleYouMayKnow />
        <TrendsComponent />
      </div>
    </div>
  </div>
</template>
