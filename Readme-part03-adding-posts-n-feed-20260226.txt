(1/10) Adding posts/feed - Build a Full-Stack Social Network with Django and Vue 3 | Part 3/16
==============================================================================================
https://www.youtube.com/watch?v=qM8WhgvbZDI&list=PLpyspNLjzwBlobEvnZzyWP8I-ORQcq4IO&index=3

0:00 Create app post (python manage.py startapp post)
 - 1:00 Database model (remember uuid, one for the posts, and one for the attachments)
 - 7:05 Set up serializers
 - 9:50 View and URLs
 - 14:32 Get a test feed and show in the frontend (Your own posts; Create a superuser)
30:30 Make it possible to add text posts
33:37 Make it possible to view a profile
33:37 Set up friendships (model changes)


(2/10) Create app post
======================
(env312) PS D:\repo-tauri\myx\xbackend> python.exe .\manage.py startapp post

Add it to settings.py.


(3/10) Add models in post.models.py
===================================
Post
PostAttachment


(4/10) python.exe .\manage.py makemigrations
==============================================
(env312) PS D:\repo-tauri\myx\xbackend> python.exe .\manage.py makemigrations
System check identified some issues:

WARNINGS:
post.Post.attachments: (fields.W340) null has no effect on ManyToManyField.
Migrations for 'post':
  post\migrations\0001_initial.py
    + Create model PostAttachment
    + Create model Post
(env312) PS D:\repo-tauri\myx\xbackend>


(4.1/10) Fix the warning above and make migrations again
---------------------------------------------------------
    # WARNINGS: post.Post.attachments: (fields.W340) null has no effect on
    # ManyToManyField.
    # attachments = models.ManyToManyField('PostAttachment', blank=True,
    #                                      null=True)
    attachments = models.ManyToManyField('PostAttachment', blank=True)

(env312) PS D:\repo-tauri\myx\xbackend> python.exe .\manage.py makemigrations
Migrations for 'post':
  post\migrations\0002_alter_post_attachments.py
    ~ Alter field attachments on post
(env312) PS D:\repo-tauri\myx\xbackend>


(5/10) python.exe .\manage.py migrate
======================================
(env312) PS D:\repo-tauri\myx\xbackend> python.exe .\manage.py migrate
Operations to perform:
  Apply all migrations: account, admin, auth, contenttypes, post, sessions
Running migrations:
  Applying post.0001_initial... OK
  Applying post.0002_alter_post_attachments... OK
(env312) PS D:\repo-tauri\myx\xbackend>


(6/10) Rgister models Post and PostAttachment
=============================================
post.admin.py


(7/10) Create a superuser
======================================
python manage.py createsuperuser


(8/10) 
======================================


(9/10) 
======================================


(10/10) 
======================================


(11/10) 
======================================
