import logging
from rest_framework import serializers
from django.contrib.auth.models import User

from models import Link
from models import Message

class PlainLinkSerializer(serializers.Serializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    profile_url = serializers.URLField(read_only=True)


class MyLinksSerializer(serializers.Serializer):
    talent_links = PlainLinkSerializer(many=True, read_only=True)
    casting_links = PlainLinkSerializer(many=True, read_only=True)


class PlainMessageSerializer(serializers.Serializer):
    pass


class NotificationSerializer(serializers.Serializer):
    pass

