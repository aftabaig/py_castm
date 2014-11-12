import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.relations import  PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from um.permissions import IsTalent

# serializers
from serializers import ProfileSerializer
from serializers import ResumeCategorySerializer

from models import ResumeCategory

# models
from um.models import MyUser
from models import TalentProfile
from models import ResumeCategory

logger = logging.getLogger(__name__)

@api_view(['GET', ])
def public_profile(request, user_id=None):
    """
    View a user's profile publicly
    """
    my_user = MyUser.objects.filter(user_id=user_id).first()
    if my_user:
        profile = TalentProfile.objects.get(my_user_id=my_user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)


class ResumeCategoryView(ListBulkCreateUpdateDestroyAPIView):
    """
    Create/Update resume categories of logged-in user in bulk.
    The app will have to keep a track of new/updated categories.
    1. Create: Send a POST request with an array of categories as payload.

    """
    model = ResumeCategory
    serializer_class = ResumeCategorySerializer
    permission_classes = [IsTalent, ]

    def allow_bulk_destroy(self, qs, filtered):
        return False







