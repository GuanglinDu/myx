<script setup lang="ts">
import axios from 'axios';
import { useToastStore } from '@/stores/toast';

const toastStore = useToastStore();

interface SignupForm {
  name: string;
  email: string;
  password1: string;
  password2: string;
}

// The JSON object sent by AXIOS to the signup API of the backend
let form: SignupForm = {
  name: "",
  email: "",
  password1: "",
  password2: "",
};

let errors: Array<string> = [];

function submitForm(): void {
  errors = [];

  if (form.name === "") {
    errors.push("Your name is missing");
  }

  if (form.email === "") {
    errors.push("Your e-mail is missing");
  }

  if (form.password1 === "") {
    errors.push("Your password is missing");
  }

  if (form.password1 !== form.password2) {
    errors.push("The password does not match");
  }

  if (errors.length === 0) {
    axios
      .post("/api/signup/", form)
      .then((response) => {
        toastStore.showToast(
          5000,
          "The user is registered. Please log in.",
          "bg-emerald-500"
        );

        form.email = "";
        form.name = "";
        form.password1 = "";
        form.password2 = "";
      })
      .catch((error) => {
        // Backend returns 400 with {errors: {field: [messages]}} on
        // invalid input (taken email, weak password, mismatch, ...).
        // Surface the first field-level message to the user.
        const fieldErrors: Record<string, string[]> | undefined =
          error.response?.data?.errors;
        const firstMsg: string | undefined = fieldErrors
          ? Object.values(fieldErrors).flat()[0]
          : undefined;
        toastStore.showToast(
          5000,
          firstMsg ?? "Something went wrong. Please try again.",
          "bg-red-300"
        );
      });
  } else {
    console.log(errors);

    let msg: string = errors[0] ?? 'Something wrong!';
    toastStore.showToast(
      5000,
      msg,
      "bg-red-300"
    );
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Sign up</h1>
        <p class="mb-6 text-gray-500">
        This is the sign up page based on the tutorial "Build a Full-Stack Social Network with Django and Vue 3: From Idea to Launch".            
        </p>

        <p class="font-bold">
          Already have an account? <RouterLink :to="{'name': 'login'}" class="underline">Click here</RouterLink> to log in.
        </p>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>Name</label><br />
            <input
              type="text"
              name="name"
              v-model="form.name"              
              placeholder="Enter your full name"
              class="w-full mt-2 py-4 px-6 border-gray-200 rounded-lg"
            />
          </div>

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
              name="password1"
              v-model="form.password1"
              placeholder="Enter your password"
              class="w-full mt-2 py-4 px-6 border-gray-200 rounded-lg"
            />
          </div>

          <div>
            <label>Repeat password</label><br />
            <input
              type="password"
              name="password2"
              v-model="form.password2"                    
              placeholder="Repeat your password"
              class="w-full mt-2 py-4 px-6 border-gray-200 rounded-lg"
            />
          </div>

          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>

          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lag">
              Sign up
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
