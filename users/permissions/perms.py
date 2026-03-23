from users.permissions.base import BasePerms, PermissionType

from enum import Enum

class PermissionList(Enum):
    ADMIN_PANEL = "adminPanel"
    
    REQFORM_AWAIT_APPROVAL = "reqformAwaitApproval"
    REQFORM_SUBMITTED = "reqformSubmitted"

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