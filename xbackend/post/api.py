import uuid
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import (api_view)
from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from .models import Post, Like, Comment, Trend
from .serializers import (
    PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
)
from .forms import PostForm


@api_view(['GET'])
def post_list(request: Request) -> JsonResponse:
    posts: QuerySet[Post] = Post.objects.filter(
        Q(created_by=request.user) |
        Q(created_by__in=request.user.friends.all())
    ).order_by('-created_at')

    # trend: str = request.GET.get('trend', '')         # Django way    
    trend: str = request.query_params.get('trend', '')  # DRF way
    if trend:
        posts = posts.filter(body__icontains=f'#{trend}')
    
    serializer: PostSerializer = PostSerializer(
        posts, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request: Request, id: uuid.UUID) -> JsonResponse:
    post: Post = Post.objects.get(pk=id)
    serializer: PostDetailSerializer = PostDetailSerializer(
        post, context={'request': request})
    return JsonResponse({ 'post': serializer.data }, safe=False)


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


# Instead of storing post_count, compute it on-the-fly
# user.post_count = user.posts.count()  # Accesses the reverse FK relation
@api_view(['POST'])
def post_create(request: Request) -> JsonResponse:
    data: dict | list = request.data
    # print('data', data)  # cannot show

    form: PostForm = PostForm(data)
    if form.is_valid():
        post: Post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        # Update the author's post_count
        user: User = request.user
        user.post_count += 1
        # This bypasses change detection — it updates exactly what you list,
        # regardless of whether Django thinks it changed.
        user.save(update_fields=['post_count'])

        serializer: PostSerializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid data', 'details': form.errors},
                            status=400, safe=False)

    # These lines were created by Copilot and they work!
    # message: str = 'success'
    # serializer: PostSerializer = PostSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save(created_by=request.user)
    # else:
    #     message: str = 'error'

    # return JsonResponse({'message': message})
    # return JsonResponse({'hello': 'hepp'})


@api_view(['POST'])
def post_like(request: Request, id: uuid.UUID) -> JsonResponse:
    """id is the post's UUID passed from the URL path variable, while
    we get the user from the request.
    """
    post: Post = Post.objects.get(pk=id)        
    # Checks if the user has already liked the post.
    existing_like: Like = post.likes.filter(created_by=request.user).first()

    # Toggles the like status: if the user has already liked the post, it
    # removes the like; otherwise, it creates a new like. It also updates
    # the like_count accordingly and returns the new like status and
    # count in the response.
    if existing_like:
        existing_like.delete()
        post.like_count = max(0, post.like_count - 1)
        liked: bool = False
    else:
        like: Like = Like(created_by=request.user)
        like.save()
        post.likes.add(like)
        post.like_count += 1
        liked: bool = True

    post.save()
    return JsonResponse({'liked': liked, 'like_count': post.like_count},
                        safe=False)


@api_view(['DELETE'])
def post_delete(request: Request, id: uuid.UUID) -> JsonResponse:
    """Delete a post. Only the author can delete their own post."""
    post: Post = Post.objects.get(pk=id)

    if post.created_by != request.user:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    author: User = post.created_by
    post.delete()

    author.post_count = max(0, author.post_count - 1)
    author.save(update_fields=['post_count'])

    return JsonResponse({'message': 'Post deleted'}, safe=False)


@api_view(['POST'])
def create_comment(request: Request, id: uuid.UUID) -> JsonResponse:
    post: Post = Post.objects.get(pk=id)
    # Similar logic to post_like, but for comments. You would create a new
    # Comment object, associate it with the post, and return the updated list
    # of comments or the new comment in the response.
    # print(request.data)
    comment: Comment = Comment(
        body=request.data.get('body', ''),
        created_by=request.user
    )
    comment.save()
    # Another way to create the comment and associate it with the post:
    # comment = Comment.objects.create(
    #     body=request.data.get('body', ''),
    #     created_by=request.user
    # )
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    serializer: CommentSerializer = CommentSerializer(comment)
    return JsonResponse(serializer.data, safe=False)


# Updated at 08:12:40 on 20260602 Tue by Guanglin Du.
# *Dunder in Django - Google AI Overview*
# In Django, the term "dunder" (short for "double underscore") refers
# to two entirely different concepts depending on whether you are
# querying data via the ORM or writing standard Python code within your
# models.
# 
# (1/2) Django ORM Query Lookup (Field Lookups)
# In the Django Object-Relational Mapper (ORM), a double underscore __
# is used as a syntax separator to perform field lookups, handle joins
# across database relationships, and apply filters.
# (1.1/2) Relationship Joins: Follow foreign keys or many-to-many
# fields to query data from related tables. 
#   # Finds books where the related author's name is 'Tolstoy':
#   Book.objects.filter(author__name='Tolstoy')
# (1.2/2) Field Lookups: Apply specific SQL modifications (like LIKE,
# IN, >, or <).
#   # Translates to an SQL 'LIKE %django%' query (case-insensitive)
#   Post.objects.filter(title__icontains='django')
#   # Translates to a greater-than (>) SQL query
#   Product.objects.filter(price__gt=50)
# 
# (2/2) Python Dunder Methods in Django Models
# To define built-in methods and variables, e.g.,
# __init__(self), __str__(self), __eq__(self), __repr__(self), etc.
@api_view(['GET'])
def trends_list(request: Request) -> JsonResponse:
    """Return top 10 trending hashtags with at least 10 occurrences."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    trends: QuerySet[Trend] = Trend.objects.filter(
        occurences__gte=1
    ).order_by('-occurences')[:10]
    # trends: QuerySet[Trend] = Trend.objects.all().order_by('-occurences')[:10]
    serializer: TrendSerializer = TrendSerializer(trends, many=True)
    return JsonResponse(serializer.data, safe=False)
