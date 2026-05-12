#!/bin/bash

# Exit on error
set -o errexit

pwd

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
    VENV_TYPE=bin

    chmod +x _scripts/_quick_migrate.sh

elif command -v python >/dev/null 2>&1; then
    PYTHON=python
    VENV_TYPE=Scripts
else
    echo "Python not found"
    exit 1
fi

$PYTHON --version

$PYTHON manage.py makemigrations
$PYTHON manage.py migrate

$PYTHON manage.py collectstatic --no-input

# Setup django server.
$PYTHON manage.py shell < "_scripts/_setup_start.py"




