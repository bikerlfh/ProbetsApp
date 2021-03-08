"""
WSGI config for probetspp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from probetspp.probetspp.settings.common import SITE_NAME
from django.core.wsgi import get_wsgi_application

settings_module = f'{SITE_NAME}.{SITE_NAME}.settings.production'
os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
"""
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'probetspp.settings'
)
"""

application = get_wsgi_application()
os.environ['DJANGO_SETTINGS_MODULE'] = f'{SITE_NAME}.settings.production'