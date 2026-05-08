from django.http import HttpRequest, JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import permission_required
from users.models import UserDataModel

from api import check_utils as UtilsHandle
from api import jwt_utils as JWTHandle

from dashboard.models import VisualReqformData, ReqformDataModel
from dashboard.warrant_wrapper import VisualWarrantData, WarrantDataModel

from django.utils import timezone

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType
from api.decorators import api_perm_log
from users.permissions.decorators import perm_req_log, perm_str_list
from users import PermissionList, PermissionType, perm_str

from django.core.exceptions import PermissionDenied

# Reqno Helper function
# Split the Number from the type and buddhist year.
# The number is chosen by court.

#Sample => "reqno": "จ.1/2569"
# Is absolutely useless now because API specification changed.
def getDataFromReqno(reqno : str):
    first_split : list[str] = reqno.split("/")
    second_split : list[str] = first_split[0].split(".")

    if (len(first_split) == 2) and (len(second_split) == 2):
        return {
            "req_case_type_id": second_split[0],
            "req_form_number": second_split[1],
            "req_year": first_split[1],
        }

    return False

def datetime_format(datetime_str : str):
    iso8601_str_format = "%Y-%m-%dT%H:%M:%S" 
    html_str_format = "%Y-%m-%d %H:%M:%S" 

    if datetime_str:
        datetime_obj = timezone.datetime.strptime(datetime_str, html_str_format).astimezone(timezone.get_current_timezone())
        return datetime_obj
    
    return None

# V1 ENDPOINTS

# Of course, we except from having to use csrf token, because... it's cross site.
# We have to add verification token of our own. Somehow.
# Or maybe not.

@csrf_exempt
def auth_api(request : HttpRequest) -> JsonResponse:
    if request.method != "POST":
        # Wrong request method.
        return JsonResponse({
            "status": 405,
            "message": "Wrong Request Method"
        }, status=405)

    data = UtilsHandle.json_retrieval(request)

    # Failed.
    if isinstance(data, JsonResponse):
        return data
    
    try:
        username = data.get("username")
        password = data.get("password")
        
        user : UserDataModel = authenticate(username=username, password=password)

        if not user:
            FileLogger.createAccessDeniedLog(request, AccessType.LOGIN, PermissionList.JWT_ENDPOINT, remark="Wrong Username or Password")

            return JsonResponse({
                "status": 401,
                "message": "Wrong Username or Password"
            }, status=401)
        
        if user.is_superuser or (not user.has_perms(
            perm_str_list([PermissionType.EDIT], PermissionList.REQFORM_SUBMITTED)
        )):
            
            FileLogger.createAccessDeniedLog(request, AccessType.LOGIN, PermissionList.JWT_ENDPOINT, user_bypass=user, remark="JWT not allowed.")
            return JsonResponse({
                "status": 403,
                "message": "JWT cannot be created for with user."
            }, status=403)
        
        token = JWTHandle.create_jwt(user)

        FileLogger.createNormalLog(request, AccessType.LOGIN, PermissionList.JWT_ENDPOINT, user_bypass=user, remark="JWT Created")

        return JsonResponse({
            "status": 200,
            "token": token,
        })
    except Exception as e:
        FileLogger.createErrorLog(request, AccessType.LOGIN, PermissionList.REQFORM_SUBMITTED, str(e))
        return JsonResponse({
            "status": 400,
            "message": "Authentication failed."
        }, status=400)

