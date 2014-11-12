import logging
from rest_framework import serializers

from models import TalentProfile
from models import ResumeCategory
from models import CategoryJob
from models import CategoryListItem

logger = logging.getLogger(__name__)


class BaseTalentSerializer(serializers.ModelSerializer):
    def restore_object(self, attrs, instance=None):
        if instance is None:
            instance = super(BaseTalentSerializer, self).restore_object(attrs, instance)
            request = self.context.get('request', None)
            profile = TalentProfile.objects.get(user=request.user)
            setattr(instance, "user", request.user)
            setattr(instance, "profile", profile)
        return instance

class CategoryListItemSerializer(BaseTalentSerializer):
    class Meta:
        model = CategoryListItem


class CategoryJobSerializer(BaseTalentSerializer):
    class Meta:
        model = CategoryJob


class ResumeCategorySerializer(BaseTalentSerializer):
    lists = CategoryListItemSerializer(many=True, read_only=True)
    jobs = CategoryJobSerializer(many=True, read_only=True)

    class Meta:
        model = ResumeCategory


class ProfileSerializer(serializers.ModelSerializer):
    categories = ResumeCategorySerializer(many=True, read_only=True)

    class Meta:
        model = TalentProfile
