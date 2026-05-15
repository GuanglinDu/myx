import pytest
from rest_framework.test import APIClient
from account.models import User
from post.models import Post, Like, Comment


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        name='Test User',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def user2(db):
    """Create a second test user."""
    return User.objects.create_user(
        name='Test User 2',
        email='test2@example.com',
        password='testpass123'
    )


@pytest.fixture
def client():
    """Return a REST framework API client."""
    return APIClient()


@pytest.mark.django_db
class TestPostAPI:
    """Tests for post/api.py endpoints."""

    def test_post_list_empty(self, user, client):
        """Test post list when user has no posts."""
        client.force_authenticate(user=user)
        response = client.get('/api/posts/')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_post_list_includes_own_posts(self, user, client):
        """Test post list includes authenticated user's posts."""
        Post.objects.create(body='Test post', created_by=user)
        client.force_authenticate(user=user)
        response = client.get('/api/posts/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['body'] == 'Test post'

    def test_post_list_includes_friends_posts(self, user, user2, client):
        """Test post list includes friends' posts."""
        user.friends.add(user2)
        Post.objects.create(body='Friend post', created_by=user2)
        client.force_authenticate(user=user)
        response = client.get('/api/posts/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['body'] == 'Friend post'

    def test_post_list_excludes_non_friends_posts(self, user, user2, client):
        """Test post list excludes posts from non-friends."""
        Post.objects.create(body='Other post', created_by=user2)
        client.force_authenticate(user=user)
        response = client.get('/api/posts/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    def test_post_create(self, user, client):
        """Test creating a post."""
        client.force_authenticate(user=user)
        response = client.post('/api/posts/create/', {
            'body': 'New post content'
        }, format='json')
        assert response.status_code == 200
        data = response.json()
        assert data['body'] == 'New post content'
        assert str(data['created_by']['id']) == str(user.id)

    def test_post_detail(self, user, client):
        """Test getting post details."""
        post = Post.objects.create(body='Test post', created_by=user)
        client.force_authenticate(user=user)
        response = client.get(f'/api/posts/{post.id}/')
        assert response.status_code == 200
        data = response.json()['post']
        assert data['body'] == 'Test post'

    def test_post_like(self, user, client):
        """Test liking a post."""
        post = Post.objects.create(body='Test post', created_by=user)
        client.force_authenticate(user=user)
        response = client.post(f'/api/posts/{post.id}/like/')
        assert response.status_code == 200
        data = response.json()
        assert data['liked'] is True
        assert data['like_count'] == 1

    def test_post_unlike(self, user, client):
        """Test unliking a post."""
        post = Post.objects.create(body='Test post', created_by=user)
        like = Like.objects.create(created_by=user)
        post.likes.add(like)
        post.like_count = 1
        post.save()
        client.force_authenticate(user=user)
        response = client.post(f'/api/posts/{post.id}/like/')
        assert response.status_code == 200
        data = response.json()
        assert data['liked'] is False
        assert data['like_count'] == 0

    def test_create_comment(self, user, client):
        """Test adding a comment to a post."""
        post = Post.objects.create(body='Test post', created_by=user)
        client.force_authenticate(user=user)
        response = client.post(f'/api/posts/{post.id}/comment/', {
            'body': 'Test comment'
        }, format='json')
        assert response.status_code == 200
        data = response.json()
        assert data['body'] == 'Test comment'

    def test_post_list_profile(self, user, user2, client):
        """Test getting posts for a specific user's profile."""
        Post.objects.create(body='User2 post', created_by=user2)
        client.force_authenticate(user=user)
        response = client.get(f'/api/posts/profile/{user2.id}/')
        assert response.status_code == 200
        data = response.json()
        assert len(data['posts']) == 1
        assert data['friendship_status'] == 'none'