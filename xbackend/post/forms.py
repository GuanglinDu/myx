from typing import TypeAlias
from django.forms import ModelForm
from .models import Post, PostAttachment


class PostForm(ModelForm):
    class Meta:
        model: TypeAlias = Post
        fields: tuple[str, ...] = ('body',)


# Appended at 19:44:17 on 20260619 Fri by Guanglin Du.
# How is an image attached to a post? - Answered by Claude Code.
# Plain ModelForm over the image field — Django's form machinery handles
# the multipart parsing, validation, and file write.
class AttachmentForm(ModelForm):
    class Meta:
        model: TypeAlias = PostAttachment
        fields: tuple[str, ...] = ('image',)
