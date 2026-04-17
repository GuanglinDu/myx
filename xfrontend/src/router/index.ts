/**
 * Created at 17:37:07 on 20260204 Wed by Guanglin Du.
 * https://router.vuejs.org/guide/
 */
import { createWebHashHistory, createRouter } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import NotFoundView from "@/views/NotFoundView.vue";

// (1/2) Creates the routes options
/*
 Updated at 09:27:54 on 20260414 Tue by Guanglin Du.
 
 1. What does "props: true" do in router/index.ts? -- I asked Claude Code

● When props: true is set on a route, the route params are automatically passed
as props to the component.

  For the route /profile/:id:
  {
    path: "/profile/:id",
    name: "profile",
    component: () => import("@/views/ProfileView.vue"),
    props: true,
  }

The :id param is passed as a prop named id to ProfileView.vue. This lets you use:
  const props = defineProps<{ id: string }>();
  // Access via props.id instead of useRoute().params.id

Why it's useful:
 - Cleaner — component doesn't need to import useRoute or couple with the router
 - More testable — the component only depends on its props, not the router
 - Reusable — the same component could be used with different props in other
   contexts
 
2. Can I use the $route.params.id at the same time, where
const $route  = useRouter() and import { useRouter }  from 'vue-router' in
ProfileView.vue?

● Yes, but it's unnecessary and redundant.

 When props: true is set on the route, useRoute().params.id and $props.id will
 have the same value. You wouldn't use both — pick one approach:

 Current approach (prop-based):
 const $props = defineProps(["id"])
 // Use: $props.id

 Alternative approach (route-based):
 const $route = useRoute()
 // Use: $route.params.id

Mixing both in the same component would be redundant and confusing.
The component is already using $props.id exclusively (lines 36, 43, etc.),
which is the cleaner pattern since it makes the component more testable and
decoupled from the router.

However, if you wanted to use $route.params.id instead of props, you would:
  1. Remove props: true from the route
  2. Add const $route = useRoute() in the component
  3. Use $route.params.id instead of props.id
 */
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
    path: "/profile/:id",
    name: "profile",
    component: () => import("@/views/ProfileView.vue"),
    props: true, // route :id param is passed as the `id` prop
  },
  {
    path: "/profile/:id/friends",
    name: "friends",
    component: () => import("@/views/FriendsView.vue"),
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
// router.push()          // Navigation method (programmatic navigation)
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
