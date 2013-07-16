import settings

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'apps.space.views.dispatch'),
                       url(r"^(?P<space_url_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/", 'apps.space.views.main'),
                       url(r'^account/', 'apps.space.views.account'),
                       url(r'^profile/SLP/(?P<user_url>\w{6})/$', 'apps.space.views.public_profile'),
                       url(r'^profile/$', 'apps.space.views.profile'),
                       url(r'^contact/(?P<user_url>\w{6})/$', 'apps.space.views.contact'),
                       url(r'^contact/contact_student_blocks/$', 'apps.space.views.contact_student_blocks'),
                       url(r'^contact/SLP/$', 'apps.space.views.contact_SLP'),
                       url(r'^save_profile/', 'apps.space.views.save_profile'),
                       url(r'^picture', 'apps.space.views.profile_picture'),
                       url(r'^upload/', 'apps.space.views.upload'),
)
