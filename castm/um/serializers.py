from rest_framework import serializers
from django.contrib.auth.models import User
import logging
# models
from models import MyUser

logger = logging.getLogger(__name__)


# default django-user serializer.
class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class BasicInfoSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True, required=False)
    email = serializers.EmailField(read_only=True, required=False)
    first_name = serializers.CharField(read_only=True, required=False)
    last_name = serializers.CharField(read_only=True, required=False)


# cast'm user serializer.
class UserSerializer(serializers.ModelSerializer):
    user = AuthUserSerializer()

    class Meta:
        model = MyUser
        fields = (
            'id',
            'type',
            'sub_type',
            'user'
        )
