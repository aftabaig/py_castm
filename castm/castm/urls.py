from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'castm.views',
    url(r'^$', 'home', name="home"),
    url(r'^activation/$', 'activation', name="activation"),)

# urls from um.
# contains user-management urls.
urlpatterns += patterns(
    'um.views',
    url(r'^api/users/', include('um.urls')),
)

# urls from talent.
# contains talent related urls.
urlpatterns += patterns(
    'talent.views',
    url(r'^api/talent/', include('talent.urls')),
)

# urls from casting.
# contains casting related urls.
urlpatterns += patterns(
    'casting.views',
    url(r'^api/casting/', include('casting.urls')),
)

# urls from events.
# contains events related urls.
urlpatterns += patterns(
    'events.views',
    url(r'^api/events/', include('events.urls')),
)

# urls from schedules.
# contains schedules related urls.
urlpatterns += patterns(
    'schedules.views',
    url(r'^api/events/(?P<event_id>[0-9]+)/schedules/', include('schedules.urls'))
)

# urls from callbacks.
# contains callbacks related urls.
urlpatterns += patterns(
    'callbacks.views',
    url(r'^api/events/(?P<event_id>[0-9]+)/callbacks/', include('callbacks.urls'))
)

# urls from forms.
# contains rating forms related urls.
urlpatterns += patterns(
    'forms.views',
    url(r'^api/organizations/(?P<organization_id>[0-9]+)/forms/', include('forms.urls'))
)

# urls from notifications.
# contains notifications related urls.
urlpatterns += patterns(
    'notifications.views',
    url(r'^api/notifications/', include('notifications.urls')),
)

# urls from my_messages.
# contains my_messages related urls.
urlpatterns += patterns(
    'my_messages.views',
    url(r'^api/messages/', include('my_messages.urls')),
)

# urls from links.
# contains links related urls.
urlpatterns += patterns(
    'links.views',
    url(r'^api/links/', include('links.urls')),
)

# urls from organizations.
# contains organizations related urls.
urlpatterns += patterns(
    'organizations.views',
    url(r'^api/organizations/', include('organizations.urls')),
)

urlpatterns += (
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
)

urlpatterns += staticfiles_urlpatterns()






