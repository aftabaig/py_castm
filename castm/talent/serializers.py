import logging
from rest_framework import serializers
from django.contrib.auth.models import User

from models import TalentProfile
from models import PlainProfile

logger = logging.getLogger(__name__)


class PlainProfileSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    stage_first_name = serializers.CharField(required=False)
    stage_last_name = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    height_feet = serializers.IntegerField(required=False)
    height_inches = serializers.IntegerField(required=False)
    weight = serializers.CharField(required=False)
    birth_day = serializers.CharField(required=False)
    hair_color = serializers.CharField(required=False)
    eye_color = serializers.CharField(required=False)
    race = serializers.CharField(required=False)
    resume_categories = serializers.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        logger.debug(attrs)
        if instance is not None:
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.stage_first_name = attrs.get('stage_first_name', instance.stage_first_name)
            instance.stage_last_name = attrs.get('stage_last_name', instance.stage_last_name)
            instance.title = attrs.get('title', instance.title)
            instance.height_feet = attrs.get('height_feet', instance.height_feet)
            instance.height_inches = attrs.get('height_inches', instance.height_inches)
            instance.weight = attrs.get('weight', instance.weight)
            instance.birth_day = attrs.get('birth_day', instance.birth_day)
            instance.hair_color = attrs.get('hair_color', instance.hair_color)
            instance.eye_color = attrs.get('eye_color', instance.eye_color)
            instance.race = attrs.get('race', instance.race)
            instance.resume_categories = attrs.get('resume_categories', instance.resume_categories)
            return instance
        return PlainProfile(**attrs)

    def save_object(self, obj, **kwargs):
        user = User.objects.get(id=obj.user_id)
        if obj.first_name:
            user.first_name = obj.first_name
        if obj.last_name:
            user.last_name = obj.last_name
        user.save()

        profile = TalentProfile.objects.get(id=obj.profile_id)
        if obj.stage_first_name:
            profile.stage_first_name = obj.stage_first_name
        if obj.stage_last_name:
            profile.stage_last_name = obj.stage_last_name
        if obj.title:
            profile.title = obj.title
        if obj.height_feet:
            profile.height_feet = obj.height_feet
        if obj.height_inches:
            profile.height_inches = obj.height_inches
        if obj.weight:
            profile.weight = obj.weight
        if obj.birth_day:
            profile.birth_day = obj.birth_day
        if obj.hair_color:
            profile.hair_color = obj.hair_color
        if obj.eye_color:
            profile.eye_color = obj.eye_color
        if obj.race:
            profile.race = obj.race
        if obj.resume_categories:
            profile.resume_categories = obj.resume_categories
        profile.save()


class MyPlainProfileSerializer(PlainProfileSerializer):
    notifications_count = serializers.CharField(read_only=True)
    links_count = serializers.CharField(read_only=True)

    def restore_object(self, attrs, instance=None):
        instance = super(MyPlainProfileSerializer, self).restore_object(attrs, instance)
        if instance is not None:
            instance.notifications_count = attrs.get('notifications_count', instance.notifications_count)
            instance.links_count = attrs.get('links_count', instance.links_count)
            return instance
        return PlainProfile(**attrs)