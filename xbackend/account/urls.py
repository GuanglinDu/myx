from django.urls import path, URLPattern, URLResolver
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api

# URL dispatcher https://docs.djangoproject.com/en/6.0/topics/http/urls/
# There’s no need to add a leading slash, because every URL has that. For
# example, it’s articles, not /articles. But the trailing slash is
# mandatory!
urlpatterns: list[ URLPattern | URLResolver] = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('friends/send/<uuid:user_id>/', api.send_friendship_request,
         name='send_friendship_request'),
    path('friends/accept/<uuid:request_id>/', api.accept_friendship_request,
         name='accept_friendship_request'),
    path('friends/reject/<uuid:request_id>/', api.reject_friendship_request,
         name='reject_friendship_request'),
    path('friends/status/<uuid:user_id>/', api.get_friendship_status,
         name='get_friendship_status'),
    path('friends/<uuid:user_id>/', api.friends, name='friends'),
    path('friends/<uuid:user_id>/requests/', api.get_friendship_requests,
          name='get_friendship_requests'),
]
