from django.urls import path, URLPattern, URLResolver
from . import api

urlpatterns: list[ URLPattern | URLResolver] = [
    path('', api.notifications, name='notifications'),
    path('read/<uuid:pk>/', api.read_notification, name='read_notifications'),
]
