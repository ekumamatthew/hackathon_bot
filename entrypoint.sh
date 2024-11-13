#!/bin/bash

echo "Collecting static files"
python manage.py collectstatic --no-input

echo "Applying migrations"
python manage.py migrate

echo "Starting the server and bot..."
exec "$@"

gunicorn --bind 0.0.0.0:8000 core.wsgi:application & python manage.py run_telegram_bot