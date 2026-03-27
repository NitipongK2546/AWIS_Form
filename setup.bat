@echo off

python --version

python manage.py makemigrations
python manage.py migrate

@REM python manage.py collectstatic

python manage.py shell < "_scripts\_setup_start.py"

pause