
import logging

from rest_framework.authtoken.models import Token

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

# django
from django.contrib.auth.models import User
from django.core.mail import send_mail

# models
from models import MyUser
from talent.models import TalentProfile

# serializers
from serializers import UserSerializer



# permissions
from permissions import IsTalent

logger = logging.getLogger(__name__)

# returns error as plain text.
# TODO: This is only 2 level deep.
# To dig deep, we might need a recursive method.
def error_as_text(errors, status):
    keys = errors.keys()
    error = errors[keys[0]]
    first_error = error[0]
    if type(first_error) is unicode:
        if keys[0] == "non_field_errors":
            message = first_error
        else:
            message = keys[0] + ' - ' + first_error
        return {
            "status": status,
            "message": message
        }
    else:
        keys = first_error.keys()
        error = first_error[keys[0]]
        first_error = error[0]
        if keys[0] == "non_field_errors":
            message = first_error
        else:
            message = keys[0] + ' - ' + first_error
        return {
            "status": status,
            "message": message
        }

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
        return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), status=HTTP_400_BAD_REQUEST)



@api_view(['POST', ])
def authenticate(request):
    """
    Authenticates user with username/password.\n
    HTTP Method:\n
        POST\n
    Accepts:\n
        {
            "username": "abc@gmail.com",
            "password": "abc123"
        }\n
    Returns:\n
        {
            "token": "b95175a8e01d3ac718d12669f1ca8ddd37bf6f3d",
            "type": 'S',
            "sub_type": ''
        }\n
    """
    serializer = AuthTokenSerializer(data=request.DATA)
    if serializer.is_valid():
        token, created = Token.objects.get_or_create(user=serializer.object['user'])
        my_user = MyUser.objects.filter(user=serializer.object['user']).first()
        type = None
        sub_type = None
        if my_user:
            type = my_user.type
            sub_type = my_user.sub_type
        response = {
            'token': token.key,
            'type': type,
            'sub_type': sub_type,
        }
        return Response(response)
    return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), status=HTTP_400_BAD_REQUEST)



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

