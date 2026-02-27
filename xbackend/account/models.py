# Updated at 15:18:36 on 20260131 Sat by Guanglin Du.
# Updated at 11:41:45 on 20260202 Mon by Guanglin Du.
# 
# (1/7) What are the relationships between the Django built-in users
# and my customized users? - doubao
# See Django-built-in-users-vs-custom-users-20260131.pdf.
# 
# (2/7) This is Pattern 2: Extend AbstractBaseUser (Full Customization)
# (3/7) Relationship to Built-in User: No Direct Inheritance (Complete
# Replacement)
# (4/7) AbstractBaseUser is a minimal abstract base class that only
# includes the core auth functionality of the built-in User — no fields
# except password and last_login (all other fields are removed). It is
# the minimal blueprint for Django’s user system.
# (5/7) By inheriting from AbstractBaseUser, your custom user:
# (5.1/7) Completely replaces the built-in User (no shared fields
# except password/last_login)
# (5.2/7) Lets you define a custom primary login field (e.g., use email
# instead of username for login)
# (5.3/7) Requires you to reimplement critical auth methods (to
# maintain Django compatibility)
# (6/7) Use Case
# Ideal for full control over the user model (e.g., login with email
# instead of username, remove unused fields like first_name/last_name).
# (7/7) Key Requirement
# You must also implement a custom UserManager (Django’s auth system
# relies on the manager for creating users/superusers).
import uuid
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.db import models
from django.db.models.fields.files import ImageFieldFile
# django.db.models.fields.related_descriptors
#     .create_forward_many_to_many_manager.<locals>.ManyRelatedManager


class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields) -> "User":
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email: str = self.normalize_email(email)  # lowercase domain
        user: "User" = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None,
                    **extra_fields) -> "User":
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None,
                         **extra_fields) -> "User":
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id: str = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    email: str = models.EmailField(unique=True)
    name: str = models.CharField(max_length=255, blank=True, default='')
    avatar: ImageFieldFile = models.ImageField(upload_to='avatars', blank=True,
                                               null=True)
    friends: "ManyRelatedManager" = models.ManyToManyField('self')
    friends_count: int = models.IntegerField(default=0)

    people_you_may_know: "ManyRelatedManager" = models.ManyToManyField('self')

    posts_count: int = models.IntegerField(default=0)

    is_active: bool = models.BooleanField(default=True)
    is_superuser: bool = models.BooleanField(default=False)
    is_staff: bool = models.BooleanField(default=False)

    date_joined: datetime = models.DateTimeField(default=timezone.now)
    last_login: datetime = models.DateTimeField(blank=True, null=True)

    # Attaches the custom object manager, e.g.,
    # from django.db.models.query import QuerySet
    # users: QuerySet[User] = User.objects.all()
    objects: "CustomUserManager" = CustomUserManager()

    # Tells Django to use email as the login field instead of username
    USERNAME_FIELD: str = 'email'
    EMAIL_FIELD: str = 'email'
    # Required fields for createsuperuser (excluds USERNAME_FIELD and password)
    REQUIRED_FIELDS: list[str] = []

    def get_avatar(self) -> str:
        if self.avatar:
            return settings.WEBSITE_URL + self.avatar.url
        else:
            return 'https://picsum.photos/200/200'


class FriendshipRequest(models.Model):
    SENT: str = 'sent'
    ACCEPTED: str = 'accepted'
    REJECTED: str = 'rejected'

    STATUS_CHOICES: tuple[[str, str], ...] = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    id: str = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    created_for: "User" = models.ForeignKey(
        User, related_name='received_friendshiprequests',
        on_delete=models.CASCADE)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    created_by: "User" = models.ForeignKey(
        User, related_name='created_friendshiprequests',
        on_delete=models.CASCADE)
    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                   default=SENT)
