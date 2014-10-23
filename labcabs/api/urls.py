from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from views import entity_list, entity_detail
from views import consignment_list, consignment_detail
from views import supply_list, supply_detail
from views import search_list, search_detail

urlpatterns = patterns(
    'api.views',
    url(r'^entities/$', entity_list, name='entity_list'),
    url(r'^entities/(?P<pk>[0-9]+)$', entity_detail, name='entity_detail'),
    url(r'^consignments/$', consignment_list, name='consignment_list'),
    url(r'^consignments/(?P<pk>[0-9]+)$', consignment_detail, name='consignment_detail'),
    url(r'^supplies/$', supply_list, name='supply_list'),
    url(r'^supplies/(?P<pk>[0-9]+)$', supply_detail, name='supply_detail'),
    url(r'^searches/$', search_list, name='search_list'),
    url(r'^searches/(?P<pk>[0-9]+)$', search_detail, name='search_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)