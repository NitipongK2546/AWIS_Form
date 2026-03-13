from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

employee_group, created = Group.objects.get_or_create(name='Employee')
manager_group, created = Group.objects.get_or_create(name='Manager')
director_group, created = Group.objects.get_or_create(name='Director')
system_admin_group, created = Group.objects.get_or_create(name='System Admin')

outside_group, created = Group.objects.get_or_create(name='Outside')

###############################################################################

awaitform_content = ContentType.objects.get(app_label="dashboard", model="formawaitingapproval")

reqform_content = ContentType.objects.get(app_label="dashboard", model="visualreqformdata")

warrant_content = ContentType.objects.get(app_label="dashboard", model="visualwarrantdata")

###############################################################################

permission_awaitform = Permission.objects.filter(
    content_type=awaitform_content
)

# employee_group.permissions.add