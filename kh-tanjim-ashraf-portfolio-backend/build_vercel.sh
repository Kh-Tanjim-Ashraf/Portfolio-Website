#!/bin/bash

# Install the dependencies
pip install -r requirements.txt

# Let Django generate the static files (CSS, javascript, images & fonts)
python manage.py collectstatic --noinput
