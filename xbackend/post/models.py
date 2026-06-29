import uuid
from datetime import datetime
# This module is nonexistent as is dynamically generated!
# from django.db.models.manager import ManyRelatedManager
from django_stubs_ext.db.models.manager import ManyRelatedManager
from django.utils.timesince import timesince
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from xbackend import settings
from account.models import User


class Comment(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    body: str = models.TextField(blank=True, null=True)
    created_by: User = models.ForeignKey(User, related_name='comments',
                                         on_delete=models.CASCADE)
    created_at: datetime = models.DateTimeField(auto_now_add=True)

    def created_at_formatted(self) -> str:
        return timesince(self.created_at)
    
    class Meta:
        ordering: list[str] = ['created_at']


class Like(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    created_by: User = models.ForeignKey(User, related_name='likes',
                                         on_delete=models.CASCADE)
    created_at: datetime = models.DateTimeField(auto_now_add=True)


class PostAttachment(models.Model):
    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    # The uploaded image will be stored in MEDIA_ROOT/post_attachments/filename.
    # The upload_to parameter determines the subfolder inside your
    # /media/ directory where images will go.
    # ImageField depends on the pillow library.
    image: ImageFieldFile = models.ImageField(upload_to='post_attachments')
    created_by: User = models.ForeignKey(
        User, related_name='post_attachments',
         on_delete=models.CASCADE)
    
    # Claude Code uses self.image directly without touching this.
    def get_image(self) -> str:
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return ''


# django.db.models.fields.related_descriptors.
#   create_forward_many_to_many_manager.<locals>.ManyRelatedManager
# 
# How to type-annotate the ManyToManyField in Django? - Google AI Overview
# To type-annotate a ManyToManyField in Django correctly, especially when
# using tools like django-stubs, you must account for the fact that accessing
# the field on a model instance returns a manager (specifically a
# ManyRelatedManager), not a list or single object.
class Post(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    body: str = models.TextField(blank=True, null=True)
    # 1. WARNINGS: post.Post.attachments: (fields.W340) null has no effect on
    # ManyToManyField.
    # attachments = models.ManyToManyField('PostAttachment', blank=True,
    #                                      null=True)
    # 2. How to type-annotate the ManyToManyField in Django?
    # *Type comments* instead of direct type annotations are used here because
    # Django's ORM does not support direct type annotations for
    # ManyToManyField. The actual field is defined without type annotations,
    # and the type is provided as a comment for static type checkers.
    attachments: "ManyRelatedManager[PostAttachment]" = models.ManyToManyField(
        'PostAttachment', blank=True)

    likes: "ManyRelatedManager[Like]" = models.ManyToManyField(Like, blank=True)
    like_count: int = models.IntegerField(default=0)
    liked: bool = models.BooleanField(default=False)

    comments: "ManyRelatedManager[Comment]" = models.ManyToManyField(
        Comment, blank=True)
    comments_count: int = models.IntegerField(default=0)

    reported_by_users: "ManyRelatedManager[User]" = models.ManyToManyField(
        User, blank=True)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    created_by: User = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)

    def created_at_formatted(self) -> str:
        return timesince(self.created_at)
    class Meta:
        ordering: list[str] = ['-created_at']


class Trend(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    hashtag: str = models.CharField(max_length=255, unique=True)
    occurences: int = models.IntegerField(default=0)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
