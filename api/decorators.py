import functools
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, JsonResponse

# from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login

# from api import check_utils as UtilsHandle
from api import jwt_utils as JWTHandle

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType
from users.permissions import PermissionList, PermissionType, perm_str_list
from users.models import UserDataModel

def api_perm_log(perm_list : list[PermissionType], system : PermissionList, access : AccessType = AccessType.VIEW):
    def decorator(view_func):
        
        @functools.wraps(view_func)
        def _wrapped_view(request : HttpRequest, *args, **kwargs):
            payload = JWTHandle.extract_jwt(request)
            if isinstance(payload, JsonResponse):
                return payload
            
            user = UserDataModel.objects.filter(
                api_uid=payload.get("user_id")
            ).first()
            try:
                # no_csrf_func = csrf_exempt(view_func)
                result = view_func(request, *args, **kwargs)

                return result
            except PermissionDenied:
                deny_reason = ["Lack Required Permission of: ",]
                deny_reason.extend(perm_list)

                FileLogger.createAccessDeniedLog(request, AccessType.VIEW, system, deny_reason, user_bypass=user, remark="VIA JSON WEB TOKEN")

                raise PermissionDenied

                # return JsonResponse({
                #     "status": 403,
                #     "message": "Current User Lack Permission" 
                # }, status=403)
            
            except Exception as e:
                error_reason = f"<{type(e).__name__}>: "
                error_reason = error_reason + str(e)
                
                FileLogger.createErrorLog(request, access, system, error_reason, user_bypass=user, remark="VIA JSON WEB TOKEN")

                raise Exception

                # return JsonResponse({
                #     "status": 500,
                #     "message": "Updating Failed." 
                # }, status=500)

        return csrf_exempt(_wrapped_view)
    
    return decorator
