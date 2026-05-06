from django.urls import path, include, URLPattern, URLResolver
from . import api

# The URL path variable will pass the user's or post's UUID to the view
# functions to retrieve the specific post from the database and perform
# the necessary operations (like fetching details, liking, etc.).
urlpatterns: list[ URLPattern | URLResolver] = [
    path('', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    # The user's UUID
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    # The post's UUID
    path('<uuid:id>/', api.post_detail, name='post_detail'),
    path('<uuid:id>/like/', api.post_like, name='post_like'),
]
