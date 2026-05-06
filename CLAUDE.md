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

- Frontend runs on port 5174 by default (configurable via `VITE_PORT`)
- Backend runs on port 8001
- User avatars use DiceBear generation in frontend, stored as ImageField in backend with picsum.photos fallback
- Custom user model uses email as USERNAME_FIELD
- JWT access tokens expire after 30 days

## graphify

Knowledge graph at `graphify-out/graph.json`. Rebuild with:

```bash
/graphify .
```
