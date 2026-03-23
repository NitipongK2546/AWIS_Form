from users.permissions import perms

class AWISPermissions:
    permissison_list : list[tuple] = []

    def __init__(self):
        self.permissison_list.extend(
            perms.all_permissions
        )
    
    def __len__(self):
        return len(self.permissison_list)
    
    def __str__(self):
        return f"All Permissions: {len(self)}"
    
    def getPermissions(self):
        return self.permissison_list

##############################################

permissions = AWISPermissions()

# print(permissions.getPermissions())

