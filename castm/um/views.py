
import logging

from rest_framework.authtoken.models import Token

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_200_OK

# serializers
from serializers import UserSerializer

from permissions import IsTalent

# django
from django.contrib.auth.models import User
from django.core.mail import send_mail

from talent.models import TalentProfile

logger = logging.getLogger(__name__)

@api_view(['POST', ])
def sign_up(request):

    # create serializer from request-data.
    serializer = UserSerializer(data=request.DATA)
    if serializer.is_valid():

        # saves user data (in both auth-user and my-user models.
        serializer.save()

        # get auth-user model from the serializer.
        # get password from request-data.
        # set password on the model and save.
        user = serializer.object.user
        password = request.DATA.get("user").get("password")
        user.set_password(password)
        user.save()

        # create token for the user
        Token.objects.create(user=user)

        # create an empty talent-profile.
        if serializer.object.type == 'T':
            talent = TalentProfile(my_user=serializer.object, user=user)
            talent.save()

        return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes([IsTalent, ])
def change_password(request):
    current_password = request.DATA.get("current_password")
    new_password = request.DATA.get("new_password")
    if request.user:
        if request.user.check_password(current_password):
            request.user.set_password(new_password)
            request.user.save()
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
    return Response(status=HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def forgot_password(request):
    email_address = request.DATA.get("email_address")
    if email_address:
        user = User.objects.get(username=email_address)
        if user:
            # create and save a random password.
            password = User.objects.make_random_password(length=16)
            user.set_password(password)
            user.save()
            # create and send email.
            subject = 'Your Cast\'M password'
            message = 'Your new password is <strong>%s</strong>' % (password, )
            message += '<br/>You can change it from right within your app'
            send_mail(subject, 'Message', 'info@castm.com', (email_address, ), html_message=message)
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
    return Response(status=HTTP_400_BAD_REQUEST)

