import logging
from rest_framework import serializers
from django.contrib.auth.models import User

from models import Message


class PlainMessageSerializer(serializers.Serializer):
    pass


class NotificationSerializer(serializers.Serializer):
    pass

