from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'fluently',            # Or path to database file if using sqlite3.
    'USER': 'fluently',            # Not used with sqlite3.
    'PASSWORD': 'password',          # Not used with sqlite3.
    'HOST': '0.0.0.0',            # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',            # Set to empty string for default. Not used with sqlite3.
  }
}

SEND_BROKEN_LINK_EMAILS = True

ALLOWED_HOSTS = ['fluentlynow.com']
