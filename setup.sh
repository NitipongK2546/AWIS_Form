#!/bin/bash

# Exit on error
set -o errexit

pwd

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
    VENV_TYPE=bin
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
    VENV_TYPE=Scripts
else
    echo "Python not found"
    exit 1
fi

$PYTHON --version

# "$DIR/_print_dir.sh"

"./_scripts/_quick_migrate.sh"

# Add collectstatic later if we have to.
#
# python manage.py collectstatic --no-input
#
# I'll need to add STATIC_ROOT later.

# source .venv/$VENV_TYPE/activate

which $PYTHON

# Setup django server.
$PYTHON manage.py shell < "_scripts/_setup_start.py"




