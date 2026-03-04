import uuid
from django.db.models.query import QuerySet
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from account.models import User
from account.serializers import UserSerializer
from .models import Post
from .serializers import PostSerializer
from .forms import PostForm


@api_view(['GET'])
def post_list(request: Request) -> JsonResponse:
    posts: QuerySet[Post] = Post.objects.all()  # change later to feed
    serializer: PostSerializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list_profile(request: Request, id: uuid.UUID) -> JsonResponse:
    user: User = User.objects.get(pk=id)
    posts: QuerySet[Post] = Post.objects.filter(created_by__id=id)
    posts_serializer: PostSerializer = PostSerializer(posts, many=True)
    user_serializer: UserSerializer = UserSerializer(user)

    return JsonResponse({
        'user': user_serializer.data,
        'posts': posts_serializer.data
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
