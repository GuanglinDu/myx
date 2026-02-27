<script setup lang="ts">
import $router from '@/router/index.ts'
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();

interface LoginCredentials {
  email: string;
  password: string;  
}

let form: LoginCredentials = {
  email: "",
  password: "",
};

let errors: Array<string> = [];

// Request interceptor: attach the token if available
// axios.interceptors.request.use((config) => {
//   const token: string = userStore.user.access;
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//   } else {
//     config.headers.Authorization = "";
//   }
//   return config;
// });

async function submitForm(): Promise<any> {
  errors = [];

  if (form.email === "") {
    errors.push("Your e-mail is missing");
  }

  if (form.password === "") {
    errors.push("Your password is missing");
  }

  if (errors.length === 0) {
    await axios
      .post("/api/login/", form)
      .then((response) => {
        // Error: response.data.message undefined!
        // if (response.data.message === "success") {
        userStore.setToken(response.data);
        
        console.log(response.data.access);

        axios.defaults.headers.common["Authorization"] =
          "Bearer " + response.data.access;
      })
      .catch((error) => {
        console.log("error", error);

        errors.push(
          "The email or password is incorrect! Or the user is not activated!"
        );
      });

    await axios
      .get("/api/me/")
      .then((response) => {
        userStore.setUserInfo(response.data);

        $router.push("/feed");
      })
      .catch((error) => {
        console.log("error", error);
      });
  } else {
    console.log(errors);
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Log in</h1>
        <p class="mb-6 text-gray-500">
        This is the log in page based on the tutorial "Build a Full-Stack Social Network with Django and Vue 3: From Idea to Launch".            
        </p>

        <p class="font-bold">
          Don't have an account? <RouterLink :to="{'name': 'signup'}" class="underline">Click here</RouterLink> to sign up.
        </p>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>E-mail</label><br />
            <input
              type="email"
              name="email"
              v-model="form.email"
              placeholder="Enter your e-mail address"
              class="w-full mt-2 py-4 px-6 border-gray-200 rounded-lg"
            />
          </div>
          
          <div>
            <label>Password</label><br />
            <input
              type="password"
              name="password"              
              v-model="form.password"              
              placeholder="Enter your password"
              class="w-full mt-2 py-4 px-6 border-gray-200 rounded-lg"
            />
          </div>

          <!-- Uses the default slot? But where is it? -->
          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>

          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lag">
              Log in
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
