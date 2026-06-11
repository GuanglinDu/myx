# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

X-like social network application built with Django REST Framework (backend) and Vue.js 3 (frontend). The project consists of two separate subprojects:

- **xbackend/** - Django 5.2 + DRF + JWT authentication
- **xfrontend/** - Vue.js 3 + TypeScript + Pinia + Tailwind CSS

## Development Commands

### Backend

```bash
cd xbackend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8001

# Linting
flake8 .

# Tests (93% coverage)
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest tests/test_account.py      # Test specific file
pytest tests/test_account.py::TestAccountAPI::test_me_returns_user_info  # Run specific test
pytest --cov                     # With coverage report
```

### Frontend

```bash
cd xfrontend
npm install
npm run dev            # Start dev server (port 5174)
npm run build          # Build for production (type-check + bundle)
npm run test:watch     # Vitest in watch mode
npm run test:once      # Vitest single run (CI)
npm run test:e2e       # Playwright e2e tests
```

> The frontend has no `lint` script — formatting/linting is handled by
> Prettier (configured in `prettier.config.js`) and Vue's `<script setup>`
> TypeScript checks at build time.

### Database

```bash
python manage.py seed_db            # Populate with fake data
python manage.py seed_db --clear    # Clear seeded data
```

### Environment activation (Windows)

```bash
xbackend/start_conda.bat    # cmd
xbackend/start_conda.ps1    # PowerShell
```

## Architecture

### Backend Apps (xbackend/)

| App | Purpose |
|-----|---------|
| **account/** | User model, friends, friendship requests |
| **post/** | Posts, attachments, comments, likes |
| **search/** | User search functionality |
| **chat/** | Direct messaging between users |

Each app contains: `models.py`, `serializers.py`, `api.py`, `urls.py`

**Backend Tests** (`xbackend/tests/`):
- `test_account.py` - User auth, signup, profile edit, friendship requests (31 tests)
- `test_post.py` - Post CRUD, likes, comments, trends (15 tests)
- `test_chat.py` - Conversations, messages (7 tests)

Pytest uses `DJANGO_SETTINGS_MODULE = xbackend.settings` (see `xbackend/pytest.ini`).

### Frontend Structure (xfrontend/src/)

- **views/** - Page components: `HomeView`, `FeedView`, `ProfileView`, `EditProfileView`, `EditPasswordView`, `FriendsView`, `ChatView`, `SearchView`, `PostView` (single post), `TrendView` (single trend), `LoginView`, `SignupView`, `AboutView`, `NotFoundView`. `FeedItem.vue` and `CommentItem.vue` are subcomponents used inside views.
- **components/** - Reusable widgets: `ToastComponent`, `TrendsComponent`, `PeopleYouMayKnow`, `NotificationsComponent`
- **stores/** - Pinia stores: `user.ts` (auth + JWT), `toast.ts` (notifications)
- **router/** - Vue Router configuration (history mode; see `router/index.ts`)
- **types/** - TypeScript type definitions

### Frontend Tests (xfrontend/tests/)

- `tests/stores/` - Pinia store unit tests (`toast.test.ts`, `user.test.ts`)
- `tests/views/` - View component tests (Login, Signup, FeedView, FeedItem, FriendsView, EditProfileView, EditPasswordView)
- `tests/components/` - Reusable component tests (Toast, Trends, PeopleYouMayKnow, Notifications)

E2E tests live in `xfrontend/e2e/` with Playwright. Config in `playwright.config.ts`. Vitest is configured to exclude the `e2e/` directory.

### URL Patterns

Frontend uses HTML5 history mode routing (no `#` prefix). Routes are
declared in `src/router/index.ts` and most are lazy-loaded. `/:id` is the
single-post `PostView` (matches before `/profile/:id` because the router
resolves in order):

- `/` - Home
- `/feed` - Friends' posts
- `/chat` - Direct messages
- `/search` - Search users
- `/profile/:id` - User profile (route param passed as `props.id`)
- `/profile/edit` - Edit own profile
- `/profile/editpassword` - Change own password
- `/profile/:id/friends` - User's friends
- `/trends/:id` - Single trend detail
- `/:id` - Single post (`PostView`)
- `/login` / `/signup` / `/about` - Auth + static
- `/:pathMatch(.*)*` - `NotFoundView`

### API Endpoints

Mounted under `xbackend/xbackend/urls.py` (`/api/<app>/...`) plus
`/silk/` for django-silk profiling.

Account (`/api/account/...`):
- `POST /api/login/` - JWT obtain (`simplejwt`)
- `POST /api/refresh/` - JWT refresh
- `POST /api/signup/` - User registration
- `GET  /api/me/` - Current user profile
- `POST /api/editprofile/` - Update own profile
- `POST /api/editpassword/` - Change own password
- `GET  /api/friends/<user_id>/` - List a user's friends
- `GET  /api/friends/<user_id>/requests/` - Incoming requests for user
- `GET  /api/friends/status/<user_id>/` - Friendship status with user
- `POST /api/friends/send/<user_id>/` - Send friend request
- `POST /api/friends/accept/<request_id>/` - Accept request
- `POST /api/friends/reject/<request_id>/` - Reject request

Posts (`/api/posts/...`):
- `GET  /api/posts/` - Feed (friends' posts)
- `POST /api/posts/create/` - Create post
- `GET  /api/posts/trends/` - Trends list
- `GET  /api/posts/profile/<user_id>/` - Posts by user
- `GET  /api/posts/<id>/` - Post detail
- `POST /api/posts/<id>/delete/` - Delete post
- `POST /api/posts/<id>/like/` - Like / unlike
- `POST /api/posts/<id>/comment/` - Add comment

Chat (`/api/chat/...`):
- `GET  /api/chat/` - List conversations
- `GET  /api/chat/<id>/` - Get conversation with messages
- `POST /api/chat/<id>/send/` - Send message
- `GET  /api/chat/<user_id>/get-or-create/` - Start new conversation

Search: `GET /api/search/`

### Key Models

- **User** (`account/`) - Custom user with UUID pk, email as username, friends M2M
- **Post** (`post/`) - Social posts with author, content, attachments
- **Like** (`post/`) - Post likes via M2M
- **Comment** (`post/`) - Post comments via M2M
- **FriendshipRequest** (`account/`) - Friend request model
- **Conversation** (`chat/`) - DM conversations with participants M2M
- **ConversationMessage** (`chat/`) - Direct messages

## Authentication Flow

JWT-based using `djangorestframework-simplejwt`. User store (`xfrontend/src/stores/user.ts`):

1. `initStore()` checks localStorage for tokens on app load
2. If `user.access` exists, calls `/api/refresh/` to refresh
3. `setToken(data)` stores tokens in localStorage
4. `logout()` clears tokens and redirects to `/login`

## Code Style

Per-project coding standards (authoritative):
- **xbackend/CLAUDE.md** - PEP 8, 4 spaces, 79 char line limit, `snake_case`
- **xfrontend/CLAUDE.md** - Vue 3 Compositional API, 2 spaces, 79 char line limit, `async/await`

## Important Notes

- Frontend dev server runs on port 5174 (configurable via `VITE_PORT`).
- Backend runs on port 8001.
- User avatars use `ImageField` with a DiceBear fallback (`@dicebear/core`
  in the frontend, generation scripts under `xbackend/scripts/`).
- `xbackend/scripts/generate_trends.py` is a stand-alone helper for
  pre-computing trend data; the live `trends/` endpoint is served by
  `xbackend/post/api.py:trends_list`.
- Chinese PyPI mirror is configured for faster installs in China.
- Django migrations are intentionally excluded from git on some apps —
  run `python manage.py makemigrations && python manage.py migrate`
  after pulling.

## graphify

Knowledge graph at `graphify-out/graph.json`. Rebuild with:

```bash
/graphify .
```
