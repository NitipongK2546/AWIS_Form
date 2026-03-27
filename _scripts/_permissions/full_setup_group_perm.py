from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

from awis_custom_settings import settings, default_perms

from users import PermissionList, PermissionType, perm_str
from users.permissions import AWISPermissions, PermissionList, PermissionType, creation

for name in PermissionList:
    ct = creation.createContentType(name)

    for perm in PermissionType:
        creation.createPermissionObj(ct, perm, name)

for role in settings.RoleList:
    role_group, created = Group.objects.get_or_create(
        name=role.value
    )
    default_permissions = default_perms.get_perm_objs(role.name)

    for item in default_permissions:
        role_group.permissions.add(item)

# employee_group.permissions.add