import uuid
from django.db.models import QuerySet
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .serializers import NotificationSerializer
from .models import Notification


""" Updated at 20:58:15 on 20260623 Tue by Guanglin Du.
How to use the related_name in django.db.models.ForeignKey?
 - Google AI Overview
 
The *related_name* attribute in Django’s ForeignKey customizes the name of
the reverse relation from the target model back to the model that defines
the foreign key. By default, Django creates a reverse manager named
<modelname>_set. Adding related_name allows you to override this default
with a cleaner, more readable name.

See history/How-to-use-the-related_name-in-django.db.models.ForeignKey-20260623.png.
"""
@api_view(['GET'])
def notifications(request: Request) -> JsonResponse:
    # Notice how this lengthy line of code is split across three lines.
    received_notifications: QuerySet[Notification] = (
        request.user.received_notifications.filter(is_read=False)
    )
    serializer: NotificationSerializer = NotificationSerializer(
        received_notifications, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def read_notification(request: Request, pk: uuid.UUID) -> JsonResponse:
    notification: Notification = Notification.objects.filter(
        created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()
    return JsonResponse({'message': 'notification read'})
