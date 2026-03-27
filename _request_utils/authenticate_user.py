from django.http import HttpRequest, JsonResponse, HttpResponse
import _request_utils.prepared_requests as RequestUtils
import os

from users.models import UserAccess, UserDataModel

from requests import Response
import requests
# import base64

# Some special case for status code.

def check_status_code(response : HttpResponse):
    if response.status_code == "401":
        raise Exception("Unauthorized. Is the Token expired?")
    elif response.status_code == "403":
        raise Exception("Forbidden. Current IP Address perhaps not allowed?")
    
def toDjangoJsonResponse(response : Response) -> JsonResponse:
    data = response.json()

    return JsonResponse(
        data, safe=False, status=response.status_code
    )


#############################################################################
# API REQUEST

# 1. Get Credentials

def post_login_authorize(version : str, request : HttpRequest, storage : str = "cookies"):
    """
    Token จะถูกใส่ลงไปใน Session/Cookie
    """

    # if not get_health_check("v1"):
    #     return False
    
    base_url = RequestUtils.get_url_from_env("AUTH_URL")
    parameter = ["login"]

    post_data = {
        "username": request.POST.get("username", ""),
        "password": request.POST.get("password", ""),
    }
    response : HttpResponse = RequestUtils.post_request(
        base_url, 
        parameter_data=parameter, 
        post_data=post_data
    )
    data : dict = response.json()
    
    if not data.get("authenticated"):
        return JsonResponse({
            "status": 400,
            "message": "Authentication Failed"
        }, status=400)
    
    ##############################################################

    # user_data : dict = data.get("user_data")
    db_user : list[dict] = data.get("db_user")

    status : UserAccess = None
    for usr in db_user:
        status = checkUserAccess(
            usr.get("USR_ID")
        )

    if not status:
      return JsonResponse({
            "status": 403,
            "message": "Forbidden"
        }, status=403)
    
    return JsonResponse({
        "status": 200,
        "message": "Success",
        "id": status.user_id,
    })

def checkUserAccess(incoming_user_id) -> bool:
    result = UserAccess.objects.filter(user_id=incoming_user_id).first()

    if result:
        return result
    
    return None