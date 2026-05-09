(1/10) Build a Full-Stack Social Network with Django and Vue 3 | Part 2/16 - The backend setup
===============================================================================================
https://www.youtube.com/watch?v=NmQyX1D5hqo&t=1700s

0:00 Overview
0:15 Set up the backend
0:40 Create a virtual environment
 - 1:42 Install Django
 - 2:15 Install djangorestframework (rest_framework, DRF)
 - 2:45 Install djangorestframework-simplejwt (rest_framework_simplejwt)
 - 3:08 Install Pillow (handling images)
3:37 Create a Django project
5:16 Set up everything ( A bigger task!)
 - 5:24 Config for JWT (settings and URLs)
 - 6:10 Config for DRF (and at 9:30)
 - 8:40 Config for csrf and cors (and at 10:00)
11:50 Create app for custom user model (using uuid)
 - 17:45 Add to settings
 - 18:52 Configure JWT URLs
21:20 Make it possible to sign up (The key part to couple the frontend with the backend. Need time to digest!😜)
 - 21:30 Implement verification, reset/forgot the password and the similar (Comes later in the course)
 - 21:45 backend work (api.py, forms.py, etc.)
 - 27:55 frontend work (a Pinia store user.ts, SignupView.vue)
 - 34:10 Modify SignupView.vue to add the AXIOS package, the client to convey info between the two ends
 - 43:05 Fix the signing up bug in SignupView.vue
 - 44:35 Modify App.vue to add the Toast.vue (Attention: use toastStore = useToastStore();)
 - 46:50 Enter the Django shell to check if the user exists
47:43 Make it possible to log in (Get and refresh the token, a Pinia store user.js, etc.)
 - 47:40 Modify LoginView.vue to test logging in
 - 52:50 Create the /api/login/ API in the backend
 - 54:00 Fix the 401 Unauthorized error
 - 57:00 Make our login persist after page-refreshing in App.vue
1:02:40 Show the middle 4 buttons only when authenticated
1:03:50 Customize the login and signup buttons


(2/10) Create a Django project named xbackend
=============================================
(env312) PS D:\repo-tauri\twitter> django-admin startproject xbackend
(env312) PS D:\repo-tauri\twitter>


(2/10) Create a Django app named account
=============================================
(env312) PS D:\repo-tauri\twitter> cd .\xbackend\
(env312) PS D:\repo-tauri\twitter\xbackend> python .\manage.py startapp account

Create a custom user model in module account.models.py and tell Django to use our custom user model instead of the built-in one in settings.py:

AUTH_USER_MODEL = 'account.User'

Install app account:

INSTALLED_APPS: list[str] = [
	...
    'account',
]


(3/10) Make migrations
=======================
(env312) PS D:\repo-tauri\twitter\xbackend> python .\manage.py makemigrations

C:\Users\Guanglin\miniconda3\envs\env312\Lib\site-packages\rest_framework_simplejwt\__init__.py:1: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
Migrations for 'account':
  account\migrations\0001_initial.py
    + Create model User
    + Create model FriendshipRequest
(env312) PS D:\repo-tauri\twitter\xbackend>


(3.1/10) Fix by Qianwen
-------------------------
The above warning is coming from djangorestframework-simplejwt (specifically its __init__.py), which still uses the legacy pkg_resources module to determine its package version.
This is not your code’s fault—it’s a known issue in older versions of the djangorestframework-simplejwt library.

How to Fix or Suppress This Warning
🔧 Option 1: Upgrade djangorestframework-simplejwt (Recommended)
Newer versions (≥ 5.3.0) have removed pkg_resources and switched to the modern importlib.metadata.
Run:
bash

pip install -U djangorestframework-simplejwt (Updated from 5.2.2 to 5.5.1)


(3.2/10) python .\manage.py migrate
------------------------------------
(env312) PS D:\repo-tauri\twitter\xbackend> python .\manage.py makemigrations
No changes detected
(env312) PS D:\repo-tauri\twitter\xbackend> python .\manage.py migrate
Operations to perform:
  Apply all migrations: account, admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying account.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying sessions.0001_initial... OK
