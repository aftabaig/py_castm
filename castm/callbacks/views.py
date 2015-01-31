# rest_framework
import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT
from django.contrib.auth.models import User

from serializers import PlainCallbackSerializer, PlainCallbackTalentSerializer

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting, IsTalent
from um.views import error_as_text

from models import Callback, PlainCallback
from models import CallbackTalent, PlainCallbackTalent

from notifications.views import create_notification

from events.models import Event, EventAttendee
from organizations.models import Organization, OrganizationMember

logger = logging.getLogger(__name__)


def event_callbacks(event):
    callbacks = Callback.event_callbacks(event)
    plain_callbacks = []
    for callback in callbacks:
        plain_callback = callback.plain()
        plain_callbacks.append(plain_callback)
    return plain_callbacks


def talent_callbacks(user, event):
    t_callbacks = CallbackTalent.talent_event_callbacks(user, event)
    plain_callbacks = []
    for callback in t_callbacks:
        plain_callback = callback.plain()
        plain_callbacks.append(plain_callback)
    return plain_callbacks


def organization_callbacks(organization, event):
    o_callbacks = CallbackTalent.organization_event_callbacks(organization, event)
    plain_callbacks = []
    for callback in o_callbacks:
        plain_callback = callback.plain()
        plain_callbacks.append(plain_callback)
    return plain_callbacks


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
            if user_organization == event.owner:
                callbacks = event_callbacks(event)
                serializer = PlainCallbackSerializer(callbacks, many=True)
                logger.debug(serializer.data)
                return Response(serializer.data)
            else:
                my_callbacks = organization_callbacks(user_organization, event)
                serializer = PlainCallbackTalentSerializer(my_callbacks, many=True)
                return Response(serializer.data)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes([IsTalent])
def get_callback_detail(request, event_id, talent_callback_id):
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    if event:
        talent_callback = CallbackTalent.objects.filter(id=talent_callback_id).first()
        if talent_callback:
            if talent_callback.talent.id == user.id:
                plain_callback = talent_callback.plain()
                serializer = PlainCallbackTalentSerializer(plain_callback)
                return Response(serializer.data)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You can only view your own callback"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Callback not found"
        }, status=HTTP_404_NOT_FOUND)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@permission_classes([IsCasting, ])
def add_talent_to_queue(request, event_id=None):
    """
    Used by a casting user to add the talent to event's callback queue.
    He/she needs to be an admin of the organization.
    The organization must be an approved attendee of the event.
    Payload:
    {
        "talent": [talent_id],
        "callback_type": 'RCB/DCB/HCB'
    }
    Notes:
    RCB - Regular Callback
    DCB - Dancer Callback
    HCB - Headshot/Resume Callback
    """
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    if event:
        user_organization = OrganizationMember.user_organization(user)
        if user_organization:
            is_attending = EventAttendee.user_is_already_attending(user, event)
            if is_attending:
                talent_id = request.DATA.get("talent")
                callback_type = request.DATA.get("callback_type")
                if talent_id:
                    talent = User.objects.filter(id=talent_id).first()
                    if talent and talent.my_user.type == 'T':
                        callback_already_sent = CallbackTalent.callback_already_sent(talent, user_organization, event)
                        if not callback_already_sent:
                            callback = Callback.organization_callback(user_organization, event)
                            if not callback:
                                callback = Callback()
                                callback.event = event
                                callback.callback_organization = user_organization
                                callback.save()
                            callback_talent = CallbackTalent()
                            callback_talent.callback = callback
                            callback_talent.talent = talent
                            callback_talent.callback_type = callback_type
                            callback_talent.save()
                            plain_callback_talent = callback_talent.plain()
                            serializer = PlainCallbackTalentSerializer(plain_callback_talent)
                            return Response(serializer.data)
                        return Response({
                            "status": HTTP_400_BAD_REQUEST,
                            "message": "Callback to this talent has already been sent"
                        }, status=HTTP_400_BAD_REQUEST)
                    return Response({
                        "status": HTTP_404_NOT_FOUND,
                        "message": "Talent not found"
                    }, status=HTTP_404_NOT_FOUND)
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "talent-id - This field is required"
                }, status=HTTP_400_BAD_REQUEST)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "Your organization must be an approved attendee of the event in order to send a callback"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You need to be an approved member of some organization to perform this action"
        }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['DELETE', ])
