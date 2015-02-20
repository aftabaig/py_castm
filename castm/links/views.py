import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User

from django.db import models

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting

from serializers import PlainLinkSerializer
from serializers import MyLinksSerializer

from models import Link
from models import PlainLink
from talent.models import TalentProfile
from casting.models import CastingProfile
from notifications.views import create_notification

logger = logging.getLogger(__name__)

@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def my_links(request):
    user = request.user
    links = Link.all_links(user)
    all_links = []
    for link in links:
        if link.from_user.id == user.id:
            l = {
                "user_id": link.to_user.id,
            }
            l["full_name"] = "%s %s" % (link.to_user.first_name, link.to_user.last_name, )
            if link.to_user.my_user.type == 'T':
                talent_profile = link.to_user.user_profile.get()
                if talent_profile.is_stage_name:
                    l["full_name"]= "%s %s" % (talent_profile.stage_first_name, talent_profile.stage_last_name, )
        else:
            l = {
                "user_id": link.from_user.id,
            }
            l["full_name"] = "%s %s" % (link.from_user.first_name, link.from_user.last_name, )
            if link.from_user.my_user.type == 'T':
                talent_profile = link.from_user.user_profile.get()
                if talent_profile.is_stage_name:
                    l["full_name"] = "%s %s" % (talent_profile.stage_first_name, talent_profile.stage_last_name, )

        all_links.append(l)

    return Response(all_links)

