import logging
import cloudinary
import cloudinary.uploader
import cloudinary.api

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

from django.db import models

from um.permissions import IsTalentOrCasting
from um.permissions import IsCasting
from um.views import error_as_text

from serializers import PlainOrganizationSerializer
from serializers import PlainMemberSerializer

from models import Organization
from models import PlainOrganization
from models import OrganizationMember
from models import PlainMember
from casting.models import CastingProfile
from notifications.views import create_notification

logger = logging.getLogger(__name__)


def get_organizations():
    """
    Get all organizations.
    :return: List of plain organizations.
    """
    orgs = Organization.objects.all()
    plain_orgs = []
    for org in orgs:
        plain_org = org.plain(include_members=True)
        plain_orgs.append(plain_org)
    return plain_orgs


def process_invitation(request, organization_id=None, invitation_id=None, accept=True):
    """
    Accepts/Rejects an invitation.
    :param request: an HTTP request
    :param organization_id: organization of the invitation
    :param invitation_id: id of inivitation
    :param accept: accept/reject
    :return: Response with success/failure
    """
    user = request.user
    organization = Organization.objects.filter(id=organization_id).first()
    invitation = OrganizationMember.objects.filter(id=invitation_id).first()
    if organization:
        if invitation:
            if invitation.user == user:
                if invitation.is_new():
                    message = ""
                    notification_type = ""
                    if accept:
                        invitation.is_accepted = True
                        message = "Your membership invitation has been accepted"
                        notification_type = "OIA"
                    else:
                        invitation.is_rejected = True
                        message = "Your membership invitation has been rejected"
                        notification_type = "OIR"
                    invitation.save()
                    plain_invitation = invitation.plain()
                    serializer = PlainMemberSerializer(plain_invitation)
                    create_notification(notification_type, invitation.id, invitation.user, invitation.initiator, message=message)
                    return Response(serializer.data)
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "This invitation had already been accepted/rejected"
                }, status=HTTP_400_BAD_REQUEST)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to accept/reject this invitation"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Invitation not found"
        }, status=HTTP_404_NOT_FOUND)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Organization not found"
    }, status=HTTP_404_NOT_FOUND)


def process_membership_request(request, organization_id=None, request_id=None, accept=True):
    """
    Accepts/Rejects a membership request.
    :param request: an HTTP request
    :param organization_id: organization of the request
    :param request_id: id of membership request
    :param accept: accept/reject
    :return: Response with success/failure
    """
    user = request.user
    organization = Organization.objects.filter(id=organization_id).first()
    membership = OrganizationMember.objects.filter(id=request_id).first()
    if organization:
        if membership:
            if OrganizationMember.user_is_admin(organization, user):
                if membership.is_new():
                    message = ""
                    notification_type = ""
                    if accept:
                        membership.is_accepted = True
                        message = "Your membership request has been accepted"
                        notification_type = "ORA"
                    else:
                        membership.is_rejected = True
                        message = "Your membership request has been rejected"
                        notification_type = "ORR"
                    membership.save()
                    plain_invitation = membership.plain()
                    serializer = PlainMemberSerializer(plain_invitation)
                    create_notification("", membership.id, membership.inititator, membership.user, message=message)
                    return Response(serializer.data)
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "This membership request had already been accepted/rejected"
                }, status=HTTP_400_BAD_REQUEST)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to accept/reject this membership request"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Membership request not found"
        }, status=HTTP_404_NOT_FOUND)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Organization not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', ])
@permission_classes([IsCasting, ])
def add_or_get_organizations(request):
    if request.method == 'GET':
        organizations = get_organizations()
        serializer = PlainOrganizationSerializer(organizations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        user = request.user
        has_no_organization = OrganizationMember.user_organization(user) is None
        if has_no_organization:
            serializer = PlainOrganizationSerializer(data=request.DATA)
            if serializer.is_valid():
                organization = serializer.save()
                admin = OrganizationMember()
                admin.organization = Organization.objects.filter(id=organization.organization_id).first()
                admin.user = request.user
                admin.role = 'ADM'
                admin.is_accepted = True
                admin.initiator = request.user
                admin.save()
                return Response(serializer.data)
            return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), HTTP_400_BAD_REQUEST)
        return Response({
            "status": HTTP_400_BAD_REQUEST,
            "message":"You can only create/join one organization at the mex",
        }, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', ])
@permission_classes([IsCasting, ])
def get_or_update_organization(request, organization_id=None):
    """
    View/Update details about an organization.
    You pass in the organization_id of the organization you need to view/update.
    You must be a member of the organization to view.
    You must be an admin of the organization to edit.
    """
    user = request.user
    organization = Organization.objects.filter(id=organization_id).first()
    logger.debug(organization)
    if organization:
        if request.method == 'GET':
            is_member = OrganizationMember.user_is_member_of(user, organization)
            if is_member:
                plain_organization = organization.plain(include_members=True)
                logger.debug(plain_organization)
                serializer = PlainOrganizationSerializer(plain_organization)
                return Response(serializer.data)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to view details of this organization"
            }, HTTP_401_UNAUTHORIZED)
        else:
            is_admin = OrganizationMember.user_is_admin(organization, user)
            if is_admin:
                plain_org = organization.plain()
                serializer = PlainOrganizationSerializer(plain_org, data=request.DATA)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), HTTP_400_BAD_REQUEST)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to edit this organization",
            }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Organization not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsCasting])
