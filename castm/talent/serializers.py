import logging
from rest_framework import serializers
from django.contrib.auth.models import User

from models import TalentProfile
from models import TalentHeadshot
from models import PlainProfile

logger = logging.getLogger(__name__)


class PlainProfileSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False, error_messages="")
    last_name = serializers.CharField(required=False)
    is_stage_name = serializers.BooleanField(required=False)
    stage_first_name = serializers.CharField(required=False)
    stage_last_name = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    height = serializers.CharField(required=False)
    weight = serializers.CharField(required=False)
    birth_day = serializers.CharField(required=False)
    hair_color = serializers.CharField(required=False)
    eye_color = serializers.CharField(required=False)
    race = serializers.CharField(required=False)
    personal_add1 = serializers.CharField(required=False)
    personal_add2 = serializers.CharField(required=False)
    personal_city = serializers.CharField(required=False)
    personal_state = serializers.CharField(required=False)
    personal_zip = serializers.CharField(required=False)
    personal_mobile = serializers.CharField(required=False)
    personal_office = serializers.CharField(required=False)
    personal_email = serializers.CharField(required=False)
    is_agency_contact = serializers.BooleanField(required=False)
    agency = serializers.CharField(required=False)
    agency_name = serializers.CharField(required=False)
    agency_add1 = serializers.CharField(required=False)
    agency_add2 = serializers.CharField(required=False)
    agency_city = serializers.CharField(required=False)
    agency_state = serializers.CharField(required=False)
    agency_zip = serializers.CharField(required=False)
    resume_categories = serializers.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        logger.debug(attrs)
        if instance is not None:
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.is_stage_name = attrs.get('is_stage_name', instance.is_stage_name)
            instance.stage_first_name = attrs.get('stage_first_name', instance.stage_first_name)
            instance.stage_last_name = attrs.get('stage_last_name', instance.stage_last_name)
            instance.title = attrs.get('title', instance.title)
            instance.height = attrs.get('height', instance.height)
            instance.weight = attrs.get('weight', instance.weight)
            instance.birth_day = attrs.get('birth_day', instance.birth_day)
            instance.hair_color = attrs.get('hair_color', instance.hair_color)
            instance.eye_color = attrs.get('eye_color', instance.eye_color)
            instance.race = attrs.get('race', instance.race)
            instance.personal_add1 = attrs.get('personal_add1', instance.personal_add1)
            instance.personal_add2 = attrs.get('personal_add2', instance.personal_add2)
            instance.personal_city = attrs.get('personal_city', instance.personal_city)
            instance.personal_state = attrs.get('personal_state', instance.personal_state)
            instance.personal_zip = attrs.get('personal_zip', instance.personal_zip)
            instance.personal_mobile = attrs.get('personal_mobile', instance.personal_mobile)
            instance.personal_office = attrs.get('personal_office', instance.personal_office)
            instance.personal_email = attrs.get('personal_email', instance.personal_email)
            instance.is_agency_contact = attrs.get('is_agency_contact', instance.is_agency_contact)
            instance.agency = attrs.get('agency', instance.agency)
            instance.agency_name = attrs.get('agency_name', instance.agency_name)
            instance.agency_add1 = attrs.get('agency_add1', instance.agency_add1)
            instance.agency_add2 = attrs.get('agency_add2', instance.agency_add2)
            instance.agency_city = attrs.get('agency_city', instance.agency_city)
            instance.agency_state = attrs.get('agency_state', instance.agency_state)
            instance.agency_zip = attrs.get('agency_zip', instance.agency_zip)
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
        if obj.is_stage_name:
            profile.stage_is_stage_name = obj.is_stage_name
        if obj.stage_first_name:
            profile.stage_first_name = obj.stage_first_name
        if obj.stage_last_name:
            profile.stage_last_name = obj.stage_last_name
        if obj.title:
            profile.title = obj.title
        if obj.height:
            profile.height = obj.height
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
        if obj.personal_add1:
            profile.personal_add1 = obj.personal_add1
        if obj.personal_add2:
            profile.personal_add2 = obj.personal_add2
        if obj.personal_city:
            profile.personal_city = obj.personal_city
        if obj.personal_state:
            profile.personal_state = obj.personal_state
        if obj.personal_zip:
            profile.personal_zip = obj.personal_zip
        if obj.personal_mobile:
            profile.personal_mobile = obj.personal_mobile
        if obj.personal_office:
            profile.personal_office = obj.personal_office
        if obj.personal_email:
            profile.personal_email = obj.personal_email
        if obj.is_agency_contact:
            profile.is_agency_contact = obj.is_agency_contact
        if obj.agency_name:
            profile.agency_name = obj.agency_name
        if obj.agency_add1:
            profile.agency_add1 = obj.agency_add1
        if obj.agency_add2:
            profile.agency_add2 = obj.agency_add2
        if obj.agency_city:
            profile.agency_city = obj.agency_city
        if obj.agency_state:
            profile.agency_state = obj.agency_state
        if obj.agency_zip:
            profile.agency_zip = obj.agency_zip
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


class HeadshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentHeadshot
        exclude = (
            'user',
        )