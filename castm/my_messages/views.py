import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

from django.db import models

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting

from serializers import PlainMessageSerializer
from serializers import MyMessagesSerializer

from models import Message
from links.models import Link
from models import PlainMessage
from talent.models import TalentProfile
from notifications.views import create_notification

logger = logging.getLogger(__name__)

@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def message_detail(request, message_id=0):
    """
    Returns detail about a message.\n
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
                {
                    "msg_id": [msg_id],
                    "created_at": [message_date],
                    "message": [message],
                    "from_user_id": [user_id],
                    "from_first_name": [first_name],
                    "from_last_name": [last_name],
                    "from_title": [title],
                    "from_thumbnail_url": [thumbnail_url],
                    "from_profile_url": [profile_url],
                    "to_user_id": [user_id],
                    "to_first_name": [first_name],
                    "to_last_name": [last_name],
                    "to_title": [title],
                    "to_thumbnail_url": [thumbnail_url],
                    "to_profile_url": [profile_url]
                }
    Status:\n
        1. 200 on success
        2. 400 if some error occurs
        3. 401 if un-authorized
        4. 404 if message not found
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n

    """
    user = request.user
    message = Message.objects.filter(id=message_id).first()
    if message:
        if message.from_user == user or message.to_user == user:
            msg = message.plain()
            serializer = PlainMessageSerializer(msg)
            return Response(serializer.data)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You are not authorized to view this message"
        }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Message not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def message_thread(request, user_id=0):
    """
    Returns current & other user's message thread.
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            [
                {
                    "msg_id": [msg_id],
                    "created_at": [message_date],
                    "message": [message],
                    "from_user_id": [user_id],
                    "from_first_name": [first_name],
                    "from_last_name": [last_name],
                    "from_title": [title],
                    "from_thumbnail_url": [thumbnail_url],
                    "from_profile_url": [profile_url],
                    "to_user_id": [user_id],
                    "to_first_name": [first_name],
                    "to_last_name": [last_name],
                    "to_title": [title],
                    "to_thumbnail_url": [thumbnail_url],
                    "to_profile_url": [profile_url]
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
    other = User.objects.filter(id=user_id)
    messages = Message.thread(user, other)
    plain_msgs = []
    for message in messages:
        plain_msg = message.plain()
        plain_msgs.append(plain_msg)

    serializer = PlainMessageSerializer(plain_msgs, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def send_message(request):
    """
    Sends a message to a linked user.
    Allowed HTTP methods are:\n
        1. POST to send\n
            Accepts following hash:\n
            . {\n
                "to": [user_id],\n
                "message": [the_message]\n
            }\n
            Returns:\n
            . Newly created message
    Status:\n
        1. 200 on success
        2. 400 if some error occurs
        3. 401 if un-authorized
        4. 404 if user not found
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    me = request.user
    to_id = request.DATA.get("to")
    msg = request.DATA.get("message")
    to = User.objects.filter(id=to_id).first()

    if to:
        if Link.is_already_link(me, to):
            message = Message()
            message.from_user = me
            message.to_user = to
            message.message = msg
            message.save()
            create_notification("MSG", message.id, me, to, message=msg)
            serializer = PlainMessageSerializer(message.plain())
            return Response(serializer.data)
        return Response({
            "status": HTTP_400_BAD_REQUEST,
            "message": "Cannot send message to a non-link"
        }, status=HTTP_400_BAD_REQUEST)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "User not found"
    }, status=HTTP_404_NOT_FOUND)


