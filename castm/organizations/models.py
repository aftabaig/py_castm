import logging

from django.db import models
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class Organization(models.Model):
    name = models.CharField("Organization Name", max_length=32, blank=False)
    add1 = models.CharField("Address 1", max_length=1024, blank=True)
    add2 = models.CharField("Address 2", max_length=1024, blank=True)
    city = models.CharField("City", max_length=16, blank=True)
    state = models.CharField("State", max_length=16, blank=True)
    zip = models.CharField("Zip", max_length=16, blank=True)
    mobile = models.CharField("Mobile #", max_length=32, blank=True)
    office = models.CharField("Office #", max_length=32, blank=True)
    logo = models.CharField("Logo", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def plain(self, include_members=False):
        plain_org = PlainOrganization(
            organization_id=self.id,
            name=self.name,
            add1=self.add1,
            add2=self.add2,
            city=self.city,
            state=self.state,
            zip=self.zip,
            mobile=self.mobile,
            office=self.office,
            logo=self.logo,
            created_at=self.created_at,
        )
        if include_members:
            members = self.members.all()
            plain_org.members = []
            for member in members:
                plain_org.members.append(member.plain())
        return plain_org

    def administrators(self):
        admins = []
        for member in self.members.all():
            if member.role == 'ADM':
                admins.append(member)
        return admins


class OrganizationMember(models.Model):
    organization = models.ForeignKey(Organization, related_name="members")
    user = models.ForeignKey(User, related_name="user_members")
    role = models.CharField("Member's Role", max_length=4, blank=False)
    initiator = models.ForeignKey(User, related_name="initiated_members")
    is_accepted = models.BooleanField('Is Accepted', default=False, blank=False)
    is_rejected = models.BooleanField('Is Rejected', default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def plain(self):
        plain_member = PlainMember(
            member_id=self.id,
            member_role=self.role,
            user_id=self.user.id,
            user_email_address=self.user.email,
            user_first_name=self.user.first_name,
            user_last_name=self.user.last_name,
            user_thumbnail_url="",
            user_profile_url="",
            initiator_id=self.initiator.id,
            initiator_email_address=self.initiator.email,
            initiator_first_name=self.initiator.first_name,
            initiator_last_name=self.initiator.last_name,
            initiator_thumbnail_url="",
            initiator_profile_url="",
            is_accepted=self.is_accepted,
            is_rejected=self.is_rejected
        )
        return plain_member

    def is_new(self):
        q1 = not self.is_accepted
        q2 = not self.is_rejected
        return q1 and q2

    @staticmethod
    def user_is_admin(organization, user):
        q1 = models.Q(organization=organization)
        q2 = models.Q(user=user)
        q3 = models.Q(role='ADM')
        q4 = models.Q(is_accepted=True)
        return OrganizationMember.objects.filter(q1 & q2 & q3 & q4).count() > 0

    @staticmethod
    def user_is_member_of(user, organization=None):
        q = models.Q(user=user)
        if organization:
            q = q & models.Q(organization=organization)
        return OrganizationMember.objects.filter(q).count() > 0

    @staticmethod
    def user_organization(user):
        q1 = models.Q(user=user)
        q2 = models.Q(is_accepted=True)
        membership = OrganizationMember.objects.filter(q1 & q2).first()
        if membership:
            return membership.organization
        else:
            return None


class PlainOrganization(object):

    def __init__(self, request=None, organization_id=None, name=None, add1=None, add2=None, city=None, state=None, zip=None, mobile=None, office=None, logo=None, created_at=None, members=None):
        if request:
            self.name = request.DATA.get("name")
            self.add1 = request.DATA.get("add1")
            self.add2 = request.DATA.get("add2")
            self.city = request.DATA.get("city")
            self.state = request.DATA.get("state")
            self.zip = request.DATA.get("zip")
            self.mobile = request.DATA.get("mobile")
            self.office = request.DATA.get("office")
        else:
            self.organization_id = organization_id
            self.name = name
            self.add1 = add1
            self.add2 = add2
            self.city = city
            self.state = state
            self.zip = zip
            self.mobile = mobile
            self.office = office
            self.logo = logo
            self.created_at = created_at
            self.members = members


class PlainMember(object):
    def __init__(self, member_id, member_role=None,
                 user_id=None, user_email_address=None, user_first_name=None, user_last_name=None, user_thumbnail_url=None, user_profile_url=None,
                 initiator_id=None, initiator_email_address=None, initiator_first_name=None, initiator_last_name=None, initiator_thumbnail_url=None, initiator_profile_url=None,
                 is_accepted=None, is_rejected=None):
        self.member_id = member_id
        self.member_role = member_role
        self.user_id = user_id
        self.user_email_address = user_email_address
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_thumbnail_url = user_thumbnail_url
        self.user_profile_url = user_profile_url
        self.initiator_id = initiator_id
        self.initiator_email_address = initiator_email_address
        self.initiator_first_name = initiator_first_name
        self.initiator_last_name = initiator_last_name
        self.initiator_thumbnail_url = initiator_thumbnail_url
        self.initiator_profile_url = initiator_profile_url
        self.is_accepted = is_accepted
        self.is_rejected = is_rejected
