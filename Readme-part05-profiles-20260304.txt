Friendships - Build a Full-Stack Social Network with Django and Vue 3 | Part 5/16
============================================================================================
https://www.youtube.com/watch?v=V4SDOq5WvS4&list=PLpyspNLjzwBlobEvnZzyWP8I-ORQcq4IO&index=5
00:00 Overview
00:10 Set up friendships (model changes)
00:29 Make it possible to send friend requests
 - 09:30 Modify the backend to respond to the friendship request sending (account/api.py)
 - 13:45 Hide the button 'Send friendship request' on the Profile page (unfinished)
15:30 Make it possible to accept friend requests
 - 16:20 Create FriendsView.vue
 - 17:50 Add FriendsView.vue to the router
 - 18:20 Add a RouterLink to FriendView.vue in ProfileView.vue
 - 21:00 Retrieve the friend list in account/api.py
 - 25:30 Modify account/urls.py to add the friends URL
 