import uuid
from datetime import datetime
from django.utils.timesince import timesince
from django.db import models
from account.models import User


class Like(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    created_by: User = models.ForeignKey(User, related_name='likes',
                                         on_delete=models.CASCADE)
    created_at: datetime = models.DateTimeField(auto_now_add=True)


class PostAttachment(models.Model):
    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    image: str = models.ImageField(upload_to='post_attachments')
    created_by: User = models.ForeignKey(
        'account.User', related_name='post_attachments',
         on_delete=models.CASCADE)


# django.db.models.fields.related_descriptors
#     .create_forward_many_to_many_manager.<locals>.ManyRelatedManager
class Post(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    body: str = models.TextField(blank=True, null=True)
    # WARNINGS: post.Post.attachments: (fields.W340) null has no effect on
    # ManyToManyField.
    # attachments = models.ManyToManyField('PostAttachment', blank=True,
    #                                      null=True)
    attachments: 'ManyRelatedManager' = models.ManyToManyField(
        'PostAttachment', blank=True)

    likes: "ManyRelatedManager" = models.ManyToManyField(Like, blank=True)
    likes_count: int = models.IntegerField(default=0)
    liked: bool = models.BooleanField(default=False)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    created_by: User = models.ForeignKey(
        'account.User', related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering: list[str] = ['-created_at']


    def created_at_formatted(self) -> str:
        return timesince(self.created_at)
