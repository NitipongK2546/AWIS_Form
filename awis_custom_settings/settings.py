from enum import Enum
from django.db import models


# เพิ่มตามที่ต้องการ
class PermissionList(models.TextChoices):

    ADMIN_PANEL = "adminPanel"

    USER_ACCESS = "userAccess"
    USER_ROLE = "userRole"

    LOG_ACCESS = "logAccess"
    
    REQFORM_AWAIT_APPROVAL = "reqformAwaitApproval"
    REQFORM_SUBMITTED = "reqformSubmitted"

    LOGIN_PAGE = "loginPage"

class RoleList(Enum):
    OUTSIDE = "Outside"

    EMPLOYEE = "Employee"
    MANAGER = "Manager"
    DIRECTOR = "Director"

    SYSTEM_ADMIN = "System Admin"

    COURT_USER = "Court User"

    def getDefaultRole():
        return RoleList.EMPLOYEE
    
    def getDefaultRoleValue():
        return RoleList.EMPLOYEE.value
    
    def getDefaultRoleChoiceAssigned():
        return RoleChoices.EMPLOYEE

class RoleChoices(models.IntegerChoices):
    OUTSIDE = (0, RoleList.OUTSIDE.value)

    EMPLOYEE = (10, RoleList.EMPLOYEE.value) 
    MANAGER = (11, RoleList.MANAGER.value)
    DIRECTOR = (12, RoleList.DIRECTOR.value)

    SYSTEM_ADMIN = (99, RoleList.SYSTEM_ADMIN.value)
    COURT_USER = (98, RoleList.COURT_USER.value)