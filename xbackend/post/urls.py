from django.urls import path, include, URLPattern, URLResolver

from . import api

urlpatterns: list[ URLPattern | URLResolver] = [
    path('', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('like/<uuid:id>/', api.post_like, name='post_like'),
]
