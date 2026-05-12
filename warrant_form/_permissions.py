from users.permissions import PermissionList, PermissionType
from _log_utils.file_logger import AccessType

CREATE_DRAFT = (
    [PermissionType.CREATE], 
PermissionList.REQFORM_DRAFT, 
AccessType.CREATE
)

VIEW_DRAFT = (
    [PermissionType.VIEW], 
PermissionList.REQFORM_DRAFT, 
AccessType.VIEW
)

DELETE_DRAFT = (
    [PermissionType.DELETE], 
PermissionList.REQFORM_DRAFT, 
AccessType.DELETE
)

EDIT_DRAFT = (
    [PermissionType.EDIT], 
PermissionList.REQFORM_DRAFT, 
AccessType.EDIT
)

# EDIT_DRAFT_WARRANT = (
#     [PermissionType.DELETE, PermissionType.EDIT], 
# PermissionList.REQFORM_DRAFT, 
# AccessType.DELETE
# )

############################################################

CREATE_REQFORM = (
    [PermissionType.CREATE], 
PermissionList.REQFORM_AWAIT_APPROVAL, 
AccessType.CREATE
)

VIEW_REQFORM = (
    [PermissionType.VIEW], 
PermissionList.REQFORM_AWAIT_APPROVAL,
AccessType.VIEW
)

EDIT_REQFORM = (
    [PermissionType.EDIT], 
PermissionList.REQFORM_AWAIT_APPROVAL, 
AccessType.EDIT
)

DELETE_REQFORM = (
    [PermissionType.DELETE], 
PermissionList.REQFORM_AWAIT_APPROVAL, 
AccessType.DELETE)

# _REQFORM = (
#     [PermissionType.CREATE], 
# PermissionList.REQFORM_AWAIT_APPROVAL, 
# AccessType.CREATE)

# _REQFORM = (
#     [PermissionType.CREATE], 
# PermissionList.REQFORM_AWAIT_APPROVAL, 
# AccessType.CREATE)

# _REQFORM = (
#     [PermissionType.CREATE], 
# PermissionList.REQFORM_AWAIT_APPROVAL, 
# AccessType.CREATE)

# _REQFORM = (
#     [PermissionType.CREATE], 
# PermissionList.REQFORM_AWAIT_APPROVAL, 
# AccessType.CREATE)
