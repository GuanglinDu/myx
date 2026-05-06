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
pip install -r requirements.txt             # Install dependencies
python manage.py migrate                    # Run migrations
python manage.py runserver 0.0.0.0:8001     # Start server
pytest                                      # Run all tests
pytest -v                                   # Verbose output
pytest tests/apps/                          # Test specific folder
pytest tests/apps/model_test.py::test_name  # Run specific test
pytest --cov                                # With coverage report
```

### Frontend

```bash
cd xfrontend
npm install                         # Install dependencies
npm run dev                         # Start dev server (port 5174)
npm run build                       # Build for production
```

### Database

```bash
# Populate with fake data (10 users, 20 comments, 20 likes)
python manage.py seed_db
python manage.py seed_db --clear  # Clear seeded data
python del_migrations.py          # Remove all migrations (development only)
```

## Architecture

### Backend Structure (xbackend/)

- **xbackend/** - Django project settings
- **account/**  - User model, friends, friendship requests
- **post/**     - Posts, attachments, comments, likes
- **search/**   - Search functionality

Key files in each app:
- `models.py`      - Database models
- `serializers.py` - DRF serializers
- `api.py`         - API views/viewsets
- `urls.py`        - URL routing

### Frontend Structure (xfrontend/src/)

- **views/** - Page components (HomeView, FeedView, ProfileView, etc.)
- **components/** - Reusable components
- **stores/** - Pinia state management (user.ts, toast.ts)
- **router/** - Vue Router configuration
- **types/** - TypeScript type definitions

### Authentication

JWT-based using `djangorestframework-simplejwt`. Tokens stored in localStorage with auto-refresh on page load. All API endpoints (except signup) require authentication via `IsAuthenticated` permission.

### URL Patterns

Frontend uses hash mode routing (`#/`) to avoid server configuration. Routes defined in `src/router/index.ts`:
- `#/` - Home
- `#/feed` - Feed
- `#/profile/:id` - User profile
- `#/search` - Search
- `#/messages` - Messages
- `#/login` / `#/signup` - Auth pages

### API Endpoints

- `/api/login/` - JWT login/refresh
- `/api/signup/` - User registration
- `/api/me/` - Current user profile
- `/api/posts/` - Posts CRUD
- `/api/posts/like/:id/` - Like/unlike post
- `/api/search/` - Search users
- `/api/friendship/request/` - Send friendship request
- `/api/friendship/accept/:id/` - Accept request
- `/api/friendship/reject/:id/` - Reject request
- `/api/friendship/remove/:id/` - Remove friend

### Key Models

- **User** (account/) - Custom user with UUID pk, email as username, friends M2M
- **Post** (post/) - Social posts with author, content, attachments
- **Like** (post/) - Post likes (note: missing post ForeignKey - bug)
- **Comment** (post/) - Post comments
- **FriendshipRequest** (account/) - Friend request model

## Important Notes

- The frontend uses hash mode routing (`#/`) to avoid server configuration requirements
- Authentication tokens are stored in localStorage with auto-refresh on page load
- User avatars use `ImageField` with fallback to `https://picsum.photos/200/200`
- Backend includes `django-extensions` for additional development utilities
- Chinese PyPI mirror configured in README for faster package installation in China

## Code Style

### Backend (Python)
- 4 spaces for indentation
- 79 character line limit
- `snake_case` for functions/variables
- Blank lines: 2 between top-level functions/classes

### Frontend (TypeScript/Vue)
- 2 spaces for indentation
- `camelCase` for functions/variables
- Use `async/await` instead of `.then()/.catch()` chains

## Authentication Flow

The user store (`xfrontend/src/stores/user.ts`) manages JWT auth:

1. `initStore()` on app load checks localStorage for stored tokens
2. If `user.access` exists, calls `/api/refresh/` to refresh the token
3. `setToken(data)` stores access/refresh tokens in localStorage
4. `logout()` clears tokens and redirects to `/login`
5. Axios `Authorization: Bearer <token>` header is set on each refresh

## API Patterns

### Backend APIs (`xbackend/*/api.py`)
- Function-based views with `@api_view` decorator
- `request.user` for authenticated user
- `request.data` for JSON body, `request.query_params` for query strings
- Return `JsonResponse` with serialized data

### Frontend API calls (`xfrontend/src/stores/user.ts`)
- Axios configured with `VITE_API_URL` base URL in `main.ts`
- JWT token attached via `axios.defaults.headers.common["Authorization"]`
- User state managed via Pinia `useUserStore`

## Frontend Architecture

- **Routing**: Vue Router with hash mode (`createWebHashHistory`) in `src/router/index.ts`
- **State**: Pinia stores (`src/stores/user.ts`, `src/stores/toast.ts`)
- **Views**: `src/views/` (HomeView, FeedView, ProfileView, etc.)
- **Components**: `src/components/` (ToastComponent, TrendsComponent, etc.)
- **Types**: `src/types/custom_types.ts` (User, Post, FriendshipRequest interfaces)

## graphify

Knowledge graph at `graphify-out/graph.json`. Rebuild with:

```bash
/graphify .
```
