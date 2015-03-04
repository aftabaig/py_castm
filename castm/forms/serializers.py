from rest_framework import serializers
import logging

from notifications.serializers import JSONField
from organizations.models import Organization
from models import FieldItem, FormField, RatingForm


class PlainFormFieldSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField(required=False, read_only=True)
    form_id = serializers.IntegerField(required=False, read_only=True)
    form_type = serializers.CharField(required=False, read_only=True)
    title = serializers.CharField(required=False, read_only=True)
    max_value = serializers.IntegerField(required=False, read_only=True)
    use_stars = serializers.BooleanField(required=False, read_only=True)
    sort_id = serializers.IntegerField(required=False)
    items = JSONField(required=False, read_only=True)

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'name',
        )


class FieldItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldItem
        fields = (
            'id',
            'title',
            'value',
        )


class RatingFormSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(many=False, allow_add_remove=False, read_only=True)

    class Meta:
        model = RatingForm
        fields = (
            'id',
            'organization',
            'created_at',
        )


class FormFieldSerializer(serializers.ModelSerializer):
    form = RatingFormSerializer()
    items = FieldItemSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = FormField
        fields = (
            'id',
            'form',
            'type',
            'title',
            'max_value',
            'use_stars',
            'sort_id',
            'items',
        )
