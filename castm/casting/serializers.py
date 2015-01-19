import logging
from rest_framework import serializers
from django.contrib.auth.models import User

from models import CastingProfile
from models import CastingHeadshot
from models import PlainProfile

from notifications.serializers import JSONField

logger = logging.getLogger(__name__)


class PlainProfileSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False, error_messages="")
    last_name = serializers.CharField(required=False)
    sub_type = serializers.CharField(required=False)
    add1 = serializers.CharField(required=False)
    add2 = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    zip = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    office = serializers.CharField(required=False)
    thumbnail = serializers.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        logger.debug(attrs)
        if instance is not None:
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.add1 = attrs.get('add1', instance.add1)
            instance.add2 = attrs.get('add2', instance.add2)
            instance.city = attrs.get('city', instance.city)
            instance.state = attrs.get('state', instance.state)
            instance.zip = attrs.get('zip', instance.zip)
            instance.mobile = attrs.get('mobile', instance.mobile)
            instance.office = attrs.get('office', instance.office)
            if attrs.get('thumbnail'):
                instance.thumbnail = attrs.get('thumbnail', instance.thumbnail)
            return instance
        return PlainProfile(**attrs)

    def save_object(self, obj, **kwargs):
        user = User.objects.get(id=obj.user_id)
        if obj.first_name:
            user.first_name = obj.first_name
        if obj.last_name:
            user.last_name = obj.last_name
        user.save()

        profile = CastingProfile.objects.get(id=obj.profile_id)
        if obj.add1:
            profile.add1 = obj.add1
        if obj.add2:
            profile.add2 = obj.add2
        if obj.city:
            profile.city = obj.city
        if obj.state:
            profile.state = obj.state
        if obj.zip:
            profile.zip = obj.zip
        if obj.mobile:
            profile.mobile = obj.mobile
        if obj.office:
            profile.office = obj.office
        if obj.thumbnail:
            profile.thumbnail = obj.thumbnail
        profile.save()


class MyPlainProfileSerializer(PlainProfileSerializer):
    notifications_count = serializers.CharField(read_only=True)
    links_count = serializers.CharField(read_only=True)
    organization = JSONField(required=False, read_only=True)

    def restore_object(self, attrs, instance=None):
        instance = super(MyPlainProfileSerializer, self).restore_object(attrs, instance)
        if instance is not None:
            instance.notifications_count = attrs.get('notifications_count', instance.notifications_count)
            instance.links_count = attrs.get('links_count', instance.links_count)
            return instance
        return PlainProfile(**attrs)


class HeadshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastingHeadshot
        exclude = (
            'user',
        )