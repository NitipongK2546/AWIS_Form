from enum import Enum
from django.db import models


# เพิ่มตามที่ต้องการ
class PermissionList(models.TextChoices):

    ADMIN_PANEL = "adminPanel"
    USER_ACCESS = "userAccess"
    LOG_ACCESS = "logAccess"

    ADMIN_ROLE = "adminRole"
    USER_ROLE = "userRole"

    REQFORM_SUBMITTED = "reqformSubmitted"

    REQFORM_DRAFT = "reqformDraft"
    REQFORM_AWAIT_APPROVAL = "reqformAwaitApproval"

    REPORT_WARRANT_ARREST = "reportWarrantArrest"
    
    LOGIN_PAGE = "loginPage"

class RoleList(Enum):
    EMPLOYEE = "เจ้าหน้าที่"
    APPROVER = "ผู้อนุมัติ"
    BRANCH_ADMIN = "ผู้ดูแลระดับฝ่าย"
    
    SYSTEM_SUPERADMIN = "ผู้ดูแลระบบ"
    COURT_USER = "เจ้าหน้าที่ของศาล"

    def getDefaultRole():
        return RoleList.EMPLOYEE
    
    def getDefaultRoleValue():
        return RoleList.EMPLOYEE.value
    
    def getDefaultRoleChoiceAssigned():
        return RoleChoices.EMPLOYEE

class RoleChoices(models.IntegerChoices):

    EMPLOYEE = (10, RoleList.EMPLOYEE.value) 
    APPROVER = (11, RoleList.APPROVER.value) 
    BRANCH_ADMIN = (12, RoleList.BRANCH_ADMIN.value) 

    SYSTEM_SUPERADMIN = (99, RoleList.SYSTEM_SUPERADMIN.value)
    COURT_USER = (98, RoleList.COURT_USER.value)