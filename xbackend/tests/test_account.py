import pytest
from rest_framework.test import APIClient
from account.models import User, FriendshipRequest


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
class TestAccountAPI:
    """Tests for account/api.py endpoints."""

    def test_me_returns_user_info(self, user, client):
        """Test the /api/me/ endpoint returns user info."""
        client.force_authenticate(user=user)
        response = client.get('/api/me/')
        assert response.status_code == 200
        data = response.json()
        assert data['email'] == user.email
        assert data['name'] == user.name
        assert str(data['id']) == str(user.id)

    def test_me_unauthenticated(self, client):
        """Test /api/me/ returns 401 for unauthenticated users."""
        response = client.get('/api/me/')
        assert response.status_code == 401

    def test_signup_success(self, client):
        """Test user signup with valid data."""
        response = client.post('/api/signup/', {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }, format='json')
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == 'success'
        assert User.objects.filter(email='newuser@example.com').exists()

    def test_signup_password_mismatch(self, client):
        """Test signup fails when passwords don't match."""
        response = client.post('/api/signup/', {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'differentpass'
        }, format='json')
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == 'error'

    def test_send_friendship_request(self, user, user2, client):
        """Test sending a friendship request."""
        client.force_authenticate(user=user)
        response = client.post(f'/api/friends/send/{user2.id}/')
        assert response.status_code == 200
        assert FriendshipRequest.objects.filter(
            created_for=user2,
            created_by=user
        ).exists()

    def test_send_friendship_request_to_self(self, user, client):
        """Test sending a friendship request to yourself succeeds (no check)."""
        client.force_authenticate(user=user)
        response = client.post(f'/api/friends/send/{user.id}/')
        # Backend doesn't prevent self-requests, just creates one
        assert response.status_code == 200

    def test_send_duplicate_friendship_request(self, user, user2, client):
        """Test sending duplicate friendship request fails."""
        client.force_authenticate(user=user)
        # First request
        client.post(f'/api/friends/send/{user2.id}/')
        # Duplicate request
        response = client.post(f'/api/friends/send/{user2.id}/')
        assert response.status_code == 400

    def test_accept_friendship_request(self, user, user2, client):
        """Test accepting a friendship request."""
        client.force_authenticate(user=user)
        # Create request from user2 to user
        friend_request = FriendshipRequest.objects.create(
            created_for=user,
            created_by=user2,
            status=FriendshipRequest.SENT
        )
        response = client.post(f'/api/friends/accept/{friend_request.id}/')
        assert response.status_code == 200

        # Verify they are now friends
        assert user.friends.filter(pk=user2.id).exists()

    def test_reject_friendship_request(self, user, user2, client):
        """Test rejecting a friendship request."""
        client.force_authenticate(user=user)
        # Create request from user2 to user
        friend_request = FriendshipRequest.objects.create(
            created_for=user,
            created_by=user2,
            status=FriendshipRequest.SENT
        )
        response = client.post(f'/api/friends/reject/{friend_request.id}/')
        assert response.status_code == 200

        # Verify request is deleted
        assert not FriendshipRequest.objects.filter(pk=friend_request.id).exists()

    def test_get_friendship_status_self(self, user, client):
        """Test getting friendship status for yourself returns 'self'."""
        client.force_authenticate(user=user)
        response = client.get(f'/api/friends/status/{user.id}/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'self'

    def test_get_friendship_status_friends(self, user, user2, client):
        """Test getting friendship status when users are friends."""
        user.friends.add(user2)
        client.force_authenticate(user=user)
        response = client.get(f'/api/friends/status/{user2.id}/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'friends'

    def test_get_friendship_status_none(self, user, user2, client):
        """Test getting friendship status when users are not friends."""
        client.force_authenticate(user=user)
        response = client.get(f'/api/friends/status/{user2.id}/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'none'

    def test_get_friendship_status_pending(self, user, user2, client):
        """Test getting friendship status when other user sent request."""
        client.force_authenticate(user=user)
        # user2 sends request to user
        FriendshipRequest.objects.create(
            created_for=user,
            created_by=user2,
            status=FriendshipRequest.SENT
        )
        response = client.get(f'/api/friends/status/{user2.id}/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'pending'

    def test_get_friendship_status_request_sent(self, user, user2, client):
        """Test getting friendship status when current user sent request."""
        client.force_authenticate(user=user)
        # user sends request to user2
        FriendshipRequest.objects.create(
            created_for=user2,
            created_by=user,
            status=FriendshipRequest.SENT
        )
        response = client.get(f'/api/friends/status/{user2.id}/')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'request_sent'

    def test_get_friendship_requests(self, user, user2, client):
        """Test getting pending friendship requests."""
        client.force_authenticate(user=user)
        # user2 sends request to user
        FriendshipRequest.objects.create(
            created_for=user,
            created_by=user2,
            status=FriendshipRequest.SENT
        )
        response = client.get(f'/api/friends/{user.id}/requests/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert str(data[0]['created_by']['id']) == str(user2.id)

    def test_friends_list(self, user, user2, client):
        """Test getting friends list."""
        user.friends.add(user2)
        client.force_authenticate(user=user)
        response = client.get(f'/api/friends/{user.id}/')
        assert response.status_code == 200
        data = response.json()
        assert len(data['friends']) == 1
        assert str(data['friends'][0]['id']) == str(user2.id)