import uuid
from rest_framework.request import Request
from account.models import User, FriendshipRequest
from post.models import Post
from .models import Notification


def create_notification(request: Request, type_of_notification: str,
                        post_id: uuid.UUID = None,
                        friendshiprequest_id: uuid.UUID = None) -> Notification:
    post: Post | None = None
    if post_id is not None:
        post = Post.objects.get(pk=post_id)

    created_for: User | None = None
    body: str = ""

    if type_of_notification == 'post_like':
        body = f"{request.user.name} liked one of your posts!"
        created_for = post.created_by
    elif type_of_notification == 'post_comment':
        body = f"{request.user.name} commented on one of your posts!"
        created_for = post.created_by
    elif type_of_notification == 'new_friend_request':
        friendshiprequest: FriendshipRequest = FriendshipRequest.objects.get(
            pk=friendshiprequest_id)
        created_for = friendshiprequest.created_for
        body = f"{request.user.name} sent you a friend request!"
    elif type_of_notification == 'accepted_friend_request':
        friendshiprequest: FriendshipRequest = FriendshipRequest.objects.get(
            pk=friendshiprequest_id)
        created_for = friendshiprequest.created_for
        body = f"{request.user.name} accepted your friend request!"
    elif type_of_notification == 'rejected_friend_request':
        friendshiprequest: FriendshipRequest = FriendshipRequest.objects.get(
            pk=friendshiprequest_id)
        created_for = friendshiprequest.created_for
        body = f"{request.user.name} rejected your friend request!"
    else:
        body = f"Unknown type_of_notification: {type_of_notification}!"

    notification: Notification = Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification,
        post=post,
        created_by=request.user,
        created_for=created_for,
    )

    return notification
