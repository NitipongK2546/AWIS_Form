from django.contrib.auth.models import Group

employee_group, created = Group.objects.get_or_create(name='Employee')
manager_group, created = Group.objects.get_or_create(name='Manager')
director_group, created = Group.objects.get_or_create(name='Director')
system_admin_group, created = Group.objects.get_or_create(name='System Admin')

outside_group, created = Group.objects.get_or_create(name='Outside')