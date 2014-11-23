import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting

from serializers import PlainLinkSerializer
from serializers import MyLinksSerializer

from models import Link
from models import PlainLink
from models import MyLinks


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def my_notifications(request):
    pass


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def my_links(request):
    user = request.user
    links = Link.user_links(user)
    talent_links = []
    casting_links = []
    for link in links:
        if link.from_user.id == request.user.id:
            plain_link = PlainLink(
                id=link.id,
                first_name=link.to_user.first_name,
                last_name=link.to_user.last_name,
                title="",
                profile_url=""
            )
            if link.to_user.my_user.type == 'T':
                plain_link.profile_url = "/api/talents/profile/" + str(link.to_user.id)
                talent_links.append(plain_link)
            else:
                plain_link.profile_url = "/api/casting/profile/" + str(link.to_user.id)
                casting_links.append(plain_link)
        else:
            plain_link = PlainLink(
                id=link.id,
                first_name=link.from_user.first_name,
                last_name=link.from_user.last_name,
                title="",
                profile_url=""
            )
            if link.from_user.my_user.type == 'T':
                plain_link.profile_url = "/api/talents/profile/" + str(link.from_user.id.str)
                talent_links.append(plain_link)
            else:
                plain_link.profile_url = "/api/casting/profile/" + str(link.from_user.id)
                casting_links.append(plain_link)

    all_links = MyLinks(talent_links=talent_links, casting_links=casting_links)
    serializer = MyLinksSerializer(all_links)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def send_link_request(request, user_id=0):
    me = request.user
    other = User.objects.filter(id=user_id).first()
    if other:
        if not Link.is_already_link(me, other):
            link = Link()
            link.from_user = me
            link.to_user = other
            link.optional_message = "You've a link request"
            link.save()
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
    return Response(status=HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def accept_link_request(request, link_id=0):
    user = request.user
    link = Link.objects.filter(id=link_id).first()
    if link and link.to_user == user:
        link.is_accepted = True
        link.is_rejected = False
        link.save()
        return Response()
    return Response(status=HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def reject_link_request(request, link_id=0):
    user = request.user
    link = Link.objects.filter(id=link_id).first()
    if link and link.to_user == user:
        link.is_rejected = True
        link.is_accepted = False
        link.save()
        return Response()
    return Response(status=HTTP_404_NOT_FOUND)


def send_message(request):
    pass


def send_callback(request):
    pass




