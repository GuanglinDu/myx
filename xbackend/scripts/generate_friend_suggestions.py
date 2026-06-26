# Created at 14:58:16 on 20260625 Thu by Guanglin Du.
# (env312) PS D:\repo-tauri\myx\xbackend> python .\scripts\generate_friend_suggestions.py
import os
import sys
import django

# Django configuration for standalone script
# 1. Point to your Django settings module (.. = os.pardir)
# 2. Initialize Django
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xbackend.settings')
django.setup()

from collections import Counter
from django.db.models import QuerySet
from account.models import User

users: QuerySet[User] = User.objects.all()
user: User
for user in users:
    user.people_you_may_know.clear()

    print(f"\n***Find friends for {user}:")

    friend: User
    for friend in user.friends.all():
        print(f"Is already friend with {friend}")

        friendsfriend: User
        for friendsfriend in friend.friends.all():
            if (friendsfriend not in user.friends.all() 
                    and friendsfriend != user):
                print('Suggest:', friendsfriend)
                user.people_you_may_know.add(friendsfriend)
