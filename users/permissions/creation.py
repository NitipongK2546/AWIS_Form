from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

from awis_custom_settings import settings, default_perms

from users import PermissionList, PermissionType, perm_str
from users.permissions import AWISPermissions

def createContentType(name : PermissionList):
    permission_ct, created = ContentType.objects.get_or_create(app_label="users", model=name.value)

    return permission_ct

def createPermissionObj(content_type : ContentType, perm_type : PermissionType, name : PermissionList):
    permission_obj, created = Permission.objects.get_or_create(
        content_type=content_type,
        codename=f"{perm_type.value}_{name.value}"
    )

    return permission_obj