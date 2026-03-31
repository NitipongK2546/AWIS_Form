import functools
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType
from users.permissions import PermissionList, PermissionType, perm_str_list

def perm_req_log(perm_list : list[PermissionType], system : PermissionList,):
    def decorator(view_func):
        decorated_view = permission_required(perm_str_list(perm_list, system), raise_exception=True)(view_func)

        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                return decorated_view(request, *args, **kwargs)
            except PermissionDenied:
                
                deny_reason = ["Lack Required Permission of",]
                deny_reason.extend(perm_list)

                FileLogger.createAccessDeniedLog(request, AccessType.VIEW, system, deny_reason)

                raise

        return _wrapped_view
    
    return decorator
