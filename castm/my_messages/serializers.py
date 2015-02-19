from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer


class PlainMessageSerializer(serializers.Serializer):
    msg_id = serializers.IntegerField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    message = serializers.CharField(required=False, read_only=True)
    from_user_id = serializers.CharField(required=False, read_only=True)
    from_first_name = serializers.CharField(required=False, read_only=True)
    from_last_name = serializers.CharField(required=False, read_only=True)
    from_title = serializers.CharField(required=False, read_only=True)
    from_thumbnail_url = serializers.CharField(required=False, read_only=True)
    from_profile_url = serializers.URLField(required=False, read_only=True)
    to_user_id = serializers.CharField(required=False, read_only=True)
    to_first_name = serializers.CharField(required=False, read_only=True)
    to_last_name = serializers.CharField(required=False, read_only=True)
    to_title = serializers.CharField(required=False, read_only=True)
    to_thumbnail_url = serializers.CharField(required=False, read_only=True)
    to_profile_url = serializers.URLField(required=False, read_only=True)


class PaginatedMessageSerializer(PaginationSerializer):
    class Meta:
        object_serializer_class = PlainMessageSerializer


class MyMessagesSerializer(serializers.Serializer):
    links = PlainMessageSerializer(many=True, read_only=True)

