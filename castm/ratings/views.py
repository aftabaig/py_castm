import logging

# rest_framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

from serializers import RatingFieldSerializer
from um.views import error_as_text
from um.permissions import IsCasting

from models import UserRating
from forms.models import RatingForm
from organizations.models import Organization, OrganizationMember
from events.models import Event, EventAttendee

@api_view(['GET', ])
@permission_classes([IsCasting])
def rate_user(request, event_id=None, talent_id=None):
    user = request.user
    event = Event.objects.filter(id=event_id).first()
    if event:
        user_organization = OrganizationMember.user_organization(user)
        if user_organization:
            is_member = OrganizationMember.user_is_member_of(user_organization, user)
            if is_member:
                has_attended_event = EventAttendee.is_organization_attending_event(user_organization, event)
                if has_attended_event:
                    talent_user = User.objects.filter(id=talent_id).first()
                    if talent_user:
                        talent_has_attended_event = EventAttendee.is_user_attending_event(talent_user, event)
                        if talent_has_attended_event:
                            already_rated = UserRating.user_is_already_rated(talent_user, user)
                            if not already_rated:
                                rating = UserRating()
                                rating.rating_form = RatingForm.organization_form(user_organization)
                                rating.talent_user = talent_user
                                rating.casting_user = user
                                rating.casting_organization = user_organization
                                rating.save()
                                serializer = RatingFieldSerializer(data=request.DATA, many=True, context={
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





