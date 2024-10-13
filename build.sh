#!/usr/bin/env bash
# exit on error
set -o errexit

export DJANGO_SETTINGS_MODULE=Config.settings.production

# Create logs directory if it doesn't exist
mkdir -p /opt/render/project/src/logs

# Install dependencies
pip install -r requirements/development.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input
echo "Static files collected."

# Remove any lingering .map files (optional)
find /opt/render/project/src/staticfiles -name "*.map" -delete

# Apply migrations
python manage.py migrate

# Create superuser if needed
if [[ $CREATE_SUPERUSER ]]; then
  python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi
