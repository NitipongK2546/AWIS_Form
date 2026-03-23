from .settings import RoleList
from enum import Enum
from users.permissions import perm_str, PermissionType, PermissionList

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

permission_ct = ContentType.objects.get(app_label="users", model="permissionlist")

permission_awaitform = Permission.objects.filter(
    content_type=permission_ct,
    codename=perm_str(
        PermissionType.VIEW
    )
)

class DefaultPermission(Enum):
    OUTSIDE = "Outside"

    EMPLOYEE = "Employee"
    MANAGER = "Manager"
    DIRECTOR = "Director"

    SYSTEM_ADMIN = "System Admin"


def get_perm(role : RoleList.name):
    return DefaultPermission[role]