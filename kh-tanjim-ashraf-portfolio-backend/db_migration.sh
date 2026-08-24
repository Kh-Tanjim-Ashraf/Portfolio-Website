#!/bin/bash

VIRTUAL_ENV_DIR="./venv"
VENV_ACTIVATION_PATH="$VIRTUAL_ENV_DIR/Scripts/activate"
SERVER_PORT=8080

echo "Activating python virtual environment..."

source $VENV_ACTIVATION_PATH

# echo "VENV Path: $VENV_ACTIVATION_PATH"

echo "Performing database migration..."

python manage.py makemigrations
python manage.py migrate

echo "Completed database migration."

echo "Spinning up the server at port $SERVER_PORT..."

python manage.py runserver $SERVER_PORT