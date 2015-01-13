import logging
from rest_framework import serializers


class PlainEventSerializer(serializers.Serializer):
    event_id = serializers.IntegerField(required=False, read_only=True)
    name = serializers.CharField(required=False, read_only=True)
    owner_id = serializers.IntegerField(required=False, read_only=True)
    owner_name = serializers.CharField(required=False, read_only=True)
    audition_date = serializers.DateField(required=False, read_only=True)
    audition_time_from = serializers.TimeField(required=False, read_only=True)
    audition_time_to = serializers.TimeField(required=False, read_only=True)
    callback_date = serializers.DateField(required=False, read_only=True)
    callback_time_from = serializers.TimeField(required=False, read_only=True)
    callback_time_to = serializers.TimeField(required=False, read_only=True)


class PlainAttendeeSerializer(serializers.Serializer):
    attendance_id = serializers.IntegerField(required=False, read_only=True)
    organization_id = serializers.IntegerField(required=False, read_only=True)
    organization_name = serializers.CharField(required=False, read_only=True)
    attendee_id = serializers.IntegerField(required=False, read_only=True)
    attendee_first_name = serializers.CharField(required=False, read_only=True)
    attendee_last_name = serializers.CharField(required=False, read_only=True)
    attendee_title = serializers.CharField(required=False, read_only=True)
    attendee_thumbnail_url = serializers.CharField(required=False, read_only=True)
    attendee_profile_url = serializers.CharField(required=False, read_only=True)
    is_accepted = serializers.BooleanField(required=False, read_only=True)
    is_rejected = serializers.BooleanField(required=False, read_only=True)