from typing import TypeAlias, override
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, FriendshipRequest


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Distinguish wrong-credentials from inactive-account login failures.

    The default simplejwt serializer returns the same error for wrong
    passwords, non-existent emails, and inactive users.  This serializer
    checks *before* authenticate() so the client can show a different
    message when the account exists but has not been activated.
    """
    default_error_messages: dict[str, str] = {
        'no_active_account': 'Invalid email or password.',
        'user_inactive': (
            'Your account is not activated yet. Please check your email'
            ' for the verification link.'
        ),
    }

    @override
    def validate(self, attrs: dict) -> dict:
        email: str = attrs.get(self.username_field, '')
        try:
            user: User = User.objects.get(
                **{self.username_field: email}
            )
            if not user.is_active:
                raise AuthenticationFailed(
                    {
                        'detail': self.error_messages['user_inactive'],
                        'code': 'user_inactive',
                    },
                )
        except User.DoesNotExist:
            pass  # Fall through to authenticate() — same error as
                  # wrong password, no email-enumeration leak.

        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model: TypeAlias = User
        fields: list[str] = [
            'id', 'name', 'email', 'friend_count', 'post_count'
        ]


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by: UserSerializer = UserSerializer(read_only=True)

    class Meta:
        model: TypeAlias = FriendshipRequest
        fields: list[str] = ['id', 'status', 'created_by']
