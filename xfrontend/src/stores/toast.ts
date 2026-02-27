/**
Created at 19:59:39 on 20260202 Mon by Guanglin Du.
Updated at 17:42:34 on 20260224 Tue by Guanglin Du.

(1/15) Build a Full-Stack Social Network with Django and Vue 3: From
Idea to Launch
https://www.youtube.com/watch?v=xOxN_7coIDw

0:00 Overview
1:50 Create a new Vue 3 project
 - 5:30 Install Axios
 - 6:45 Install Tailwind CSS
 - 10:20 Make sure everything is running
10:38 Set up the app.vue file (Menu, etc)
 - 11:25 Set the indentation to 2 spaces
 - 12:30 Create the menu
 - 16:20 Create the main tag
17:02 Create static sign up page
25:35 Create static log in page
28:55 Create static feed page
 - 30:25 Create the post layout and the profile (the left column)
 - 32:34 Create the text area for images & posts (the central 2 columns)
 - 34:58 Create the Attach image and Post buttons
 - 36:57 Create a post with an image
 - 40:00 Create a pure textual post
 - 40:39 Create the PeopleYouMayKnow and Trends elements (the right column)
44:54 Create the static messages page
53:46 Create the static search page
1:00:53 Make PeopleYouMayKnow a component
1:04:38 Make Trends a component
1:05:48 Create the toast component (* this store created here)

What does toast mean in a Vue.js 3 Pinia store? And how to translate
it into Chinese? - qianwen
In the context of Vue.js 3 + Pinia, the term "toast" does not refer
to bread or food—it refers to a UI notification component commonly
called a "toast message" or "toast notification."
It’s called a “toast” because it pops up like a piece of toast from
a toaster. (轻提示, 消息提示, 屏幕弹出消息)
*/
import { ref } from 'vue';
import type { Ref } from 'vue';
import { defineStore } from 'pinia';

// Updated at 20:00:53 on 20260129 Thu by Guanglin Du.
const useToastStore = defineStore("toast", () => {
  // The state
  const milliseconds = ref<number>(0); // milliseconds
  const message = ref<string>('');
  const classes: Ref<string> = ref('');
  const isVisible = ref<boolean>(false);

  // The actions
  function showToast(t: number, msg: string, clses: string): void {
    milliseconds.value = t;
    message.value = msg;
    classes.value = clses;
    isVisible.value = true;

    setTimeout(() => {
      classes.value += ' -translate-y-28';
    }, 10);

    setTimeout(() => {
      classes.value = classes.value.replace('-translate-y-28', '');
    }, milliseconds.value - 500);

    setTimeout(() => {
      isVisible.value = false;
    }, milliseconds.value);
  }

  return { milliseconds, message, classes, isVisible, showToast };
});

export { useToastStore };
