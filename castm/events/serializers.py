import logging
from rest_framework import serializers


class PlainEventSerializer(serializers.Serializer):
    event_id = serializers.IntegerField(required=False, read_only=True)
    name = serializers.CharField(required=False, read_only=True)
    owner_id = serializers.IntegerField(required=False, read_only=True)
    owner_name = serializers.CharField(required=False, read_only=True)
    owner_logo = serializers.CharField(required=False, read_only=True)
    add1 = serializers.CharField(required=False, read_only=True)
    add2 = serializers.CharField(required=False, read_only=True)
    city = serializers.CharField(required=False, read_only=True)
    state = serializers.CharField(required=False, read_only=True)
    zip = serializers.CharField(required=False, read_only=True)
    audition_start_date = serializers.CharField(required=False, read_only=True)
    audition_end_date = serializers.CharField(required=False, read_only=True)
    audition_time_from = serializers.CharField(required=False, read_only=True)
    audition_time_to = serializers.CharField(required=False, read_only=True)
    callback_start_date = serializers.CharField(required=False, read_only=True)
    callback_end_date = serializers.CharField(required=False, read_only=True)
    callback_time_from = serializers.CharField(required=False, read_only=True)
    callback_time_to = serializers.CharField(required=False, read_only=True)
    my_attending_status = serializers.CharField(required=False, read_only=True)


class PlainAttendeeSerializer(serializers.Serializer):
    attendance_id = serializers.IntegerField(required=False, read_only=True)
    organization_id = serializers.IntegerField(required=False, read_only=True)
    organization_name = serializers.CharField(required=False, read_only=True)
    attendee_audition_id = serializers.CharField(required=False, read_only=True)
    attendee_id = serializers.IntegerField(required=False, read_only=True)
    attendee_first_name = serializers.CharField(required=False, read_only=True)
    attendee_last_name = serializers.CharField(required=False, read_only=True)
    attendee_title = serializers.CharField(required=False, read_only=True)
    attendee_thumbnail_url = serializers.CharField(required=False, read_only=True)
    attendee_profile_url = serializers.CharField(required=False, read_only=True)
    is_accepted = serializers.BooleanField(required=False, read_only=True)
    is_rejected = serializers.BooleanField(required=False, read_only=True)


class PlainTalentEventInfoSerializer(serializers.Serializer):
    audition_id = serializers.CharField(required=False, read_only=True)
    availability_date_start = serializers.DateField(required=False, read_only=True)
    availability_date_end = serializers.DateField(required=False, read_only=True)
    availability_flexible = serializers.BooleanField(required=False, read_only=True)
    hiring_preferences = serializers.CharField(required=False, read_only=True)
