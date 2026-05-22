from .settings import RoleList
from enum import Enum
import csv

from users.permissions import perm_str, perm_str_list, perm_str_list_of_all
from users.permissions import PermissionList as N
from users.permissions import PermissionType as T

# from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

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

##################################################################

class DefaultPermission(Enum):

    COURT_USER = [
        perm_str(T.EDIT, N.REQFORM_SUBMITTED),
    ]

    #####################################################################

    WEBHOOK_USER = [
        perm_str(T.DELETE, N.USER_ACCESS),
    ]

    #####################################################################

    EMPLOYEE = perm_str_list(
        [T.VIEW, T.CREATE, T.EDIT, T.DELETE, T.APPROVE], 
        N.REQFORM_DRAFT
    ) + perm_str_list(
        [T.VIEW, T.CREATE, T.EDIT, T.DELETE], 
        N.REQFORM_AWAIT_APPROVAL
    ) + perm_str_list(
        [T.VIEW, T.CREATE, T.DELETE], 
        N.REQFORM_SUBMITTED
    ) + perm_str_list(
        [T.VIEW, T.CREATE, T.EDIT, T.DELETE, T.APPROVE], 
        N.REPORT_WARRANT_ARREST
    )

    APPROVER = perm_str_list_of_all(
        [T.VIEW, T.CREATE, T.EDIT, T.DELETE, T.APPROVE],
        [
            N.REQFORM_DRAFT, 
            N.REQFORM_AWAIT_APPROVAL,
            N.REPORT_WARRANT_ARREST,
        ]
    ) + perm_str_list(
        [T.VIEW, T.CREATE, T.DELETE], 
        N.REQFORM_SUBMITTED
    )

    BRANCH_ADMIN = perm_str_list_of_all(
        [T.VIEW, T.CREATE, T.EDIT, T.DELETE, T.APPROVE],
        [
            N.ADMIN_PANEL,
            N.USER_ROLE, 
            N.USER_ACCESS,  
            N.LOG_ACCESS,
            N.API_KEY,
            N.COURT_LIST,

            N.REQFORM_DRAFT, 
            N.REQFORM_AWAIT_APPROVAL,
            N.REPORT_WARRANT_ARREST,
        ]
    ) + perm_str_list(
        [T.VIEW, T.CREATE, T.DELETE], 
        N.REQFORM_SUBMITTED
    ) + perm_str_list(
        [T.VIEW,], 
        N.STATISTICS,
    )


    SYSTEM_SUPERADMIN = perm_str_list_of_all(
        [T.VIEW, T.CREATE, T.EDIT, T.DELETE, T.APPROVE],
        [
            N.ADMIN_PANEL,
            N.USER_ROLE, 
            N.USER_ACCESS, 
            N.LOG_ACCESS,
            N.ADMIN_ROLE,
            N.API_KEY,
            N.COURT_LIST,
        ]
    )
# for perm in DefaultPermission:
#     print(perm.value)