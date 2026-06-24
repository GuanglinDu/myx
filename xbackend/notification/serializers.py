from typing import TypeAlias
from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)

    class Meta:
        model: TypeAlias = Notification
        fields: tuple[str, ...] = (
            'id', 'body', 'is_read', 'type_of_notification', 'post_id',
            'created_by', 'created_for'
        )