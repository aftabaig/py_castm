import logging
from rest_framework import serializers
from notifications.serializers import JSONField

from django.contrib.auth.models import User
from models import Schedule, PlainSchedule
from models import ScheduleAttendee, PlainScheduleAttendee
from events.models import Event

logger = logging.getLogger(__name__)


class PlainScheduleSerializer(serializers.Serializer):
    schedule_id = serializers.IntegerField(required=False)
    schedule_title = serializers.CharField(required=False)
    event_id = serializers.IntegerField(required=False)
    event_name = serializers.CharField(required=False)
    schedule_date = serializers.DateField(required=False)
    schedule_time_from = serializers.TimeField(required=False)
    schedule_time_to = serializers.TimeField(required=False)
    sort_id = serializers.IntegerField(required=False)
    attendees = JSONField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.schedule_id = attrs.get("schedule_id", instance.schedule_id)
            instance.schedule_title = attrs.get("schedule_title", instance.schedule_title)
            instance.event_id = attrs.get("event_id", instance.event_id)
            instance.event_name = attrs.get("event_name", instance.event_name)
            instance.schedule_date = attrs.get("schedule_date", instance.schedule_date)
            instance.schedule_time_from = attrs.get("schedule_time_from", instance.schedule_time_from)
            instance.schedule_time_to = attrs.get("schedule_time_to", instance.schedule_time_to)
            instance.sort_id = attrs.get("sort_id", instance.sort_id)
            return instance
        return PlainSchedule(**attrs)

    def from_native(self, data, files=None):
        # data['event_id'] = self.context['event_id']
        return super(PlainScheduleSerializer, self).from_native(data, files)

    def save_object(self, obj, **kwargs):
        schedule = Schedule.objects.filter(id=obj.schedule_id).first()
        if not schedule:
            logger.debug("no schedule")
            schedule = Schedule()
        logger.debug(schedule)
        if obj.schedule_title:
            schedule.title = obj.schedule_title
        if obj.event_id:
            schedule.event = Event.objects.filter(id=obj.event_id).first()
        if obj.schedule_date:
            schedule.schedule_date = obj.schedule_date
        if obj.schedule_time_from:
            schedule.schedule_time_from = obj.schedule_time_from
        if obj.schedule_time_to:
            schedule.schedule_time_to = obj.schedule_time_to
        if obj.sort_id:
            schedule.sort_id = obj.sort_id
        logger.debug("event:")
        logger.debug(obj.event_id)
        schedule.save()

        obj.schedule_id = schedule.id


class PlainAttendeeSerializer(serializers.Serializer):
    schedule_id = serializers.IntegerField(required=True)
    attendance_id = serializers.IntegerField(required=True)
    attendee_id = serializers.IntegerField(required=False, read_only=True)
    attendee_audition_id = serializers.IntegerField(required=False, read_only=True)
    attendee_first_name = serializers.CharField(required=False, read_only=True)
    attendee_last_name = serializers.CharField(required=False, read_only=True)
    attendee_title = serializers.CharField(required=False, read_only=True)
    attendee_thumbnail_url = serializers.CharField(required=False, read_only=True)
    attendee_profile_url = serializers.CharField(required=False, read_only=True)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.attendance_id = attrs.get("attendance_id", instance.attendance_id)
            instance.attendee_id = attrs.get("attendee_id", instance.attendee_id)
            instance.attendee_first_name = attrs.get("attendee_first_name", instance.attendee_first_name)
            instance.attendee_last_name = attrs.get("attendee_last_name", instance.attendee_last_name)
            instance.attendee_title = attrs.get("attendee_title", instance.attendee_title)
            instance.attendee_thumbnail_url = attrs.get("attendee_thumbnail_url", instance.attendee_thumbnail_url)
            instance.attendee_profile_url = attrs.get("attendee_profile_url", instance.attendee_profile_url)
            return instance
        return PlainScheduleAttendee(**attrs)

    def save_object(self, obj, **kwargs):
        attendance = ScheduleAttendee()
        if obj.schedule_id:
            attendance.schedule = Schedule.objects.filter(id=obj.schedule_id)
        if obj.attendee_id:
            attendance.attendee = User.objects.filter(id=obj.attendee_id)

