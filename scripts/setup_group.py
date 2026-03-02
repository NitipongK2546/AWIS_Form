import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "awis.settings")
django.setup()

from django.contrib.auth.models import Group

new_group, created = Group.objects.get_or_create(name='Employee')
new_group, created = Group.objects.get_or_create(name='Manager')
new_group, created = Group.objects.get_or_create(name='Director')
new_group, created = Group.objects.get_or_create(name='System Admin')