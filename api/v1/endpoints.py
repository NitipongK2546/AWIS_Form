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
            return JsonResponse({
                "status": 401,
                "message": "Wrong Username or Password"
            }, status=401)
        
        if user.is_superuser or (not user.has_perms(
            perm_str_list([PermissionType.EDIT], PermissionList.REQFORM_SUBMITTED)
        )):
            
            FileLogger.createAccessDeniedLog(request, AccessType.LOGIN, PermissionList.REQFORM_SUBMITTED, user_bypass=user, remark="JWT not allowed.")
            return JsonResponse({
                "status": 403,
                "message": "JWT cannot be created for with user."
            }, status=403)
        
        token = JWTHandle.create_jwt(user)

        FileLogger.createNormalLog(request, AccessType.LOGIN, PermissionList.REQFORM_SUBMITTED, user_bypass=user, remark="JWT Created")

        return JsonResponse({
            "status": 200,
            "token": token,
        })
    except Exception as e:
        return JsonResponse({
            "status": 400,
            "message": "Authentication failed."
        }, status=400)

@api_perm_log([PermissionType.EDIT], PermissionList.REQFORM_SUBMITTED, AccessType.EDIT)
def update_status_req_warrant(request : HttpRequest) -> JsonResponse:
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
    #     "recive_date": "2006-01-02T00:00:00",
    #     "reqno": "จ.1/2569",
    #     "accept": 1,
    #     "accept_date": "2006-01-02T00:00:00"
    # }

    try:
        # Should be unique, so there's really only 1.
        form_obj = ReqformDataModel.objects.get(
            req_no_plaintiff = data.get("req_no_plaintiff"),
        )

        target_object = VisualReqformData.objects.filter(
            form=form_obj,
        )

        iso8601_str_format = "%Y-%m-%dT%H:%M:%S" 

        data_recive_date = data.get("recive_date")
        data_accept_date = data.get("accept_date")

        reqno_data = getDataFromReqno(data.get("reqno"))

        update_dict = {
            "req_form_number": reqno_data.get("req_form_number"),
            "req_year": reqno_data.get("req_year"),
            "req_case_type_id": reqno_data.get("req_case_type_id"),
        }

        if data_recive_date:
            recive_date = timezone.datetime.strptime(data_recive_date, iso8601_str_format)
            recive_date = timezone.make_aware(recive_date, timezone.UTC,)

            update_dict.update({"recive_date": recive_date})
        else:
            raise HttpResponseBadRequest("No receive date")

        if data_accept_date:
            accept_date = timezone.datetime.strptime(data_accept_date, iso8601_str_format) 
            accept_date = timezone.make_aware(accept_date, timezone.UTC,)

            update_dict.update({"accept_date": accept_date})
            update_dict.update({"accept": data.get("accept")})
        else:
            raise HttpResponseBadRequest("No accept date")

        target_object.update(
            **update_dict,
        )

        affected_objs = [obj.getLogInfoDict() for obj in target_object]

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
def update_status_warrant(request : HttpRequest) -> JsonResponse:
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

        # {
        #     "req_no_plaintiff": "123456789",
        #     "reqno": "จ.1/2569",

        #     "woa_no": 2,
        #     "woa_year": 2569,
        #     "woa_type": 2,
        #     "woa_refno": "1234",

        #     "judge_name": "xxxxxx xxxx",
        #     "court_injunction": 1,
        #     "injunction_date": "2006-01-02T00:00:00",
        #     "file_path": "",
        #     "because": ""
        # }

    try:
        return JsonResponse({
            "status": "UNFINISHED",
            "message": "TODO: PLEASE ASK THE COURT WHAT KIND OF FIELD THEY WANT TO REFER SO THEY CAN UPDATE THE CORRECT WARRANT! PLEASE! THE API DOESN'T SEND ANYTHING REQUIRED"
        })

        #
        # A VERY BIG TO DO LIST
        #
        #


        form_obj = ReqformDataModel.objects.get(
            req_no_plaintiff = data.get("req_no_plaintiff"),
        )

        related_warrants = form_obj.warrants.all()

        warrants_matched : WarrantDataModel = related_warrants.filter(
            woa_refno = data.get("woa_refno"),
            woa_type = data.get("woa_type"),
        ).first()

        woa_wrapper_matched = VisualWarrantData.objects.filter(
            warrant=warrants_matched,
        )

        if len(woa_wrapper_matched) == 0:
            raise JsonResponse({
                "status": 400,
                "message": "No warrant found."
            }, status=400)

        iso8601_str_format = "%Y-%m-%dT%H:%M:%S"    

        injunction_date = timezone.datetime.strptime(data.get("injunction_date"), iso8601_str_format)
        injunction_date = timezone.make_aware(injunction_date, timezone.UTC,)

        # reqno_data = getDataFromReqno(data.get("reqno"))

        update_dict = {
            # "req_form_number": reqno_data.get("req_form_number"),
            # "req_year": reqno_data.get("req_year"),
            # "req_case_type_id": reqno_data.get("req_case_type_id"),

            
            "judge_name": data.get("judge_name"),
            "court_injunction": data.get("court_injunction"),
            "injunction_date": injunction_date,
            "file_path": data.get("file_path", ""),
            "because": data.get("because", ""),
        }

        woa_wrapper_matched.update(
            **update_dict,
        )

        warrants_matched.woa_no = data.get("woa_no")
        warrants_matched.save()
        # warrants_matched.

        FileLogger.createNormalLog(request, AccessType.EDIT, PermissionList.REQFORM_SUBMITTED, warrants_matched.getLogInfoDict(), user_bypass=user, remark="VIA JSON WEB TOKEN")

        return JsonResponse({
            "status": 200,
            "message": "Update Success"
        }, status=200)

    except PermissionDenied:
        return JsonResponse({
            "status": 403,
            "message": "Current User Lack Permission" 
        }, status=403)
    except HttpResponseBadRequest:
        return JsonResponse({
            "status": 400,
            "message": "Updating Failed." 
        }, status=400)


        
