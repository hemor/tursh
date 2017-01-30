#!/bin/bash

VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3

source /usr/local/bin/virtualenvwrapper.sh

workon tursh

source $HOME/.bashrc

python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --no-input && gunicorn -D -w 3 -b 0.0.0.0:8000 config.wsgi:application --reload --access-logfile logs/gunicorn_access.log --error-logfile logs/gunicorn_error.log
