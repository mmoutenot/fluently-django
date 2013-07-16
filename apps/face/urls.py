import settings

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'apps.face.views.splash'),
                       url(r'^about/$', 'apps.face.views.about'),
                       url(r'^how/$', 'apps.face.views.how'),
                       url(r'^privacy/$', 'apps.face.views.privacy'),
                       url(r'^handle_signin/$', 'apps.face.views.handle_signin'),
                       url(r'^signin/$', 'apps.face.views.signin'),
                       url(r'^student/$', 'apps.face.views.student_account_handler'),
                       url(r'^register/$', 'apps.face.views.register'),
                       url(r'^register/register_blocks', 'apps.face.views.register_blocks'),
                       url(r'^register/emailed', 'apps.face.views.register_emailed'),
                       url(r'^confirm/$', 'apps.face.views.confirm'),
                       url(r'^confirm/user', 'apps.face.views.confirm_user'),
                       url(r'^confirm/password', 'apps.face.views.confirm_password'),
                       url(r'^confirm/confirm_blocks', 'apps.face.views.confirm_blocks'),
                       url(r'^register/student/$', 'apps.face.views.register_student'),
                       url(r'^register/student/student_blocks', 'apps.face.views.register_student_blocks'),
                       url(r'^register/account_handler', 'apps.face.views.register_account_handler'),
)
