import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from models import Schedule
from models import ScheduleAttendee
from events.models import Event
from organizations.models import Organization, OrganizationMember

from um.permissions import IsTalentOrCasting, IsCasting

from serializers import PlainScheduleSerializer
from serializers import PlainAttendeeSerializer


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
                serializer = PlainScheduleSerializer(data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to perform this operation"
            }, HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Event not found"
        }, HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE', ])
@permission_classes([IsTalentOrCasting, ])
def update_or_delete_schedule(request, event_id=None, schedule_id=None):
    if request.method == 'PUT':
        user = request.user
        event = Event.objects.filter(id=event_id).first()
        if event:
            event_owner = event.owner
            is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
            if is_event_admin:
                schedule = Schedule.objects.filter(id=schedule_id).first()
                plain_schedule = schedule.plain()
                serializer = PlainScheduleSerializer(plain_schedule, data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
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
                    delete_schedule(schedule_id)
                    return Response({
                        "status": HTTP_204_NO_CONTENT,
                        "message": "OK"
                    }, HTTP_204_NO_CONTENT)
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


@api_view(['POST', ])
@permission_classes([IsCasting, ])
def add_attendee(request, event_id=None, schedule_id=None, attendance_id=None):
    if request.method == 'POST':
        user = request.user
        event = Event.objects.filter(id=event_id).first()
        if event:
            event_owner = event.owner
            is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
            if is_event_admin:
                serializer = PlainAttendeeSerializer(data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to perform this operation"
            }, HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Event not found"
        }, HTTP_404_NOT_FOUND)


@api_view(['DELETE', ])
@permission_classes([IsCasting, ])
def delete_attendee(request, event_id=None, schedule_id=None, attendance_id=None):
    if request.method == 'DELETE':
        user = request.user
        event = Event.objects.filter(id=event_id).first()
        if event:
            event_owner = event.owner
            is_event_admin = OrganizationMember.user_is_admin(event_owner, user)
            if is_event_admin:
                schedule = Schedule.objects.filter(id=schedule_id).first()
                if schedule:
                    schedule_attendance = ScheduleAttendee.objects.filter(id=attendance_id)
                    if schedule_attendance:
                        delete_schedule_attendance(attendance_id)
                        return Response({
                            "status": HTTP_204_NO_CONTENT,
                            "message": "OK"
                        }, HTTP_204_NO_CONTENT)
                    return Response({
                        "status": HTTP_404_NOT_FOUND,
                        "message": "Schedule Attendance not found"
                    }, HTTP_404_NOT_FOUND)
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