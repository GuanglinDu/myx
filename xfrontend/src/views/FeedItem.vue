<script setup lang="ts">
import { computed } from 'vue';
import { createAvatar } from '@dicebear/core';
import { adventurer } from '@dicebear/collection';
import axios from 'axios';
import type { Post } from '@/types/custom_types';

const $props = defineProps<{
  post: Post;
}>();

// Emit event to parent to refresh posts
const emit = defineEmits<{
  (e: 'postUpdated', post: Post): void;
}>();

// Generate the avatar as a Data URI
const avatarDataUri = computed(() =>
  createAvatar(adventurer, {
    seed: $props.post.created_by.id,
    size: 128,
  }).toDataUri()
);

// Handle like button click
async function toggleLike() {
  try {
    const response = await axios.post(
      `/api/posts/like/${$props.post.id}/`
    );
    const { liked, likes_count } = response.data;
    emit('postUpdated', {
      ...$props.post,
      liked,
      likes_count,
    });
  } catch (error) {
    console.error('Failed to toggle like:', error);
  }
}
</script>

<template>
  <!-- The avatar, name, & how long has the post been published? -->
  <div class="mb-6 flex justify-between">
    <div class="flex space-x-1 justify-between">
      <img
        :src="avatarDataUri"
        alt="User Avatar"
        class="w-[40px] rounded-full" />
      <p>
        <strong>
        <RouterLink
          :to="{ name: 'profile', params: { id: post.created_by.id } }"
        >
            {{ post.created_by.name }}
        </RouterLink>
        </strong>
      </p>
    </div>
    <p class="text-gray-600">{{ post.created_at_formatted }} ago</p>
  </div>

  <!-- The textual body -->
  <p>{{ post.body }}</p>

  <div class="my-6 flex justify-between">
    <div class="flex space-x-6">
      <!-- Count of likes -->
      <div class="flex items-center space-x-2">
        <button
          @click="toggleLike"
          class="focus:outline-none"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            :fill="post.liked ? 'currentColor' : 'none'"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            :stroke="post.liked ? 'none' : 'currentColor'"
            class="size-6"
            :class="post.liked ? 'text-red-500' : 'text-gray-500'"
            >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6.633 10.25c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 0 1 2.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 0 0 .322-1.672V2.75a.75.75 0 0 1 .75-.75 2.25 2.25 0 0 1 2.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282m0 0h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 0 1-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 0 0-1.423-.23H5.904m10.598-9.75H14.25M5.904 18.5c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 0 1-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 9.953 4.167 9.5 5 9.5h1.053c.472 0 .745.556.5.96a8.958 8.958 0 0 0-1.302 4.665c0 1.194.232 2.333.654 3.375Z"
            />
          </svg>
        </button>
        <span class="text-gray-500 text-xs">{{ post.likes_count }}</span>
      </div>

      <!-- Count of comments -->
      <div class="flex items-center space-x-2">
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
            d="M8.625 9.75a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 0 1 .778-.332 48.294 48.294 0 0 0 5.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z"
        />
        </svg>
        <span class="text-gray-500 text-xs">0 comments</span>
    </div>
    </div>

    <!-- The ellipsis symbol -->
    <div>
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
        d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z"
        />
    </svg>
    </div>
  </div>
</template>
