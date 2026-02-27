import { fileURLToPath, URL } from 'node:url';
import { defineConfig, loadEnv } from "vite";
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd());
  return {
    plugins: [
      vue(),
    ],
    resolve: {
      // (1/2) Makes alias @ work. (2/2) is in tsconfig.app.json.
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      port: parseInt(env.VITE_PORT || '5174'),
      // host: 'localhost', // optional
      // open: true         // optional: auto-opens the brwoser
    },
  };
});
