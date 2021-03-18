from .common import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

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
DEBUG = True
# For demo purposes only. Use a white list in the real world.
CORS_ORIGIN_ALLOW_ALL = True
SHELL_PLUS = "ipython"
THIRD_PARTY_APPS += ['django_extensions']
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS  # noqa

# STATIC_URL = 'http://192.168.0.10:8000/static/'
# STATIC_ROOT = "/tmp/probetspp/static/"
# STATICFILES_DIRS = [
#     '/tmp/probetspp/',
# ]

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

