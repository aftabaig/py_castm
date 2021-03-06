import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from models import Schedule
from models import ScheduleAttendee
from events.models import Event, EventAttendee
from organizations.models import Organization, OrganizationMember
from django.contrib.auth.models import User

from um.permissions import IsTalentOrCasting, IsCasting
from um.views import error_as_text

from serializers import PlainScheduleSerializer
from serializers import PlainAttendeeSerializer

logger = logging.getLogger(__name__)


def get_schedules(event_id):
    event = Event.objects.filter(id=event_id)
    all_schedules = Schedule.objects.filter(event=event)
    plain_schedules = []
    for schedule in all_schedules:
        plain_schedules.append(schedule.plain())
    return plain_schedules


def delete_schedule(schedule_id):
    schedule = Schedule.objects.filter(id=schedule_id).first()
    schedule.delete()


def delete_schedule_attendance(attendance_id):
    attendance = ScheduleAttendee.objects.filter(id=attendance_id)
    attendance.delete()


@api_view(['GET', 'POST', ])
@permission_classes([IsTalentOrCasting, ])
def get_or_add_schedules(request, event_id=None):
    """
    POST NOT for mobiles
    """
    if request.method == 'GET':
        user = request.user
        event = Event.objects.filter(id=event_id).first()
        if event:
            event_owner = event.owner
            is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
            if not is_event_admin:
                if not event.schedule_published:
                    return Response({
                        "status": HTTP_200_OK,
                        "message": "The general audition schedule is not yet prepared, please check back later"
                    })
            serializer = PlainScheduleSerializer(get_schedules(event_id), many=True)
            return Response(serializer.data)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Event not found"
        }, HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        user = request.user
        event = Event.objects.filter(id=event_id).first()
        if event:
            event_owner = event.owner
            is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
            if is_event_admin:
                serializer = PlainScheduleSerializer(data=request.DATA, context={
                    'event_id': event.id
                })
                if serializer.is_valid():
                    serializer.save()
                    schedule = Schedule.objects.filter(id=serializer.object.schedule_id).first()
                    plain_schedule = schedule.plain()
                    serializer = PlainScheduleSerializer(plain_schedule)
                    return Response(serializer.data)
                return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), HTTP_400_BAD_REQUEST)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to perform this operation"
            }, HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Event not found"
        }, HTTP_404_NOT_FOUND)


@api_view(['GET', ])
@permission_classes([IsCasting, ])
def get_talent_schedule(request, event_id=None, talent_id=None):
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    if event:
        event_owner = event.owner
        is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
        if is_event_admin:
            talent = User.objects.filter(id=talent_id).first()
            if talent:
                if talent.my_user.type == 'T':
                    talent_schedule = ScheduleAttendee.user_schedule(talent, event)
                    talent_schedule_plain = None
                    if talent_schedule:
                        talent_schedule_plain = talent_schedule.plain()
                    serializer = PlainAttendeeSerializer(talent_schedule_plain)
                    return Response(serializer.data)
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "Casting users does not have schedules"
                }, status=HTTP_400_BAD_REQUEST)
            return Response({
                "status": HTTP_404_NOT_FOUND,
                "message": "Talent not found"
            }, status=HTTP_404_NOT_FOUND)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "Only event administrators have the right to view talent's schedule"
        }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE', ])
@permission_classes([IsTalentOrCasting, ])
def update_or_delete_schedule(request, event_id=None, schedule_id=None):
    """
    NOT for mobiles
    """
    if request.method == 'PUT':
        user = request.user
        event = Event.objects.filter(id=event_id).first()
        if event:
            event_owner = event.owner
            is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
            if is_event_admin:
                schedule = Schedule.objects.filter(id=schedule_id).first()
                if schedule.event == event:
                    plain_schedule = schedule.plain()
                    logger.debug(request.DATA)
                    serializer = PlainScheduleSerializer(plain_schedule, data=request.DATA)
                    if serializer.is_valid():
                        serializer.save()
                        # schedule = Schedule.objects.filter(id=serializer.object.schedule_id).first()
                        # plain_schedule = schedule.plain()
                        # serializer = PlainScheduleSerializer(plain_schedule)
                        return Response(serializer.data)
                return Response({
                    "status": HTTP_401_UNAUTHORIZED,
                    "message": "The schedule does not belong to the event"
                }, status=HTTP_401_UNAUTHORIZED)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to perform this operation"
            }, HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Event not found"
        }, HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        user = request.user
        event = Event.objects.filter(id=event_id).first()
        if event:
            event_owner = event.owner
            is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
            if is_event_admin:
                schedule = Schedule.objects.filter(id=schedule_id).first()
                if schedule:
                    if schedule.event == event:
                        delete_schedule(schedule_id)
                        return Response({
                            "status": HTTP_204_NO_CONTENT,
                            "message": "OK"
                        }, HTTP_204_NO_CONTENT)
                    return Response({
                        "status": HTTP_401_UNAUTHORIZED,
                        "message": "The schedule does not belong to the event"
                    }, status=HTTP_401_UNAUTHORIZED)
                return Response({
                    "status": HTTP_404_NOT_FOUND,
                    "message": "Schedule not found"
                }, HTTP_404_NOT_FOUND)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to perform this operation"
            }, HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Event not found"
        }, HTTP_404_NOT_FOUND)


