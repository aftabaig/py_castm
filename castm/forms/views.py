from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.decorators import api_view, permission_classes

from um.permissions import IsCasting
from um.views import error_as_text

from serializers import RatingFormSerializer, FormFieldSerializer
from models import RatingForm, FormField, FieldItem
from organizations.models import Organization, OrganizationMember


@api_view(['GET', 'POST', ])
@permission_classes([IsCasting, ])
def add_or_get_fields(request, organization_id=None):
    user = request.user
    organization = Organization.objects.filter(id=organization_id).first()
    if organization:
        is_admin = OrganizationMember.user_is_admin(organization, user)
        if is_admin:
            if request.method == 'GET':
                fields = FormField.objects.filter(form__organization=organization)
                serializer = FormFieldSerializer(fields, many=True)
                return Response(serializer.data)
            else:
                field = FormField()
                field.title = request.DATA.get("title")
                field.type = request.DATA.get("type")
                field.use_stars = request.DATA.get("use_stars")
                field.max_value = request.DATA.get("max_value")
                items = request.DATA.get("items")
                form = RatingForm.objects.filter(organization=organization).first()
                if not form:
                    form = RatingForm(organization=organization)
                    form.save()
                field.form = form
                field.save()
                for item in items:
                    new_item = FieldItem(field=field)
                    new_item.title = item.get("title")
                    new_item.value = item.get("value")
                    new_item.save()
                serializer = FormFieldSerializer(field)
                return Response(serializer.data)
        return Response({
            "status": HTTP_401_UNAUTHORIZED,
            "message": "You are not authorized to view this form"
        })
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Organization not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['PUT', 'DELETE', ])
@permission_classes([IsCasting, ])
def update_or_delete_field(request, organization_id=None, field_id=None):
    organization = Organization.objects.filter(id=organization_id).first()
    if organization:
        field = FormField.objects.filter(id=field_id).first()
        if field:
            if request.method == 'PUT':
                form = RatingForm.objects.filter(organization=organization).first()
                if form:
                    field.title = request.DATA.get("title")
                    field.type = request.DATA.get("type")
                    field.use_stars = request.DATA.get("use_stars")
                    field.max_value = request.DATA.get("max_value")

                    items = request.DATA.get("items")
                    for item in items:
                        item_id = item.get("id")
                        field_item = FieldItem(field=field)
                        if item_id:
                            field_item = FieldItem.objects.filter(id=item_id).first()
                        field_item.title = item.get("title")
                        field_item.value = item.get("value")
                        field_item.save()

                    deleted_items = request.DATA.get("deleted_items")
                    for item in deleted_items:
                        item_id = item.get("id")
                        field_item = FieldItem.objects.filter(id=item_id).first()
                        if field_item:
                            field_item.delete()
                    serializer = FormFieldSerializer(field)
                    return Response(serializer.data)
                return Response({
                    "status": HTTP_404_NOT_FOUND,
                    "message": "No form found"
                }, status=HTTP_404_NOT_FOUND)
            else:
                field.delete()
                return Response({
                    "status": HTTP_204_NO_CONTENT,
                    "message": "OK"
                }, status=HTTP_204_NO_CONTENT)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Field not found"
        }, status=HTTP_404_NOT_FOUND)
    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Organization not found"
    }, status=HTTP_404_NOT_FOUND)


