from django.conf.urls import patterns, include, url

from api.views import entity_router
from api.views import consignment_router
from api.views import supply_router
from api.views import search_router

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^api/', include(entity_router.urls)),
    url(r'^api/', include(consignment_router.urls)),
    url(r'^api/', include(supply_router.urls)),
    url(r'^api/', include(search_router.urls))
)

urlpatterns += patterns(
    'labcabs.views',
    url(r'^$', 'home', name="home"))




