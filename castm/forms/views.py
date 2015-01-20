from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from um.permissions import IsTalentOrCasting
from um.views import error_as_text

from serializers import RatingFormSerializer
from models import RatingForm, FormField, FieldItem
from organizations.models import Organization


class RatingFormViewSet(viewsets.ViewSet):

    queryset = RatingForm.objects.all()
    permission_classes = [IsTalentOrCasting, ]

    def list(self, request, organization_id=None):
        queryset = self.queryset.filter(organization=organization_id)
        serializer = RatingFormSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, organization_id=None):
        serializer = RatingFormSerializer(data=request.DATA)
        serializer.organization = Organization.objects.filter(id=organization_id)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), status=HTTP_400_BAD_REQUEST)

    def update(self, request, organization_id=None):
        serializer = RatingFormSerializer(data=request.DATA)
        serializer.organization = Organization.objects.filter(id=organization_id)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), status=HTTP_400_BAD_REQUEST)
