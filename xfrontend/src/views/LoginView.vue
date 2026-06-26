<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router"; // vs userRoute
import axios, { type AxiosResponse } from "axios";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
const $router = useRouter(); // vs $route = useRoute()

interface LoginCredentials {
  email: string;
  password: string;
}

const form: LoginCredentials = {
  email: "",
  password: "",
};

const errors = ref<Array<string>>([]);

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

async function submitForm(): Promise<void> {
  errors.value = [];

  if (form.email === "") {
    errors.value.push("Your e-mail is missing");
  }

  if (form.password === "") {
    errors.value.push("Your password is missing");
  }

  if (errors.value.length === 0) {
    await axios
      .post("/api/login/", form)
      .then((response: AxiosResponse) => {
        // Error: response.data.message undefined!
        // if (response.data.message === "success") {
        userStore.setToken(response.data);

        console.log(response.data.access);

        axios.defaults.headers.common["Authorization"] =
          "Bearer " + response.data.access;
      })
      .catch((error) => {
        console.log("Login error: ", error);

        errors.value.push(
          error.response?.data?.detail ??
            "Invalid email or password.",
        );
      });

    await axios
      .get("/api/me/")
      .then((response) => {
        userStore.setUserInfo(response.data);

        $router.push("/feed"); // dynamic routing
      })
      .catch((error) => {
        console.log("About me error: ", error);
      });
  } else {
    console.log(errors.value);
  }
}
</script>

<template>
  <div class="mx-auto grid max-w-7xl grid-cols-2 gap-4">
    <div class="main-left">
      <div class="rounded-lg border border-gray-200 bg-white p-12">
        <h1 class="mb-6 text-2xl">Log in</h1>
        <p class="mb-6 text-gray-500">
          This is the log in page based on the tutorial "Build a Full-Stack
          Social Network with Django and Vue 3: From Idea to Launch".
        </p>

        <p class="font-bold">
          Don't have an account?
          <RouterLink :to="{ name: 'signup' }" class="underline"
            >Click here</RouterLink
          >
          to sign up.
        </p>
      </div>
    </div>

    <div class="main-right">
      <div class="rounded-lg border border-gray-200 bg-white p-12">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>E-mail</label><br />
            <input
              type="email"
              name="email"
              v-model="form.email"
              placeholder="Enter your e-mail address"
              class="mt-2 w-full rounded-lg border-gray-200 px-6 py-4"
            />
          </div>

          <div>
            <label>Password</label><br />
            <input
              type="password"
              name="password"
              v-model="form.password"
              placeholder="Enter your password"
              class="mt-2 w-full rounded-lg border-gray-200 px-6 py-4"
            />
          </div>

          <!-- The template works as a place-holder. -->
          <template v-if="errors.length > 0">
            <div class="rounded-lg bg-red-300 p-6 text-white">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>

          <button class="rounded-lag bg-purple-600 px-6 py-4 text-white">
            Log in
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
