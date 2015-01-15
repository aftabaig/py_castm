import logging
from rest_framework import serializers
from notifications.serializers import JSONField

from django.contrib.auth.models import User
from models import Schedule, PlainSchedule
from models import ScheduleAttendee, PlainScheduleAttendee
from events.models import Event


class PlainScheduleSerializer(serializers.Serializer):
    schedule_id = serializers.IntegerField(required=False, read_only=True)
    schedule_title = serializers.CharField(required=False, read_only=True)
    event_id = serializers.IntegerField(required=False, read_only=True)
    event_name = serializers.CharField(required=False, read_only=True)
    schedule_date = serializers.DateField(required=False, read_only=True)
    schedule_time_from = serializers.TimeField(required=False, read_only=True)
    schedule_time_to = serializers.TimeField(required=False, read_only=True)
    attendees = JSONField(required=False, read_only=True)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.schedule_id = attrs.get("schedule_id", instance.schedule_id)
            instance.schedule_title = attrs.get("schedule_title", instance.schedule_title)
            instance.event_id = attrs.get("event_id", instance.event_id)
            instance.event_name = attrs.get("event_name", instance.event_name)
            instance.schedule_date = attrs.get("schedule_date", instance.schedule_date)
            instance.schedule_time_from = attrs.get("schedule_time_from", instance.schedule_time_from)
            instance.schedule_time_to = attrs.get("schedule_time_to", instance.schedule_time_to)
            return instance
        return PlainSchedule(**attrs)

    def save_object(self, obj, **kwargs):
        schedule = Schedule.objects.filter(id=obj.schedule_id)
        if not schedule:
            schedule = Schedule()
        if obj.schedule_title:
            schedule.title = obj.schedule_title
        if obj.event_id:
            schedule.event = Event.objects.filter(id=obj.event_id)
        if obj.schedule_date:
            schedule.schedule_date = obj.schedule_date
        if obj.schedule_time_from:
            schedule.schedule_time_from = obj.schedule_time_from
        if obj.schedule_time_to:
            schedule.schedule_time_from = obj.schedule_time_from
        schedule.save()

        obj.schedule_id = schedule.id


class PlainAttendeeSerializer(serializers.Serializer):
    schedule_id = serializers.IntegerField(required=True)
    attendance_id = serializers.IntegerField(required=True)
    attendee_id = serializers.IntegerField(required=False, read_only=True)
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

