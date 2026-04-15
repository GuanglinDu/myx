from django.template.defaultfilters import safe
from django.db.models.query import QuerySet
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from account.models import User
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer


# (1/2) Double underscore in Django - Google AI Overview
# 
# In Django, the double underscore (__), often pronounced "dunder," has a
# special meaning within the Object-Relational Mapper (ORM). It serves as
# a separator to traverse relationships between models and to specify
# field lookups in database queries. 
# 
# Usage in Django ORM
# The primary use of the double underscore is in methods like filter(),
# exclude(), get(), and order_by(), where it allows you to perform complex
# lookups and join across related models. 
# 
# (1.1/2) Relationship Traversal: It is used to access fields of a related
# model via a ForeignKey, ManyToManyField, or OneToOneField. This works
# similarly to chaining together properties with a dot in regular Python
# code. Example: 
# To find all Car objects with an Engine made by a specific company, you
# would use:
#   cars = Car.objects.filter(engine__engine_make__company_name="something")
# Here, engine__engine_make__company_name tells Django to look at the
# engine relationship, then the engine_make relationship within that, and 
# finally filter by the company_name field.

# (2.1/2) Field Lookups: The part after the last double underscore specifies
# a type of comparison or lookup (e.g., "less than," "case-insensitive
# contains," etc.).Examples of common lookups:
#   field__lte: less than or equal to.
#   field__icontains: case-insensitive containment test.
#   field__year: extracts the year part from a date/datetime field. 
# Django's ORM internally splits the query string by __ to generate the
# appropriate SQL WHERE clauses and JOIN statements.
# 
# (2/2) How to create a Django JsonResponse object? - Google AI Overview
# The Django JsonResponse class automatically serializes a Python
# dictionary into a JSON string and sets the Content-Type header to
# application/json.
@api_view(['POST'])
def search(request: Request) -> JsonResponse:
    data: dict | list = request.data
    query = data['query']

    # The double underscore (dunder) is used to separate the field name
    # from the lookup type. In this case, `name__icontains` means that we
    # want to filter the `name` field of the `User` model using a
    # case-insensitive containment test. This will return all users whose
    # names contain the query string, regardless of case.
    users: QuerySet[User] = User.objects.filter(name__icontains=query)
    user_serializer: UserSerializer = UserSerializer(users, many=True)

    posts: QuerySet[Post] = Post.objects.filter(body__icontains=query)
    post_serializer: PostSerializer = PostSerializer(posts, many=True)

    return JsonResponse({
        'users': user_serializer.data,
        'posts': post_serializer.data
    }, safe=False)
