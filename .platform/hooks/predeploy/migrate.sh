#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/staging
if [[ "$EB_IS_COMMAND_LEADER" == "true" ]]; then
    # leader
    python probetspp/manage.py migrate --settings=probetspp.probetspp.settings.custom_manager --pythonpath /var/app/current/ --noinput
fi