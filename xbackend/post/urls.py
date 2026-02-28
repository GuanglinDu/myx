from django.urls import path, include, URLPattern, URLResolver

from . import api

urlpatterns: list[ URLPattern | URLResolver] = [
    path('', api.post_list, name='post_list'),
]
