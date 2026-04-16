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
    """
    Example:\n
    perm_str(PermissionType.VIEW, PermissionList.ADMIN_PANEL)\n
    Result:\n
    users.(type)_(list)
    """
    return _returnPermissionString(type, name)

def perm_str_list(type_list : list[PermissionType], name : PermissionList):
    """
    Example:\n
    perm_str(PermissionType.VIEW, PermissionList.ADMIN_PANEL)\n
    Result:\n
    [users.(type1)_(list), users.(type2)_(list), ...]
    """

    output_list : list[str] = []

    for type in type_list:
        output_list.append(
            _returnPermissionString(type, name)
        )

    return output_list