#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/staging
if [[ "$EB_IS_COMMAND_LEADER" == "true" ]]; then
    # leader
    python probetspp/manage.py migrate --settings=probetspp.probetspp.settings.production --pythonpath /var/app/staging/ --noinput
fi