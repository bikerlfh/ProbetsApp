#!/bin/bash
source /var/app/venv/*/bin/activate
cd /var/app/current
# python probetspp/manage.py qcluster --settings=probetspp.probetspp.settings.production --pythonpath /var/app/current/