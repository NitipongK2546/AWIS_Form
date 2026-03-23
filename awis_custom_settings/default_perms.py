from .settings import RoleList
from enum import Enum
from users.permissions import perm_str, PermissionType, PermissionList

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class DefaultPermission(Enum):
    OUTSIDE = "Outside"

    EMPLOYEE = "Employee"
    MANAGER = "Manager"
    DIRECTOR = "Director"

    SYSTEM_ADMIN = "System Admin"


def get_perm(role : RoleList):
    return DefaultPermission[role]