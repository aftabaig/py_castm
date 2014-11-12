from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'castm.views',
    url(r'^$', 'home', name="home"))

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





