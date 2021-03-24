#!/bin/sh

set -e
python probetspp/manage.py collectstatic --noinput --settings=probetspp.settings.production
#uwsgi --socket :8000 --master --enable-threads --module probetspp.probetspp.wsgi:application
gunicorn -c config/gunicorn/conf.py --bind 0.0.0.0:8000 --chdir probetspp probetspp.wsgi:application