@api_perm_log([PermissionType.EDIT], PermissionList.REQFORM_SUBMITTED, AccessType.EDIT)
def update_status_req_warrant(request : HttpRequest, req_no_plaintiff : str) -> JsonResponse:
    if request.method != "PUT":
        # Wrong request method.
        return JsonResponse({
            "status": 405,
            "message": "Wrong Request Method"
        }, status=405)
    
    payload = JWTHandle.extract_jwt(request)
    if isinstance(payload, JsonResponse):
        return payload

    user = UserDataModel.objects.filter(
        api_uid=payload.get("user_id")
    ).first()

    # if not user.has_perm(perm_str(PermissionType.EDIT, PermissionList.REQFORM_SUBMITTED)):
    #     raise PermissionDenied

    data = UtilsHandle.json_retrieval(request)

    # Failed.
    if isinstance(data, JsonResponse):
        return data
    
    # Data confirm to be dictionary.   
    # Sample
    # {
    #     "req_no_plaintiff": "123456789",
    #     "req_year": 2569
    #     "req_no": 1
    #     "req_case_type_id": 0-1,
    #     "accept": 1,
    #     "accept_date": "2006-01-02 00:00:00"
    # }

    try:
        # Should be unique, so there's really only 1.
        form_obj = ReqformDataModel.objects.filter(
            req_no_plaintiff = req_no_plaintiff,
        )

        if not form_obj.first():
            return JsonResponse({
                "status": 404,
                "message": "ไม่มีคำร้องที่มีเลขคำร้องดังกล่าว" 
            }, status=400)

        form_status_obj = VisualReqformData.objects.filter(
            form__in=form_obj,
        )

        wrapper_update_dict = {
            "accept": data.get("accept"),
            "accept_date": datetime_format(data.get("accept_date")),
        }

        reqform_update_dict = {
            "req_year": data.get("req_year"),
            "req_form_number": data.get("req_no"),
            "req_case_type_id": data.get("req_case_type_id"),
        }

        form_status_obj.update(
            **wrapper_update_dict,
        )

        form_obj.update(
            **reqform_update_dict
        )

        affected_objs = [obj.getLogInfoDict() for obj in form_status_obj]

        FileLogger.createNormalLog(request, AccessType.EDIT, PermissionList.REQFORM_SUBMITTED, affected_objs, user_bypass=user, remark="VIA JSON WEB TOKEN")

        return JsonResponse({
            "status": 200,
            "message": "Update Success"
        }, status=200)
    
    except PermissionDenied:
        return JsonResponse({
            "status": 403,
            "message": "Current User Lack Permission" 
        }, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({
            "status": 400,
            "message": "Updating Failed." 
        }, status=400)

@api_perm_log([PermissionType.EDIT], PermissionList.REQFORM_SUBMITTED, AccessType.EDIT)
def update_status_warrant(request : HttpRequest, woa_refno : str) -> JsonResponse:
    if request.method != "PUT":
        # Wrong request method.
        return JsonResponse({
            "status": 405,
            "message": "Wrong Request Method"
        }, status=405)
    
    payload = JWTHandle.extract_jwt(request)
    if isinstance(payload, JsonResponse):
        return payload

    user = UserDataModel.objects.filter(
        api_uid=payload.get("user_id")
    ).first()

    # if not user.has_perm(perm_str(PermissionType.EDIT, PermissionList.REQFORM_SUBMITTED)):
    #     raise PermissionDenied

    data = UtilsHandle.json_retrieval(request)

    # Failed.
    if isinstance(data, JsonResponse):
        return data
    
        # Data confirm to be dictionary.   

        # Data confirm to be dictionary.   
        # Sample
        # {
        #     "req_case_type_id": 0-1,
        #     "req_num": 000,
        #     "req_num_year": 2569,
        #     "req_no_plaintiff": "123456789",

        #     "woa_no": 2,
        #     "woa_year": 2569,
        #     "woa_type": 2,
        #     "woa_refno": "1234",

        #     "judge_name": "xxxxxx xxxx",
        #     "court_injuction": 1,
        #     "injunction_date": "2006-01-02T00:00:00",
        #     "file_path": "",
        #     "because": ""

        #     "prescription_unit": 1 2 3, #ประเภท ปี เดือน วัน
        #     "prescription": 00 # จำนวน
        #     "woa_start_date":
        #     "woa_end_date": 
        # }

    try:

        form_obj = ReqformDataModel.objects.filter(
            req_no_plaintiff = data.get("req_no_plaintiff"),
        )
        
        if not form_obj.first():
            return JsonResponse({
                "status": 404,
                "message": "ไม่มีคำร้องที่มีเลขคำร้องดังกล่าว" 
            }, status=400)

        related_warrants = form_obj.first().warrants.all()

        warrants_matched = related_warrants.filter(
            woa_refno=woa_refno,
        )

        if not warrants_matched.first():
            return JsonResponse({
                "status": 404,
                "message": "ไม่มีหมายที่มีเลขอ้างอิงกล่าว" 
            }, status=400)

        woa_wrapper_matched = VisualWarrantData.objects.filter(
            warrant__in=warrants_matched,
        )

        if len(woa_wrapper_matched) == 0:
            raise JsonResponse({
                "status": 400,
                "message": "No warrant found."
            }, status=400)
        
        wrapper_update_dict = {
            "judge_name": data.get("judge_name"),
            "court_injunction": data.get("court_injuction"),
            "file_path": data.get("file_path", ""),
            "because": data.get("because", ""),
        }

        warrant_update_dict = {
            "woa_type": data.get("woa_type"),
            "woa_no": data.get("woa_no"),
            "woa_year": data.get("woa_year"),
        }

        reqform_update_dict = {
            # "prescription_unit": data.get("prescription_unit"), 
            "judge_name": data.get("judge_name"),
            "prescription": data.get("prescription"), 
            "woa_start_date": datetime_format(data.get("woa_start_date")),
            "woa_end_date": datetime_format(data.get("woa_end_date")),
        }

        woa_wrapper_matched.update(
            **wrapper_update_dict,
        )

        warrants_matched.update(
            **warrant_update_dict,
        )

        form_obj.update(
            **reqform_update_dict
        )

        FileLogger.createNormalLog(request, AccessType.EDIT, PermissionList.REQFORM_SUBMITTED, woa_wrapper_matched.first().getLogInfoDict(), user_bypass=user, remark="VIA JSON WEB TOKEN")

        return JsonResponse({
            "status": 200,
            "message": "Update Success"
        }, status=200)

    except PermissionDenied:
        return JsonResponse({
            "status": 403,
            "message": "Current User Lack Permission" 
        }, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({
            "status": 400,
            "message": "Updating Failed." 
        }, status=400)

        
