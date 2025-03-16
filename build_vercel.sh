#!/bin/bash
pip install -r requirements.txt
python -c "import django; django.setup(); from django.core.management import call_command; call_command('collectstatic', '--noinput')" 