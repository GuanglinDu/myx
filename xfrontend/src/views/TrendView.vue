<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios, { type AxiosResponse } from 'axios';
import type { Post } from '@/types/custom_types';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import TrendsComponent from '@/components/TrendsComponent.vue';
import FeedItem from './FeedItem.vue';

const $route = useRoute();
const posts = ref<Post[]>([]); 

async function getTrendPosts(): Promise<void> {
  const hashtag = $route.params.id as string;
  await axios
    .get(`/api/posts/?trend=${hashtag}`)
    .then((response: AxiosResponse) => {
      console.log('trend posts data', response.data);
      posts.value = response.data;
    })
    .catch((error: any) => {
      console.error('Error fetching trend posts:', error);
    });
}

function handlePostUpdated(updatedPost: Post): void {
  const index = posts.value.findIndex((p) => p.id === updatedPost.id);
  if (index !== -1) {
    posts.value[index] = updatedPost;
  }
}

onMounted(() => {
  getTrendPosts();
});

watch(
  () => $route.params.id,
  () => { getTrendPosts(); },
  { deep: true, immediate: true }
);
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- (2/3) The central column for the trending posts -->
    <div class="main-center col-span-3 space-y-4">
      <!-- (2.1/3) The header for trending posts -->
      <div class="bg-white border border-gray-200 rounded-lg">
        <h2 class="p-4 text-xl font-bold">
          Trend: #{{ $route.params.id }}
        </h2>
      </div>

      <!-- (2.2/3) The list of posts filtered by hashtag -->
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        :key="post.id"
      >
        <FeedItem :post="post" @post-updated="handlePostUpdated" />
      </div>
    </div>

    <!-- (3/3) The main-right column: PeopleYouMayKnow & Trends
    (sibling of main-center)
    -->
    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <TrendsComponent />
    </div>
  </div>
</template>