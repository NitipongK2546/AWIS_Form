import functools
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

# from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType
from users.permissions import PermissionList, PermissionType, perm_str_list

def perm_req_log(perm_list : list[PermissionType], system : PermissionList, access : AccessType = AccessType.VIEW):
    def decorator(view_func):
        
        @functools.wraps(view_func)
        def _wrapped_view(request : HttpRequest, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            try:
                decorated_view = permission_required(perm_str_list(perm_list, system), raise_exception=True)(view_func)
                
                result = decorated_view(request, *args, **kwargs)

                return result
            except PermissionDenied:
                deny_reason = ["Lack Required Permission of: ",]
                deny_reason.extend(perm_list)

                FileLogger.createAccessDeniedLog(request, AccessType.VIEW, system, deny_reason)

                raise PermissionDenied
            
            except Exception as e:
                error_reason = "Error Occured while accessing: "
                error_reason = error_reason + str(e)
                
                FileLogger.createErrorLog(request, access, system, error_reason)

                raise Exception

        return _wrapped_view
    
    return decorator
