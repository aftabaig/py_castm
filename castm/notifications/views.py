import logging
import urbanairship as ua

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting

from notifications.serializers import PlainNotificationSerializer
from notifications.serializers import MyNotificationSerializer

from links.models import Link
from links.serializers import PlainLinkSerializer

from my_messages.models import Message
from organizations.models import OrganizationMember
from organizations.serializers import PlainMemberSerializer
from callbacks.models import Callback
from callbacks.models import CallbackTalent

from notifications.models import Notification
from notifications.models import PlainNotification
from notifications.models import MyNotifications

from models import Notification

logger = logging.getLogger(__name__)


def get_notifications(user, type):
    notifications = Notification.unread_notifications(user, type)
    my_notifications = []
    for notification in notifications:
        plain_notification = notification.plain()
        my_notifications.append(plain_notification)
    return PlainNotificationSerializer(my_notifications, many=True)


def create_notification(type, source_id, from_user, for_user, message=None):

        notification = Notification(type=type,
                                    source_id=source_id,
                                    from_user=from_user, for_user=for_user,
                                    message=message, seen=False, action_taken=False)

        notification.save()

        extra = {
            "id": notification.id,
            "type": notification.type
        }

        airship = ua.Airship('d6awtJp0T-Cyx5QRXUYr7Q', 'gpSq1dyuZYZy-Q1i6qtEit')
        devices = for_user.user_devices.all()
        for device in devices:
            if device.push_token:
                push = airship.create_push()
                if device.device_type == 'iOS':
                    push.audience = ua.device_token(device.push_token)
                elif device.device_type == 'Android':
                    push.audience = ua.apid(device.push_token)

                push.notification = ua.notification(ios=ua.ios(alert=message,
                                                               badge="+1",
                                                               extra=extra),
                                                    android=ua.android(alert=message,
                                                                       extra=extra))
                push.device_types = ua.device_types('ios', 'android', )
                push.send()

        return notification


@api_view(['GET'])
@permission_classes([IsTalentOrCasting, ])
def get_notification(request, notification_id=None):
    user = request.user
    notification = Notification.objects.filter(id=notification_id).first()
    if notification:
        if user == notification.for_user:
            plain_notification = notification.plain()
            serializer = PlainNotificationSerializer(plain_notification)
            return Response(serializer.data)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You are not authorized to perform this action"
        }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Notification not found"
    }, status=HTTP_404_NOT_FOUND)



@api_view(['DELETE', ])
@permission_classes([IsTalentOrCasting, ])
def delete_notification(request, notification_id=None):
    """
    Deletes a notification.
    Status:\n
        1. 204 on success
        2. 401 if un-authorized
        3. 404 if notification not found
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    notification = Notification.objects.filter(id=notification_id)
    if notification:
        if notification.for_user == user:
            notification.delete()
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You are not authorized to perform this action"
        }, HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Notification not found"
    }, HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def notifications_callbacks(request):
    """
    Returns callback notifications.
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            [
                {
                    notification_id: 7,
                    notification_type: "CB",
                    created_at: "2015-01-07T12:35:59.396Z",
                    user_id: 14,
                    first_name: "Ikarma",
                    last_name: "Khan",
                    title: "Link Request",
                    description: "",
                    thumbnail_url: "",
                    profile_url: "",
                },
            ]
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    type = "CB"
    serializer = get_notifications(user, type)
    return Response(serializer.data)

@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def notifications_link_requests(request):
    """
    Returns link-request notifications.
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            [
                {
                    notification_id: 7,
                    notification_type: "LR",
                    created_at: "2015-01-07T12:35:59.396Z",
                    user_id: 14,
                    first_name: "Ikarma",
                    last_name: "Khan",
                    title: "Link Request",
                    description: "",
                    thumbnail_url: "",
                    profile_url: "",
                },
            ]
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    type = "LR"
    serializer = get_notifications(user, type)
    return Response(serializer.data)

@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def notifications_messages(request):
    """
    Returns message notifications.
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            [
                {
                    notification_id: 7,
                    notification_type: "LR",
                    created_at: "2015-01-07T12:35:59.396Z",
                    user_id: 14,
                    first_name: "Ikarma",
                    last_name: "Khan",
                    title: "Link Request",
                    description: "",
                    thumbnail_url: "",
                    profile_url: "",
                },
            ]
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    type = "MSG"
    serializer = get_notifications(user, type)
    return Response(serializer.data)

@api_view(['GET', ])
@permission_classes([IsCasting, ])
def notifications_membership_requests(request):
    """
    Returns membership requests notifications.
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            [
                {
                    notification_id: 7,
                    notification_type: "LR",
                    created_at: "2015-01-07T12:35:59.396Z",
                    user_id: 14,
                    first_name: "Ikarma",
                    last_name: "Khan",
                    title: "Link Request",
                    description: "",
                    thumbnail_url: "",
                    profile_url: "",
                },
            ]
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    type = "OMR"
    serializer = get_notifications(user, type)
    return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes([IsTalentOrCasting, ])
def mark_as_seen(request):
    """
    Marks multiple notifications as seen.\n
    Needs to send the following hash:\n
    {\b
        "notifications": [\n
            1,2,3,4\n
        ]\n
    }\n
    Allowed HTTP methods are:\n
        1. PUT to update\n
            Returns:\n
            [
                {
                    "status": 200,
                    "message": "OK"
                },
            ]
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    str_notifications = request.DATA.get("notifications")
    notification_ids = str_notifications.split(",")

    for notification_id in notification_ids:
        notification = Notification.objects.filter(id=int(notification_id)).first()
        if notification:
            if notification.for_user == user:
                notification.seen = True
                notification.save()
            else:
                return Response({
                    "status": HTTP_401_UNAUTHORIZED,
                    "message": "You are not authorized to process this notification"
                }, HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                "status": HTTP_404_NOT_FOUND,
                "message": "Notification not found"
            }, HTTP_404_NOT_FOUND)
    return Response({
        "status": HTTP_200_OK,
        "message": "OK"
    }, status=HTTP_200_OK)


@api_view(['PUT', ])
@permission_classes([IsTalentOrCasting, ])
def action_taken(request, notification_id):
    """
    To respond to a notification.
    Allowed HTTP methods are:\n
        1. PUT to update\n
            Returns:\n
            [
                {
                    "status": 200,
                    "message": "OK"
                },
            ]
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    notification = Notification.objects.get(pk=notification_id)
    if notification.type == "MSG":
        related_notifications = Notification.unread_notifications(user, "MSG")
        for related_notification in related_notifications:
            related_notification.action_taken = True
            related_notification.seen = True
            related_notification.save()
    if notification.for_user == user:
        notification.action_taken = True
        notification.seen = True
        notification.save()
    return Response({
        "status": HTTP_200_OK,
        "message": "OK"
    }, status=HTTP_200_OK)




