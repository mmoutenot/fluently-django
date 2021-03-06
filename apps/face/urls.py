import settings

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'apps.face.views.main'),
                       url(r'^login/', 'apps.face.views.login_user'),
                       url(r'^register/', 'apps.face.views.register_user'),
                       url(r'^getstarted/', 'apps.face.views.get_started'),
                       url(r'^welcome/', 'apps.face.views.welcome'),
)
