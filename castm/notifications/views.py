import logging
import urbanairship as ua

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting

from notifications.serializers import PlainNotificationSerializer
from notifications.serializers import MyNotificationSerializer

from notifications.models import Notification
from notifications.models import PlainNotification
from notifications.models import MyNotifications

from models import Notification

logger = logging.getLogger(__name__)


def get_notifications(user, type):

    notifications = Notification.unread_notifications(user, type)
    my_notifications = []
    for notification in notifications:
        plain_notification = PlainNotification(
            notification_id=notification.id,
            notification_type=notification.type,
            created_at=notification.created_at,
            user_id=notification.from_user.id,
            first_name=notification.from_user.first_name,
            last_name=notification.from_user.last_name,
            title=notification.title,
            description=notification.message,
            thumbnail_url=notification.from_user.user_profile.get().thumbnail,
            profile_url="",
        )
        my_notifications.append(plain_notification)

    return PlainNotificationSerializer(my_notifications, many=True)


def create_notification(type, from_user, for_user, title=None, message=None):

        # airship = ua.Airship('', '')
        # push = airship.create_push()
        # push.audience = ua.device_token(for_user.my_user.push_token)
        # push.notification = ua.notification(alert=message)
        # push.device_types = ua.device_types('all')
        # push.send()

        notification = Notification(type=type, from_user=from_user, for_user=for_user, title=title, message=message, seen=False, action_taken=False)
        notification.save()
        return notification


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def notifications_callbacks(request):
    user = request.user
    type = "CB"
    serializer = get_notifications(user, type)
    return Response(serializer.data)

@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def notifications_link_requests(request):
    user = request.user
    type = "LR"
    serializer = get_notifications(user, type)
    return Response(serializer.data)

@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def notifications_messages(request):
    user = request.user
    type = "MSG"
    serializer = get_notifications(user, type)
    return Response(serializer.data)




