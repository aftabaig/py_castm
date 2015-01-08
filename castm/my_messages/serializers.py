from rest_framework import serializers


class PlainMessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    user_id = serializers.CharField(required=False, read_only=True)
    first_name = serializers.CharField(required=False, read_only=True)
    last_name = serializers.CharField(required=False, read_only=True)
    message = serializers.CharField(required=False, read_only=True)
    thumbnail_url = serializers.CharField(required=False, read_only=True)
    profile_url = serializers.URLField(required=False, read_only=True)


class MyMessagesSerializer(serializers.Serializer):
    links = PlainMessageSerializer(many=True, read_only=True)

