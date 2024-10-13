#!/usr/bin/env bash
# exit on error
set -o errexit

mkdir -p /opt/render/project/src/logs  # Create logs directory
pip install -r requirements/development.txt
python manage.py collectstatic --no-input
python manage.py migrate
if [[ $CREATE_SUPERUSER ]]; then
  python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi
