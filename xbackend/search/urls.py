from django.urls import path, include, URLPattern, URLResolver

from . import api

urlpatterns: list[ URLPattern | URLResolver] = [
    path('', api.search, name='search'),
]
