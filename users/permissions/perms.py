from users.permissions.base import BasePerms, PermissionType
from awis_custom_settings.settings import PermissionList

def _returnAllPermissions():
    output_list = []

    for perm in PermissionList:
        output_list.extend(BasePerms(perm.value).get())

    return output_list

def _returnPermissionString(type : PermissionType, name : PermissionList):
    source = "users"
    return f"{source}.{type.value}_{name.value}"

def perm_str(type : PermissionType, name : PermissionList):
    return _returnPermissionString(type, name)

all_permissions = _returnAllPermissions()