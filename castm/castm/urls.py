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

# urls from notifications.
# contains notifications related urls.
urlpatterns += patterns(
    'notifications.views',
    url(r'^api/notifications/', include('notifications.urls')),
)

# urls from links.
# contains links related urls.
urlpatterns += patterns(
    'links.views',
    url(r'^api/links/', include('links.urls')),
)


urlpatterns += staticfiles_urlpatterns()






