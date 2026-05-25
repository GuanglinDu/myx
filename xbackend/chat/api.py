import uuid
from django.db.models import QuerySet
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import (api_view)
from account.models import User                                       
from .models import Conversation, ConversationMessage
from .serializers import (ConversationSerializer, ConversationDetailSerializer,
                          ConversationMessageSerializer)


@api_view(['GET'])
def conversation_list(request: Request) -> JsonResponse:
    conversations: QuerySet[Conversation] = Conversation.objects.filter(
        participants=request.user).order_by('-modified_at')
    serializer: ConversationSerializer = ConversationSerializer(
        conversations, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_detail(request: Request, id: uuid.UUID) -> JsonResponse:
    """The id is the conversation ID, not the user ID. This is because
    we want to be able to fetch conversation details for conversations
    we haven't had with a specific user yet.
    """
    conversation: Conversation = Conversation.objects.filter(
        participants__in=list([request.user])).get(pk=id)
    serializer: ConversationDetailSerializer = ConversationDetailSerializer(
        conversation, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_or_create_conversation(request: Request,
                               user_id: uuid.UUID) -> JsonResponse:
    """The user_id is NOT the conversation ID but the id of the
    recipient. This is because we want to be able to send messages to
    users we haven't had conversations with yet.
    """
    recipient: User = User.objects.get(pk=user_id)
    conversations: QuerySet[Conversation] = Conversation.objects.filter(
        participants__in=list([request.user])).filter(
        participants__in=list([recipient]))

    conversation: Conversation
    if conversations.exists():
        print('Conversation already exists, using existing one.')
        conversation = conversations.first()
    else:
        print('No existing conversation, creating new one.')
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)
        conversation.save()

    serializer: ConversationSerializer = ConversationSerializer(
        conversation, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def send_message(request: Request, id: uuid.UUID) -> JsonResponse:
    """The id is the conversation ID, not the user ID. This is because
    we want to be able to send messages in conversations with a specific
    user.
    """
    conversation: Conversation = Conversation.objects.filter(
        participants__in=list([request.user])).get(pk=id)
    
    # TODO: What to do if no conversation found?
    sent_to_id: uuid.UUID = None
    for participant in conversation.participants.all():
        if participant != request.user:
            sent_to_id = participant.id
            break

    body: str = request.data.get('body', '')
     # Use provided sent_to, or fall back to auto-determined
    sent_to_id: uuid.UUID = request.data.get('sent_to') or sent_to_id
    message: ConversationMessage = ConversationMessage.objects.create(
        conversation=conversation,
        body=body,
        sent_to=User.objects.get(pk=sent_to_id),
        created_by=request.user
    )
    serializer: ConversationMessageSerializer = ConversationMessageSerializer(
        message, context={'request': request})
    return JsonResponse(serializer.data, safe=False)