@permission_classes([IsCasting, ])
def remove_talent_from_queue(request, event_id=None, talent_callback_id=None):
    """
    Used by the a casting user to remove a talent from event's callback queue.
    Needs to pass "talent_callback_id"
    Notes:
    Cannot remove it once it's sent to the event.
    """
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    if event:
        user_organization = OrganizationMember.user_organization(user)
        if user_organization:
            is_admin = OrganizationMember.user_is_admin(user_organization, user)
            if is_admin:
                talent_callback = CallbackTalent.objects.filter(id=talent_callback_id).first()
                if talent_callback:
                    if talent_callback.callback.callback_organization == user_organization:
                        if talent_callback.sent_to_event_organization or talent_callback.sent_to_talent:
                            return Response({
                                "status": HTTP_400_BAD_REQUEST,
                                "message": "You cannot delete a callback once it's sent"
                            }, status=HTTP_400_BAD_REQUEST)
                        else:
                            talent_callback.delete()
                            return Response({
                                "status": HTTP_204_NO_CONTENT,
                                "message": "OK"
                            }, status=HTTP_204_NO_CONTENT)
                    return Response({
                        "status": HTTP_401_UNAUTHORIZED
                    }, status=HTTP_401_UNAUTHORIZED)
                return Response({
                    "status": HTTP_404_NOT_FOUND,
                    "message": "Talent callback not found"
                }, status=HTTP_404_NOT_FOUND)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You must be an admin of your organization to be able to delete a callback"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You need to be an approved member of some organization to perform this action"
        }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def send_callbacks_to_event_organization(request, event_id=None):
    """
    Used by casting user to send callbacks to the event on behalf of his/her organization.
    The event will then actually pass these callbacks to the talent.
    He/she needs to be an admin of the organization.
    The organization must be an approved attendee of the event.
    Payload:
    {
        "talent_callbacks": [comma separated talent_callback_id list]
    }
    """
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    str_talent_callbacks = request.DATA.get("talent_callbacks")
    if event:
        user_organization = OrganizationMember.user_organization(user)
        if user_organization:
            is_admin = OrganizationMember.user_is_admin(user_organization, user)
            if is_admin:
                talent_callback_ids = str_talent_callbacks.split(",")
                for talent_callback_id in talent_callback_ids:
                    talent_callback = CallbackTalent.objects.filter(id=talent_callback_id).first()
                    if talent_callback:
                        if talent_callback.callback.callback_organization == user_organization:
                            talent_callback.sent_to_event_organization = True
                            talent_callback.save()
                        else:
                            return Response({
                                "status": HTTP_401_UNAUTHORIZED,
                                "message": "You are not authorized to perform this action"
                            }, status=HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({
                            "status": HTTP_404_NOT_FOUND,
                            "message": "Talent callback not found"
                        }, status=HTTP_404_NOT_FOUND)
                return Response({
                    "status": HTTP_200_OK,
                    "message": "OK"
                }, status=HTTP_200_OK)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You must be an admin of your organization to be able to send callbacks"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You need to be an approved member of some organization to perform this action"
        }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def send_callbacks_to_talent(request, event_id=None):
    """
    NOT for mobiles
    """
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    str_talent_callbacks = request.DATA.get("talent_callbacks")
    if event:
        user_organization = OrganizationMember.user_organization(user)
        if user_organization:
            is_admin = OrganizationMember.user_is_admin(user_organization, user)
            if is_admin and event.owner.id == user_organization.id:
                talent_callback_ids = str_talent_callbacks.split(",")
                for talent_callback_id in talent_callback_ids:
                    talent_callback = CallbackTalent.objects.filter(id=talent_callback_id).first()
                    if talent_callback:
                        if talent_callback.callback.callback_organization == user_organization:
                            talent_callback.sent_to_event_organization = True
                            talent_callback.save()
                            create_notification("CB", talent_callback.id, user, talent_callback.talent.id, message="Callback Request")
                        else:
                            return Response({
                                "status": HTTP_401_UNAUTHORIZED,
                                "message": "You are not authorized to perform this action"
                            }, status=HTTP_401_UNAUTHORIZED)
                    return Response({
                        "status": HTTP_404_NOT_FOUND,
                        "message": "Talent callback not found"
                    }, status=HTTP_404_NOT_FOUND)
                return Response({
                    "status": HTTP_200_OK,
                    "message": "OK"
                }, status=HTTP_200_OK)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You must be an admin of the event's organization to be able to send callbacks to talents on behalf of the casting organization"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You need to be an approved member of some organization to perform this action"
        }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)
