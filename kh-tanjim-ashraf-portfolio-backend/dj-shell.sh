#!/bin/bash

VIRTUAL_ENV_DIR="./venv"
VENV_FOLDER_NAME="venv"
VENV_ACTIVATION_PATH="./$VENV_FOLDER_NAME/Scripts/activate"
REQUIREMENTS_FILE="./requirements.txt"


echo "Checking $VIRTUAL_ENV_DIR in the directory..."

if [ -d $VIRTUAL_ENV_DIR ]; then

    echo "Python virtual environment exists."

    echo "Activating python virtual environment..."

    source $VENV_ACTIVATION_PATH

else

    echo "Python virtual environment doesn't exist."
    echo "Creating python virtual environment..."

    python -m venv $VENV_FOLDER_NAME

    echo "Activating python virtual environment..."

    source $VENV_ACTIVATION_PATH

    echo "Installing the dependency packages..."

    pip install -r $REQUIREMENTS_FILE

    echo "Updating to a new release of pip..."

    python.exe -m pip install --upgrade pip

fi

python manage.py shell
