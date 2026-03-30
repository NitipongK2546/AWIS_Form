from .settings import RoleList
from enum import Enum
import csv

from users.permissions import perm_str, perm_str_list
from users.permissions import PermissionList as N
from users.permissions import PermissionType as T

# from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

# class PermissionTypeNum(Enum):
#     T.CREATE = 16
#     T.

def getBinaryString(number : int):
    return f"{number:b}"

# def handleEachBit(binary_string : str, ):
#     for bit, perm_type in zip(binary_string, PermissionType):
#         if bit == "1":
#             codename = perm_str(perm_type,)

def get_perm(role : RoleList) -> list[str]:
    return DefaultPermission[role].value

def get_perm_objs(role : RoleList) -> list[Permission]:
    perm_obj_list : list[Permission] = []
    
    all_perms = get_perm(role)
    for perm in all_perms:

        app_label, codename = perm.split(".")

        perm_obj = Permission.objects.filter(
            content_type__app_label=app_label,
            codename=codename
        ).first()

        if perm_obj:
            perm_obj_list.append(perm_obj.pk)

    return perm_obj_list


# PERMISSION_PATH = "awis_custom_settings/permission.csv"

# try:
#     with open(PERMISSION_PATH, mode='r', newline='', encoding='utf-8') as file: 
#         csv_reader = csv.reader(file, delimiter=',')

#         for row in csv_reader:
#             if row[0] == "STOP":
#                 break

#             print(row)

# except Exception as e:
#     print(e)


class DefaultPermission(Enum):
    OUTSIDE = [
            perm_str(T.EDIT, N.REQFORM_SUBMITTED),
        ]
    EMPLOYEE = perm_str_list(
        [T.VIEW, T.CREATE, T.EDIT, T.DELETE], 
        N.REQFORM_AWAIT_APPROVAL
    )
    
    MANAGER = []

    DIRECTOR = perm_str_list(
        [T.VIEW, T.CREATE, T.EDIT, T.DELETE, T.APPROVE], 
        N.REQFORM_AWAIT_APPROVAL
    )

    SYSTEM_ADMIN = perm_str_list(
        [T.VIEW, T.CREATE, T.EDIT, T.DELETE, T.APPROVE], 
        N.ADMIN_PANEL
    )

# for perm in DefaultPermission:
#     print(perm.value)