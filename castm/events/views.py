import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting
from um.views import error_as_text

from serializers import PlainEventSerializer
from serializers import PlainAttendeeSerializer
from serializers import PlainTalentEventInfoSerializer

from models import Event, PlainEvent
from models import EventAttendee, PlainAttendee
from models import EventTalentInfo, PlainEventTalentInfo

from talent.models import TalentProfile
from casting.models import CastingProfile
from organizations.models import Organization
from organizations.models import OrganizationMember
from notifications.views import create_notification

logger = logging.getLogger(__name__)


def all_events(organization=None, user=None):
    """
    Get all events.
    :return: List of plain events.
    """
    events = None
    if organization:
        events = Event.objects.filter(owner=organization)
    else:
        events = Event.objects.all()
    plain_events = []
    for event in events:
        plain_event = event.plain()
        if user:
            my_attending_status = EventAttendee.attendance_status(user, event)
            plain_event.my_attending_status = my_attending_status
        plain_events.append(plain_event)
    return plain_events


def talent_attending_events(user):
    events = Event.talent_events(user)
    plain_events = []
    for event in events:
        plain_event = event.plain()
        my_attending_status = EventAttendee.attendance_status(user, event)
        plain_event.my_attending_status = my_attending_status
        plain_events.append(plain_event)
    return plain_events


def casting_attending_events(user):
    events = Event.casting_events(user)
    plain_events = []
    for event in events:
        plain_event = event.plain()
        my_attending_status = EventAttendee.attendance_status(user, event)
        plain_event.my_attending_status = my_attending_status
        plain_events.append(plain_event)
    return plain_events


def get_event(event_id):
    """
    Returns detail of an event
    :param event_id: id of the event
    :return: A plain event
    """
    event = Event.objects.filter(id=event_id).first()
    return event.plain()


def process_attendance_request(request, event_id=None, request_id=None, accept=True):
    """
    Accepts/Rejects a membership request.
    :param request: an HTTP request
    :param event_id: organization of the request
    :param request_id: id of membership request
    :param accept: accept/reject
    :return: Response with success/failure
    """
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    attend_request = EventAttendee.objects.filter(id=request_id).first()
    if event:
        organization = event.owner
        if attend_request:
            if OrganizationMember.user_is_admin(organization, user):
                if attend_request.is_new():
                    message = ""
                    n_type = "ERA"
                    if accept:
                        attend_request.is_accepted = True
                        message = "Your attendance request has been accepted"
                    else:
                        attend_request.is_rejected = True
                        n_type = "ERR"
                        message = "Your attendance request has been rejected"
                    attend_request.save()
                    plain_request = attend_request.plain()
                    serializer = PlainAttendeeSerializer(plain_request)
                    create_notification(n_type, plain_request.attendance_id, user, attend_request.attendee, message=message)
                    return Response(serializer.data)
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "The request to attend by this user has already been accepted/rejected"
                }, status=HTTP_400_BAD_REQUEST)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to accept/reject this membership request"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "User request not found"
        }, status=HTTP_404_NOT_FOUND)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def get_events(request):
    user = request.user
    events = all_events(user=user)
    serializer = PlainEventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsCasting, ])
def my_events(request):
    """
    NOT for mobiles
    """
    user = request.user
    organization = OrganizationMember.user_organization(user)
    if organization:
        events = all_events(organization=organization, user=user)
        serializer = PlainEventSerializer(events, many=True)
        return Response(serializer.data)
    return Response({
        "status": HTTP_400_BAD_REQUEST,
        "message": "You don't have any associated organization"
    }, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def user_attending_events(request):
    user = request.user
    if user.my_user.type == 'T':
        events = talent_attending_events(user)
    else:
        events = []
        #events = casting_attending_events(user)
    serializer = PlainEventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def get_event(request, event_id=None):
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    if event:
        plain_event = event.plain()
        my_attending_status = EventAttendee.attendance_status(user, event)
        plain_event.my_attending_status = my_attending_status
        serializer = PlainEventSerializer(plain_event)
        return Response(serializer.data)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def all_talent_attendees(request, event_id=None):
    event = Event.objects.filter(id=event_id)
    all_attendees = EventAttendee.all_attendees(event)
    plain_attendees = []
    for attendee in all_attendees:
        plain_attendee = attendee.plain()
        plain_attendees.append(plain_attendee)
    serializer = PlainAttendeeSerializer(plain_attendees, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def qualified_talent_attendees(request, event_id=None):
    event = Event.objects.filter(id=event_id)
    all_attendees = EventAttendee.qualified_attendees(event)
    plain_attendees = []
    for attendee in all_attendees:
        plain_attendee = attendee.plain()
        plain_attendees.append(plain_attendee)
    serializer = PlainAttendeeSerializer(plain_attendees, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def pending_talent_attendees(request, event_id=None):
    event = Event.objects.filter(id=event_id)
    all_attendees = EventAttendee.pending_attendees(event)
    plain_attendees = []
    for attendee in all_attendees:
        plain_attendee = attendee.plain()
        plain_attendees.append(plain_attendee)
    serializer = PlainAttendeeSerializer(plain_attendees, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsCasting, ])
def all_casting_attendees(request, event_id=None):
    """
    NOT for mobiles
    """
    event = Event.objects.filter(id=event_id)
    all_attendees = EventAttendee.all_attendees(event, talents=False)
    plain_attendees = []
    for attendee in all_attendees:
        logger.debug(attendee.attendee.id)
        plain_attendee = attendee.plain()
        plain_attendees.append(plain_attendee)
    serializer = PlainAttendeeSerializer(plain_attendees, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsCasting, ])
def qualified_casting_attendees(request, event_id=None):
    """
    NOT for mobiles
    """
    event = Event.objects.filter(id=event_id)
    all_attendees = EventAttendee.qualified_attendees(event, talents=False)
    logger.debug("23")
    plain_attendees = []
    for attendee in all_attendees:
        plain_attendee = attendee.plain()
        plain_attendees.append(plain_attendee)
    serializer = PlainAttendeeSerializer(plain_attendees, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsCasting, ])
