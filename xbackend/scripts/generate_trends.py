# Created at 11:57:51 on 20260601 Mon by Guanglin Du.
# (env312) PS D:\repo-tauri\myx\xbackend> python .\scripts\generate_trends.py
import os
import sys
import django

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbackend.settings')
django.setup()

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

# To meet the qniqueness restrictions
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
