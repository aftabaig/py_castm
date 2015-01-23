from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.decorators import api_view, permission_classes

from um.permissions import IsTalentOrCasting
from um.views import error_as_text

from serializers import RatingFormSerializer, FormFieldSerializer
from models import RatingForm, FormField, FieldItem
from organizations.models import Organization


class RatingFormViewSet(viewsets.ViewSet):

    queryset = FormField.objects.all()
    permission_classes = [IsTalentOrCasting, ]

    def list(self, request, organization_id=None):
        queryset = self.queryset.filter(form__organization=organization_id)
        serializer = FormFieldSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, organization_id=None):
        serializer = FormFieldSerializer(data=request.DATA)
        organization = Organization.objects.filter(id=organization_id).first()
        if organization:
            form = RatingForm.objects.filter(organization=organization).first()
            if not form:
                form = RatingForm(organization=organization)
                form.save()
            serializer.form = RatingFormSerializer(form)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), status=HTTP_400_BAD_REQUEST)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Organization not found"
        }, status=HTTP_404_NOT_FOUND)

    def update(self, request, organization_id=None, field_id=None):
        field = FormField.objects.filter(id=field_id).first()
        serializer = FormFieldSerializer(field, data=request.DATA)
        organization = Organization.objects.filter(id=organization_id).first()
        if organization:
            form = RatingForm.objects.filter(organization=organization).first()
            serializer.form = form
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(error_as_text(serializer.errors, HTTP_400_BAD_REQUEST), status=HTTP_400_BAD_REQUEST)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Organization not found"
        }, status=HTTP_404_NOT_FOUND)
