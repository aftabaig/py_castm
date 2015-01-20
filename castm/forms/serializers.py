from rest_framework import serializers
import logging

from organizations.models import Organization
from models import FieldItem, FormField, RatingForm


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
            'title',
            'value',
        )


class FormFieldSerializer(serializers.ModelSerializer):
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
            'items',
        )


class RatingFormSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(many=False, allow_add_remove=False, read_only=True)
    fields = FormFieldSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = RatingForm
        fields = (
            'id',
            'organization',
            'created_at',
            'fields',
        )

