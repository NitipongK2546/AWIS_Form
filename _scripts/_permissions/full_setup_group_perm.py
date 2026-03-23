from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

from awis_custom_settings import settings

for role in settings.RoleList:
    role_group, created = Group.objects.get_or_create(
        name=role.value
    )

###############################################################################

permission_ct = ContentType.objects.get(app_label="users", model="permissionlist")

###############################################################################

permission_awaitform = Permission.objects.filter(
    content_type=permission_ct
)

# employee_group.permissions.add