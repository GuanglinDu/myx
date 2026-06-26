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

# Tests (63 tests)
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest tests/test_account.py      # Test specific file
pytest -k "test_signup"           # Run tests matching keyword
pytest tests/test_account.py::TestAccountAPI::test_me_returns_user_info  # Run specific test
pytest --cov                     # With coverage report
pytest -x --tb=short             # Stop on first failure, short traceback
```

### Frontend

```bash
cd xfrontend
npm install
npm run dev            # Start dev server (port 5174)
npm run build          # Build for production (vue-tsc type-check + vite build)
npm run test:watch     # Vitest in watch mode
npm run test:once      # Vitest single run (CI, 379 tests across 14 files)
npm run test:e2e       # Playwright e2e tests

# Type-check without building
npx vue-tsc --noEmit
```

> The frontend has no `lint` script — formatting/linting is handled by
> Prettier (configured in `prettier.config.js`) and Vue's `<script setup>`
> TypeScript checks at build time.

### Database

```bash
cd xbackend
python manage.py seed_db            # Populate with fake data
python manage.py seed_db --clear    # Clear seeded data
python manage.py makemigrations     # Generate migrations after model changes
python manage.py migrate            # Apply migrations
```

### Environment activation (Windows)

```bash
xbackend/start_conda.bat    # cmd
xbackend/start_conda.ps1    # PowerShell
```

## Architecture

### Backend Apps (xbackend/)

| App | Purpose | Key Endpoints |
|-----|---------|---------------|
| **account/** | User model, auth, friendships | login, signup, me, editprofile, editpassword, friends CRUD |
| **post/** | Posts, likes, comments, trends | feed, create, like, comment, trends |
| **search/** | User search | `/api/search/?query=` |
| **chat/** | Direct messaging | conversations, messages, get-or-create |

Each app contains: `models.py`, `serializers.py`, `api.py`, `urls.py`

**Pytest** uses `DJANGO_SETTINGS_MODULE = xbackend.settings` (see `xbackend/pytest.ini`).

**Backend Tests** (63 tests across `xbackend/tests/`):
- `test_account.py` — User auth, signup (with email verification), profile edit, edit password, friendship requests, login with inactive-user handling
- `test_post.py` — Post CRUD, likes, comments, trends
- `test_chat.py` — Conversations, messages, permissions

### Frontend Structure (xfrontend/src/)

- **views/** — Page components. `FeedItem.vue` and `CommentItem.vue` are subcomponents embedded inside views.
- **components/** — Reusable widgets: `ToastComponent`, `TrendsComponent`, `PeopleYouMayKnow`, `NotificationsComponent`
- **stores/** — Pinia stores: `user.ts` (auth + JWT lifecycle), `toast.ts` (UI notifications)
- **router/** — Vue Router with history mode
- **types/** — TypeScript interfaces (`custom_types.ts`: User, Post, Comment, FriendshipRequest, Conversation)

### Frontend Tests (379 tests across 14 files)

- `tests/stores/` — Pinia store unit tests (`toast.test.ts`, `user.test.ts`)
- `tests/views/` — View component integration tests
- `tests/components/` — Reusable component tests
- E2E tests in `xfrontend/e2e/` with Playwright. Vitest is configured to exclude `e2e/`.

### URL Patterns

Frontend uses HTML5 history mode routing (no `#` prefix). Routes are
declared in `src/router/index.ts` and most are lazy-loaded:

- `/` — Home
- `/feed` — Friends' posts (feed)
- `/chat` — Direct messages
- `/search` — Search users
- `/profile/:id` — User profile (`props: true` passes `:id` as prop)
- `/profile/edit` — Edit own profile
- `/profile/editpassword` — Change own password
- `/profile/:id/friends` — User's friends list
- `/trends/:id` — Single trend detail
- `/:id` — Single post (`PostView`; only matches single-segment paths like `/post-uuid`, so coexists with `/profile/:id` etc.)
- `/login` / `/signup` / `/about` — Auth + static pages
- `/:pathMatch(.*)*` — `NotFoundView` (catch-all)

### API Endpoints

Mounted under `xbackend/xbackend/urls.py` (`/api/<app>/...`) plus
`/silk/` for django-silk profiling.

