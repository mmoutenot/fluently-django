import settings

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                  # Marketing Site
                  url(r'^$', 'apps.fluently.views.splash'),
                  url(r'^about/$', 'apps.fluently.views.about'),    
                  url(r'^how-it-works/$', 'apps.fluently.views.how_it_works'),
                  url(r'^privacy/$', 'apps.fluently.views.privacy'),

                  # App Site
                  url(r'^sign-in/$', 'apps.fluently.views.sign_in'),
                  url(r'^sign-in/handler/$', 'apps.fluently.views.sign_in_handler'),
                   
                  # App Site # Provider Signup 
                  url(r'^join/$', 'apps.fluently.views.provider_sign_up'),
                  url(r'^join/blocks/$', 'apps.fluently.views.provider_sign_up_blocks'),
                  url(r'^join/emailed/$', 'apps.fluently.views.provider_sign_up_emailed'),
                  url(r'^join/handler/$', 'apps.fluently.views.provider_sign_up_handler'),
                  url(r'^confirm/$', 'apps.fluently.views.provider_confirm'),
                  url(r'^confirm/id/$', 'apps.fluently.views.provider_confirm_id'),
                  url(r'^confirm/password/$', 'apps.fluently.views.provider_confirm_password'),
                  url(r'^confirm/blocks/$', 'apps.fluently.views.provider_confirm_blocks'),

                  # App Site # Consumer Request
                  url(r'^consumer-request/$', 'apps.fluently.views.consumer_request'),
                  url(r'^consumer-request/blocks/$', 'apps.fluently.views.consumer_request_blocks'),
                  url(r'^consumer-request/handler/$', 'apps.fluently.views.consumer_request_handler'),

                  # App Site # Personal Account
                  url(r'^account/$', 'apps.fluently.views.account'),
                  url(r'^save-profile/$', 'apps.fluently.views.save_profile'),
                  url(r'^picture/$', 'apps.fluently.views.profile_picture_handler'),
                  
                  # App Site # Public Profile
                  url(r'^profile/(?P<user_url>\w{6})/$', 'apps.fluently.views.public_profile'),

                  # App Site # Public Profile # Consumer Contact
                  url(r'^consumer-contact/(?P<user_url>\w{6})/$', 'apps.fluently.views.consumer_contact'),
                  url(r'^consumer-contact/(?P<user_url>\w{6})/blocks/$', 'apps.fluently.views.consumer_contact_blocks'),
                  url(r'^consumer-contact/handler/$', 'apps.fluently.views.consumer_contact_handler'),
)

