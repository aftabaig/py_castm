import stripe

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

from um.views import error_as_text
from um.permissions import IsTalentOrCasting


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def subscribe(request, user_id=None):
    user = request.user
    if user.my_user.type == 'T':
        pass
    else:
        pass


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def un_subscribe(request, user_id=None):
    pass


