# # from .settings import RoleList
# # from enum import Enum
# import csv

# # from users.permissions import perm_str
# # from users.permissions import PermissionList
# # from users.permissions import PermissionType

# # from django.contrib.contenttypes.models import ContentType
# # from django.contrib.auth.models import Permission

# # class PermissionTypeNum(Enum):
# #     T.CREATE = 16
# #     T.

# def getBinaryString(number : int):
#     return f"{number:b}"

# # def handleEachBit(binary_string : str, ):
# #     for bit, perm_type in zip(binary_string, PermissionType):
# #         if bit == "1":
# #             codename = perm_str(perm_type,)

# # def get_perm(role : RoleList):
# #     return DefaultPermission[role]

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


# # class DefaultPermission(Enum):
# #     OUTSIDE = [
# #             perm(T.EDIT, N.REQFORM_SUBMITTED),
# #         ]
# #     EMPLOYEE = [
# #             perm(T.VIEW, N.REQFORM_AWAIT_APPROVAL),
# #         ]
# #     MANAGER = [
# #             perm(T.EDIT, N.REQFORM_SUBMITTED),
# #         ]
# #     DIRECTOR = [
# #             perm(T.EDIT, N.REQFORM_SUBMITTED),
# #         ]

# #     SYSTEM_ADMIN = [
# #             perm(T.EDIT, N.REQFORM_SUBMITTED),
# #         ]

