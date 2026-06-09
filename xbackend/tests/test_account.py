import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response
from account.models import User, FriendshipRequest


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
class TestAccountAPI:
    """Tests for account/api.py endpoints."""

    def test_me_returns_user_info(self, user: User, client: APIClient) -> None:
        """Test the /api/me/ endpoint returns user info."""
        client.force_authenticate(user=user)
        response: Response = client.get('/api/me/')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['email'] == user.email
        assert data['name'] == user.name
        assert str(data['id']) == str(user.id)

    def test_me_unauthenticated(self, client: APIClient) -> None:
        """Test /api/me/ returns 401 for unauthenticated users."""
        response: Response = client.get('/api/me/')
        assert response.status_code == 401

    def test_signup_success(self, client: APIClient) -> None:
        """Test user signup with valid data."""
        response: Response = client.post('/api/signup/', {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }, format='json')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['message'] == 'success'
        assert User.objects.filter(email='newuser@example.com').exists()

    def test_signup_password_mismatch(self, client: APIClient) -> None:
        """Test signup fails when passwords don't match."""
        response: Response = client.post('/api/signup/', {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'differentpass'
        }, format='json')
        assert response.status_code == 400
        data: dict = response.json()
        assert 'errors' in data
        assert 'password2' in data['errors']

    def test_send_friendship_request(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test sending a friendship request."""
        client.force_authenticate(user=user)
        response: Response = client.post(f'/api/friends/send/{user2.id}/')
        assert response.status_code == 200
        assert FriendshipRequest.objects.filter(
            created_for=user2,
            created_by=user
        ).exists()

    def test_send_friendship_request_to_self(
            self, user: User, client: APIClient) -> None:
        """Test sending a friendship request to yourself succeeds (no check)."""
        client.force_authenticate(user=user)
        response: Response = client.post(f'/api/friends/send/{user.id}/')
        # Backend doesn't prevent self-requests, just creates one
        assert response.status_code == 200

    def test_send_duplicate_friendship_request(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test sending duplicate friendship request fails."""
        client.force_authenticate(user=user)
        # First request
        client.post(f'/api/friends/send/{user2.id}/')
        # Duplicate request
        response: Response = client.post(f'/api/friends/send/{user2.id}/')
        assert response.status_code == 400

    def test_accept_friendship_request(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test accepting a friendship request increments friend_count."""
        client.force_authenticate(user=user)
        # Create request from user2 to user
        friend_request = FriendshipRequest.objects.create(
            created_for=user,
            created_by=user2,
            status=FriendshipRequest.SENT
        )
        response: Response = client.post(
            f'/api/friends/accept/{friend_request.id}/')
        assert response.status_code == 200

        # Verify they are now friends
        assert user.friends.filter(pk=user2.id).exists()

        # Verify friend_count incremented for both
        user.refresh_from_db()
        user2.refresh_from_db()
        assert user.friend_count == 1
        assert user2.friend_count == 1

    def test_reject_friendship_request(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test rejecting a friendship request."""
        client.force_authenticate(user=user)
        # Create request from user2 to user
        friend_request = FriendshipRequest.objects.create(
            created_for=user,
            created_by=user2,
            status=FriendshipRequest.SENT
        )
        response: Response = client.post(
            f'/api/friends/reject/{friend_request.id}/')
        assert response.status_code == 200

        # Verify request is deleted
        assert not FriendshipRequest.objects.filter(
            pk=friend_request.id).exists()

    def test_get_friendship_status_self(self, user: User,
                                        client: APIClient) -> None:
        """Test getting friendship status for yourself returns 'self'."""
        client.force_authenticate(user=user)
        response: Response = client.get(f'/api/friends/status/{user.id}/')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['status'] == 'self'

    def test_get_friendship_status_friends(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting friendship status when users are friends."""
        user.friends.add(user2)
        client.force_authenticate(user=user)
        response: Response = client.get(f'/api/friends/status/{user2.id}/')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['status'] == 'friends'

    def test_get_friendship_status_none(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting friendship status when users are not friends."""
        client.force_authenticate(user=user)
        response: Response = client.get(f'/api/friends/status/{user2.id}/')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['status'] == 'none'

    def test_get_friendship_status_pending(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting friendship status when other user sent request."""
        client.force_authenticate(user=user)
        # user2 sends request to user
        FriendshipRequest.objects.create(
            created_for=user,
            created_by=user2,
            status=FriendshipRequest.SENT
        )
        response: Response = client.get(f'/api/friends/status/{user2.id}/')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['status'] == 'pending'

    def test_get_friendship_status_request_sent(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting friendship status when current user sent request."""
        client.force_authenticate(user=user)
        # user sends request to user2
        FriendshipRequest.objects.create(
            created_for=user2,
            created_by=user,
            status=FriendshipRequest.SENT
        )
        response: Response = client.get(f'/api/friends/status/{user2.id}/')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['status'] == 'request_sent'

    def test_get_friendship_requests(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting pending friendship requests."""
        client.force_authenticate(user=user)
        # user2 sends request to user
        FriendshipRequest.objects.create(
            created_for=user,
            created_by=user2,
            status=FriendshipRequest.SENT
        )
        response: Response = client.get(f'/api/friends/{user.id}/requests/')
        assert response.status_code == 200
        data: dict = response.json()
        assert len(data) == 1
        assert str(data[0]['created_by']['id']) == str(user2.id)

    def test_friends_list(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting friends list."""
        user.friends.add(user2)
        client.force_authenticate(user=user)
        response: Response = client.get(f'/api/friends/{user.id}/')
        assert response.status_code == 200
        data: dict = response.json()
        assert len(data['friends']) == 1
        assert str(data['friends'][0]['id']) == str(user2.id)

    def test_editprofile_success(self, user: User, client: APIClient) -> None:
        """Test the /api/editprofile/ endpoint updates name and email."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editprofile/', {
            'name': 'Updated Name',
            'email': 'updated@example.com',
        }, format='json')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['name'] == 'Updated Name'
        assert data['email'] == 'updated@example.com'
        assert str(data['id']) == str(user.id)

        user.refresh_from_db()
        assert user.name == 'Updated Name'
        assert user.email == 'updated@example.com'

    def test_editprofile_preserves_unchanged_fields(
            self, user: User, client: APIClient) -> None:
        """Test that omitting a field does not blank it out."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editprofile/', {
            'name': 'Only Name Changed',
        }, format='json')
        assert response.status_code == 200
        data: dict = response.json()
        assert data['name'] == 'Only Name Changed'
        assert data['email'] == user.email

    def test_editprofile_rejects_invalid_email(
            self, user: User, client: APIClient) -> None:
        """Test that an invalid email is rejected with 400."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editprofile/', {
            'name': 'Test User',
            'email': 'not-an-email',
        }, format='json')
        assert response.status_code == 400

    def test_editprofile_rejects_blank_name(
            self, user: User, client: APIClient) -> None:
        """Test that a blank name is rejected with 400."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editprofile/', {
            'name': '   ',
            'email': 'test@example.com',
        }, format='json')
        assert response.status_code == 400

    def test_editprofile_rejects_duplicate_email(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test that taking another user's email is rejected with 400."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editprofile/', {
            'name': 'Test User',
            'email': user2.email,
        }, format='json')
        assert response.status_code == 400

    def test_editprofile_unauthenticated(self, client: APIClient) -> None:
        """Test /api/editprofile/ returns 401 for unauthenticated users."""
        response: Response = client.post('/api/editprofile/', {
            'name': 'Test User',
            'email': 'test@example.com',
        }, format='json')
        assert response.status_code == 401


@pytest.mark.django_db
class TestEditPasswordAPI:
    """Tests for the /api/editpassword/ endpoint."""

    def test_editpassword_success(self, user: User,
                                  client: APIClient) -> None:
        """Successful change actually rotates the stored password."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editpassword/', {
            'currentPassword': 'testpass123',
            'newPassword': 'newpassword456',
            'confirmNewPassword': 'newpassword456',
        }, format='json')
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.check_password('newpassword456') is True
        assert user.check_password('testpass123') is False

    def test_editpassword_unauthenticated(self, client: APIClient) -> None:
        """Returns 401 when no user is authenticated."""
        response: Response = client.post('/api/editpassword/', {
            'currentPassword': 'testpass123',
            'newPassword': 'newpassword456',
            'confirmNewPassword': 'newpassword456',
        }, format='json')
        assert response.status_code == 401

    def test_editpassword_wrong_current_password(
            self, user: User, client: APIClient) -> None:
        """Rejects the request when currentPassword does not match."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editpassword/', {
            'currentPassword': 'wrong-current',
            'newPassword': 'newpassword456',
            'confirmNewPassword': 'newpassword456',
        }, format='json')
        assert response.status_code == 400
        user.refresh_from_db()
        assert user.check_password('testpass123') is True

    def test_editpassword_mismatched_confirmation(
            self, user: User, client: APIClient) -> None:
        """Rejects the request when new/confirm passwords differ."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editpassword/', {
            'currentPassword': 'testpass123',
            'newPassword': 'newpassword456',
            'confirmNewPassword': 'different999',
        }, format='json')
        assert response.status_code == 400
        user.refresh_from_db()
        assert user.check_password('testpass123') is True

    def test_editpassword_short_new_password(
            self, user: User, client: APIClient) -> None:
        """Rejects a new password shorter than 8 characters."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editpassword/', {
            'currentPassword': 'testpass123',
            'newPassword': 'short',
            'confirmNewPassword': 'short',
        }, format='json')
        assert response.status_code == 400
        user.refresh_from_db()
        assert user.check_password('testpass123') is True

    def test_editpassword_new_same_as_current(
            self, user: User, client: APIClient) -> None:
        """Rejects a new password that equals the current password."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editpassword/', {
            'currentPassword': 'testpass123',
            'newPassword': 'testpass123',
            'confirmNewPassword': 'testpass123',
        }, format='json')
        assert response.status_code == 400

    def test_editpassword_missing_current_password(
            self, user: User, client: APIClient) -> None:
        """Rejects the request when currentPassword is missing."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editpassword/', {
            'newPassword': 'newpassword456',
            'confirmNewPassword': 'newpassword456',
        }, format='json')
        assert response.status_code == 400

    def test_editpassword_missing_new_password(
            self, user: User, client: APIClient) -> None:
        """Rejects the request when newPassword is missing."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editpassword/', {
            'currentPassword': 'testpass123',
            'confirmNewPassword': 'newpassword456',
        }, format='json')
        assert response.status_code == 400

    def test_editpassword_missing_confirmation(
            self, user: User, client: APIClient) -> None:
        """Rejects the request when confirmNewPassword is missing."""
        client.force_authenticate(user=user)
        response: Response = client.post('/api/editpassword/', {
            'currentPassword': 'testpass123',
            'newPassword': 'newpassword456',
        }, format='json')
        assert response.status_code == 400