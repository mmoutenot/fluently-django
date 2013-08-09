import settings

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

                  # Development Site

                  url(r'^newaccount/$', 'apps.fluently.views.newaccount'),        
                  url(r'^newaccount-handler/$', 'apps.fluently.views.newaccount_handler'),        

                  # Marketing Site
                  url(r'^$', 'apps.fluently.views.splash'),
                  url(r'^about/$', 'apps.fluently.views.about'),    
                  url(r'^for-parents/$', 'apps.fluently.views.for_parents'),
                  url(r'^faq/$', 'apps.fluently.views.faqs'),
                  url(r'^privacy/$', 'apps.fluently.views.privacy'),
                  url(r'^example-profile/$', 'apps.fluently.views.example_profile'),
                  url(r'^example-consumer-contact/$', 'apps.fluently.views.example_consumer_contact'),
                  url(r'^example-consumer-contact/blocks/$', 'apps.fluently.views.example_consumer_contact_blocks'),
                  url(r'^for-therapists/$', 'apps.fluently.views.for_therapists'),
                  url(r'^ebook/$', 'apps.fluently.views.send_ebook'),

                  # App Site
                  url(r'^sign-in/$', 'apps.fluently.views.sign_in'),
                  url(r'^sign-in/handler/$', 'apps.fluently.views.sign_in_handler'),
                  url(r'^search/$', 'apps.fluently.views.search'),
                  
                  # App Site # Search View
                  url(r'^search/$', 'apps.fluently.views.search'),
                  url(r'^search/card/$', 'apps.fluently.views.profile_card'),
                  url(r'^search/no-results/$', 'apps.fluently.views.no_results'),
                  url(r'^search/search-results/$', 'apps.fluently.views.search_results'),

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

                  url(r'^account-edit/$', 'apps.fluently.views.account_edit'),
                  url(r'^account-edit/blocks/$', 'apps.fluently.views.account_edit_blocks'),
                  url(r'^account-edit/handler/$', 'apps.fluently.views.account_edit_handler'),
                  url(r'^account-edit/options-handler-1/$', 'apps.fluently.views.account_options_handler'),
                  url(r'^account-edit/options-handler-2/$', 'apps.fluently.views.account_advanced_options_handler'),
                  url(r'^account-edit/fields-handler-1/$', 'apps.fluently.views.account_field_handler'),
                  url(r'^account-edit/fields-handler-2/$', 'apps.fluently.views.account_advanced_field_handler'),
                  url(r'^save-profile/$', 'apps.fluently.views.save_profile'),
                  url(r'^picture/$', 'apps.fluently.views.profile_picture_handler'),
                  
                  # App Site # Public Profile
                  url(r'^profile/(?P<user_url>\w{6})/$', 'apps.fluently.views.public_profile'),

                  # App Site # Public Profile # Consumer Contact
                  url(r'^consumer-contact/(?P<user_url>\w{6})/$', 'apps.fluently.views.consumer_contact'),
                  url(r'^consumer-contact/(?P<user_url>\w{6})/blocks/$', 'apps.fluently.views.consumer_contact_blocks'),
                  url(r'^consumer-contact/handler/$', 'apps.fluently.views.consumer_contact_handler'),
)

