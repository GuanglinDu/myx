<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface Trend {
  hashtag: string;
  occurences: number;
}

const trends = ref<Trend[]>([]);

async function getTrends(): Promise<void> {
  try {
    const response = await axios.get('/api/posts/trends/');
    trends.value = response.data;
  } catch (error) {
    console.error('Error fetching trends:', error);
  }
}

onMounted(() => {
  getTrends();
});
</script>

<template>
<div class="p-4 bg-white border border-gray-200 space-y-2
            text-center rounded-lg">
  <h3 class="mb-6 text-xl">Trends</h3>

  <!-- The trend list -->
  <div class="space-y-4">
    <div v-for="trend in trends" :key="trend.hashtag"
         class="flex items-center justify-between">
      <p class="text-xs">
        <strong>#{{ trend.hashtag }}</strong>
        <span class="text-gray-500">{{ trend.occurences }} posts</span>
      </p>

      <a href="#"
        class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg"
      >
        Explore
      </a>
    </div>
  </div>
</div>
</template>