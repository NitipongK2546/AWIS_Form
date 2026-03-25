from enum import Enum
from django.db import models

# import enum

# # Dynamic data (e.g., from a database or external configuration)
# dynamic_data = {
#     'RED': '#FF0000',
#     'GREEN': '#00FF00',
#     'BLUE': '#0000FF'
# }

# # Create the Enum dynamically
# Color = enum.Enum('Color', dynamic_data)

# # Accessing members
# print(Color.RED)
# print(Color.RED.name)
# print(Color.RED.value)

# เพิ่มตามที่ต้องการ
class PermissionList(Enum):
    ADMIN_PANEL = "adminPanel"
    
    REQFORM_AWAIT_APPROVAL = "reqformAwaitApproval"
    REQFORM_SUBMITTED = "reqformSubmitted"

class PermissionListGrouping(Enum):
    REQFORM = [
        PermissionList.REQFORM_AWAIT_APPROVAL, 
        PermissionList.REQFORM_SUBMITTED,
    ]

class RoleList(Enum):
    OUTSIDE = "Outside"

    EMPLOYEE = "Employee"
    MANAGER = "Manager"
    DIRECTOR = "Director"

    SYSTEM_ADMIN = "System Admin"

class RoleChoices(models.IntegerChoices):
    OUTSIDE = (0, RoleList.OUTSIDE.value)

    EMPLOYEE = (10, RoleList.EMPLOYEE.value) 
    MANAGER = (11, RoleList.MANAGER.value)
    DIRECTOR = (12, RoleList.DIRECTOR.value)

    SYSTEM_ADMIN = (99, RoleList.SYSTEM_ADMIN.value)