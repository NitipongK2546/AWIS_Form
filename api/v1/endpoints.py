from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from api import check_utils as UtilsHandle
from api import jwt_utils as JWTHandle

from dashboard.models import VisualFinalizedFormData, ReqformDataModel

from dashboard.warrant_wrapper import VisualWarrantData

from django.utils import timezone

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

    username = data.get("username")
    password = data.get("password")
    
    user = authenticate(username=username, password=password)

    if not user:
        return JsonResponse({
            "status": 401,
            "message": "Wrong Username or Password"
        }, status=401)
    
    token = JWTHandle.create_jwt(user.id)

    return JsonResponse({
        "status": 200,
        "token": token,
    })

@csrf_exempt
def update_status_req_warrant(request : HttpRequest) -> JsonResponse:
    if request.method != "PUT":
        # Wrong request method.
        return JsonResponse({
            "status": 405,
            "message": "Wrong Request Method"
        }, status=405)

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

        form_obj = ReqformDataModel.objects.get(
            req_no_plaintiff = data.get("req_no_plaintiff"),
            reqno = data.get("reqno"),
        )

        target_object = VisualFinalizedFormData.objects.filter(
            form=form_obj,
        )

        iso8601_str_format = "%Y-%m-%dT%H:%M:%S"     

        recive_date = timezone.datetime.strptime(data.get("recive_date"), iso8601_str_format)
        recive_date = timezone.make_aware(recive_date, timezone.UTC,)

        accept_date = timezone.datetime.strptime(data.get("accept_date"), iso8601_str_format) 
        accept_date = timezone.make_aware(accept_date, timezone.UTC,)

        target_object.update(
            recive_date = recive_date,
            accept_date = accept_date,
            accept = data.get("accept"),
        )

        return JsonResponse({
            "status": 200,
            "message": "Update Success"
        }, status=200)

    except Exception as e:
        print(e)
        print(data)

        return JsonResponse({
            "status": 400,
            "message": "Update Failed",
        }, status=400)

    
@csrf_exempt
def update_status_warrant(request : HttpRequest) -> JsonResponse:
    if request.method != "PUT":
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
        form_obj = ReqformDataModel.objects.filter(
            req_no_plaintiff = data.get("req_no_plaintiff"),
            reqno = data.get("reqno"),
        ).first()

        warrants_list = form_obj.warrants

        target_object = warrants_list.get(
            woa_no = data.get("woa_no"),
            woa_date_year = data.get("woa_year"),
            woa_type = data.get("woa_type"),
            woa_refno = data.get("woa_refno"),
        )

        target_object = VisualWarrantData.objects.filter(
            warrant=target_object,
        )

        iso8601_str_format = "%Y-%m-%dT%H:%M:%S"    

        injunction_date = timezone.datetime.strptime(data.get("injunction_date"), iso8601_str_format)
        recive_date = timezone.make_aware(recive_date, timezone.UTC,)

        target_object.update(
            judge_name = data.get("judge_name"),
            court_injunction = data.get("court_injunction"),
            injunction_date = injunction_date,
            file_path = "",
            because = "",
        )

        return JsonResponse({
            "status": 200,
            "message": "Update Success"
        }, status=200)

    except Exception as e:
        print(e)

        return JsonResponse({
            "status": 400,
            "message": "Update Failed",
        }, status=400)


        
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