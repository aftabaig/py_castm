from rest_framework import serializers


class PlainLinkSerializer(serializers.Serializer):
    link_id = serializers.IntegerField(required=False, read_only=True)
    link_type = serializers.CharField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    user_id = serializers.CharField(required=False, read_only=True)
    first_name = serializers.CharField(required=False, read_only=True)
    last_name = serializers.CharField(required=False, read_only=True)
    title = serializers.CharField(required=False, read_only=True)
    thumbnail_url = serializers.CharField(required=False, read_only=True)
    profile_url = serializers.URLField(required=False, read_only=True)
    link_status = serializers.CharField(required=False, read_only=True)


class MyLinksSerializer(serializers.Serializer):
    links = PlainLinkSerializer(many=True, read_only=True)
