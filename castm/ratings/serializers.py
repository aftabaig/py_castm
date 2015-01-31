from rest_framework import serializers

from models import UserRating, UserRatingField
from forms.models import RatingForm, FormField


class RatingFieldSerializer(serializers.Serializer):
    rating_id = serializers.IntegerField(required=True)
    form_field_id = serializers.IntegerField(required=True)
    form_field_value = serializers.CharField(required=True)

    def from_native(self, data, files=None):
        data['rating_id'] = self.context['rating_id']
        return super(RatingFieldSerializer, self).from_native(data, files)

    def save_object(self, obj, **kwargs):
        rating_field = UserRatingField(rating=obj.rating_id)
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


