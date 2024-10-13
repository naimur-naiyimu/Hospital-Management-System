#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE=Config.settings.production
pip install -r requirements/development.txt
echo "Collecting static files..."
python manage.py collectstatic --no-input
echo "Static files collected."
python manage.py migrate
if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi
