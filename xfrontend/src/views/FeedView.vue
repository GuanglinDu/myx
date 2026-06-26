<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import axios, { type AxiosResponse } from "axios";
import type { Post } from "@/types/custom_types";
import PeopleYouMayKnow from "@/components/PeopleYouMayKnow.vue";
import TrendsComponent from "@/components/TrendsComponent.vue";
import FeedItem from "./FeedItem.vue";

const posts = ref<Post[]>([]);
const body = ref<string>("");
const selectedFile = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const imagePreviewUrl = ref<string | null>(null);

function onFileSelected(event: Event): void {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0];
    if (imagePreviewUrl.value) {
      URL.revokeObjectURL(imagePreviewUrl.value);
    }
    imagePreviewUrl.value = URL.createObjectURL(selectedFile.value);
  }
}

function clearSelectedFile(): void {
  selectedFile.value = null;
  if (fileInput.value) {
    fileInput.value.value = "";
  }
  if (imagePreviewUrl.value) {
    URL.revokeObjectURL(imagePreviewUrl.value);
    imagePreviewUrl.value = null;
  }
}

async function getFeed(): Promise<void> {
  await axios
    .get("/api/posts/")
    .then((response: AxiosResponse) => {
      console.log("data", response.data);

      posts.value = response.data;
    })
    .catch((error: any) => {
      console.error("Error fetching feed:", error);
    });
}

// 1. How to use a FormData object in Vue.js? - Google AI Overview
// 2. How to use a FormData object in Vue.js with TypeScript?
// To use a FormData object in Vue.js, you instantiate the native JavaScript
// FormData constructor inside your submission method, append your reactive
// Vue state or file inputs, and send it to your API. This approach is highly
// recommended when your form includes file uploads alongside text fields, as
// it handles the multipart/form-data encoding automatically.
async function submitForm(): Promise<void> {
  const formData: FormData = new FormData();
  formData.append("body", body.value);
  if (selectedFile.value) {
    formData.append("image", selectedFile.value);
  }

  await axios
    .post("/api/posts/create/", formData)
    .then((response: AxiosResponse) => {
      console.log("Post created:", response.data);

      posts.value.unshift(response.data);
      body.value = "";
      clearSelectedFile();
    })
    .catch((error: any) => {
      console.error("Error creating post:", error);
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

onUnmounted(() => {
  if (imagePreviewUrl.value) {
    URL.revokeObjectURL(imagePreviewUrl.value);
  }
});
</script>

<template>
  <div class="mx-auto grid max-w-7xl grid-cols-4 gap-4">
    <!-- (2/3) The central two columns for the text area to create posts -->
    <div class="main-center col-span-3 space-y-4">
      <!-- (2.1/3) The text area for images & posts -->
      <div class="rounded-lg border border-gray-200 bg-white">
        <!-- (2.1.1/3) The textarea element -->
        <form @submit.prevent="submitForm" method="POST">
          <div class="p-4">
            <textarea
              v-model="body"
              class="w-full rounded-lg bg-gray-100 p-4"
              placeholder="What are you curious about? - FeedView.vue"
            />
          </div>
          <!-- The image preview  -->
          <div v-if="imagePreviewUrl" class="px-4 pb-2">
            <img
              :src="imagePreviewUrl"
              data-testid="image-preview"
              alt="Image preview"
              class="max-h-48 rounded-lg object-contain"
            />
          </div>

          <!-- (2.1.2/3) The Attach image and Post buttons -->
          <div class="flex justify-between border-t border-gray-100 p-4">
            <label
              class="inline-block cursor-pointer rounded-lg bg-gray-600 px-6 py-4 text-white"
            >
              <span v-if="!selectedFile">Attach image</span>
              <span v-else>{{ selectedFile.name }}</span>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="onFileSelected"
              />
            </label>
            <button
              v-if="selectedFile"
              type="button"
              class="inline-block rounded-lg bg-gray-400 px-6 py-4 text-white"
              @click="clearSelectedFile"
            >
              Remove
            </button>

            <button
              class="inline-block rounded-lg bg-purple-600 px-6 py-4 text-white"
            >
              Post
            </button>
          </div>
        </form>
      </div>

      <!-- @post-updated vs @postUpdated
      The camelCase and kebab-case event names in Vue.js 3 emits - Google AI Overview
      In Vue 3, event names undergo an automatic case transformation, allowing you to emit an event using camelCase in your JavaScript code and listen to it using kebab-case in your HTML templates.
      -->
      <div
        class="rounded-lg border border-gray-200 bg-white p-4"
        v-for="post in posts"
        :key="post.id"
      >
        <FeedItem :post="post" @post-updated="handlePostUpdated" />
      </div>
    </div>

    <!-- (3/3) The main-right column: PeopleYouMayKnow & Trends (sibling of main-center) -->
    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />
      <TrendsComponent />
    </div>
  </div>
</template>
