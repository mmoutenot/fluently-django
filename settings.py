import os, sys


# ===========================
# = Directory Declaractions =
# ===========================

PROJECT_PATH 		= os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR   		= os.path.dirname(__file__)
TEMPLATE_DIRS 		= (os.path.join(CURRENT_DIR, 'templates'),)
STATICFILES_DIRS 	= (os.path.join(CURRENT_DIR, 'static'),)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'fluently',            # Or path to database file if using sqlite3.
    'USER': 'fluently',            # Not used with sqlite3.
    'PASSWORD': 'password',          # Not used with sqlite3.
    'HOST': 'localhost',            # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',            # Set to empty string for default. Not used with sqlite3.
  }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = 'media/'
MEDIA_URL = 'media/'

# STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'


STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'PLEASE_ADD_ME'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'


INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.admin',

  # vendor apps
  #'vendor.TokBox',
  #'django_socketio',
  'south',

  # fluently apps
  #'apps.space',
  #'apps.face',
  'apps.fluently'
)


LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
  'mail_admins': {
    'level': 'ERROR',
    'class': 'django.utils.log.AdminEmailHandler'
  }
  },
  'loggers': {
  'django.request': {
    'handlers': ['mail_admins'],
    'level': 'ERROR',
    'propagate': True,
  },
  }
}
