import os
import django
from django.contrib.contenttypes.models import ContentType
from dashboard.models import VisualFormApprovalData, VisualFinalizedFormData
from django.contrib.auth.models import Group, Permission

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_awis.settings")
django.setup()

employee_group, created = Group.objects.get_or_create(name='Employee')
manager_group, created = Group.objects.get_or_create(name='Manager')
director_group, created = Group.objects.get_or_create(name='Director')
system_admin_group, created = Group.objects.get_or_create(name='System Admin')

outside_group, created = Group.objects.get_or_create(name='Outside')

ct = ContentType.objects.get_for_model(VisualFormApprovalData)

permission_view, success = Permission.objects.get_or_create(
    codename='can_view_visual_form_approval_data',
    # name='Can view form approval data container',
    content_type=ct
)

permission_add, success = Permission.objects.get_or_create(
    codename='can_add_visual_form_approval_data',
    # name='Can add form approval data container',
    content_type=ct
)

permission_update, success = Permission.objects.get_or_create(
    codename='can_change_visual_form_approval_data',
    # name='Can change form approval data container',
    content_type=ct
)

permission_delete, success = Permission.objects.get_or_create(
    codename='can_delete_visual_form_approval_data',
    # name='Can delete form approval data container',
    content_type=ct
)

permission_approve, success = Permission.objects.get_or_create(
    codename='can_approve_visual_form_approval_data',
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

# for perm in dir_perm:
#     outside_group.permissions.add(perm)

# print("ADDED OUTSIDE PERMISSIONS")