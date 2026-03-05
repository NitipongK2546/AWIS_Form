import os
import django
from django.contrib.contenttypes.models import ContentType
from dashboard.models import FormApprovalDataContainer
from django.contrib.auth.models import Group, Permission

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "awis.settings")
django.setup()

employee_group, created = Group.objects.get_or_create(name='Employee')
manager_group, created = Group.objects.get_or_create(name='Manager')
director_group, created = Group.objects.get_or_create(name='Director')
system_admin_group, created = Group.objects.get_or_create(name='System Admin')

ct = ContentType.objects.get_for_model(FormApprovalDataContainer)

permission_view, success = Permission.objects.get_or_create(
    codename='can_view_form_approval_data_container',
    # name='Can view form approval data container',
    content_type=ct
)

permission_add, success = Permission.objects.get_or_create(
    codename='can_add_form_approval_data_container',
    # name='Can add form approval data container',
    content_type=ct
)

permission_update, success = Permission.objects.get_or_create(
    codename='can_change_form_approval_data_container',
    # name='Can change form approval data container',
    content_type=ct
)

permission_delete, success = Permission.objects.get_or_create(
    codename='can_delete_form_approval_data_container',
    # name='Can delete form approval data container',
    content_type=ct
)

permission_approve, success = Permission.objects.get_or_create(
    codename='can_approve_form',
    # name='Can approve form', 
    content_type=ct
)

emp_perm = [permission_view, permission_update, permission_delete, permission_add]

dir_perm = [permission_view, permission_update, permission_delete, permission_add, permission_approve]

for perm in emp_perm:
    employee_group.permissions.add(perm)

print("ADDED EMPLOYEE PERMISSIONS")

for perm in dir_perm:
    director_group.permissions.add(perm)

print("ADDED DIRECTOR PERMISSIONS")