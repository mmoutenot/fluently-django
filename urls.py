import settings

from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', include('apps.face.urls')),
                       url(r'^face/', include('apps.face.urls')),
                       url(r'^space/', include('apps.space.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url("", include('django_socketio.urls')),
)
