#
from typing import TypeAlias
from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Post, PostAttachment, Comment, Like


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model: TypeAlias = PostAttachment
        fields: list[str] = ['id', 'image']


class PostSerializer(serializers.ModelSerializer):
    created_by: UserSerializer = UserSerializer(read_only=True)

    class Meta:
        model: TypeAlias = Post
        fields: list[str] = ['id', 'body', 'attachments', 'created_by',
                             'created_at_formatted', 'likes_count', 'liked']

    liked: serializers.SerializerMethodField

    def get_liked(self, obj: Post) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(pk=request.user.pk).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    created_by: UserSerializer = UserSerializer(read_only=True)
    
    class Meta:
        model: TypeAlias = Comment
        fields: list[str] = ['id', 'body', 'created_by', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    created_by: UserSerializer = UserSerializer(read_only=True)
    attachments: PostAttachmentSerializer = PostAttachmentSerializer(
        many=True, read_only=True)
    comments: CommentSerializer = CommentSerializer(many=True, read_only=True)

    class Meta:
        model: TypeAlias = Post
        fields: list[str] = ['id', 'body', 'attachments', 'created_by',
           'created_at_formatted', 'likes_count', 'liked', 'comments']

    liked: serializers.SerializerMethodField

    def get_liked(self, obj: Post) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(pk=request.user.pk).exists()
        return False
