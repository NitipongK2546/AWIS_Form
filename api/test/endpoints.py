from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

# from api import check_utils as UtilsHandle
# from api import jwt_utils as JWTHandle

# # from dashboard.models import VisualReqformData, ReqformDataModel

# from dashboard.warrant_wrapper import VisualWarrantData
# from django.utils import timezone

from _request_utils import connect_api as AWISConnectAPI

def health_check(request : HttpRequest) -> dict:
    return JsonResponse(AWISConnectAPI.get_health_check("v1",))

def fetch_token(request : HttpRequest) -> JsonResponse:
    return AWISConnectAPI.post_login_authorize("v1.1", request)

def check_all_reqforms(request : HttpRequest) -> JsonResponse:
    return AWISConnectAPI.get_req_form_status("v1.1", request, "tcctd20260304002",)
