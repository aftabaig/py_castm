import logging
from rest_framework import serializers

from models import TalentProfile
from models import ResumeCategory
from models import CategoryJob
from models import CategoryListItem

logger = logging.getLogger(__name__)


class BaseTalentSerializer(serializers.ModelSerializer):
    def restore_object(self, attrs, instance=None):
        logger.debug("test")
        logger.debug(attrs)
        if instance is None:
            instance = super(BaseTalentSerializer, self).restore_object(attrs, instance)
            request = self.context.get('request', None)
            logger.debug(request)
            profile = TalentProfile.objects.get(user=request.user)
            setattr(instance, "user", request.user)
            setattr(instance, "profile", profile)
            return instance

    def get_validation_exclusions(self, instance=None):
        logger.debug("validations")
        exclusions = super(BaseTalentSerializer, self).get_validation_exclusions(instance)
        return exclusions + ['user', 'profile', ]


class CategoryListItemSerializer(BaseTalentSerializer):
    class Meta:
        model = CategoryListItem


class CategoryJobSerializer(BaseTalentSerializer):
    class Meta:
        model = CategoryJob


class BulkCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=32)
    order = serializers.IntegerField(required=False, default=0)
    is_list = serializers.BooleanField(required=False)
    is_deleted = serializers.BooleanField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.description = attrs.get('description', instance.description)
            return instance
        return ResumeCategory(**attrs)

    def validate(self, attrs):
        logger.debug("haw hayye")
        return attrs


class ResumeCategorySerializer(BaseTalentSerializer):
    lists = CategoryListItemSerializer(many=True, read_only=True)
    jobs = CategoryJobSerializer(many=True, read_only=True)

    class Meta:
        model = ResumeCategory


class ProfileSerializer(serializers.ModelSerializer):
    categories = ResumeCategorySerializer(many=True, read_only=True)

    class Meta:
        model = TalentProfile
        fields = (
            'stage_first_name',
            'stage_last_name',
            'title',
            'height_feet',
            'height_inches',
            'weight',
            'birth_day',
            'hair_color',
            'eye_color',
            'race',
            'categories',
        )
