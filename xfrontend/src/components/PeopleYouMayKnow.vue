<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import axios, { type AxiosResponse } from "axios";
import { createAvatar, license } from "@dicebear/core";
import { adventurer } from "@dicebear/collection";
import type { User } from "@/types/custom_types";

const users = ref<User[]>([]);

async function getFriendSuggestions(): Promise<void> {
  try {
    const response: AxiosResponse = await axios.get("/api/friends/suggested/");
    // console.log("Suggested friends: ", response.data);
    users.value = response.data;
  } catch (error: any) {
    console.error("Error fetching requests:", error);
  }
}

const suggestedUsers = computed(() =>
  users.value.map((u) => ({
    ...u,
    avatarUri: createAvatar(adventurer, {
      seed: u.id,
      size: 128,
    }).toDataUri(),
  })),
);

onMounted(() => {
  getFriendSuggestions();
});
</script>

<template>
  <div
    class="space-y-2 rounded-lg border border-gray-200 bg-white p-4 text-center"
  >
    <h3 class="mb-6 text-xl">People you may know</h3>

    <!-- Suggested friends -->
    <ul class="space-y-3">
      <li
        v-for="person in suggestedUsers"
        :key="person.id"
        class="flex items-center justify-between space-x-2"
      >
        <div class="flex items-center space-x-2">
          <img
            :src="person.avatarUri"
            alt="avatar"
            class="w-[40px] rounded-full"
          />
          <p class="text-sm">{{ person.name }}</p>
        </div>

        <RouterLink
          :to="{ name: 'profile', params: { id: person.id } }"
          class="shrink-0 rounded-lg bg-purple-600 px-3 py-2 text-xs text-white"
        >
          Show
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
