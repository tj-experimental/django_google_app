"""
WSGI config for eval_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

production = os.environ.get('PRODUCTION', False)
staging = os.environ.get('STAGING', False)

# This should be set depending on the context.
if production:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'eval_project.production_settings'
elif staging:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'eval_project.staging_settings'
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'eval_project.settings'

application = get_wsgi_application()

if staging or production:
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(application)

