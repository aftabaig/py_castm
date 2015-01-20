import logging
import cloudinary
import cloudinary.uploader
import cloudinary.api

# rest_framework
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User

# um
from um.permissions import IsCasting
from um.views import error_as_text

# serializers
from serializers import PlainProfileSerializer
from serializers import MyPlainProfileSerializer
from serializers import HeadshotSerializer

# models
from models import CastingProfile
from models import CastingHeadshot
from models import PlainProfile
from notifications.models import NotificationSummary
from organizations.models import Organization
from organizations.models import OrganizationMember

logger = logging.getLogger(__name__)

@api_view(['GET', ])
def public_profile(request, user_id=None):
    """
    View a user's profile publicly.\n
    Allowed HTTP methods are:\n
        1. GET to view\n
        Returns:\n
        {
            "username": "aftab.flash@gmail.com",
            "email": "aftab.flash@gmail.com",
            "first_name": "",
            "last_name": "",
            "add1": "",
            "add2": "",
            "city: "",
            "state: "",
            "zip: "",
            "mobile": "",
            "office": "",
            "thumbnail": "thumbnail_url"
        }\n
    Status:\n
        1. 200 on success
        2. 404 if talent's profile wasn't found.\n
    Notes:\n
        1. This API would be used to view other talent's profile.\n
    """
    user = User.objects.filter(id=user_id).first()
    profile = CastingProfile.objects.filter(user_id=user_id).first()
    if user and profile:
        plain_profile = PlainProfile(user=user, profile=profile)
        serializer = PlainProfileSerializer(plain_profile)
        return Response(serializer.data, HTTP_200_OK)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "User not found",
    }, status=HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', ])
@permission_classes([IsCasting, ])
def my_profile(request):
    """
    View/Update user's own profile.\n
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            {
                "username": "aftab.flash@gmail.com",
                "email": "aftab.flash@gmail.com",
                "first_name": "",
                "last_name": "",
                "add1": "",
                "add2": "",
                "city: "",
                "state: "",
                "zip: "",
                "mobile": "",
                "office": "",
                "thumbnail": "thumbnail_url",
                "organization_id": 6,
                "organization_name": [organization_name],
                "notifications_count": 5,
                "links_count": 6
            }\n
        2. PUT to update\n
            - You need to create a dictionary of items (mentioned above) that you need to update.\n
            - You can change any item apart from username, email, organization_id, organization_name, notifications_count & links_count.\n
    Status:\n
        1. 200 on success
        2. 400 if some error occurs
        3. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    profile = CastingProfile.objects.filter(user_id=user.id).first()
    if profile:

        notification = NotificationSummary.get_notifications(user.id)
        organization = OrganizationMember.user_organization(user)
        invitation = OrganizationMember.user_invitation(user)

        if organization:
            organization = organization.plain()
        if invitation:
            invitation = invitation.plain()

        plain_profile = PlainProfile(user=user,
                                     profile=profile,
                                     notification=notification,
                                     organization=organization,
                                     invitation=invitation)
        if request.method == 'GET':
            serializer = MyPlainProfileSerializer(plain_profile)
            return Response(serializer.data, HTTP_200_OK)
        else:
            serializer = MyPlainProfileSerializer(plain_profile, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, HTTP_200_OK)
            return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), HTTP_400_BAD_REQUEST)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "User not found"
    }, HTTP_404_NOT_FOUND)



@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def upload_thumbnail(request):
    """
    Upload user's thumbnail
    Allowed HTTP methods are:\n
        1. PUT to view\n
            Returns:\n
            "An empty string"
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
        2. The Content-Type header should be set as "multipart/form-data"\n
        3. Both key/filename should be "thumbnail"
    """
    user = request.user
    profile = CastingProfile.objects.get(user_id=user.id)
    response = cloudinary.uploader.upload(request.FILES['thumbnail'])
    profile.thumbnail = response['url']
    profile.save()
    return Response({
        "thumbnail_url": profile.thumbnail
    })


class HeadshotViewSet(viewsets.ModelViewSet):
    permission_classes = (IsCasting, )
    queryset = CastingHeadshot.objects.all()
    serializer_class = HeadshotSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def pre_save(self, obj):
        response = cloudinary.uploader.upload(self.request.FILES['headshot'])
        obj.headshot = response['url']
        obj.user = self.request.user




