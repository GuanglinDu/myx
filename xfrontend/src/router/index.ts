/**
 * Created at 17:37:07 on 20260204 Wed by Guanglin Du.
 * https://router.vuejs.org/guide/
 */
import { createWebHashHistory, createRouter } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import NotFoundView from "@/views/NotFoundView.vue";

// (1/2) Creates the routes options
const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    component: () => import("@/views/AboutView.vue"),
  },
  {
    path: "/feed",
    name: "feed",
    component: () => import("@/views/FeedView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
  },
  {
    path: "/messages",
    name: "messages",
    component: () => import("@/views/MessagesView.vue"),
  },
  {
    path: "/search",
    name: "search",
    component: () => import("@/views/SearchView.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("@/views/SignupView.vue"),
  },
  { path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFoundView
  },
];

// (2/2) Creates the router instance which has
// router.currentRoute    // Current route info
// router.options         // Configuration options
// router.beforeEach()    // Navigation guard method
// router.afterEach()     // Post-navigation hook
// router.push()          // Navigation method
// router.replace()       // Replace method
// router.go()            // History method
//
// Why cannot I open the URLs defined by RouterView in Vue.js 3
// manually? - Google AI Overview
// Using Hash Mode
// If you cannot configure the server, you can use Hash Mode
//  (createWebHashHistory()). 
// How it works:
// This adds a # to the URL (e.g., example.com/#/user/1). The browser
// does not send the part after # to the server, so the server always
// serves the main index.html, allowing Vue Router to handle the route.
// e.g.,
// http://localhost:5174/#/signup/
// http://localhost:5174/#/UserDetails/
const router = createRouter({
  history: createWebHashHistory(),
  routes, // property sharthand
  scrollBehavior(to, from, savedPosition) {
    // Always scroll to top
    return { top: 0 };
  },
});

export default router;
