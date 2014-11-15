import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.relations import  PrimaryKeyRelatedField
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from um.permissions import IsTalent

# serializers
from serializers import ProfileSerializer
from serializers import ResumeCategorySerializer
from serializers import BulkCategorySerializer

from models import ResumeCategory

# models
from um.models import MyUser
from models import TalentProfile
from models import ResumeCategory

logger = logging.getLogger(__name__)

@api_view(['GET', ])
def public_profile(request, user_id=None):
    """
    View a user's profile publicly.\n
    Allowed HTTP methods are:\n
    1. GET to view\n
    Returns:\n
    1. 200 on success
    2. 404 if talent's profile wasn't found.\n
    Notes:\n
    1. This API would be used to view other talent's profile.\n
    """
    my_user = MyUser.objects.filter(user_id=user_id).first()
    if my_user:
        profile = TalentProfile.objects.get(my_user_id=my_user.id)
        logger.debug("profile")
        logger.debug(profile)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', ])
@permission_classes([IsTalent, ])
def my_profile(request):
    """
    View/Update user's own profile.\n
    Allowed HTTP methods are:\n
    1. GET to view\n
    2. PUT to update.\n
    Returns:\n
    1. 200 on success\n
    2. 400 if some error occurs\n
    Notes:\n
    1. Require user's token to be sent in the header as:\n
        Authorization: Token [token]\n
    2. This API won't update user's categories and jobs/lists.\n
        Separate APIs would be available to update categories and jobs/lists.
    """
    profile = TalentProfile.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        logger.debug("profile")
        logger.debug(profile)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, HTTP_200_OK)
    else:
        serializer = ProfileSerializer(profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def resume_categories(request):
    serializer = BulkCategorySerializer(data=request.DATA, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_200_OK)


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







