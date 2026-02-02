from .common import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME', 'probets_pp'),
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'postgres'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

DEBUG = True
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
ROOT_URLCONF = f'{SITE_NAME}.urls'

# CORS configuration - only set CORS_ALLOWED_ORIGINS if we have valid origins
# If ALLOWED_HOSTS contains '*', use CORS_ORIGIN_ALLOW_ALL instead
if '*' in ALLOWED_HOSTS or not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    CORS_ORIGIN_ALLOW_ALL = True
else:
    # Convert hosts to proper CORS origins (add http:// if no scheme)
    CORS_ALLOWED_ORIGINS = [
        origin if origin.startswith('http://') or origin.startswith('https://') 
        else f'http://{origin}' 
        for origin in ALLOWED_HOSTS if origin.strip()
    ]

# STATICS AND MEDIA FILES
#AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_FILES')
#AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#STATICFILES_LOCATION = 'static'
#STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/"
#STATICFILES_STORAGE = 'custom_storages.StaticStorage'
#MEDIAFILES_LOCATION = 'media'
#DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'


sentry_sdk.init(
    dsn=os.getenv('SENTRY_URL'),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    environment=os.getenv('ENVIRONMENT', 'alpha')
)