@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def update_schedules_order(request, event_id=None):
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    arr_schedules = request.DATA.get("schedules")
    if event:
        event_owner = event.owner
        is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
        if is_event_admin:
            for dict_schedule in arr_schedules:
                schedule_id = dict_schedule.get("schedule_id")
                sort_id = dict_schedule.get("sort_id")
                schedule = Schedule.objects.filter(id=schedule_id).first()
                if schedule:
                    schedule.sort_id = sort_id
                    schedule.save()
                else:
                    return Response({
                        "status": HTTP_404_NOT_FOUND,
                        "message": "Schedule not found"
                    }, status=HTTP_404_NOT_FOUND)
            serializer = PlainScheduleSerializer(get_schedules(event_id), many=True)
            return Response(serializer.data)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You are not authorized to perform this operation"
        }, HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@permission_classes([IsCasting, ])
def add_attendee(request, event_id=None, schedule_id=None):
    """
    NOT for mobiles
    """
    if request.method == 'POST':
        user = request.user
        event = Event.objects.filter(id=event_id).first()
        if event:
            schedule = Schedule.objects.filter(id=schedule_id).first()
            if schedule:
                event_owner = event.owner
                is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
                if is_event_admin:
                    attendee_id = request.DATA.get("attendee_id")
                    if attendee_id:
                        attendee = User.objects.filter(id=attendee_id).first()
                        if attendee:
                            if attendee.my_user.type == 'T':
                                is_attending = EventAttendee.is_user_attending_event(attendee, event)
                                if is_attending:
                                    current_schedule = ScheduleAttendee.user_schedule(attendee, event)
                                    logger.debug(current_schedule)
                                    if current_schedule:
                                        logger.debug("delettteeddddd")
                                        current_schedule.delete()
                                    attendance = ScheduleAttendee()
                                    attendance.schedule = schedule
                                    attendance.attendee = attendee
                                    attendance.save()
                                    logger.debug("okkkkkkkkkk")
                                    return Response({
                                        "schedule_id": schedule.id,
                                        "attendee_id": attendee.id
                                    })
                                return Response({
                                    "status": HTTP_400_BAD_REQUEST,
                                    "message": "User is not an approved attendee for the event"
                                }, status=HTTP_400_BAD_REQUEST)
                            return Response({
                                "status": HTTP_400_BAD_REQUEST,
                                "message": "Only talent users can be added as an attendee for a schedule"
                            }, status=HTTP_400_BAD_REQUEST)
                        return Response({
                            "status": HTTP_404_NOT_FOUND,
                            "message": "User not found"
                        }, status=HTTP_404_NOT_FOUND)
                    return Response({
                        "status": HTTP_400_BAD_REQUEST,
                        "message": "No Attendee provided"
                    }, status=HTTP_400_BAD_REQUEST)
                return Response({
                    "status": HTTP_401_UNAUTHORIZED,
                    "message": "You are not authorized to perform this operation"
                }, status=HTTP_401_UNAUTHORIZED)
            return Response({
                "status": HTTP_404_NOT_FOUND,
                "message": "Schedule not found"
            }, status=HTTP_404_NOT_FOUND)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Event not found"
        }, HTTP_404_NOT_FOUND)


@api_view(['DELETE', ])
@permission_classes([IsCasting, ])
def delete_attendee(request, event_id=None, schedule_id=None, attendance_id=None):
    """
    NOT for mobiles
    """
    if request.method == 'DELETE':
        user = request.user
        event = Event.objects.filter(id=event_id).first()
        if event:
            event_owner = event.owner
            is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
            if is_event_admin:
                schedule = Schedule.objects.filter(id=schedule_id).first()
                if schedule.event == event:
                    if schedule:
                        schedule_attendance = ScheduleAttendee.objects.filter(id=attendance_id).first()
                        if schedule_attendance:
                            if schedule_attendance.schedule == schedule:
                                delete_schedule_attendance(attendance_id)
                                return Response({
                                    "status": HTTP_204_NO_CONTENT,
                                    "message": "OK"
                                }, HTTP_204_NO_CONTENT)
                            return Response({
                                "status": HTTP_401_UNAUTHORIZED,
                                "message": "Attendee does not belong to this schedule"
                            }, )
                        return Response({
                            "status": HTTP_404_NOT_FOUND,
                            "message": "Schedule Attendance not found"
                        }, status=HTTP_404_NOT_FOUND)
                    return Response({
                        "status": HTTP_404_NOT_FOUND,
                        "message": "Schedule not found"
                    }, status=HTTP_404_NOT_FOUND)
                return Response({
                    "status": HTTP_401_UNAUTHORIZED,
                    "message": "The schedule does not belong to the event"
                }, status=HTTP_401_UNAUTHORIZED)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to perform this operation"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Event not found"
        }, status=HTTP_404_NOT_FOUND)