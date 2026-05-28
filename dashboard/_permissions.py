from users.permissions import PermissionList, PermissionType
from _log_utils.file_logger import AccessType

DASHBOARD_PAGE = (
    [PermissionType.VIEW,], 
    PermissionList.DASHBOARD, 
    AccessType.VIEW
)

REQFORM_AWAIT_APPROVAL_PAGE = (
    [PermissionType.VIEW, PermissionType.APPROVE], 
    PermissionList.REQFORM_AWAIT_APPROVAL, 
    AccessType.VIEW
)

APPROVE_REQFORM = (
    [PermissionType.APPROVE], 
    PermissionList.REQFORM_AWAIT_APPROVAL, 
    AccessType.APPROVE
)

REJECT_REQFORM = (
    [PermissionType.APPROVE], 
    PermissionList.REQFORM_AWAIT_APPROVAL, 
    AccessType.REJECT
)

CANCEL_REQFORM = (
    [PermissionType.DELETE], 
    PermissionList.REQFORM_AWAIT_APPROVAL, 
    AccessType.DELETE
)

##########################################################################

REQFORM_SUBMITTED_PAGE = (
    [PermissionType.VIEW], 
    PermissionList.REQFORM_SUBMITTED,
    AccessType.VIEW
)


WARRANT_SUBMITTED_PAGE = (
    [PermissionType.VIEW], 
    PermissionList.REQFORM_SUBMITTED, 
    AccessType.VIEW
)

DELETE_REQFORM_SUBMITTED = (
    [PermissionType.DELETE], 
    PermissionList.REQFORM_SUBMITTED, 
    AccessType.DELETE
)

##########################################################################

CREATE_REPORT_WARRANT_SUBMITTED = (
    [
        PermissionType.VIEW, 
        PermissionType.EDIT, 
        PermissionType.CREATE, 
        PermissionType.APPROVE
    ], 
    PermissionList.REPORT_WARRANT_ARREST, 
    AccessType.CREATE
)

VIEW_REQFORM_DETAILS = (
    [PermissionType.VIEW], 
    PermissionList.REQFORM_AWAIT_APPROVAL,
    AccessType.VIEW
)

##########################################################################

DOWNLOAD_REQFORM = (
    [PermissionType.VIEW], 
    PermissionList.REQFORM_SUBMITTED,
    AccessType.DOWNLOAD
)

DOWNLOAD_WARRANT = (
    [PermissionType.VIEW], 
    PermissionList.REQFORM_SUBMITTED,
    AccessType.DOWNLOAD
)

##########################################################################

VIEW_STATISTIC_PAGE = (
    [PermissionType.VIEW], 
    PermissionList.STATISTICS,
    AccessType.VIEW
)