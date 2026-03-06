from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from _request_utils import connect_api as AWISAPIConnect

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
def test1(request : HttpRequest) -> JsonResponse:
    if AWISAPIConnect.get_health_check("v1"):
        return JsonResponse({
            "status": "success"
        })
    
    return JsonResponse({
        "status": "fail"
    }, status=500)

@csrf_exempt
def test2(request : HttpRequest) -> JsonResponse:
    response, data = AWISAPIConnect.post_login_authorize("v1.1", request, "session")
    storage = ""

    return JsonResponse({
        "status": "success",
        "token_from_cookie": request.COOKIES.get("token"),
    })