import settings

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'apps.fluently.views.splash'),
                       url(r'^about/$', 'apps.fluently.views.about'),
                       url(r'^how-it-works/$', 'apps.fluently.views.how_it_works'),
                       url(r'^privacy/$', 'apps.fluently.views.privacy'),
                       url(r'^handle-sign-in/$', 'apps.fluently.views.handle_sign_in'),
                       url(r'^sign-in/$', 'apps.fluently.views.sign-in'),
                       url(r'^join/$', 'apps.fluently.views.provider_sign_up'),
                       url(r'^join/blocks/$', 'apps.fluently.views.provider_sign_up_blocks'),
                       url(r'^join/emailed/$', 'apps.fluently.views.provider_sign_up_emailed'),
                       url(r'^join/account-handler/$', 'apps.fluently.views.provider_request_account_handler'),
                       url(r'^confirm/$', 'apps.fluently.views.confirm'),
                       url(r'^confirm/id/$', 'apps.fluently.views.confirm_id'),
                       url(r'^confirm/password/$', 'apps.fluently.views.confirm_password'),
                       url(r'^confirm/blocks/$', 'apps.fluently.views.confirm_blocks'),
                       url(r'^consumer-request/$', 'apps.fluently.views.consumer_request'),
                       url(r'^consumer-request/blocks/$', 'apps.fluently.views.consumer_request_blocks'),
                       url(r'^consumer-request/account-handler/$', 'apps.fluently.views.consumer_request_account_handler'),
                       url(r'^account/$', 'apps.fluently.views.account'),
                       url(r'^profile/(?P<user_url>\w{6})/$', 'apps.fluently.views.profile'),
                       url(r'^consumer-contact/(?P<user_url>\w{6})/$', 'apps.fluently.views.consumer_contact'),
                       url(r'^consumer-contact/blocks/$', 'apps.fluently.views.consumer_contact_blocks'),
                       url(r'^consumer-contact/handler/$', 'apps.fluently.views.consumer_contact_handler'),
                       url(r'^save-profile/$', 'apps.fluently.views.save_profile'),
                       url(r'^picture/$', 'apps.fluently.views.profile_picture'),
                       url(r'^upload/$', 'apps.fluently.views.upload'),
)

