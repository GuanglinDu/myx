import uuid
from django.http import JsonResponse
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
# from notification.utils import create_notification
from .forms import SignupForm, ProfileForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer


# Appended at 10:40:46 on 20260416 Thu by Guanglin Du.
# How HTTP Requests Are Created & Processed in Django REST Framework (DRF)
# - doubao
# 1. The DRF Request fixes big weaknesses of Django’s raw request:
# - Unifies all input data into one place (request.data)
# - Automatically parses JSON, form data, files
# - Handles authentication cleanly
# - Gives you better error handling
# 
# 2. Key Properties of the DRF Request Object (You Use These Daily!)
# Property	        Purpose
# request.method	HTTP method: GET, POST, PUT, etc.
# request.data	Parsed body data (JSON/form data) → replaces Django’s
#                request.POST/request.body
# request.query_params	Query parameters (?page=1&search=test) → replaces
#                       request.GET
# request.headers	HTTP headers (Authorization, Content-Type)
# request.user	Authenticated user (from token/session)
# request.auth	Authentication token (JWT, etc.)
# 
# 3. Demos (JSON body parsed automatically)
# token: str = request.headers.get('Authorization')
# request.query_params.get('page') = parsed query string (e.g., ?page=2)
# request.data.get('email') = parsed request body (JSON/form)
@api_view(['GET'])
def me(request: Request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request: Request) -> JsonResponse:
    data: dict | list = request.data
    message: str = 'success'

    form: SignupForm = SignupForm({
        'name': data.get('name'),      
        'email': data.get('email'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    # form.save() creates and returns a User object with a securely
    # hashed password.
    if form.is_valid():
        user: User = form.save()

        # Sends verification email later!
    else:
      message: str = 'error'

    return JsonResponse({'message': message})


@api_view(['POST'])
def send_friendship_request(request: Request,
                            user_id: uuid.UUID) -> JsonResponse:
    """Send a friendship request to another user.
    
    user_id: the target user's UUID
    """
    user: User = request.user  # the logged-in user sending the request

    # target_user: user whose profile we are visiting
    try:
        target_user: User = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Check if they are already friends
    if user.friends.filter(pk=user_id).exists():
        return JsonResponse({'error': 'You are already friends'}, status=400)

    # Check if a request already exists
    existing_request: FriendshipRequest | None = \
      FriendshipRequest.objects.filter(
        created_for=user,        # created_for = you, the logged-in user
        created_by=target_user,  # created_by = them
        status=FriendshipRequest.SENT
    ).first()

    if existing_request:
        return JsonResponse({'error': 'They already sent you a request'},
                             status=400)

    # Check if we already sent a request
    existing_request_sent: FriendshipRequest | None = \
      FriendshipRequest.objects.filter(
        created_for=target_user,   # created_for = them
        created_by=user,           # created_by = you, the logged-in user
        status=FriendshipRequest.SENT
    ).first()

    if existing_request_sent:
        return JsonResponse({'error': 'You already sent a request'}, status=400)

    # Create the friendship request if all checks pass
    FriendshipRequest.objects.create(
        created_for=target_user,
        created_by=user,
        status=FriendshipRequest.SENT
    )

    # Remove each other from people_you_may_know since you both are going
    # to become friends if the request is accepted.
    user.people_you_may_know.remove(target_user)
    target_user.people_you_may_know.remove(user)

    return JsonResponse({'message': 'Friendship request sent'})


@api_view(['POST'])
def accept_friendship_request(request: Request,
                              request_id: uuid.UUID) -> JsonResponse:
    """Accept a friendship request."""
    user: User = request.user

    try:
        friendship_request: FriendshipRequest = FriendshipRequest.objects.get(
            pk=request_id,
            created_for=user,
            status=FriendshipRequest.SENT
        )
    except FriendshipRequest.DoesNotExist:
        return JsonResponse({'error': 'Request not found'}, status=404)

    # Add each user to other's friends list
    user.friends.add(friendship_request.created_by)
    friendship_request.created_by.friends.add(user)

    # Increment friends_count for both users
    user.friends_count += 1
    user.save()
    friendship_request.created_by.friends_count += 1
    friendship_request.created_by.save()

    # Delete the friendship request
    friendship_request.delete()

    return JsonResponse({'message': 'Friendship request accepted'})


@api_view(['POST'])
def reject_friendship_request(request: Request,
                              request_id: uuid.UUID) -> JsonResponse:
    """Reject a friendship request."""
    user: User = request.user

    try:
        friendship_request: FriendshipRequest = \
          FriendshipRequest.objects.get(
            pk=request_id,
            created_for=user,
            status=FriendshipRequest.SENT
        )
    except FriendshipRequest.DoesNotExist:
        return JsonResponse({'error': 'Request not found'}, status=404)

    # Update status to rejected and delete
    friendship_request.status = FriendshipRequest.REJECTED
    friendship_request.save()
    friendship_request.delete()

    return JsonResponse({'message': 'Friendship request rejected'})


@api_view(['GET'])
def get_friendship_status(request: Request,
                          user_id: uuid.UUID) -> JsonResponse:
    """Get friendship status with another user."""
    current_user: User = request.user

    # Don't check status for yourself
    if str(current_user.id) == str(user_id):
        return JsonResponse({'status': 'self'})

    try:
        target_user: User = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Check if already friends
    if current_user.friends.filter(pk=user_id).exists():
        return JsonResponse({'status': 'friends'})

    # Check if they sent us a request (we need to accept/reject)
    pending_request: FriendshipRequest | None = \
      FriendshipRequest.objects.filter(
        created_for=current_user,
        created_by=target_user,
        status=FriendshipRequest.SENT
    ).first()

    if pending_request:
        return JsonResponse({
            'status': 'pending',
            'request_id': str(pending_request.id)
        })

    # Check if we sent them a request
    sent_request: FriendshipRequest | None = \
      FriendshipRequest.objects.filter(
        created_for=target_user,
        created_by=current_user,
        status=FriendshipRequest.SENT
    ).first()

    if sent_request:
        return JsonResponse({'status': 'request_sent'})

    return JsonResponse({'status': 'none'})


@api_view(['GET'])
def get_friendship_requests(request: Request,
                            user_id: uuid.UUID) -> JsonResponse:
    """Get all pending friendship requests sent to the current user."""
    user: User = request.user

    # Get all pending requests sent to the current user
    pending_requests: list[FriendshipRequest] = \
      FriendshipRequest.objects.filter(
        created_for=user,
        status=FriendshipRequest.SENT
    ).select_related('created_by')

    serializer: FriendshipRequestSerializer = FriendshipRequestSerializer(
        pending_requests, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def friends(request: Request, user_id: uuid.UUID) -> JsonResponse:
    """Get a list of friends for a specific user."""
    # The user whose friends we want to get
    # user: User = request.user
    user: User = User.objects.get(pk=user_id)
    friendshipRequests: QuerySet[FriendshipRequest] = []

    # If the user is requesting their own friends list, we can optimize by
    # using the already prefetched friends
    if user == request.user:
        friendshipRequests: QuerySet[FriendshipRequest] = \
            FriendshipRequest.objects.filter(created_for=user)
    
    # Get friends for the current user
    friends: list[User] = user.friends.all()

    # Without .data, there'll be the following error:
    # TypeError: Object of type UserSerializer is not JSON serializable
    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'friendshipRequests': FriendshipRequestSerializer(
            friendshipRequests, many=True).data
    }, safe=False)
