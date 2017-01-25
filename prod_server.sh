python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --no-input && gunicorn -D -w 3 -b 0.0.0.0:8000 config.wsgi:application --reload
