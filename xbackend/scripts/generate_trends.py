# Created at 11:57:51 on 20260601 Mon by Guanglin Du.
# (env312) PS D:\repo-tauri\myx\xbackend> python .\scripts\generate_trends.py
# 
# Common Pitfalls to Avoid - How to use django.setup? - Google AI Overview
# (1) Wrong Import Order: Never import a Django model or utility before
# executing django.setup(). Doing so throws an AppRegistryNotReady
# exception.
# (2) Missing Python Path: If your script resides outside your
# project's root folder, Python will fail to find your settings module.
# You must add the root path to your script manually.
# (3) Logging Conflicts: Avoid putting logging statements directly
# inside your settings.py file, as django.setup() initializes the
# logging framework dynamically during boot.
import os
import sys
import django

# Django configuration for standalone script
# 1. Point to your Django settings module (.. = os.pardir)
# 2. Initialize Django
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbackend.settings')
django.setup()

# 3. Import and use your models safely AFTER django.setup()
from collections import Counter
from django.db.models import QuerySet
from post.models import Post, Trend


def extract_hashtags(content: str) -> list[str]:
    """Extract hashtags from the content. A hashtag is defined as a word
    that starts with '#' and is followed by alphanumeric characters or
    underscores. The hashtag is case-insensitive, but we will store it
    in lowercase.
    """
    words: list[str] = content.split()
    hashtags: list[str] = []
    word: str
    for word in words:
        if word.startswith('#') and len(word) > 1:
            hashtag: str = word[1:].lower()
            if (hashtag.endswith('.') or
                hashtag.endswith(',') or
                hashtag.endswith('!') or
                hashtag.endswith('?')):
                hashtags.append(hashtag[:-1])
            else:
                hashtags.append(hashtag)
    return hashtags


posts: QuerySet[Post] = Post.objects.all()
trends: list[str] = []

# Ensures uniqueness constraints are met
trend: Trend
for trend in Trend.objects.all():
    trend.delete()

post: Post
for post in posts:
    body: str = post.body
    hashtags: list[str] = extract_hashtags(body)
    if hashtags:
        for hashtag in hashtags:
                trends.append(hashtag)

hashtag: str
occurences: int
trend_counter: Counter[str] = Counter(trends)
for hashtag, occurences in trend_counter.most_common(10):
    Trend.objects.create(hashtag=hashtag, occurences=occurences)
    print(f"{hashtag}: {occurences}")
