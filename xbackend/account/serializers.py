# 
from typing import TypeAlias
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: TypeAlias = User
        fields: list[str] = ['id', 'name', 'email']
