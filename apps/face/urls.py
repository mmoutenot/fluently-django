import settings

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'apps.face.views.main'),
                       url(r'^login/', 'apps.face.views.login_user'),
                       url(r'^register/$', 'apps.face.views.register_user'),
                       url(r'^register/account_handler', 'apps.face.views.register_account_handler'),
)