def upload_logo(request, organization_id=None):
    user = request.user
    organization = Organization.objects.filter(id=organization_id).first()
    if organization:
        is_admin = OrganizationMember.user_is_admin(organization, user)
        if is_admin:
            response = cloudinary.uploader.upload(request.FILES['logo'])
            organization.logo = response['url']
            organization.save()
            return Response({
                "thumbnail_url": organization.logo
            })
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You are not authorized to perform this operation"
        }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Organization not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsCasting, ])
def get_organization_members(request, organization_id=None):
    organization = Organization.objects.get(id=organization_id)
    if organization:
        all_members = organization.members.all()
        plain_members = []
        for member in all_members:
            plain_member = member.plain()
            plain_members.append(plain_member)
            serializer = PlainMemberSerializer(plain_members, many=True)
        return Response(serializer.data)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Organization not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsCasting, ])
def invite_user(request, organization_id=None):
    initiator = request.user
    organization = Organization.objects.filter(id=organization_id).first()
    if organization:
        if OrganizationMember.user_is_admin(organization, initiator):
            user_id = request.DATA.get("to")
            user = User.objects.filter(id=user_id).first()
            role = request.DATA.get("role")
            if not OrganizationMember.user_is_member_of(user, organization):
                if not OrganizationMember.user_is_member_of(user):
                    invitation = OrganizationMember()
                    invitation.organization = organization
                    invitation.user = user
                    invitation.role = role
                    invitation.initiator = initiator
                    invitation.save()
                    plain_member = invitation.plain()
                    serializer = PlainMemberSerializer(plain_member)
                    message = "You have been invited to join %s as %s" % (organization.name, "as an administrator" if invitation.role == "ADM" else "as a coordinator", )
                    create_notification("OMI", invitation.id, invitation.initiator, invitation.user, message=message)
                    return Response(serializer.data)
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "The user is already a member of some other organization"
                }, status=HTTP_400_BAD_REQUEST)
            return Response({
                "status": HTTP_400_BAD_REQUEST,
                "message": "The user is already a member/awaiting membership of this organization"
            }, status=HTTP_400_BAD_REQUEST)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You are not authorized to send membership invitation"
        }, status=HTTP_401_UNAUTHORIZED)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Organization not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def accept_invitation(request, organization_id=None, invitation_id=None):
    """
    Accepts an invitation.
    """
    return process_invitation(request, organization_id, invitation_id)


@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def reject_invitation(request, organization_id=None, invitation_id=None):
    """
    Rejects an invitation.
    """
    return process_invitation(request, organization_id, invitation_id, accept=False)


@api_view(['POST', ])
@permission_classes([IsCasting, ])
def request_membership(request, organization_id=None):
    user = request.user
    organization = Organization.objects.filter(id=organization_id).first()
    if organization:
        role = request.DATA.get("role")
        if not OrganizationMember.user_is_member_of(user, organization):
            if not OrganizationMember.user_is_member_of(user):
                membership = OrganizationMember()
                membership.organization = organization
                membership.user = user
                membership.role = role
                membership.initiator = user
                membership.save()
                plain_member = membership.plain()
                serializer = PlainMemberSerializer(plain_member)
                message = "%s %s has requested membership of %s as %s" % (user.first_name, user.last_name, organization.name, "as an administrator" if membership.role == "ADM" else "as a coordinator", )
                for admin in organization.administrators():
                    create_notification("OMR", membership.id, membership.user, admin.user, message=message)
                return Response(serializer.data)
            return Response({
                "status": HTTP_400_BAD_REQUEST,
                "message": "You are already a member/awaiting membership of some other organization"
            }, status=HTTP_400_BAD_REQUEST)
        return Response({
            "status": HTTP_400_BAD_REQUEST,
            "message": "You are already a member/awaiting membership of this organization"
        }, status=HTTP_400_BAD_REQUEST)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Organization not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def accept_request(request, organization_id=None, request_id=None):
    return process_membership_request(request, organization_id, request_id)


@api_view(['PUT', ])
@permission_classes([IsCasting, ])
def reject_request(request, organization_id=None, request_id=None):
    return process_membership_request(request, organization_id, request_id, accept=False)

