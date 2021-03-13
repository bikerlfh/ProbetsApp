#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/staging
if [[ "$EB_IS_COMMAND_LEADER" == "true" ]]; then
    # leader
    python manage.py migrate --noinput --settings=probetspp.probetspp.custom_manager
fi