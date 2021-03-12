#!/bin/bash
source /var/app/venv/*/bin/activate
cd /var/app/staging
python probetspp/manage.py qcluster --settings=probetspp.probetspp.settings.production