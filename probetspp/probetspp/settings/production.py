from .common import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('RDS_DB_NAME'),
        'USER': os.getenv('RDS_USERNAME'),
        'PASSWORD': os.getenv('RDS_PASSWORD'),
        'HOST': os.getenv('RDS_HOSTNAME'),
        'PORT': os.getenv('RDS_PORT'),
    }
}

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
ROOT_URLCONF = f'{SITE_NAME}.{SITE_NAME}.urls'
# STATICS AND MEDIA FILES
AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_FILES')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
STATICFILES_LOCATION = 'static'
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/"
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'


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
