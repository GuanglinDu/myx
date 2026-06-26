import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response
from account.models import User
from chat.models import Conversation, ConversationMessage
from notification.utils import create_notification


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


# DRF's test response object: 
# response is of type rest_framework.response.Response
# Key properties available:
# ┌──────────────────────┬─────────────┬───────────────────┐
# │       Property       │    Type     │      Example      │
# ├──────────────────────┼─────────────┼───────────────────┤
# │ response.status_code │ int         │ 200               │
# ├──────────────────────┼─────────────┼───────────────────┤
# │ response.json()      │ dict | list │ {'key': 'value'}  │
# ├──────────────────────┼─────────────┼───────────────────┤
# │ response.content     │ bytes       │ raw response body │
# └──────────────────────┴─────────────┴───────────────────┘
@pytest.mark.django_db
class TestChatAPI:
    """Tests for chat/api.py endpoints."""

    def test_conversation_list_empty(self, user: User,
                                     client: APIClient) -> None:
        """Test conversation list when no conversations exist."""
        client.force_authenticate(user=user)
        response: Response = client.get('/api/chat/')
        assert response.status_code == 200
        data: dict | list = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_conversation_list(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting conversation list."""
        # Create a conversation between users
        conv: Conversation = Conversation.objects.create()
        conv.participants.add(user, user2)

        client.force_authenticate(user=user)
        response: Response = client.get('/api/chat/')
        assert response.status_code == 200
        data: dict | list = response.json()
        assert len(data) == 1

    def test_get_or_create_conversation_new(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test creating a new conversation."""
        client.force_authenticate(user=user)
        response: Response = client.get(f'/api/chat/{user2.id}/get-or-create/')
        assert response.status_code == 200
        data: dict = response.json()
        assert len(data['participants']) == 2

        # Verify conversation was created
        assert Conversation.objects.filter(participants=user).filter(
            participants=user2).exists()

    def test_get_or_create_conversation_existing(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting existing conversation."""
        # Create existing conversation
        conv: Conversation = Conversation.objects.create()
        conv.participants.add(user, user2)
        client.force_authenticate(user=user)
        response: Response = client.get(f'/api/chat/{user2.id}/get-or-create/')
        assert response.status_code == 200

    def test_conversation_detail(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test getting conversation details."""
        # Create conversation with a message
        conv: Conversation = Conversation.objects.create()
        conv.participants.add(user, user2)
        ConversationMessage.objects.create(
            conversation=conv,
            body='Hello',
            sent_to=user2,
            created_by=user
        )

        client.force_authenticate(user=user)
        response: Response = client.get(f'/api/chat/{conv.id}/')
        assert response.status_code == 200
        data: dict = response.json()
        assert len(data['messages']) == 1
        assert data['messages'][0]['body'] == 'Hello'

    def test_send_message(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test sending a message."""
        # Create conversation
        conv = Conversation.objects.create()
        conv.participants.add(user, user2)

        client.force_authenticate(user=user)
        response: Response = client.post(
            f'/api/chat/{conv.id}/send/',
            {'body': 'Test message', 'sent_to': str(user2.id)},
            format='json'
        )
        assert response.status_code == 200
        data: dict = response.json()
        assert data['body'] == 'Test message'

        # Verify message was created
        assert ConversationMessage.objects.filter(body='Test message').exists()

    def test_cannot_see_other_conversations(
            self, user: User, user2: User, client: APIClient) -> None:
        """Test that users cannot see other users' conversations.

        A non-participant asking for a conversation they're not in
        should get 404, not 500 — and not leak whether the id is valid.
        """
        # Create conversation between user2 and another user
        other_user = User.objects.create_user(
            name='Other', email='other@example.com', password='pass123'
        )
        conv = Conversation.objects.create()
        conv.participants.add(user2, other_user)

        client.force_authenticate(user=user)
        response = client.get(f'/api/chat/{conv.id}/')
        assert response.status_code == 404