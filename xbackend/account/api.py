from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
# from notification.utils import create_notification
from .forms import SignupForm, ProfileForm
from .models import User


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
