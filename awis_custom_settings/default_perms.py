from .settings import RoleList
from enum import Enum
from users.permissions import perm_str as perm
from users.permissions import PermissionList as N
from users.permissions import PermissionType as T

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

# class DefaultPermission(Enum):
#     OUTSIDE = [
#             perm(T.EDIT, N.REQFORM_SUBMITTED),
#         ]
#     EMPLOYEE = [
#             perm(T.VIEW, N.REQFORM_AWAIT_APPROVAL),
#         ]
#     MANAGER = [
#             perm(T.EDIT, N.REQFORM_SUBMITTED),
#         ]
#     DIRECTOR = [
#             perm(T.EDIT, N.REQFORM_SUBMITTED),
#         ]

#     SYSTEM_ADMIN = [
#             perm(T.EDIT, N.REQFORM_SUBMITTED),
#         ]


# def get_perm(role : RoleList):
#     return DefaultPermission[role]