from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from api import check_utils as UtilsHandle
from api import jwt_utils as JWTHandle

from dashboard.receiver_models import ReceivedReqFormStatus
from dashboard.models import VisualFinalizedFormData, ReqformDataModel

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
    
    # Data confirm to be dictionary.   

    # print(data)

    return JsonResponse({
        "status": "success",
    })


        
    