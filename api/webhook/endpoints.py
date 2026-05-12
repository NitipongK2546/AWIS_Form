from django.http import HttpRequest, JsonResponse
from _log_utils.file_logger import AccessType
from api.decorators import api_perm_log
from users import PermissionList, PermissionType

from api import check_utils as UtilsHandle

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType
from users.models import UserAccess, UserDataModel

from django.views.decorators.csrf import csrf_exempt

# @api_perm_log([PermissionType.DELETE], PermissionList.USER_ACCESS, AccessType.DELETE)
@csrf_exempt
def delete_user_access_webhook(request : HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({
            "status": 405,
            "message": "Method not allowed. Please POST JSON Data."
        }, status=405)
    
    data = UtilsHandle.json_retrieval(request)

    # Failed.
    if isinstance(data, JsonResponse):
        return data
    
    try:
        user_id = data.get("USR_ID")

        if not user_id:
            return JsonResponse({
                "status": 400,
                "message": "Missing Data or Wrong Field Name."
            }, status=400)
        
        if not isinstance(user_id, int):
            return JsonResponse({
                "status": 400,
                "message": "Wrong Data Type. Use Integer."
            }, status=400)

        user_access_obj = UserAccess.objects.filter(user_id=user_id).first()

        if not user_access_obj:
            return JsonResponse({
                "status": 404,
                "message": "User did not get the access in the first place."
            }, status=404)
        
        django_user : UserDataModel = UserDataModel.objects.filter(api_uid=user_id).first()

        if not django_user:
            return JsonResponse({
                "status": 500,
                "message": "User Data is missing from the this server database."
            }, status=500)
        
        user_access_obj.delete()

        FileLogger.createNormalLog(request, AccessType.DELETE, PermissionList.USER_ACCESS, django_user.getLogInfoDict(), "Via Webhook")

        return JsonResponse({
            "status": 200,
            "message": "Success. User Access deleted."
        })

    except Exception as e:
        FileLogger.createErrorLog(request, AccessType.DELETE, PermissionList.USER_ACCESS, {
            "message": str(e)
        }, remark="Via Webhook")

        return JsonResponse({
            "status": 500,
            "message": "Something went wrong."
        }, status=500)