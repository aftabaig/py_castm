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
from um.permissions import IsTalent
from um.views import error_as_text

# serializers
from serializers import PlainProfileSerializer
from serializers import MyPlainProfileSerializer
from serializers import HeadshotSerializer

# models
from models import TalentProfile
from models import TalentHeadshot
from models import PlainProfile
from models import Notification

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
            "is_stage_name": false,
            "first_name": "",
            "last_name": "",
            "stage_first_name": "Aftab",
            "stage_last_name": "Baig",
            "title": "",
            "height_feet": 0,
            "height_inches": 0,
            "weight": 0,
            "birth_day": null,
            "hair_color": "",
            "eye_color": "",
            "race": "",
            "personal_add1": "",
            "personal_add2": "",
            "personal_city: "",
            "personal_state: "",
            "personal_zip: "",
            "personal_mobile": "",
            "personal_office": "",
            "personal_email": "",
            "is_agency_contact": "",
            "agency": "",
            "agency_name": "",
            "agency_add1": "",
            "agency_add2": "",
            "agency_city: "",
            "agency_state: "",
            "agency_zip: "",
            "resume_categories": "",
            "thumbnail": "thumbnail_url"
        }\n
    Status:\n
        1. 200 on success
        2. 404 if talent's profile wasn't found.\n
    Notes:\n
        1. This API would be used to view other talent's profile.\n
    """
    user = User.objects.filter(id=user_id).first()
    profile = TalentProfile.objects.filter(user_id=user_id).first()
    if user and profile:
        plain_profile = PlainProfile(user=user, profile=profile)
        serializer = PlainProfileSerializer(plain_profile)
        return Response(serializer.data, HTTP_200_OK)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "User not found",
    }, status=HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', ])
@permission_classes([IsTalent, ])
def my_profile(request):
    """
    View/Update user's own profile.\n
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            {
                "username": "aftab.flash@gmail.com",
                "email": "aftab.flash@gmail.com",
                "is_stage_name": false,
                "first_name": "",
                "last_name": "",
                "stage_first_name": "Aftab",
                "stage_last_name": "Baig",
                "title": "",
                "height": "",
                "weight": "",
                "birth_day": null,
                "hair_color": "",
                "eye_color": "",
                "race": "",
                "personal_add1": "",
                "personal_add2": "",
                "personal_city: "",
                "personal_state: "",
                "personal_zip: "",
                "personal_mobile": "",
                "personal_office": "",
                "personal_email": "",
                "is_agency_contact": "",
                "agency": "",
                "agency_name": "",
                "agency_add1": "",
                "agency_add2": "",
                "agency_city": "",
                "agency_state": "",
                "agency_zip": "",
                "resume_categories": "",
                "thumbnail": "thumbnail_url",
                "notifications_count": 5,
                "links_count": 6
            }\n
        2. PUT to update\n
            - You need to create a dictionary of items (mentioned above) that you need to update.\n
            - You can change any item apart from username, email, notifications_count & links_count.\n
    Status:\n
        1. 200 on success
        2. 400 if some error occurs
        3. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    profile = TalentProfile.objects.get(user_id=user.id)
    notification = Notification.get_notifications(user.id)
    plain_profile = PlainProfile(user=user, profile=profile, notification=notification)
    if request.method == 'GET':
        serializer = MyPlainProfileSerializer(plain_profile)
        return Response(serializer.data, HTTP_200_OK)
    else:
        serializer = MyPlainProfileSerializer(plain_profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, HTTP_200_OK)
        return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), HTTP_400_BAD_REQUEST)



@api_view(['PUT', ])
@permission_classes([IsTalent, ])
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
    profile = TalentProfile.objects.get(user_id=user.id)
    response = cloudinary.uploader.upload(request.FILES['thumbnail'])
    profile.thumbnail = response['url']
    profile.save()
    return Response(HTTP_200_OK)


class HeadshotViewSet(viewsets.ModelViewSet):
    permission_classes = (IsTalent, )
    queryset = TalentHeadshot.objects.all()
    serializer_class = HeadshotSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def pre_save(self, obj):
        response = cloudinary.uploader.upload(self.request.FILES['headshot'])
        obj.headshot = response['url']
        obj.user = self.request.user




