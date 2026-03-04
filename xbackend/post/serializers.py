# 
from typing import TypeAlias
from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Post, PostAttachment


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model: TypeAlias = PostAttachment
        fields: list[str] = ['id', 'image']


class PostSerializer(serializers.ModelSerializer):
    created_by: UserSerializer = UserSerializer(read_only=True)

    class Meta:
        model: TypeAlias = Post
        fields: list[str] = ['id', 'body', 'attachments', 'created_by',
                             'created_at_formatted']