(env312) PS D:\repo-tauri\twitter\xbackend>


(4/10) Creat account.urls.py
=============================
from django.urls import path, URLPattern, URLResolver
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns: list[ URLPattern | URLResolver] = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


(5/10) Modify xbackend.urls.py
===============================
urlpatterns: list[ URLPattern | URLResolver] = [
    ...
    path('api/', include('account.urls')),
]


(5.1/10) python .\manage.py show_urls
--------------------------------------
(env312) PS D:\repo-tauri\twitter\xbackend> python .\manage.py show_urls
/admin/ django.contrib.admin.sites.index        admin:index
/admin/<app_label>/     django.contrib.admin.sites.app_index    admin:app_list
/admin/<url>    django.contrib.admin.sites.catch_all_view
/admin/auth/group/      django.contrib.admin.options.changelist_view    admin:auth_group_changelist
/admin/auth/group/<path:object_id>/     django.views.generic.base.RedirectView
/admin/auth/group/<path:object_id>/change/      django.contrib.admin.options.change_view        admin:auth_group_change
/admin/auth/group/<path:object_id>/delete/      django.contrib.admin.options.delete_view        admin:auth_group_delete
/admin/auth/group/<path:object_id>/history/     django.contrib.admin.options.history_view       admin:auth_group_history
/admin/auth/group/add/  django.contrib.admin.options.add_view   admin:auth_group_add
/admin/autocomplete/    django.contrib.admin.sites.autocomplete_view    admin:autocomplete
/admin/jsi18n/  django.contrib.admin.sites.i18n_javascript      admin:jsi18n
/admin/login/   django.contrib.admin.sites.login        admin:login
/admin/logout/  django.contrib.admin.sites.logout       admin:logout
/admin/password_change/ django.contrib.admin.sites.password_change      admin:password_change
/admin/password_change/done/    django.contrib.admin.sites.password_change_done admin:password_change_done
/admin/r/<path:content_type_id>/<path:object_id>/       django.contrib.contenttypes.views.shortcut      admin:view_on_site
/api/login/     rest_framework_simplejwt.views.TokenObtainPairView      token_obtain
/api/refresh/   rest_framework_simplejwt.views.TokenRefreshView token_refresh
(env312) PS D:\repo-tauri\twitter\xbackend>


(6/10) Create account.api.py and account.forms.py
==================================================
21:20 Make it possible to sign up (The key part to couple the frontend with the backend. Need time to digest!😜)
 - 21:30 Implement verification, reset/forgot the password and the similar (Comes later in the course)
 - 21:45 backend work (api.py)
 - 27:55 frontend work (SignupView.vue)
 
 
 *** In the xfrontend ***


(7/10) Modify xfrontend to enable login
=======================================
Creates the Pinia store stores.user.ts
Modify views.SignupView.vue to enable submitting the signup info


(8/10) Make it possible to log in
==================================
Unauthorized: /api/me/

views/LoginView.vue:
Error: response.data.message undefined!
// if (response.data.message === "success") {


(9/10) /api/me/: {"detail":"Method \"GET\" not allowed."}
===========================================================
xbackend/settings.py

# 4/6. Optional (for auth tokens/JWT): Allow credentials
# Enable this if your requests include auth tokens/cookies
# Optional: Allow credentials if using cookies/sessions
CORS_ALLOW_CREDENTIALS: bool = True

# 5/6. Optional: Allow specific HTTP methods (for preflight requests)
# Preflight requests (OPTIONS) are blocked if methods aren't allowed
CORS_ALLOW_METHODS: list[str] = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",  # Critical for preflight checks
]

# 6/6. Optional: Allow custom headers (e.g., Authorization)
CORS_ALLOW_HEADERS: list[str] = [
    "accept",
    "accept-encoding",
    "authorization",  # For token auth (Token/JWT)
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


@api_view(['POST']) # wrong method
def me(request: Request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })


@api_view(['GET'])


(10/10) Make the login persistent
=================================
App.vue

userStore.initStore();

const token: string = userStore.user.access;
if (token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
} else {
  axios.defaults.headers.common["Authorization"] = "";
}
