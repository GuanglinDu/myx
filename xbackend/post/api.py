from django.db.models.query import QuerySet
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from .models import Post
from .serializers import PostSerializer


@api_view(['GET'])
def post_list(request: Request) -> JsonResponse:
    posts: QuerySet[Post] = Post.objects.all()
    serializer: PostSerializer = PostSerializer(posts, many=True)
    return JsonResponse({'data': serializer.data})
