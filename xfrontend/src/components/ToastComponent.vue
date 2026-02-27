<script setup lang="ts">
// import { useToastStore } from '@/stores/toast.ts';
import { useToastStore } from '../stores/toast.ts';

const toastStore = useToastStore();
</script>

<template>
  <div v-if="toastStore.isVisible"
    class="transition ease-in-out delay-500 duration-500 px-6 py-6 fixed
           top-full right-8 rounded-xl shadow-xl"
    :class="store.classes"
  >
    {{ toastStore.message }}
  </div>
</template>
