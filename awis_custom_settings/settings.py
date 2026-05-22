from enum import Enum
from django.db import models


# เพิ่มตามที่ต้องการ
class PermissionList(models.TextChoices):

    # Admin => 1000
    ADMIN_PANEL             = "adminPanel"          # 1100
    USER_ACCESS             = "userAccess"          # 1200
    LOG_ACCESS              = "logAccess"           # 1300
    
    ADMIN_ROLE              = "adminRole"           # 1410
    USER_ROLE               = "userRole"            # 1420

    COURT_LIST              = "courtList"            # 1500
    API_KEY                 = "apiKey"               # 1600

    # Form => 2000
    REQFORM_DRAFT           = "reqformDraft"        # 2100
    REQFORM_AWAIT_APPROVAL  = "reqformAwaitApproval"# 2200
    REQFORM_SUBMITTED       = "reqformSubmitted"    # 2300
    REPORT_WARRANT_ARREST   = "reportWarrantArrest" # 2400
    
    # Login => 3000
    LOGIN_PAGE              = "loginPage"           # 3100
    JWT_ENDPOINT            = "jwtEndpoint"         # 3200

    # Statistic => 4000
    STATISTICS              = "statisticsPage"

# class PermissionCode(models.TextChoices):
PERMISSION_CODE = {
    # Admin => 1000
    PermissionList.ADMIN_PANEL             : "1100",
    PermissionList.USER_ACCESS             : "1110",  
    PermissionList.LOG_ACCESS              : "1120",   
    PermissionList.ADMIN_ROLE              : "1130",   
    PermissionList.USER_ROLE               : "1140",    
    PermissionList.COURT_LIST              : "1150",   
    PermissionList.API_KEY                 : "1160",    

    # Form => 2000
    PermissionList.REQFORM_DRAFT           : "2100",   
    PermissionList.REQFORM_AWAIT_APPROVAL  : "2200",   
    PermissionList.REQFORM_SUBMITTED       : "2300",   
    PermissionList.REPORT_WARRANT_ARREST   : "2400",   
    
    # Login => 3000
    PermissionList.LOGIN_PAGE              : "3100",
    PermissionList.JWT_ENDPOINT            : "3200",

    # Statistic => 4000
    PermissionList.STATISTICS              : "4100",
}

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
    
    def getSystemAdminRoleValue():
        return RoleList.SYSTEM_SUPERADMIN.value

class RoleChoices(models.IntegerChoices):

    EMPLOYEE = (10, RoleList.EMPLOYEE.value) 
    APPROVER = (11, RoleList.APPROVER.value) 
    BRANCH_ADMIN = (12, RoleList.BRANCH_ADMIN.value) 

    SYSTEM_SUPERADMIN = (99, RoleList.SYSTEM_SUPERADMIN.value)
    COURT_USER = (98, RoleList.COURT_USER.value)