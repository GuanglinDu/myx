<script setup lang="ts">
import { computed } from 'vue';
import { createAvatar } from '@dicebear/core';
import { adventurer } from '@dicebear/collection';
import type { Comment } from '@/types/custom_types';

const $props = defineProps<{
  comment: Comment;
}>();

// Generate the avatar as a Data URI
const avatarDataUri = computed(() =>
  createAvatar(adventurer, {
    seed: $props.comment.created_by.id,
    size: 128,
  }).toDataUri()
);
</script>

<template>
  <div class="mb-6 flex justify-between">
    <div class="flex space-x-1 justify-between">
      <img
        :src="avatarDataUri"
        alt="User Avatar"
        class="w-[40px] rounded-full"
      />

      <p class="text-sm text-gray-500">
        <strong>
          <RouterLink :to="`/profile/${comment.created_by.id}`">
            {{ comment.created_by.name }}
          </RouterLink>
        </strong>
      </p>
    </div>

    <p class="text-sm text-gray-500">
      {{ comment.created_at_formatted }} ago
    </p>
  </div>

  <p>{{ comment.body }}</p>
</template>
