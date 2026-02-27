import { createApp } from 'vue';
import router from './router';
import { createPinia } from 'pinia';
import axios from 'axios';
import './index.css';
import App from './App.vue';

axios.defaults.baseURL = import.meta.env.VITE_API_URL;

const app = createApp(App);

app.use(createPinia());
app.use(router);
// app.use(axios); // causes many recursion errors
app.mount('#app');
