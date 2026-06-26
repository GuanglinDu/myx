import uuid
from datetime import datetime
from django.db import models
from account.models import User
from post.models import Post


# How to set the choices in django.db.models.CharField? - Google AI Overview
# Key Behaviors to Keep in Mind:
# (1/3) Database Representation
# Django stores the short code (e.g., "new_friendrequest") inside the
# database, while the Django Admin panel displays the long description
# (e.g., "New friend request").
# (2/3) Accessing the Display Name
# You can access the human-readable string in your templates or views
# using the auto-generated getter method:
# instance.get_type_of_notification_display().
# (3/3) Form Layout
# When used inside a Django ModelForm, this field automatically renders
# as a drop-down HTML <select> widget.
class Notification(models.Model):
    NEWFRIENDREQUEST: str = 'new_friend_request'
    ACCEPTEDFRIENDREQUEST: str = 'accepted_friend_request'
    REJECTEDFRIENDREQUEST: str = 'rejected_friend_request'
    POST_LIKE: str = 'post_like'
    POST_COMMENT: str = 'post_comment'
    CHOICES_TYPE_OF_NOTIFICATION: tuple[tuple[str, str]] = (
        (NEWFRIENDREQUEST, 'New friend request'),
        (ACCEPTEDFRIENDREQUEST, 'Accepted friend request'),
        (REJECTEDFRIENDREQUEST, 'Rejected friend request'),
        (POST_LIKE, 'Post like'),
        (POST_COMMENT, 'Post comment')
    )

    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    body: str = models.TextField(blank=False, null=False)
    is_read: bool = models.BooleanField(default=False)
    type_of_notification: str = models.CharField(
        max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    # Django stores this FK as the column post_id in the
    # notification_notification table. It's nullable — it holds a Post
    # UUID or NULL.
    post: Post = models.ForeignKey(Post, on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_by: User = models.ForeignKey(
        User, related_name='created_notifications', on_delete=models.CASCADE)
    created_for: User = models.ForeignKey(
        User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at: datetime = models.DateTimeField(auto_now_add=True)


""" Updated at 20:58:15 on 20260623 Tue by Guanglin Du.
How to use the related_name in django.db.models.ForeignKey?
 - Google AI Overview
 
The *related_name* attribute in Django’s ForeignKey customizes the name of
the reverse relation from the target model back to the model that defines
the foreign key. By default, Django creates a reverse manager named
<modelname>_set. Adding related_name allows you to override this default
with a cleaner, more readable name.

See history/How-to-use-the-related_name-in-django.db.models.ForeignKey-20260623.png.
"""
