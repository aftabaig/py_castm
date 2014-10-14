from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from views import entity_list, entity_detail
from views import consignment_list, consignment_detail

urlpatterns = patterns(
    'api.views',
    url(r'^entities/$', entity_list, name='entity_list'),
    url(r'^entities/(?P<pk>[0-9]+)$', entity_detail, name='entity_detail'),
    url(r'^consignments/$', consignment_list, name='consignment_list'),
    url(r'^consignments/(?P<pk>[0-9]+)$', consignment_detail, name='consignment_detail')
)

urlpatterns = format_suffix_patterns(urlpatterns)