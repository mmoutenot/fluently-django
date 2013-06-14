import settings

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'apps.face.views.main'),
                       url(r'^signin/', 'apps.face.views.signin'),
                       url(r'^signin_user/', 'apps.face.views.signin_user'),
                       url(r'^register/$', 'apps.face.views.register_user'),
                       url(r'^register/register_blocks', 'apps.face.views.register_blocks'),
                       url(r'^register/account_handler', 'apps.face.views.register_account_handler'),
)
