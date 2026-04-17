import uuid
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from .models import Post
from .serializers import PostSerializer
from .forms import PostForm


@api_view(['GET'])
def post_list(request: Request) -> JsonResponse:
    posts: QuerySet[Post] = Post.objects.filter(
        Q(created_by=request.user) |
        Q(created_by__in=request.user.friends.all())
    ).order_by('-created_at')
    serializer: PostSerializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list_profile(request: Request, id: uuid.UUID) -> JsonResponse:
    user: User = User.objects.get(pk=id)
    posts: QuerySet[Post] = Post.objects.filter(created_by__id=id)
    posts_serializer: PostSerializer = PostSerializer(posts, many=True)
    user_serializer: UserSerializer = UserSerializer(user)

    # Determine friendship status if user is authenticated
    friendship_status: str = 'none'
    request_id: str = ''
    if request.user.is_authenticated:
        if str(request.user.id) == str(id):
            friendship_status = 'self'
        elif request.user.friends.filter(pk=id).exists():
            friendship_status = 'friends'
        else:
            # Check if they sent us a request
            pending_request: FriendshipRequest | None = \
              FriendshipRequest.objects.filter(
                created_for=request.user,
                created_by=user,
                status=FriendshipRequest.SENT
            ).first()
            if pending_request:
                friendship_status = 'pending'
                request_id = str(pending_request.id)
            else:
                # Check if we sent them a request
                sent_request: FriendshipRequest | None = \
                  FriendshipRequest.objects.filter(
                    created_for=user,
                    created_by=request.user,
                    status=FriendshipRequest.SENT
                ).first()
                if sent_request:
                    friendship_status = 'request_sent'

    return JsonResponse({
        'user': user_serializer.data,
        'posts': posts_serializer.data,
        'friendship_status': friendship_status,
        'request_id': request_id
    }, safe=False)


@api_view(['POST'])
def post_create(request: Request) -> JsonResponse:
    data: dict | list = request.data
    # print('data', data)  # cannot show

    form: PostForm = PostForm(data)
    if form.is_valid():
        post: Post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        serializer: PostSerializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        # return JsonResponse(form.errors, status=400)
        return JsonResponse('error', 'Add something here later')

    # These lines were created by Copilot and they work!
    # message: str = 'success'
    # serializer: PostSerializer = PostSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save(created_by=request.user)
    # else:
    #     message: str = 'error'

    # return JsonResponse({'message': message})
    # return JsonResponse({'hello': 'hepp'})
