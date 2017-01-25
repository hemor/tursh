fuser -k 8000/tcp

python manage.py makemigrations --settings=config.local_settings && python manage.py migrate --settings=config.local_settings && DJANGO_SETTINGS_MODULE=config.local_settings gunicorn -w 3 -b :8000 config.wsgi:application --reload
