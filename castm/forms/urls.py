from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from views import add_or_get_fields, update_or_delete_field

urlpatterns = patterns(
    'forms.views',
    url(r'^$', add_or_get_fields),
    url(r'^(?P<field_id>[0-9]+)/$', update_or_delete_field)
)
