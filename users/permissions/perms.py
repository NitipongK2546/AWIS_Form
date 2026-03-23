from .base import BasePerms, PermissionType
from awis_custom_settings.settings import PermissionList

def getAllPermissions(name : PermissionList = None, type : PermissionType = None, ):
    output_list = []

    for perm in PermissionList:
        if not (name == perm):
            continue
        output_list.extend(BasePerms(perm.value).get())

    return output_list

def _returnPermissionString(type : PermissionType, name : PermissionList):
    source = "users"
    return f"{source}.{type.value}_{name.value}"

def perm_str(type : PermissionType, name : PermissionList):
    return _returnPermissionString(type, name)