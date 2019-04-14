from __future__ import absolute_import

import os
from .settings import *
import dj_database_url

DEBUG = False
# Required env var
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=600)

DATABASES = {
    'default': db_from_env
}

OAUTH2_CLIENT_REDIRECT_PATH = (
    'https://googlefusion.herokuapp.com/oauth2callback'
)

# Serving static files with whitenoise
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

SITE_NAME = 'googlefusion.herokuapp.com'
SITE_DOMAIN = 'googlefusion.herokuapp.com'

# From registration email
REGISTRATION_DEFAULT_FROM_EMAIL = 'django_google@yahoo.com'
DEFAULT_FROM_EMAIL = REGISTRATION_DEFAULT_FROM_EMAIL
# Set the email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Email connect to host
EMAIL_HOST = 'smtp.mail.yahoo.com'
# Email port
EMAIL_PORT = 587
# Email user to send the mail from
EMAIL_HOST_USER = 'django_google@yahoo.com'
# Email user password
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
# Enable TLS
EMAIL_USE_TLS = True
