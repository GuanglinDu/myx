from typing import TypeAlias
from rest_framework import serializers
from .models import User, FriendshipRequest


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model: TypeAlias = User
        fields: list[str] = [
            'id', 'name', 'email', 'friend_count', 'post_count'
        ]


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by: UserSerializer = UserSerializer(read_only=True)

    class Meta:
        model: TypeAlias = FriendshipRequest
        fields: list[str] = ['id', 'status', 'created_by']
