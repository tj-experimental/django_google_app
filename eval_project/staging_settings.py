from .settings import *
import dj_database_url


# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# Serving static files with whitenoise
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
