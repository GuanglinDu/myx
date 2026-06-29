<script setup lang="ts">
import { computed, ref } from "vue";
import axios, { type AxiosResponse } from "axios";
import { createAvatar } from "@dicebear/core";
import { adventurer } from "@dicebear/collection";
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";
import type { Post } from "@/types/custom_types";

const isLiking = ref<boolean>(false);
const $props = defineProps<{
  post: Post;
}>();
const showExtraModal = ref<boolean>(false);
const userStore = useUserStore();
const toastStore = useToastStore();

// Emits event to parent ProfileView.vue to refresh posts
const emit = defineEmits<{
  (e: "postUpdated", post: Post): void;
  (e: "postDeleted", id: string): void;
}>();

// Generates the avatar as a Data URI
const avatarDataUri = computed(() =>
  createAvatar(adventurer, {
    seed: $props.post.created_by.id,
    size: 128,
  }).toDataUri(),
);

// Handles the like-button click
async function toggleLike(): Promise<void> {
  // if (isLiking.value) return;  // Prevent multiple clicks

  isLiking.value = true;
  try {
    const response: AxiosResponse = await axios.post(
      `/api/posts/${$props.post.id}/like/`,
    );
    const { liked, like_count } = response.data;
    emit("postUpdated", {
      ...$props.post,
      liked,
      like_count: like_count,
    });
  } catch (error) {
    console.error("Failed to toggle like:", error);
  } finally {
    isLiking.value = false;
  }
}

function toggleExtraModal(): void {
  console.log("toggleExtraModal");
  showExtraModal.value = !showExtraModal.value;
}

async function deletePost(): Promise<void> {
  console.log("FeedItem.vue - Delete post: ", $props.post.id);

  emit("postDeleted", $props.post.id);

  try {
    const response: AxiosResponse = await axios.delete(
      `/api/posts/${$props.post.id}/delete/`,
    );

    // console.log("deletePost: ", response.data);
    toastStore.showToast(5000, "The post was deleted", "bg-emerald-500");
  } catch (error) {
    console.error("Failed to delete the post:", error);
  }
}
</script>

<template>
  <!-- The avatar, name, & the time elapsed since the post was published. -->
  <div class="mb-6 flex justify-between">
    <div class="flex justify-between space-x-1">
      <img
        :src="avatarDataUri"
        alt="User Avatar"
        class="w-[40px] rounded-full"
      />
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

  <!-- Attachment images -->
  <div v-if="post.attachments && post.attachments.length > 0" class="mt-4">
    <img
      v-for="att in post.attachments"
      :key="att.id"
      :src="att.image"
      alt="Post image"
      class="h-auto max-w-full rounded-lg"
    />
  </div>

  <!-- The textual body. The SVG icon is from heroicons.com. -->
  <p>{{ post.body }}</p>

  <div class="my-6 flex justify-between">
    <div class="flex space-x-6">
      <!-- Count of likes -->
      <div class="flex items-center space-x-2">
        <button @click="toggleLike" class="focus:outline-none">
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
        <span class="text-xs text-gray-500">{{ post.like_count }}</span>
      </div>

      <!-- Count of comments. The SVG icon is from heroicons.com. -->
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
        <RouterLink
          :to="{ name: 'postview', params: { id: post.id } }"
          class="text-xs text-gray-500"
        >
          {{ post.comments_count }} comments
        </RouterLink>
      </div>
    </div>

    <!-- The ellipsis symbol -->
    <div @click="toggleExtraModal">
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

  <div v-if="showExtraModal">
    <div class="flex items-center space-x-6">
      <!-- Delete a post. The SVG icon is from heroicons.com. -->
      <div
        class="flex items-center space-x-2"
        @click="deletePost"
        v-if="userStore.user.id == post.created_by.id"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-6 text-red-500"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
          />
        </svg>
        <span class="text-xs text-red-500">Delete post</span>
      </div>

      <div class="flex items-center space-x-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="size-6 text-orange-500"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3 3v1.5M3 21v-6m0 0 2.77-.693a9 9 0 0 1 6.208.682l.108.054a9 9 0 0 0 6.086.71l3.114-.732a48.524 48.524 0 0 1-.005-10.499l-3.11.732a9 9 0 0 1-6.085-.711l-.108-.054a9 9 0 0 0-6.208-.682L3 4.5M3 15V4.5"
          />
        </svg>
        <span class="text-xs text-orange-500">Report post</span>
      </div>
    </div>
  </div>
</template>
