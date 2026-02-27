/**
 * Created at 20:33:01 on 20260202 Mon by Guanglin Du.
 * (2/15) Build a Full-Stack Social Network with Django and Vue 3: From
 * Idea to Launch | Part 2
 * https://www.youtube.com/watch?v=NmQyX1D5hqo&list=PLpyspNLjzwBlobEvnZzyWP8I-ORQcq4IO&t=0s
 * 0:00 Overview
 * 0:15 Set up the backend
 * 0:40 Create a virtual environment
 *  - 1:42 Install Django
 *  - 2:15 Install djangorestframework (rest_framework, DRF)
 *  - 2:45 Install djangorestframework-simplejwt (rest_framework_simplejwt)
 *  - 3:08 Install Pillow (handling images)
 * 3:37 Create a Django project
 * 5:16 Set up everything ( A bigger task!)
 *  - 5:24 Config for JWT (settings and URLs)
 *  - 6:10 Config for DRF (and at 9:30)
 *  - 8:40 Config for csrf and cors (and at 10:00)
 * 11:50 Create app for custom user model (remember uuid)
 *  - 17:45 Add to settings
 *  - 18:52 Configure JWT URLs
 * 21:20 Make it possible to sign up (The key part to couple the frontend
 *       with the backend. Need time to digest!😜)
 *  - 21:30 Implement verification, reset/forgot the password and the
 *          similar (Comes later in the course)
 *  - 21:45 backend work (api dot py)
 *  - 27:55 frontend work (SignupView dot vue)
 * 
 * What does toast mean in a Vue.js 3 Pinia store? And how to translate
 * it into Chinese? - qianwen
 * In the context of Vue.js 3 + Pinia, the term "toast" does not refer
 * to bread or food—it refers to a UI notification component commonly
 * called a "toast message" or "toast notification."
 * It’s called a “toast” because it pops up like a piece of toast from
 * a toaster. (轻提示, 消息提示, 屏幕弹出消息)
 */
import { reactive } from 'vue';
import { defineStore } from "pinia";
// Warning: module axios can only be default imported using
// the allowSyntheticDefaultImports flag
import axios from 'axios';

interface User {
  id: string;
  name: string;
  email: string;
  access: string;
  refresh: string;
  avatar: string;
  isAuthenticated: boolean,
}

// window.localStorage vs window.sessionStorage
const useUserStore = defineStore('user', () => {
  /* The state */
  // const user = reactive<User>({ // discouraged
  const user: User = reactive({    
    id: '',
    name: '',
    email: '',
    access: '',
    refresh: '',
    avatar: '',
    isAuthenticated: false,
  });

  /* The actions */
  // user.access is the API JWT token
  function initStore(): void {
    console.log("initStore", localStorage.getItem("user.access"));

    // If the token exists, the user is believed to have been logged in.
    if (localStorage.getItem("user.access")) {
      console.log("User has access!");

      user.access = localStorage.getItem("user.access") ?? '';
      user.refresh = localStorage.getItem("user.refresh") ?? '';
      user.id = localStorage.getItem("user.id") ?? '';
      user.name = localStorage.getItem("user.name") ?? '';
      user.email = localStorage.getItem("user.email") ?? '';
      user.avatar = localStorage.getItem("user.avatar") ?? '';
      user.isAuthenticated = true;

      refreshToken();

      console.log("Initialized user:", user);
    }
  }

  // Stores the API token to window.localStorage (vs window.sessionStorage)
  function setToken(data: any): void {
    console.log("setToken", data);

    user.access = data.access; // the API token
    user.refresh = data.refresh;
    user.isAuthenticated = true;

    localStorage.setItem("user.access", data.access);
    localStorage.setItem("user.refresh", data.refresh);

    console.log("user.access: ", localStorage.getItem("user.access"));
  }

  // Logs out
  function removeToken(): void {
    console.log("removeToken");

    user.refresh = '';
    user.access = '';
    user.id = '';
    user.name = '';
    user.email = '';
    user.avatar = '';
    user.isAuthenticated = false;

    localStorage.setItem("user.access", "");
    localStorage.setItem("user.refresh", "");
    localStorage.setItem("user.id", "");
    localStorage.setItem("user.name", "");
    localStorage.setItem("user.email", "");
    localStorage.setItem("user.avatar", "");
  }

  function setUserInfo(usr: User): void {
    console.log("setUserInfo", user);

    user.id = usr.id;
    user.name = usr.name;
    user.email = usr.email;
    user.avatar = usr.avatar;

    localStorage.setItem("user.id", user.id);
    localStorage.setItem("user.name", user.name);
    localStorage.setItem("user.email", user.email);
    localStorage.setItem("user.avatar", user.avatar);

    console.log("User: ", user);
  }

  // Refreshes the API token
  function refreshToken(): void {
    axios
      .post("/api/refresh/", {
        refresh: user.refresh,
      })
      .then((response) => {
        user.access = response.data.access; // the API token

        localStorage.setItem("user.access", response.data.access);

        axios.defaults.headers.common["Authorization"] =
          "Bearer " + response.data.access;
      })
      .catch((error) => {
        console.log(error);

        removeToken();
      });
  }

  return { user, initStore, setToken, removeToken, setUserInfo, refreshToken };
});

export { useUserStore };
