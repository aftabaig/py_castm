import logging
from rest_framework import serializers
from django.contrib.auth.models import User


class PlainNotificationSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField(required=False, read_only=True)
    notification_type = serializers.CharField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    user_id = serializers.IntegerField(required=False, read_only=True)
    first_name = serializers.CharField(required=False, read_only=True)
    last_name = serializers.CharField(required=False, read_only=True)
    title = serializers.CharField(required=False, read_only=True)
    description = serializers.CharField(required=False, read_only=True)
    thumbnail_url = serializers.CharField(required=False, read_only=True)
    profile_url = serializers.URLField(required=False, read_only=True)


class MyNotificationSerializer(serializers.Serializer):
    links = PlainNotificationSerializer(many=True, read_only=True)


