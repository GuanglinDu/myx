# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an X-like demo social network application built with Django (backend) and Vue.js 3 (frontend), following the "Build a Full-Stack Social Network with Django and Vue 3" YouTube tutorial series. The project is organized as two separate subprojects:

- `xbackend/` - Django REST Framework backend with JWT authentication
- `xfrontend/` - Vue.js 3 frontend with TypeScript, Pinia, and Tailwind CSS

## Development Setup

### Backend (Django)

```bash
cd xbackend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8001
```

**Notes:**

- Uses SQLite database (`db.sqlite3`) by default
- Custom user model defined in `account/models.py` (UUID primary key, email as username)
- JWT authentication configured with 30-day access tokens
- CORS configured for `http://localhost:5174`

**Useful commands:**

- `python manage.py makemigrations` - Create migrations after model changes
- `python manage.py seed_db` - Populate database with fake data (formations, workspaces, projects) *[may not be implemented]*
- `python manage.py seed_db --clear` - Clear seeded data *[may not be implemented]*
- `python manage.py seed_result --project_results=10` - Populate project results table *[may not be implemented]*
- `python del_migrations.py` - Remove all migrations (development only) *[may not be implemented]*
- `pytest` - Run backend tests (see README for detailed pytest options) *[test files may not exist yet]*

### Frontend (Vue.js 3)

```bash
cd xfrontend
npm install
npm run dev
```

**Notes:**

- Frontend runs on port 5174 by default (configurable via `VITE_PORT` env var)
- Uses Vue Router with hash mode (`createWebHashHistory`)
- Pinia stores for state management (`src/stores/`)
- Axios configured with base URL from `VITE_API_URL` environment variable
- Tailwind CSS for styling

## API Architecture

### Authentication

- JWT-based authentication using `djangorestframework-simplejwt`
- Endpoints: `/api/login/`, `/api/refresh/`, `/api/signup/`
- Custom user model with email as `USERNAME_FIELD`
- All API endpoints (except signup) require authentication via `IsAuthenticated` permission

### Core Apps

1. **Account** (`xbackend/account/`)
   - User model with `friends`, `friends_count`, `people_you_may_know`, `posts_count` fields
   - `FriendshipRequest` model for friend requests
   - API endpoints: `/api/me/`, `/api/signup/`

2. **Post** (`xbackend/post/`)
   - Social media posts with attachments
   - API endpoints under `/api/posts/`

3. **Search** (`xbackend/search/`)
   - Search functionality
   - API endpoints under `/api/search/`

### Frontend Architecture

- **Routing**: Vue Router with hash mode (see `src/router/index.ts`)
- **State Management**: Pinia stores (`user.ts`, `toast.ts`)
- **Authentication**: JWT tokens stored in localStorage, auto-refresh mechanism
- **Views**: Located in `src/views/` (Home, Feed, Login, Profile, Search, etc.)
- **Components**: Reusable UI components in `src/components/`
- **API Client**: Axios instance configured in `src/main.ts`

## Testing

### Backend Tests

The README references pytest but test files may not yet be implemented. When tests are added, use:

```bash
cd xbackend
pytest                     # Full test suite
pytest -v                  # Verbose output
pytest -vv                 # Very verbose
pytest -rP                 # Show print output
pytest -x                  # Stop at first failure
pytest --cov               # Test coverage report
```

### Frontend Tests

Testing setup described in README but not fully implemented. Uses Vitest, @vue/test-utils, @testing-library/vue, and happy-dom.

## Database Management

- SQLite database file: `xbackend/db.sqlite3` (ignored by git)
- Custom user model requires migrations when changed
- Seed commands available for development data
- Friendship system uses `ManyToManyField` on User model

## Environment Variables

### Backend

- `DEBUG`: Django debug mode (default: `True`)
- `SECRET_KEY`: Django secret key (insecure default for development)
- `CORS_ALLOWED_ORIGINS`: List of allowed origins (default: `["http://localhost:5174"]`)

### Frontend

- `VITE_API_URL`: Base URL for API requests (set in `.env` or `vite.config.ts`)
- `VITE_PORT`: Frontend development server port (default: `5174`)

## Important Notes

- The frontend uses hash mode routing (`#/`) to avoid server configuration requirements
- Authentication tokens are stored in localStorage with auto-refresh on page load
- User avatars use `ImageField` with fallback to `https://picsum.photos/200/200`
- Backend includes `django-extensions` for additional development utilities
- Chinese PyPI mirror configured in README for faster package installation in China

## Common Development Tasks

1. **Adding a new Django app**: Create app, add to `INSTALLED_APPS`, define models, create migrations
2. **Creating new API endpoints**: Add view to app's `api.py`, define URL in app's `urls.py`, include in main `urls.py`
3. **Adding frontend view**: Create Vue component in `src/views/`, add route to `src/router/index.ts`
4. **Creating new Pinia store**: Add file to `src/stores/` with `defineStore`
5. **Styling components**: Use Tailwind CSS utility classes in Vue components

## graphify

A knowledge graph of this codebase lives at `graphify-out/graph.json` (run `/graphify .` to rebuild).

Before answering questions about code architecture, relationships, or dependencies, check the graph:

```bash
/graphify query "your question"
```

Use `/graphify path "NodeA" "NodeB"` to find shortest paths between concepts.
Use `/graphify explain "node_name"` for plain-language explanation of a node and its connections.
Use `/graphify --update` after making significant code changes to refresh the graph.

