#!/usr/bin/env bash

# Build script used to deploy in "Render"

# Exit on error
set -o errexit

# Install packages
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files for DRF dashboard & Django admin panel styling
python manage.py collectstatic --noinput
