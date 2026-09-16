#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

pip install --upgrade pip

# Let Django generate the static files (CSS, javascript, images & fonts)
python manage.py collectstatic --noinput