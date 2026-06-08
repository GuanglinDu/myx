from django.urls import path, URLPattern, URLResolver
from . import api

urlpatterns: list[ URLPattern | URLResolver] = [
    path('', api.conversation_list, name='conversation_list'),
    # The id is the conversation id, not the user id.
    path('<uuid:id>/', api.conversation_detail, name='conversation_detail'),
    path('<uuid:id>/send/', api.send_message, name='send_message'),
    path('<uuid:user_id>/get-or-create/', api.get_or_create_conversation,
         name='get_or_create_conversation'),
]
