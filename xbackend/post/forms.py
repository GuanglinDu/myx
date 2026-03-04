
from typing import TypeAlias
from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model: TypeAlias = Post
        fields: tuple[str, ...] = ('body',)