@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def my_talent_links(request):
    """
    Returns all qualified talent links for the user.
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            [
                {
                    id=[link_id],
                    first_name=[requester first name],
                    last_name=[requester last name],
                    title=[requester title],
                    profile_url=[requester profile]
                },
                {
                    id=[link_id],
                    first_name=[requester first name],
                    last_name=[requester last name],
                    title=[requester title],
                    profile_url=[requester profile]
                },
            ]
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    links = Link.talent_links(user)
    talent_links = []
    for link in links:
        if link.from_user.id == user.id:
            plain_link = PlainLink(
                link_id=link.id,
                created_at=link.created_at,
                user_id=link.to_user.id,
                first_name=link.to_user.first_name,
                last_name=link.to_user.last_name,
                title=link.to_user.user_profile.get().title,
                thumbnail_url=link.to_user.user_profile.get().thumbnail,
                profile_url="/api/talents/profile/%d" % (link.to_user.id, ),
            )
            talent_links.append(plain_link)
        else:
            plain_link = PlainLink(
                link_id=link.id,
                created_at=link.created_at,
                user_id=link.from_user.id,
                first_name=link.from_user.first_name,
                last_name=link.from_user.last_name,
                title=link.from_user.user_profile.get().title,
                thumbnail_url=link.from_user.user_profile.get().thumbnail,
                profile_url="/api/talents/profile/%d" % (link.from_user.id, ),
            )
            talent_links.append(plain_link)

    serializer = PlainLinkSerializer(talent_links, many=True)
    return Response(serializer.data)

@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def my_casting_links(request):
    """
    Returns all qualified casting links for the user.
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            [
                {
                    id=[link_id],
                    first_name=[requester first name],
                    last_name=[requester last name],
                    title=[requester title],
                    profile_url=[requester profile]
                },
                {
                    id=[link_id],
                    first_name=[requester first name],
                    last_name=[requester last name],
                    title=[requester title],
                    profile_url=[requester profile]
                },
            ]
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    links = Link.casting_links(user)
    casting_links = []
    for link in links:
        if link.from_user.id == request.user.id:
            logger.debug(request.user.id)
            logger.debug(link.to_user.id)
            plain_link = PlainLink(
                link_id=link.id,
                link_type=link.to_user.my_user.type,
                created_at=link.created_at,
                user_id=link.to_user.id,
                first_name=link.to_user.first_name,
                last_name=link.to_user.last_name,
                title="",
                thumbnail_url=link.to_user.casting_profile.get().thumbnail,
                profile_url="/api/casting/profile/%s" % (link.to_user.id, )
            )
            casting_links.append(plain_link)
        else:
            logger.debug("no")
            plain_link = PlainLink(
                link_id=link.id,
                link_type=link.from_user.my_user.type,
                created_at=link.created_at,
                user_id=link.from_user.id,
                first_name=link.from_user.first_name,
                last_name=link.from_user.last_name,
                title="",
                thumbnail_url=link.from_user.casting_profile.get().thumbnail,
                profile_url="/api/casting/profile/%s" % (link.from_user.id, )
            )
            casting_links.append(plain_link)

    serializer = PlainLinkSerializer(casting_links, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def search_links(request):
    """
    Searches & returns talents and casting links based on the query_string.
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            [
                {
                    id=[link_id],
                    first_name=[requester first name],
                    last_name=[requester last name],
                    title=[requester title],
                    thumbnail_url=[requester thumbnail image],
                    profile_url=[requester profile],
                    link_status=[U/F/RH/PH/RY/PY"
                },
                {
                    id=[link_id],
                    first_name=[requester first name],
                    last_name=[requester last name],
                    title=[requester title],
                    thumbnail_url=[requester thumbnail image],
                    profile_url=[requester profile],
                    link_status=[U/F/RH/PH/RY/PY"
                },
            ]
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """

    # get logged in user.
    user = request.user

    # get query_string.
    query_string = request.GET.get("query_string")

    logger.debug(query_string)

    # array of results.
    search_results = []

    # build search query.
    q = models.Q(stage_first_name__icontains=query_string)
    q = q | models.Q(stage_last_name__icontains=query_string)
    q = q | models.Q(title__icontains=query_string)
    q = q | models.Q(user__first_name__icontains=query_string)
    q = q | models.Q(user__last_name__icontains=query_string)
    talents = TalentProfile.objects.filter(q)

    q = models.Q(user__first_name__icontains=query_string)
    q = q | models.Q(user__last_name__icontains=query_string)
    castings = CastingProfile.objects.filter(q)

    # loop through the talents and build a link model.
    for talent in talents:

        if talent.user.id != user.id:

            # build a link search query that will return
            # a link if the current user and the talent
            # are friends or the link requests are pending.
            q1 = models.Q(from_user=talent.user)
            q2 = models.Q(to_user=talent.user)
            q3 = models.Q(from_user=user)
            q4 = models.Q(to_user=user)
            link = Link.objects.filter((q1 & q4) | (q2 & q3)).first()

            # create a plain link model.
            plain_link = PlainLink(
                link_type=talent.my_user.type,
                user_id=talent.user.id,
                first_name=talent.user.first_name,
                last_name=talent.user.last_name,
                title=talent.title,
                thumbnail_url=talent.thumbnail,
                profile_url="/api/talent/profile/%s" % (talent.user.id, ),
                link_status="U"
            )

            # here, we determine the link status.
            # U  - Unknown (no link)
            # F  - Friends
            # RH - Rejected by him (the other user)
            # PH - Pending by him
            # RY - Rejected by you (logged-in user)
            # PY - Pending by you
            if link:
                plain_link.link_id = link.id
                if link.is_accepted:
                    plain_link.link_status = "F"
                else:
                    if link.from_user == user:
                        if link.is_rejected:
                            plain_link.link_status = "RH"
                        else:
                            plain_link.link_status = "PH"
                    else:
                        if link.is_rejected:
                            plain_link.link_status = "RY"
                        else:
                            plain_link.link_status = "PY"

            # finally, add the link to search results.
            search_results.append(plain_link)

    # loop through the talents and build a link model.
    for casting in castings:

        if casting.user.id != user.id:

            # build a link search query that will return
            # a link if the current user and the talent
            # are friends or the link requests are pending.
            q1 = models.Q(from_user=casting.user)
            q2 = models.Q(to_user=casting.user)
            q3 = models.Q(from_user=user)
            q4 = models.Q(to_user=user)
            link = Link.objects.filter((q1 & q4) | (q2 & q3)).first()

            # create a plain link model.
            plain_link = PlainLink(
                link_type=casting.my_user.type,
                user_id=casting.user.id,
                first_name=casting.user.first_name,
                last_name=casting.user.last_name,
                title="",
                thumbnail_url=casting.thumbnail,
                profile_url="/api/casting/profile/%s" % (casting.user.id, ),
                link_status="U"
            )

            # here, we determine the link status.
            # U  - Unknown (no link)
            # F  - Friends
            # RH - Rejected by him (the other user)
            # PH - Pending by him
            # RY - Rejected by you (logged-in user)
            # PY - Pending by you
            if link:
                plain_link.link_id = link.id
                if link.is_accepted:
                    plain_link.link_status = "F"
                else:
                    if link.from_user == user:
                        if link.is_rejected:
                            plain_link.link_status = "RH"
                        else:
                            plain_link.link_status = "PH"
                    else:
                        if link.is_rejected:
                            plain_link.link_status = "RY"
                        else:
                            plain_link.link_status = "PY"

            # finally, add the link to search results.
            search_results.append(plain_link)

    serializer = PlainLinkSerializer(search_results, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def my_link_requests(request):
    """
    Returns un-attended link requests for the user.
    Allowed HTTP methods are:\n
        1. GET to view\n
            Returns:\n
            {
                "talents": [
                    {
                    id=[link_id],
                    first_name=[requester first name],
                    last_name=[requester last name],
                    title=[requester title],
                    profile_url=[requester profile]
                    }
                ],
                "casting": [
                    {
                        id=[link_id],
                        first_name=[requester first name],
                        last_name=[requester last name],
                        title=[requester title],
                        profile_url=[requester profile]
                    },
                ]
            }
    Status:\n
        1. 200 on success
        2. 401 if un-authorized
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    links = Link.link_requests(user)
    logger.debug(user.id)
    link_requests = []
    for link in links:
        plain_link = PlainLink(
            link_id=link.id,
            link_type=link.from_user.my_user.type,
            created_at=link.created_at,
            first_name=link.from_user.first_name,
            last_name=link.from_user.last_name,
        )
        if link.from_user.my_user.type == 'T':
            plain_link.title = link.from_user.user_profile.get().title
            plain_link.thumbnail_url = link.from_user.user_profile.get().thumbnail
            plain_link.profile_url = "/api/talents/profile/%d" % (link.from_user.id, )
        else:
            plain_link.title = ""
            plain_link.thumbnail_url = link.from_user.casting_profile.get().thumbnail
            plain_link.profile_url = "/api/casting/profile/%d" % (link.from_user.id, )
        link_requests.append(plain_link)

    serializer = PlainLinkSerializer(link_requests)
    return Response(serializer.data)

@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def send_link_request(request, user_id=0):
    """
    Sends a link request
    Allowed HTTP methods are:\n
        1. POST to send\n
            Returns:\n
            . Newly created link (which will initially be a request only link)
    Status:\n
        1. 200 on success
        2. 400 if some error occurs
        3. 401 if un-authorized
        4. 404 if link request not found.
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    me = request.user
    other = User.objects.filter(id=user_id).first()
    if other:
        if not Link.is_already_link(me, other):
            link_request = Link()
            link_request.from_user = me
            link_request.to_user = other
            link_request.optional_message = ""
            link_request.save()
            create_notification("LR", link_request.id, me, other, message="Link Request")
            serializer = PlainLinkSerializer(link_request.plain(me))
            return Response(serializer.data)
        return Response({
            "status": HTTP_400_BAD_REQUEST,
            "message": "You are already linked to this user"
        }, status=HTTP_400_BAD_REQUEST)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "User not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def accept_link_request(request, link_id=0):
    """
    Accepts a link request
    Allowed HTTP methods are:\n
        1. POST to accept\n
            Returns:\n
            . Accepted user's profile
    Status:\n
        1. 200 on success
        2. 400 if some error occurs
        3. 401 if un-authorized
        4. 404 if user not found.
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    link = Link.objects.filter(id=link_id).first()
    if link and link.to_user == user:
        link.is_accepted = True
        link.is_rejected = False
        link.save()
        create_notification("LA", link.id, user, link.from_user, message="Link Accepted")
        serializer = PlainLinkSerializer(link.plain(user))
        return Response(serializer.data)
    return Response(status=HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def reject_link_request(request, link_id=0):
    """
    Rejects a link request
    Allowed HTTP methods are:\n
        1. POST to accept\n
            Returns:\n
            . Rejected user's profile
    Status:\n
        1. 200 on success
        2. 400 if some error occurs
        3. 401 if un-authorized
        4. 404 if link request not found.
    Notes:\n
        1. Require user's token to be sent in the header as:\n
            Authorization: Token [token]\n
    """
    user = request.user
    link = Link.objects.filter(id=link_id).first()
    if link and link.to_user == user:
        link.is_rejected = True
        link.is_accepted = False
        link.save()
        create_notification("LD", link.id, user, link.from_user, message="Link Declined")
        serializer = PlainLinkSerializer(link.plain(user))
        return Response(serializer.data)
    return Response(status=HTTP_404_NOT_FOUND)