**Account** (`/api/account/...`):
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/login/` | JWT obtain (simplejwt) |
| POST | `/api/refresh/` | JWT refresh |
| POST | `/api/signup/` | Register + send verification email |
| GET | `/api/me/` | Current user info |
| POST | `/api/editprofile/` | Update name/email |
| POST | `/api/editpassword/` | Change password (requires current pw) |
| GET | `/api/friends/<user_id>/` | List user's friends |
| GET | `/api/friends/<user_id>/requests/` | Pending requests for user |
| GET | `/api/friends/status/<user_id>/` | Friendship status with user |
| POST | `/api/friends/send/<user_id>/` | Send friend request |
| POST | `/api/friends/accept/<request_id>/` | Accept request |
| POST | `/api/friends/reject/<request_id>/` | Reject request |

**Posts** (`/api/posts/...`):
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/posts/` | Feed (friends' posts, filterable by `?trend=`) |
| POST | `/api/posts/create/` | Create post |
| GET | `/api/posts/trends/` | Trending hashtags |
| GET | `/api/posts/profile/<user_id>/` | Posts by a specific user |
| GET | `/api/posts/<id>/` | Post detail |
| POST | `/api/posts/<id>/delete/` | Delete post |
| POST | `/api/posts/<id>/like/` | Like / unlike (toggle) |
| POST | `/api/posts/<id>/comment/` | Add comment |

**Chat** (`/api/chat/...`):
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/chat/` | List conversations |
| GET | `/api/chat/<id>/` | Conversation with messages |
| POST | `/api/chat/<id>/send/` | Send message |
| GET | `/api/chat/<user_id>/get-or-create/` | Start (or find existing) conversation |

**Search**: `GET /api/search/?query=<term>`

### Key Models

| Model | App | Notes |
|-------|-----|-------|
| **User** | account | UUID pk, email as USERNAME_FIELD, friends M2M, friend_count/post_count denormalized |
| **FriendshipRequest** | account | Status-based (sent/accepted/rejected), created_by/created_for |
| **Post** | post | Text body, attachments M2M, likes M2M, comments M2M, denormalized like_count/comments_count |
| **Like** | post | Created by user, linked to Post via M2M |
| **Comment** | post | Text body, created by user, linked to Post via M2M |
| **PostAttachment** | post | Image uploads for posts |
| **Trend** | post | Hashtag with occurrence count |
| **Conversation** | chat | Participants M2M, modified_at for sorting |
| **ConversationMessage** | chat | Body, sent_to, created_by |

## Authentication & Security

### JWT Flow

JWT-based using `djangorestframework-simplejwt`. User store (`xfrontend/src/stores/user.ts`):

1. `initStore()` checks localStorage for tokens on app load
2. If `user.access` exists, calls `/api/refresh/` to refresh
3. `setToken(data)` stores tokens in localStorage
4. `logout()` clears tokens and redirects to `/login`

### Email Verification (current work-in-progress on `verify-email` branch)

The signup flow now includes email verification:
1. `POST /api/signup/` creates the user with `is_active=False` and sends a verification email via Django's `send_mail()` (printed to console in development)
2. `CustomTokenObtainPairSerializer` (in `account/serializers.py`) checks `is_active` *before* `authenticate()` and returns a distinct error message for inactive accounts (prevents email enumeration for non-existent users)
3. `account/views.py:activate_email` handles the activation link (WIP — currently a stub)

## Code Style

Per-project coding standards (authoritative):
- **xbackend/CLAUDE.md** — PEP 8, 4 spaces, 79 char line limit, `snake_case`
- **xfrontend/CLAUDE.md** — Vue 3 Compositional API, 2 spaces, 79 char line limit, `async/await`

## Important Notes

- **Migrations**: Django migrations are intentionally excluded from git on some apps — run `python manage.py makemigrations && python manage.py migrate` after pulling.
- **Ports**: Frontend dev server on port 5174 (configurable via `VITE_PORT`), backend on port 8001.
- **Avatars**: `ImageField` with a DiceBear fallback (`@dicebear/core` in the frontend).
- **CORS**: Configured for `http://localhost:5174`. JWT access token TTL = 30 days, refresh TTL = 180 days.
- **Requests are DRF `@api_view` decorators**, not generic views — all endpoints are function-based with `JsonResponse`. The project intentionally avoids DRF serializers for most endpoints in favor of manual validation.
- **Password policy**: Minimum 8 characters, new password must differ from current, confirmation field required.
- **graphify**: Knowledge graph at `graphify-out/graph.json`. Rebuild with `/graphify .`.
