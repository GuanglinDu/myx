<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import axios, { type AxiosResponse } from 'axios';
import { createAvatar } from '@dicebear/core';
import { adventurer } from '@dicebear/collection';
import type { Conversation, User } from '@/types/custom_types';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const conversations = ref<Conversation[]>([]);
const activeConversation = ref<Conversation | null>(null);
// The other participant in the conversation
const participant = ref<User | null>(null);
const body = ref<string>('');

// Generates the avatar as a Data URI
const avatarDataUri = computed(() =>
  createAvatar(adventurer, {
    seed: participant.value?.id,
    size: 128,
  }).toDataUri()
);

// Fetches conversations
function getConversations(): void {
  console.log('Fetching conversations...');

  axios
    .get('/api/chat/')
    .then((response: AxiosResponse) => {
      console.log('Conversations:', response.data);

      conversations.value = response.data;

      if (conversations.value.length > 0) {
        activeConversation.value = conversations.value[0];
        participant.value = activeConversation.value.participants.find(
          (p) => p.id !== userStore.user.id
        ) || null;
      }

      console.log('Active Conversation:', activeConversation.value);
      console.log('Participant:', participant.value);

      getMessages();
    })
    .catch(error => {
      console.error('Error fetching conversations:', error);
    });
}

// Fetches messages for the active conversation
function getMessages(): void {
  if (!activeConversation.value) return;

  console.log('Fetching messages for conversation:',
              activeConversation.value.id);

  axios
    .get(`/api/chat/${activeConversation.value.id}/`)
    .then((response: AxiosResponse) => {
      console.log('Messages:', response.data);

      activeConversation.value = response.data;
    })
    .catch(error => {
      console.error('Error fetching messages:', error);
    });
}

// Submits a new message to the active conversation
function submitForm(): void {
  if (!activeConversation.value) return;

  console.log('Submitting message to conversation:',
              activeConversation.value.id);

  axios
    .post(`/api/chat/${activeConversation.value.id}/send/`, {
      body: body.value,
    })
    .then((response: AxiosResponse) => {
      console.log('Message sent:', response.data);
      // Appends the new message to the active conversation's message array
      // instead of refetching all messages from the DB for better performance.
      activeConversation.value.messages.push(response.data);
      body.value = '';      
    })
    .catch(error => {
      console.error('Error sending message:', error);
    });
}

function setActiveConversation(conversationId: string): void {
  console.log('Setting active conversation to ID:', conversationId);

//   activeConversation.value = conversations.value.find(    
//     (c) => c.id === conversationId
//   ) || null;
  activeConversation.value.id = conversationId;
  getMessages();
}

onMounted(() => {
  getConversations();
});
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <!-- Conversation list on the left 1 column -->
    <div class="main-left col-span-1">
      <div class="space-y-4">
        <div
          class="flex items-center justify-between"
          v-for="conversation in conversations"
          :key="conversation.id"
          @click="setActiveConversation(conversation.id)"
        >
          <div class="flex items-center space-x-1">
            <img
              :src="avatarDataUri"
              alt="avatar"
              class="w-[40px] rounded-full"
            />
            <!--
            Embedded <template> tags are used in Vue components as "invisible"
            wrappers to group multiple elements for directives like v-if or
            v-for without adding extra nodes to the final rendered HTML.
            -->
            <template
              v-for="participant in conversation.participants"
              :key="participant.id"
            >
              <!-- Only shows the other participant's name -->
              <p
                class="text-xs font-bold"
                v-if="participant.id !== userStore.user.id"
              >
                {{ participant.name }}              
              </p>
            </template>
          </div>
          <span class="text-xs text-gray-500">
            {{conversation.modified_at_formatted}} ago
          </span>
        </div>      
      </div>
    </div>

    <!-- Messages on the right 3 columns -->
    <div class="main-center col-span-3 space-y-2">
      <div class="bg-white border border-gray-200 rounded-lg">
        <div class="flex flex-col flex-grow p-4">
          <template
            v-for="message in activeConversation?.messages"
            :key="message.id"
          >
            <!-- Messages you sent: v-if -->          
            <div
              class="flex mt-2 space-x-3 max-w-md ml-auto justify-end"
              v-if="message.created_by.id == userStore.user.id"
            >
              <div class="bg-blue-600 text-white p-3 rounded-l-lg
                          rounded-br-lg"
              >
                <p class="text-sm">{{ message.body }}</p>
              </div>
              <span class="text-xs text-gray-500 leading-none">
                {{ message.created_at_formatted }} ago
              </span>

              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  src="@/assets/Brian-40x40px.png"
                  class="w-[40px] rounded-full"
                />
              </div>
            </div>

            <!-- Messages you received: v-else -->
            <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
              <div class="flex-shrink-0 h-10 w-10 rounded-full">
                <img
                  src="@/assets/Adrian-40x40px.png"
                  class="w-[40px] rounded-full"
                />
              </div>

              <div class="flex mt-2 space-x-3 max-w-md ml-auto">
                <div class="bg-gray-300 text-black p-3 rounded-l-lg
                            rounded-br-lg">
                  <p class="text-sm">{{ message.body }}</p>
                </div>

                <span class="text-xs text-gray-500 leading-none">
                  {{ message.created_at_formatted }} ago
                </span>
              </div>
            </div>          
          </template>
        </div>       
      </div>

      <!-- Creates and sends messages -->
      <div class="bg-white border border-gray-200 rounded-lg">
        <form @submit.prevent="submitForm" method="POST">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What do you want to say?"
            />
          </div>

          <!-- The Send button -->
          <div class="p-4 border-t border-gray-100 flex justify-between">
            <button type="submit"
              class="inline-block py-4 px-6 bg-purple-600 text-white
                     rounded-lg">
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
