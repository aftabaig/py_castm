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

from links.models import Link
from links.serializers import PlainLinkSerializer
from my_messages.models import Message
from organizations.models import OrganizationMember
from organizations.serializers import PlainMemberSerializer

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
            description=notification.message,
            source_id=notification.source_id,
        )
        if notification.from_user.my_user.type == 'T':
            plain_notification.title = notification.from_user.user_profile.get().title,
            plain_notification.thumbnail_url = notification.from_user.user_profile.get().thumbnail,
            plain_notification.profile_url = "/api/talents/profile/%d" % (notification.from_user.id, ),
        else:
            plain_notification.title = "",
            # plain_notification.thumbnail_url = notification.from_user.casting_profile.get().thumbnail,
            # plain_notification.profile_url = "/api/casting/profile/%d" % (notification.from_user.id, ),

        if type == 'LR' or type == 'LA' or type == 'LR':
            plain_notification.source = Link.objects.filter(id=notification.source_id).first().plain()
        elif type == 'MSG':
            plain_notification.source = Message.objects.filter(id=notification.source_id).first().plain()
        elif type == 'OMI' or type == 'OIA' or type == 'OIR' or type == 'OMR' or type == 'ORA' or type == 'ORR':
            plain_notification.source = OrganizationMember.objects.filter(id=notification.source_id).first().plain()
            logger.debug(plain_notification.source)

        my_notifications.append(plain_notification)

    return PlainNotificationSerializer(my_notifications, many=True)


def create_notification(type, source_id, from_user, for_user, message=None):

        # airship = ua.Airship('', '')
        # push = airship.create_push()
        # push.audience = ua.device_token(for_user.my_user.push_token)
        # push.notification = ua.notification(alert=message)
        # push.device_types = ua.device_types('all')
        # push.send()

        notification = Notification(type=type, source_id=source_id,
                                    from_user=from_user, for_user=for_user,
                                    message=message, seen=False, action_taken=False)

        notification.save()
        return notification


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
    notifications = request.DATA.get("notifications")

    for notification_id in notifications:
        notification = Notification.objects.get(pk=notification_id)
        if notification.for_user == user:
            notification.seen = True
            notification.save()

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
    if notification.for_user == user:
        notification.action_taken = True
        notification.seen = True
        notification.save()

    return Response({
        "status": HTTP_200_OK,
        "message": "OK"
    }, status=HTTP_200_OK)




