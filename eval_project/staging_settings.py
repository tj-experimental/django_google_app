from .settings import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['gogglefusion.herokuapp.com']

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

OAUTH2_CLIENT_REDIRECT_PATH = (
    'https://gogglefusion.herokuapp.com/oauth2callback')

# Serving static files with whitenoise
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

SITE_NAME = 'gogglefusion.herokuapp.com'
SITE_DOMAIN = 'gogglefusion.herokuapp.com'

# From registration email
REGISTRATION_DEFAULT_FROM_EMAIL = 'django_google@yahoo.com'
# Set the email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Email connect to host
EMAIL_HOST = 'smtp.mail.yahoo.com'
# Email port
EMAIL_PORT = 587
# Email user to send the mail from
EMAIL_HOST_USER = 'django_google@yahoo.com'
# Email user password
EMAIL_HOST_PASSWORD = 'rtlfjdckpeltxusf'
# Enable TLS
EMAIL_USE_TLS = True
