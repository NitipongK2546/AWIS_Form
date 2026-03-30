from enum import Enum

class PermissionType(Enum):
    VIEW = "view"
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"
    APPROVE = "approve"

class AccessType(Enum):
    VIEW = "View"
    CREATE = "Create"
    EDIT = "Edit"
    DELETE = "Delete"
    APPROVE = "Approve"
    REJECT = "Reject"
    LOGIN = "Login"

class BasePerms:
    permission_name = ""
    reqform_permissions = []

    def __init__(self, perm_name : str = "base_name"):
        self.permission_name = perm_name
        self.reqform_permissions = self.createAllPermission()

    def getPermissions(self):
        return self.reqform_permissions
    
    def get(self): #short
        return self.getPermissions()
        
    ################################################################

    def createAllPermission(self):
        return [
            self.assemblePermission(perm.value, self.permission_name) 
            for perm in PermissionType
        ]
        
    def assemblePermission(self, type : PermissionType, permission : str):
        return (f"{type}_{permission}", "")

