# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

from serializers import PlainCallbackSerializer, PlainCallbackTalentSerializer

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting
from um.views import error_as_text

from models import Callback, PlainCallback
from models import CallbackTalent, PlainCallbackTalent

from events.models import Event
from organizations.models import Organization, OrganizationMember


def talent_callbacks(user, event):
    t_callbacks = CallbackTalent.talent_event_callbacks(user, event)
    plain_callbacks = []
    for callback in t_callbacks:
        plain_callback = callback.plain()
        plain_callbacks.append(plain_callback)
    return plain_callbacks


def callback_organization_callbacks(organization, event):
    pass


def event_organization_callbacks(organization, event):
    pass


def add_talent_callback(organization, event):
    pass


def send_callback_to_event_organization(callback):
    pass


def notify_callback_to_talents(callback):
    pass


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def get_callbacks(request, event_id=None):
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    if event:
        if user.my_user.type == 'T':
            my_callbacks = talent_callbacks(user, event)
            serializer = PlainCallbackTalentSerializer(my_callbacks, many=True)
            return Response(serializer.data)
        else:
            user_organization = OrganizationMember.user_organization(user)
            if event.owner == user_organization:
                pass
            else:
                pass
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, HTTP_404_NOT_FOUND)

