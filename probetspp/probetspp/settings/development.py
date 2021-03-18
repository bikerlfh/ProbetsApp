from .common import *

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
# For demo purposes only. Use a white list in the real world.
CORS_ORIGIN_ALLOW_ALL = True
SHELL_PLUS = "ipython"
THIRD_PARTY_APPS += ['django_extensions']
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS  # noqa

STATIC_URL = 'http://192.168.0.10:8000/static/'
STATIC_ROOT = "/var/probetspp/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

