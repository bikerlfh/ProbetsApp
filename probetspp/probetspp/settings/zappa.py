from .common import *
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME', 'probets_pp'),
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'postgres'),
        'HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
ROOT_URLCONF = f'{SITE_NAME}.urls'
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
    integrations=[AwsLambdaIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    environment=os.getenv('ENVIRONMENT', 'alpha')
)
