import logging

from rest_framework import serializers

from models import UserRating, UserRatingField, PlainUserRatingField
from forms.models import RatingForm, FormField

logger = logging.getLogger(__name__)


class RatingFieldSerializer(serializers.Serializer):
    rating_id = serializers.IntegerField(required=True)
    form_field_id = serializers.IntegerField(required=True)
    form_field_value = serializers.CharField(required=True)

    def from_native(self, data, files=None):
        data['rating_id'] = self.context['rating_id']
        return super(RatingFieldSerializer, self).from_native(data, files)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.form_field_id = attrs.get("form_field_id", instance.schedule_id)
            instance.form_field_value = attrs.get("form_field_value", instance.schedule_title)
            return instance
        return PlainUserRatingField(**attrs)

    def save_object(self, obj, **kwargs):
        rating = UserRating.objects.filter(id=self.context['rating_id']).first()
        rating_field = UserRatingField(rating=rating)
        rating_field.form_field = FormField.objects.filter(id=obj.form_field_id).first()
        rating_field.field_value = obj.form_field_value
        rating_field.save()


class UserAverageRatingSerializer(serializers.Serializer):
    # talent info
    talent_id = serializers.CharField(required=False, read_only=True)
    talent_first_name = serializers.CharField(required=False, read_only=True)
    talent_last_name = serializers.CharField(required=False, read_only=True)
    talent_thumbnail_url = serializers.CharField(required=False, read_only=True)
    talent_profile_url = serializers.CharField(required=False, read_only=True)
    # event info
    event_id = serializers.CharField(required=False, read_only=True)
    event_name = serializers.CharField(required=False, read_only=True)


