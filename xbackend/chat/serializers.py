from typing import TypeAlias
from rest_framework import serializers
from account.serializers import UserSerializer
from  .models import Conversation, ConversationMessage


# *Nested Serializers in DRF*
# How to create a serializer which uses another model in DRF?
#  - Google AI Overview
# To create a serializer that uses another model in Django REST
# Framework (DRF), you typically use a nested serializer. This involves
# defining a serializer for the related model and then including it as
# a field in your main serializer.
# 
# (1/3) Basic Nested Serializer (Read-Only)
# The simplest way to include another model's data is to nest its
# serializer within the parent. This is ideal for GET requests where you
# want full details of a related object instead of just its ID.
# 
# (2/3) Handling One-to-Many Relationships
# If the relationship is a "to-many" (like a blog post having many
# comments), use the many=True argument.
class ConversationSerializer(serializers.ModelSerializer):
    """Nested Serializers are read-only by default, so we don't need to
    explicitly set read_only=True here.
    """
    participants: UserSerializer = UserSerializer(many=True, read_only=True)

    class Meta:
        model: TypeAlias = Conversation
        fields: tuple[str, ...] = (
            'id', 'participants', 'created_at', 'modified_at_formatted'
        )


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to: UserSerializer = UserSerializer(read_only=True)
    created_by: UserSerializer = UserSerializer(read_only=True)

    class Meta:
        model: TypeAlias = ConversationMessage
        fields: tuple[str, ...] = (
            'id', 'body', 'sent_to', 'created_by', 'created_at_formatted'
        )


class ConversationDetailSerializer(serializers.ModelSerializer):
    participants: UserSerializer = UserSerializer(many=True, read_only=True)
    messages: ConversationMessageSerializer = ConversationMessageSerializer(
        many=True, read_only=True)

    class Meta:
        model: TypeAlias = Conversation
        fields: tuple[str, ...] = (
            'id', 'participants', 'created_at', 'modified_at_formatted',
            'messages'
        )


# (3/3) Writable Nested Serializers
# By default, nested serializers are read-only. If you want to create
# or update related objects through a single request, you must override
# the .create() or .update() methods in the parent serializer to handle
# the nested data manually.