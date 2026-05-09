Profiles - Build a Full-Stack Social Network with Django and Vue 3 | Part 4/16
https://www.youtube.com/watch?v=qM8WhgvbZDI&list=PLpyspNLjzwBlobEvnZzyWP8I-ORQcq4IO&index=4

0:00 Make it possible to view a profile
0:29 Create ProfileView.vue based on FeedView.vue
1:45 Use a RouterLink to replace the <a> tag for the profile image in App.vue
4:20 Show only your own posts on your own profile page
5:35 Remove the profile <div> on the top-left corner in FeedView.vue
6:20 Make sure the user get only his own feed on his profile page
10:00 Log out to create a new user to test other user's profile
11:20 Fix correct name on the profile page
11:50 Hide post when you're visiting someone else's profile
14:20 Show the user's name on his profile page
16:57 Hide the post form when you're visiting someone else profile (? bugs when switching user profiles)
18:05 Set up friendships (model changes)
18:50 Implement the search function in SearchView.vue
 - 19:25 Create the search app
 - 23:00 Set up a simple search
 - 26:00 Show the search result on SearchView.vue
 - 27:30 Search for the post at the same time
 - 29:50 Ignore empty posts
30:25 enable to click the user avatar to go to his avatar
32:45 Convert feed to a separate component (FeedItem.vue, refactoring SearchView.vue and FeedView.vue)
36:31 Reactore ProfileView.vue
38:10 Fix the infinite loop when calling onMounted hook in ProfileView.vue
40:20 Fix the bug that content cannot not update after clicking your own avatar on the top right corner

