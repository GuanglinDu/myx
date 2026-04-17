<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { onMounted } from 'vue';
import axios from 'axios';
import { createAvatar } from '@dicebear/core';
import { adventurer } from '@dicebear/collection';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import TrendsComponent from '@/components/TrendsComponent.vue';
import FeedItem from './FeedItem.vue';
import { useUserStore } from '@/stores/user';
import type { Post, User } from '@/types/custom_types';

const userStore = useUserStore();

// router/index.ts defines the route for this view as '/profile/:id', where
// ':id' is a dynamic segment representing the user UUID of the profile being
// viewed. We will access this UUID via props.
const props = defineProps({
  id: { type: String, required: true }
});

const user = ref<User>({} as User);
const posts = ref<Post[]>([]);
const body = ref<string>('');
const friendshipStatus =
  ref<'none' | 'pending' | 'request_sent' | 'friends' | 'self'>('none');
const requestId = ref<string>('');
const isSendingRequest = ref<boolean>(false);
const isProcessingRequest = ref<boolean>(false);

const isOwnProfile = computed(() => {
  return userStore.user.id === props.id;
});

// Generate the avatar as a Data URI
const avatarDataUri = computed(() => 
  createAvatar(adventurer, {
    seed: props.id,
    size: 128,
  }).toDataUri()
);

async function getFeed(): Promise<void> {
  try {
    const response = await axios.get(`/api/posts/profile/${props.id}/`);
    console.log('data', response.data);
    posts.value = response.data.posts;
    user.value = response.data.user;
    friendshipStatus.value = response.data.friendship_status || 'none';
    requestId.value = response.data.request_id || '';
  } catch (error) {
    console.error('Error fetching feed:', error);
  }
}

// We expect to receive an 'id' prop of type string, which represents the
// UUID of the user whose profile we want to display. This id is passed via
// the route parameters. See src/router/index.ts for the route definition.
async function sendFriendshipRequest(): Promise<void> {
  if (isSendingRequest.value || friendshipStatus.value !== 'none') return;

  isSendingRequest.value = true;
  try {
    await axios.post(`/api/friends/send/${props.id}/`);
    friendshipStatus.value = 'request_sent';
  } catch (error) {
    console.error('Error sending friendship request:', error);
  } finally {
    isSendingRequest.value = false;
  }
}

async function acceptFriendshipRequest(): Promise<void> {
  if (!requestId.value || isProcessingRequest.value) return;

  isProcessingRequest.value = true;
  try {
    await axios.post(`/api/friends/accept/${requestId.value}/`);
    friendshipStatus.value = 'friends';
  } catch (error) {
    console.error('Error accepting friendship request:', error);
  } finally {
    isProcessingRequest.value = false;
  }
}

async function rejectFriendshipRequest(): Promise<void> {
  if (!requestId.value || isProcessingRequest.value) return;

  isProcessingRequest.value = true;
  try {
    await axios.post(`/api/friends/reject/${requestId.value}/`);
    friendshipStatus.value = 'none';
    requestId.value = '';
  } catch (error) {
    console.error('Error rejecting friendship request:', error);
  } finally {
    isProcessingRequest.value = false;
  }
}

async function submitForm(): Promise<void> {
  console.log('submitForm:', body.value);
  try {
    const response = await axios.post('/api/posts/create/', { body: body.value });
    console.log('Post created:', response.data);
    posts.value.unshift(response.data);
    body.value = '';
  } catch (error) {
    console.error('Error creating post:', error);
  }
}

onMounted(() => {
  getFeed();
});

watch(() => props.id, () => {
  getFeed();
});
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- (1/3) The main-left profile column: avatar, name, & statistics -->
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200
                  text-center rounded-lg">
        <img :src="avatarDataUri" alt="User Avatar" />
        
        <!-- the logged-in user's name vs any user's name
          <p><strong>{{ userStore.user.name }}</strong></p>
        -->
        <p><strong>{{ user.name }}</strong></p>

        <div class="mt-6 flex space-x-8 justify-around">
          <RouterLink
            :to="{name: 'friends', params: {user_id: user.id}}"
            class="text-xs text-gray-500"
          >
            {{ user.friends_count || 0 }} friends
          </RouterLink>
          <p class="text-xs text-gray-500">
            {{ user.posts_count || 0 }} posts
          </p>
        </div>

        <!-- Sends friend request -->
        <div class="mt-6" v-if="!isOwnProfile">
          <!-- If not friends, show send button -->
          <button
            v-if="friendshipStatus === 'none'"
            @click="sendFriendshipRequest"
            :disabled="isSendingRequest"
            class="inline-block p-3 bg-purple-600 text-white text-sm
                   rounded-lg hover:bg-purple-700 disabled:opacity-50"
          >
            {{ isSendingRequest ? 'Sending...' : 'Send friendship request' }}
          </button>

          <!-- If request already sent -->
          <button
            v-else-if="friendshipStatus === 'request_sent'"
            disabled
            class="inline-block p-3 bg-gray-400 text-white text-sm
                   rounded-lg cursor-not-allowed"
          >
            Request sent
          </button>

          <!-- If pending request from them -->
          <div v-else-if="friendshipStatus === 'pending'" class="flex space-x-2">
            <button
              @click="acceptFriendshipRequest"
              :disabled="isProcessingRequest"
              class="flex-1 p-3 bg-green-600 text-white text-sm
                     rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              {{ isProcessingRequest ? 'Processing...' : 'Accept' }}
            </button>
            <button
              @click="rejectFriendshipRequest"
              :disabled="isProcessingRequest"
              class="flex-1 p-3 bg-red-500 text-white text-sm
                     rounded-lg hover:bg-red-600 disabled:opacity-50"
            >
              Reject
            </button>
          </div>

          <!-- If already friends -->
          <button
            v-else-if="friendshipStatus === 'friends'"
            disabled
            class="inline-block p-3 bg-green-600 text-white text-sm
                   rounded-lg cursor-not-allowed"
          >
            Friends
          </button>
        </div>

        <!-- Log out (only on own profile) -->
        <div class="mt-6" v-if="isOwnProfile">
          <button
            @click="userStore.logout()"
            class="w-full p-3 bg-red-500 text-white text-sm
                   rounded-lg hover:bg-red-600"
          >
            Log out
          </button>
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
