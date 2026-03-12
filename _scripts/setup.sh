#!/bin/bash

# Exit on error
set -o errexit

DIR="$(cd "$(dirname "$0")" && pwd)"

python --version

# "$DIR/print_dir.sh"

# Start by migrating...
"$DIR/quick_migrate.sh"

python manage.py shell < "$DIR/full_setup_group_perm.py"

# Add collectstatic later if we have to.
#
# python manage.py collectstatic --no-input
#
# I'll need to add STATIC_ROOT later.

export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=adminpass999999

python manage.py createsuperuser --no-input
unset DJANGO_SUPERUSER_USERNAME DJANGO_SUPERUSER_EMAIL DJANGO_SUPERUSER_PASSWORD

