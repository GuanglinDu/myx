from typing import TypeAlias
from rest_framework import serializers
from account.serializers import UserSerializer
from  .models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
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
