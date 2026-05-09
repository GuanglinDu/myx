<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute }  from 'vue-router';
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import type { Post } from '@/types/custom_types';
import FeedItem from './FeedItem.vue';
import CommentItem from './CommentItem.vue';

const $route  = useRoute();
// Uses both the type annotation and initialization at the same timeto ensure
// the correct type is inferred.
const post = ref<Post>({
  id: '',
  body: '',
  created_by: {
    id: '',
    name: '',
  },
  created_at: '',
  likes_count: 0,
  liked: false,
  comments: [],
  comments_count: 0,
});

const body = ref<string>(''); // the comment body

async function getPost(): Promise<void> {
  await axios
    .get(`/api/posts/${$route.params.id}/`)
    .then((response: AxiosResponse) => {
      console.log('data', response.data);

      post.value = response.data.post;
    })
    .catch((error: any) => {
      console.error('Error fetching feed:', error);
    });
}

// Forces the post to be re-fetched from the backend, ensuring that the latest
// data is displayed. This is useful after actions like liking a post or adding
// a comment, which may change the post's data (e.g., likes count, comments
// count).
getPost();

async function submitCommentForm(): Promise<void> {
  console.log('submitCommentForm:', body.value);
  await axios
    .post(`/api/posts/${$route.params.id}/comment/`, { body: body.value })
    .then((response: AxiosResponse) => {
      console.log('Comment created:', response.data);

      // post.value.comments.unshift(response.data);
      post.value.comments.push(response.data);
      post.value.comments_count += 1;
      body.value = '';
    })
    .catch((error: any) => {
      console.error('Error creating comment:', error);
    });
}

onMounted(() => {
  getPost();
});
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- The main left columns -->
    <div class="main-left col-span-3 space-y-4">
      <h1 class="text-2xl font-bold mb-4">Post Detail View</h1>
      <p>This is the Post View. It will show the details of a single post.</p>

      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
      >
        <FeedItem v-if="post" :post="post" />
      </div>

      <!-- Lists all the comments -->
      <div class="ml-6 bg-white border border-gray-200 rounded-lg p-4">
        <h2 class="text-xl font-semibold mb-2">Comments</h2>
        <div
          v-for="comment in post.comments"
          :key="comment.id"
          class="border-b border-gray-200 py-2"
        >
          <CommentItem :comment="comment" />
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-lg p-4">
        <h2 class="text-xl font-semibold mb-2">Add a Comment</h2>
        <textarea
          v-model="body"
          class="w-full p-2 border border-gray-300 rounded mb-2"
          placeholder="Write your comment here..."
        ></textarea>
        <button
          @click="submitCommentForm"
          class="px-4 py-2 bg-blue-500 text-white rounded
               hover:bg-blue-600"
        >
          Comment
        </button>
      </div>
    </div>
  </div>
</template>
