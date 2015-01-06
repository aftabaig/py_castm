import logging
import urbanairship as ua

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting

from links.serializers import PlainLinkSerializer
from links.serializers import MyLinksSerializer

from links.models import Link
from links.models import PlainLink
from links.models import MyLinks

from models import Notification

logger = logging.getLogger(__name__)

@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def my_notifications(request):
    pass


def send_message(request):
    pass


def send_callback(request):
    pass


def create_notification(type, for_user, title=None, message=None):

        airship = ua.Airship('', '')
        push = airship.create_push()
        push.audience = ua.device_token(for_user.my_user.push_token)
        push.notification = ua.notification(alert=message)
        push.device_types = ua.device_types('all')
        push.send()

        notification = Notification(type=type, for_user=for_user, title=title, message=message, seen=False, action_taken=False)
        notification.save()
        return notification




