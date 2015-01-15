import logging
from rest_framework import serializers


class PlainCallbackSerializer(serializers.Serializer):
    callback_id = serializers.IntegerField(required=False, read_only=True)
    callback_organization_id = serializers.IntegerField(required=False, read_only=True)
    callback_organization_name = serializers.CharField(required=False, read_only=True)
    callback_organization_logo_url = serializers.CharField(required=False, read_only=True)
    callback_location = serializers.CharField(required=False, read_only=True)
    callback_schedule_date = serializers.DateField(required=False, read_only=True)
    callback_schedule_time_from = serializers.TimeField(required=False, read_only=True)
    callback_schedule_time_to = serializers.TimeField(required=False, read_only=True)
    instructions_by_callback = serializers.CharField(required=False, read_only=True)
    instructions_by_event = serializers.CharField(required=False, read_only=True)
    event_id = serializers.IntegerField(required=False, read_only=True)
    event_name = serializers.CharField(required=False, read_only=True)


class PlainCallbackTalentSerializer(serializers.Serializer):
    talent_callback_id = serializers.IntegerField(required=False, read_only=True)
    callback_id = serializers.IntegerField(required=False, read_only=True)
    callback_organization_id = serializers.IntegerField(required=False, read_only=True)
    callback_organization_name = serializers.CharField(required=False, read_only=True)
    callback_organization_logo_url = serializers.CharField(required=False, read_only=True)
    callback_location = serializers.CharField(required=False, read_only=True)
    callback_schedule_date = serializers.DateField(required=False, read_only=True)
    callback_schedule_time_from = serializers.TimeField(required=False, read_only=True)
    callback_schedule_time_to = serializers.TimeField(required=False, read_only=True)
    instructions_by_callback = serializers.CharField(required=False, read_only=True)
    instructions_by_event = serializers.CharField(required=False, read_only=True)
    talent_id = serializers.IntegerField(required=False, read_only=True)
    talent_first_name = serializers.CharField(required=False, read_only=True)
    talent_last_name = serializers.CharField(required=False, read_only=True)
    talent_title = serializers.CharField(required=False, read_only=True)
    talent_thumbnail_url = serializers.CharField(required=False, read_only=True)
    talent_profile_url = serializers.CharField(required=False, read_only=True)
    event_id = serializers.IntegerField(required=False, read_only=True)
    event_name = serializers.CharField(required=False, read_only=True)