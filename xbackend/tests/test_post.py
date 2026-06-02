import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response
from account.models import User
from post.models import Post, Like, Trend


@pytest.fixture
def user(db) -> User:
    """Create a test user."""
    return User.objects.create_user(
        name='Test User',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def user2(db) -> User:
    """Create a second test user."""
    return User.objects.create_user(
        name='Test User 2',
        email='test2@example.com',
        password='testpass123'
    )


@pytest.fixture
def client() -> APIClient:
    """Return a REST framework API client."""
    return APIClient()


@pytest.mark.django_db
class TestPostAPI:
    """Tests for post/api.py endpoints."""

    def test_post_list_empty(self, user: User, client: APIClient) -> None:
        """Test post list when user has no posts."""
        client.force_authenticate(user=user)
        response: Response = client.get('/api/posts/')
        assert response.status_code == 200
        data: dict | list = response.json()
        assert isinstance(data, list)

    def test_post_list_includes_own_posts(self, user: User,
                                          client: APIClient) -> None:
        """Test post list includes authenticated user's posts."""
        Post.objects.create(body='Test post', created_by=user)
        client.force_authenticate(user=user)
        response: Response = client.get('/api/posts/')
        assert response.status_code == 200
        data: dict | list = response.json()
        assert len(data) == 1
        assert data[0]['body'] == 'Test post'

    def test_post_list_includes_friends_posts(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test post list includes friends' posts."""
        user.friends.add(user2)
        Post.objects.create(body='Friend post', created_by=user2)
        client.force_authenticate(user=user)
        response: Response = client.get('/api/posts/')
        assert response.status_code == 200
        data: dict | list = response.json()
        assert len(data) == 1
        assert data[0]['body'] == 'Friend post'

    def test_post_list_excludes_non_friends_posts(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test post list excludes posts from non-friends."""
        Post.objects.create(body='Other post', created_by=user2)
        client.force_authenticate(user=user)
        response: Response = client.get('/api/posts/')
        assert response.status_code == 200
        data: dict | list = response.json()
        assert len(data) == 0

    def test_post_create(self, user: User, client: APIClient) -> None:
        """Test creating a post increments author's post_count."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/posts/create/', {
            'body': 'New post content'
        }, format='json')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['body'] == 'New post content'
        assert str(data['created_by']['id']) == str(user.id)
        user.refresh_from_db()
        assert user.post_count == 1

    def test_post_detail(self, user: User, client: APIClient) -> None:
        """Test getting post details."""
        post = Post.objects.create(body='Test post', created_by=user)
        client.force_authenticate(user=user)
        response: Response = client.get(f'/api/posts/{post.id}/')
        assert response.status_code == 200
        data: dict = response.json()['post']
        assert data['body'] == 'Test post'

    def test_post_like(self, user: User, client: APIClient) -> None:
        """Test liking a post."""
        post = Post.objects.create(body='Test post', created_by=user)
        client.force_authenticate(user=user)
        response: Response = client.post(f'/api/posts/{post.id}/like/')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['liked'] is True
        assert data['like_count'] == 1

    def test_post_unlike(self, user: User, client: APIClient) -> None:
        """Test unliking a post."""
        post = Post.objects.create(body='Test post', created_by=user)
        like = Like.objects.create(created_by=user)
        post.likes.add(like)
        post.like_count = 1
        post.save()
        client.force_authenticate(user=user)
        response: Response = client.post(f'/api/posts/{post.id}/like/')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['liked'] is False
        assert data['like_count'] == 0

    def test_create_comment(self, user: User, client: APIClient) -> None:
        """Test adding a comment to a post."""
        post = Post.objects.create(body='Test post', created_by=user)
        client.force_authenticate(user=user)
        response: Response = client.post(f'/api/posts/{post.id}/comment/', {
            'body': 'Test comment'
        }, format='json')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['body'] == 'Test comment'

    def test_post_list_profile(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting posts for a specific user's profile."""
        Post.objects.create(body='User2 post', created_by=user2)
        client.force_authenticate(user=user)
        response: Response = client.get(f'/api/posts/profile/{user2.id}/')
        assert response.status_code == 200
        data: dict = response.json()
        assert len(data['posts']) == 1
        assert data['friendship_status'] == 'none'

    def test_post_delete(self, user: User, client: APIClient) -> None:
        """Test deleting a post decrements author's post_count."""
        post = Post.objects.create(body='Test post', created_by=user)
        user.post_count = 1
        user.save()
        client.force_authenticate(user=user)
        response: Response = client.delete(f'/api/posts/{post.id}/delete/')
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.post_count == 0

    def test_post_delete_not_author(self, user: User, user2: User,
                                     client: APIClient) -> None:
        """Test non-author cannot delete another's post."""
        post = Post.objects.create(body='Test post', created_by=user2)
        client.force_authenticate(user=user)
        response: Response = client.delete(f'/api/posts/{post.id}/delete/')
        assert response.status_code == 403


@pytest.mark.django_db
class TestTrendsAPI:
    """Tests for trends API endpoint."""

    def test_trends_returns_top_10_hashtags(
            self, user: User, client: APIClient) -> None:
        """Test trends endpoint returns top 10 hashtags ordered by
        occurrence.
        """
        Trend.objects.create(hashtag='coding', occurences=100)
        Trend.objects.create(hashtag='python', occurences=50)
        Trend.objects.create(hashtag='django', occurences=200)

        client.force_authenticate(user=user)
        response: Response = client.get('/api/posts/trends/')
        assert response.status_code == 200
        data: dict | list = response.json()
        assert len(data) == 3
        # Ordered by occurences descending
        assert data[0]['hashtag'] == 'django'
        assert data[1]['hashtag'] == 'coding'
        assert data[2]['hashtag'] == 'python'

    def test_trends_excludes_hashtags_below_threshold(
            self, user: User, client: APIClient) -> None:
        """Test trends endpoint excludes hashtags below 10 occurrences."""
        Trend.objects.create(hashtag='popular', occurences=50)
        Trend.objects.create(hashtag='rare', occurences=5)

        client.force_authenticate(user=user)
        response: Response = client.get('/api/posts/trends/')
        assert response.status_code == 200
        data: dict | list = response.json()
        assert len(data) == 2
        assert data[0]['hashtag'] == 'popular'

    def test_trends_unauthenticated_returns_empty(
            self, client: APIClient) -> None:
        """Test trends endpoint returns empty list for unauthenticated."""
        response: Response = client.get('/api/posts/trends/')
        assert response.status_code == 401