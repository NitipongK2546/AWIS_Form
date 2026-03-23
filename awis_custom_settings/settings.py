from enum import Enum
from django.db import models

# เพิ่มตามที่ต้องการ
class PermissionList(Enum):
    ADMIN_PANEL = "adminPanel"
    
    REQFORM_AWAIT_APPROVAL = "reqformAwaitApproval"
    REQFORM_SUBMITTED = "reqformSubmitted"

class RoleList(Enum):
    OUTSIDE = "Outside"

    EMPLOYEE = "Employee"
    MANAGER = "Manager"
    DIRECTOR = "Director"

    SYSTEM_ADMIN = "System Admin"

class RoleChoices(models.IntegerChoices):
    OUTSIDE = (0, RoleList.OUTSIDE)

    EMPLOYEE = (10, RoleList.EMPLOYEE) 
    MANAGER = (11, RoleList.MANAGER)
    DIRECTOR = (12, RoleList.DIRECTOR)

    SYSTEM_ADMIN = (99, RoleList.SYSTEM_ADMIN)