def pending_casting_attendees(request, event_id=None):
    """
    NOT for mobiles
    """
    event = Event.objects.filter(id=event_id)
    all_attendees = EventAttendee.pending_attendees(event, talents=False)
    plain_attendees = []
    for attendee in all_attendees:
        plain_attendee = attendee.plain()
        plain_attendees.append(plain_attendee)
    serializer = PlainAttendeeSerializer(plain_attendees, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def request_attendance(request, event_id=None):
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    event_organization = event.owner
    if event:
        if user.my_user.type == 'C':
            user_organization = OrganizationMember.user_organization(user)
            if user_organization is None:
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "You must be associated with your organization to attend this event"
                }, HTTP_400_BAD_REQUEST)
            elif user_organization.id == event_organization.id:
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "You are the organizer of this event and don't need to link to the event"
                }, HTTP_400_BAD_REQUEST)
        if not EventAttendee.user_is_already_attending(user, event):
            attendance = EventAttendee()
            attendance.event = event
            if user.my_user.type == 'C':
                attendance.organization = user_organization
            else:
                attendance.organization = None
            attendance.attendee = user
            attendance.save()
            plain_attendance = attendance.plain()
            serializer = PlainAttendeeSerializer(plain_attendance)
            message = "%s %s has requested to attend %s" % (user.first_name, user.last_name, event.name, )
            for admin in event_organization.administrators():
                logger.debug(admin.user.first_name)
                create_notification("ER", attendance.id, attendance.attendee, admin.user, message=message)
            return Response(serializer.data)
        return Response({
            "status": HTTP_400_BAD_REQUEST,
            "message": "You are already attending/awaiting approval of this event"
        }, status=HTTP_400_BAD_REQUEST)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def accept_request(request, event_id=None, request_id=None):
    """
    NOT for mobiles
    """
    return process_attendance_request(request, event_id, request_id)


@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def reject_request(request, event_id=None, request_id=None):
    """
    NOT for mobiles
    """
    return process_attendance_request(request, event_id, request_id, accept=False)


@api_view(['GET', 'PUT', ])
@permission_classes([IsTalentOrCasting, ])
def talent_event_info(request, event_id=None, talent_id=None):
    user = User.objects.filter(id=talent_id).first()
    event = Event.objects.filter(id=event_id).first()
    if event:
        if user:
            if user.my_user.type == 'T':
                talent_info = EventTalentInfo.get_talent_info(event, user)
                if talent_info:
                    plain_info = talent_info.plain()
                    if request.method == 'PUT':
                        audition_id = request.DATA.get("audition_id")
                        if audition_id:
                            talent_info.audition_id = audition_id
                            talent_info.save()
                        else:
                            return Response({
                                "status": HTTP_400_BAD_REQUEST,
                                "message": "Audition # is required"
                            }, status=HTTP_400_BAD_REQUEST)
                    serializer = PlainTalentEventInfoSerializer(plain_info)
                    return Response(serializer.data)
                return Response({
                    "status": HTTP_404_NOT_FOUND,
                    "message": "No information given"
                }, status=HTTP_404_NOT_FOUND)
            return Response({
                "status": HTTP_404_NOT_FOUND,
                "message": "Talent not found"
            }, status=HTTP_404_NOT_FOUND)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Talent not found"
        }, status=HTTP_404_NOT_FOUND)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)
