from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

# views
from views import plans
from views import subscribe, un_subscribe
from views import subscription_status
from views import event_handler

urlpatterns = patterns(
    'subscriptions.views',
    url(r'^plans/$', plans),
    url(r'^subscribe/$', subscribe),
    url(r'^un-subscribe/$', un_subscribe),
    url(r'^status/$', subscription_status),
    url(r'^handler/$', event_handler),
)
