import uuid
from datetime import datetime
from django.db import models
# This module is nonexistent as is dynamically generated!
# from django.db.models.manager import ManyRelatedManager
from django_stubs_ext.db.models.manager import ManyRelatedManager
from django.utils.timesince import timesince
from account.models import User


class Conversation(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)    
    participants: "ManyRelatedManager[User]" = models.ManyToManyField(
        User, related_name='conversations')
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    def modified_at_formatted(self) -> str:
        return timesince(self.modified_at)


class ConversationMessage(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)    
    conversation: Conversation = models.ForeignKey(
        Conversation, related_name='messages', on_delete=models.CASCADE)
    body: str = models.TextField(blank=True, null=True)
    sent_to: User = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE)
    created_by: User = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE)
    created_at: datetime = models.DateTimeField(auto_now_add=True)        

    def created_at_formatted(self) -> str:
        return timesince(self.created_at)
