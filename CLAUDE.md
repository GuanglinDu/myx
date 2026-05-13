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
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest tests/apps/               # Test specific folder
pytest tests/apps/model_test.py::test_name  # Run specific test
pytest --cov                    # With coverage report
```

### Frontend

```bash
cd xfrontend
npm install
npm run dev         # Start dev server (port 5174)
npm run build       # Build for production
```

### Database

```bash
python manage.py seed_db           # Populate with fake data
python manage.py seed_db --clear  # Clear seeded data
python del_migrations.py      # Remove all migrations (dev only)
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

### Frontend Structure (xfrontend/src/)

- **views/** - Page components (HomeView, FeedView, ProfileView, ChatView, etc.)
- **components/** - Reusable components
- **stores/** - Pinia state management (`user.ts`, `toast.ts`)
- **router/** - Vue Router configuration
- **types/** - TypeScript type definitions

### URL Patterns

Frontend uses hash mode routing (`#/`) by default. Routes in `src/router/index.ts`:
- `#/` - Home
- `#/feed` - Friends' posts
- `#/chat` - Direct messages
- `#/search` - Search users
- `#/profile/:id` - User profile
- `#/profile/:id/friends` - User's friends
- `#/login` / `#/signup` - Authentication

### API Endpoints

Authentication:
- `POST /api/login/` - JWT login
- `POST /api/refresh/` - Refresh token
- `POST /api/signup/` - User registration
- `GET /api/me/` - Current user profile

Posts:
- `GET /api/posts/` - Feed (friends' posts)
- `POST /api/posts/create/` - Create post
- `GET /api/posts/:id/` - Post detail
- `POST /api/posts/:id/like/` - Like/unlike
- `POST /api/posts/:id/comment/` - Add comment

Friends:
- `POST /api/friends/send/:id/` - Send request
- `POST /api/friends/accept/:id/` - Accept request
- `POST /api/friends/reject/:id/` - Reject request
- `POST /api/friends/remove/:id/` - Remove friend

Chat:
- `GET /api/chat/` - List conversations
- `GET /api/chat/:id/` - Get conversation with messages
- `POST /api/chat/:id/send/` - Send message
- `GET /api/chat/:user_id/get-or-create/` - Start new conversation

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

### Backend (Python)
- 4 spaces indentation
- 79 character line limit
- `snake_case` for functions/variables
- 2 blank lines between top-level definitions

### Frontend (TypeScript/Vue)
- 2 spaces indentation
- Use `async/await` instead of `.then()/.catch()` chains

## Important Notes

- Frontend runs on port 5174 (configurable via `VITE_PORT`)
- Backend runs on port 8001
- User avatars use `ImageField` with fallback to DiceBear generation
- Chinese PyPI mirror configured for faster installs in China

## graphify

Knowledge graph at `graphify-out/graph.json`. Rebuild with:

```bash
/graphify .
```