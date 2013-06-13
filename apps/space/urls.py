import settings

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'apps.space.views.dispatch'),
                       url(r"^(?P<space_url_id>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})/", 'apps.space.views.main'),
                       url(r'^upload/', 'apps.space.views.upload'),
                       url(r'^account/', 'apps.space.views.account'),
)
