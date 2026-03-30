from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

from awis_custom_settings import settings, default_perms

from users import PermissionList, PermissionType, perm_str
from users.permissions import AWISPermissions, PermissionList, PermissionType, creation, perm_str_list

from users.models import PathPermission

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


instance, created = PathPermission.objects.get_or_create(pk=1)

instance.set_perms(
    "create_reqform", perm_str_list([PermissionType.VIEW, PermissionType.CREATE,], PermissionList.REQFORM_AWAIT_APPROVAL)
)
instance.set_perms(
    "approve_reqform", perm_str_list([PermissionType.VIEW, PermissionType.APPROVE], PermissionList.REQFORM_AWAIT_APPROVAL)
)

print(PathPermission.of_view("create_reqform"))
print(PathPermission.of_view("approve_reqform"))
