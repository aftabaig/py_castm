import logging
from rest_framework import serializers
from django.contrib.auth.models import User

from models import Organization
from models import OrganizationMember
from models import PlainOrganization

logger = logging.getLogger(__name__)


class PlainMemberSerializer(serializers.Serializer):
    member_id = serializers.IntegerField(required=False)
    member_role = serializers.CharField(required=False)
    user_id = serializers.IntegerField(required=False)
    user_email_address = serializers.CharField(required=False)
    user_first_name = serializers.CharField(required=False)
    user_last_name = serializers.CharField(required=False)
    user_thumbnail_url = serializers.CharField(required=False)
    user_profile_url = serializers.CharField(required=False)
    initiator_id = serializers.IntegerField(required=False)
    initiator_email_address = serializers.CharField(required=False)
    initiator_first_name = serializers.CharField(required=False)
    initiator_last_name = serializers.CharField(required=False)
    initiator_thumbnail_url = serializers.CharField(required=False)
    initiator_profile_url = serializers.CharField(required=False)
    is_accepted = serializers.BooleanField(required=False)
    is_rejected = serializers.BooleanField(required=False)


class PlainOrganizationSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    add1 = serializers.CharField(required=False)
    add2 = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    zip = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    office = serializers.CharField(required=False)
    logo = serializers.CharField(required=False)
    disable_forms = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    members = PlainMemberSerializer(read_only=True, many=True)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.organization_id = attrs.get('organization_id', instance.organization_id)
            instance.name = attrs.get('name', instance.name)
            instance.add1 = attrs.get('add1', instance.add1)
            instance.add2 = attrs.get('add2', instance.add2)
            instance.city = attrs.get('city', instance.city)
            instance.state = attrs.get('state', instance.state)
            instance.zip = attrs.get('zip', instance.zip)
            instance.mobile = attrs.get('mobile', instance.mobile)
            instance.office = attrs.get('office', instance.office)
            if attrs.get('logo'):
                instance.logo = attrs.get('logo', instance.logo)
            instance.disable_forms
            return instance
        return PlainOrganization(**attrs)

    def save_object(self, obj, **kwargs):
        org = Organization.objects.filter(id=obj.organization_id).first()
        if not org:
            org = Organization()
        if obj.name:
            org.name = obj.name
        if obj.add1:
            org.add1 = obj.add1
        if obj.add2:
            org.add2 = obj.add2
        if obj.city:
            org.city = obj.city
        if obj.state:
            org.state = obj.state
        if obj.zip:
            org.zip = obj.zip
        if obj.mobile:
            org.mobile = obj.mobile
        if obj.office:
            org.office = obj.office
        org.save()

        obj.organization_id = org.id
        obj.created_at = org.created_at

        obj.members = []
        for member in org.members.all():
            obj.members.append(member.plain())
