import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

from serializers import RatingFieldSerializer
from um.views import error_as_text
from um.permissions import IsCasting

from models import UserRating, UserRatingField
from forms.models import RatingForm
from organizations.models import Organization, OrganizationMember
from events.models import Event, EventAttendee

logger = logging.getLogger(__name__)


def user_rating_info(event, organization, talent):

    event_info = {
        "event_id": event.id,
        "event_name": event.name
    }

    talent_info = {
        "talent_id": talent.id,
        "talent_first_name": talent.first_name,
        "talent_last_name": talent.last_name,
        "talent_title": talent.user_profile.get().title,
        "talent_thumbnail_url": talent.user_profile.get().thumbnail,
        "talent_profile_url": "/api/talents/profile/%d" % (talent.id, )
    }

    members = OrganizationMember.organization_members(organization)

    form = RatingForm.organization_form(organization)
    form_fields = form.fields.all()

    fields = []
    for form_field in form_fields:

        field_info = {
            "field_id": form_field.id,
            "field_title": form_field.title,
            "field_type": form_field.type,
            "max_value": form_field.max_value
        }

        ratings = []

        for member in members:
            member_info = {
                "member_id": member.user.id,
                "member_first_name": member.user.first_name,
                "member_last_name": member.user.last_name
            }
            rating_value = UserRatingField.user_field_ratings(talent, member.user, form_field)
            rating = {
                "member_info": member_info,
                "rating": rating_value
            }
            ratings.append(rating)

        field = {
            "field_info": field_info,
            "ratings": ratings
        }
        fields.append(field)

    return {
        "event_info": event_info,
        "talent_info": talent_info,
        "fields": fields
    }


@api_view(['GET', 'POST', ])
@permission_classes([IsCasting])
def user_ratings(request, event_id=None, talent_id=None):
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    if event:
        user_organization = OrganizationMember.user_organization(user)
        if user_organization:
            is_member = OrganizationMember.user_is_member_of(user, user_organization)
            if is_member:
                has_attended_event = EventAttendee.is_organization_attending_event(user_organization, event)
                is_owner = event.owner == user_organization
                if has_attended_event or is_owner:
                    talent_user = User.objects.filter(id=talent_id).first()
                    if talent_user:
                        talent_has_attended_event = EventAttendee.is_user_attending_event(talent_user, event)
                        if talent_has_attended_event:
                            if request.method == 'POST':
                                already_rated = UserRating.user_is_already_rated(talent_user, user)
                                if not already_rated:
                                    rating = UserRating()
                                    rating.rating_form = RatingForm.organization_form(user_organization)
                                    rating.talent_user = talent_user
                                    rating.casting_user = user
                                    rating.casting_organization = user_organization
                                    rating.save()
                                    data = request.DATA.get("fields")
                                    serializer = RatingFieldSerializer(data=data, many=True, context={
                                        'rating_id': rating.id
                                    })
                                    if serializer.is_valid():
                                        serializer.save()
                                        return Response(serializer.data)
                                    return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), status=HTTP_400_BAD_REQUEST)
                                return Response({
                                    "status": HTTP_400_BAD_REQUEST,
                                    "message": "You have already rated this user for this event"
                                }, status=HTTP_400_BAD_REQUEST)
                            else:
                                return Response(user_rating_info(event, user_organization, talent_user))
                        return Response({
                            "status": HTTP_400_BAD_REQUEST,
                            "message": "This talent has not attended this event"
                        })
                    return Response({
                        "status": HTTP_404_NOT_FOUND,
                        "message": "Talent not found"
                    }, status=HTTP_404_NOT_FOUND)
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "Your organization did not attend the event"
                }, status=HTTP_400_BAD_REQUEST)
            return Response({
                "status": HTTP_401_UNAUTHORIZED,
                "message": "You are not an approved member of an organization"
            }, status=HTTP_401_UNAUTHORIZED)
        return Response({
            "status": HTTP_400_BAD_REQUEST,
            "message": "You must be associated with an organization to perform this action"
        }, status=HTTP_400_BAD_REQUEST)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Event not found"
    }, status=HTTP_404_NOT_FOUND)



