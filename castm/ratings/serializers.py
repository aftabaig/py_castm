from rest_framework import serializers


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


