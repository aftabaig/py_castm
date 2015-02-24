
import logging

from rest_framework.authtoken.models import Token

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

# django
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail

from mobi.decorators import detect_mobile

# models
from models import MyUser, UserDevice
from talent.models import TalentProfile
from casting.models import CastingProfile

# serializers
from serializers import UserSerializer

# permissions
from permissions import IsTalent
from permissions import IsTalentOrCasting

logger = logging.getLogger(__name__)

# returns error as plain text.
# TODO: This is only 2 level deep.
# To dig deep, we might need a recursive method.
def error_as_text(errors, status):
    logger.debug(errors)
    logger.debug(status)
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


def message(msg):
    return {
        'message': msg,
        'status': HTTP_200_OK
    }


def error_message(msg, status=HTTP_400_BAD_REQUEST):
    return {
        'message': msg,
        'status': status
    }

@api_view(['POST', ])
def sign_up(request):

    # create serializer from request-data.
    serializer = UserSerializer(data=request.DATA)
    if serializer.is_valid():

        activation_key = MyUser.generate_activation_key()
        serializer.object.activation_key = activation_key

        # saves user data (in both auth-user and my-user models.
        serializer.save()

        # get auth-user model from the serializer.
        # get password from request-data.
        # set password on the model and save.
        user = serializer.object.user
        password = request.DATA.get("user").get("password")
        user.set_password(password)
        user.is_active = False
        user.save()

        # create token for the user
        Token.objects.create(user=user)

        # create an empty talent-profile.
        if serializer.object.type == 'T':
            talent = TalentProfile(my_user=serializer.object, user=user)
            talent.save()
        else:
            casting = CastingProfile(my_user=serializer.object, user=user)
            casting.save()

        # send activation e-mail.
        subject = 'Cast\'M account activation'
        relative_url = "/api/users/activate/%s" % (activation_key, )
        msg = 'Hi %s<br/>' % (user.username, )
        msg += 'Click on the following link to activate your account:<br/>'
        msg += '<a href="%s">Activate</a>' % (request.build_absolute_uri(relative_url), )
        logger.debug(msg)
        send_mail(subject, 'Message', 'info@castm.com', (user.username, ), html_message=msg)

        return Response(message('An activation link is sent to your email address.'), status=HTTP_200_OK)
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
            "password": "abc123",
            "device_type": "[iPhone/Android/Desktop]",
            "token": "[token]",
            "push_token": [push_token]"
        }\n
    Returns:\n
        {
            "token": "b95175a8e01d3ac718d12669f1ca8ddd37bf6f3d",
            "type": 'S'
        }\n
    """
    serializer = AuthTokenSerializer(data=request.DATA)
    if serializer.is_valid():
        user = serializer.object['user']
        device_type = request.DATA.get("device_type")
        push_token = request.DATA.get("push_token")
        token, created = Token.objects.get_or_create(user=user)
        my_device, created = UserDevice.objects.get_or_create(user=user, device_type=device_type, push_token=push_token)
        my_device.push_token = push_token
        my_device.save()
        my_user = MyUser.objects.filter(user=user).first()
        if my_user:
            if my_user.user.is_active:
                type = my_user.type
                response = {
                    'token': token.key,
                    'type': type,
                }
                return Response(response)
    return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), status=HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def logout(request):
    user = request.user
    device_type = request.DATA.get("device_type")
    push_token = request.DATA.get("push_token")
    if device_type and push_token:
        user_device = UserDevice.get_user_device(user, device_type, push_token)
        if user_device:
            user_device.delete()
            return Response({
                "status": HTTP_200_OK,
                "message": ""
            })
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "User device not found"
        }, status=HTTP_404_NOT_FOUND)
    return Response({
        "status": HTTP_400_BAD_REQUEST,
        "message": "Required fields missing"
    }, status=HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
@permission_classes([IsTalentOrCasting, ])
def change_password(request):
    current_password = request.DATA.get("current_password")
    new_password = request.DATA.get("new_password")
    if request.user:
        if request.user.check_password(current_password):
            request.user.set_password(new_password)
            request.user.save()
            return Response(status=HTTP_200_OK)
        return Response({
            "status": HTTP_400_BAD_REQUEST,
            "message": "Invalid password"
        }, status=HTTP_400_BAD_REQUEST)
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
            msg = 'Your new password is <strong>%s</strong>' % (password, )
            msg += '<br/>You can change it from right within your app'
            send_mail(subject, 'Message', 'info@castm.com', (email_address, ), html_message=msg)
            return Response(message("An email has been sent to you with the new password"), status=HTTP_200_OK)
        return Response(error_message("Account with this email does not exist."), status=HTTP_400_BAD_REQUEST)
    return Response(error_message("Email is required."), status=HTTP_400_BAD_REQUEST)


@detect_mobile
@api_view(['GET', ])
def activate_user(request, activation_key):
    my_user = MyUser.objects.filter(activation_key=activation_key)[0]
    if my_user:
        user = User.objects.get(id=my_user.user.id)
        user.is_active = True
        user.save()
        if request.mobile:
            location = "castm://login?email_address=%s" % (user.username, )
            response = HttpResponse(location, status=302)
            response['Location'] = location
            return response
        else:
            return HttpResponseRedirect('/activation')
