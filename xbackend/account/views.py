from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import User


def activate_email(request: HttpRequest):
    email: str = request.GET.get('email', '')
    id: str = request.GET.get('id', '')

    if email and id:
        user: User = User.objects.filter(email=email, id=id).first()
        if user:
            user.is_active = True
            user.save()
        else:
            return HttpResponse("Invalid activation link.")

    return HttpResponse(
        f"User activated successfully: Email: {email}, ID: {id}")
