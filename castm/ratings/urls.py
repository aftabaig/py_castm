from django.conf.urls import patterns, url

# views
from views import user_ratings

urlpatterns = patterns(
    'rate.views',
    url(r'^(?P<talent_id>[0-9]+)/$', user_ratings),
)
