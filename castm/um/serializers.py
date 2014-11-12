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
