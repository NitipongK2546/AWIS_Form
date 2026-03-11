"""
File สำหรับรวม Function ทุกตัว ที่มีไว้สำหรับการส่งข้อมูลให้ API Server\n
ใส่ข้อมูลตามที่ Function ขอมา แล้วจะได้ข้อมูล Output หรือ ข้อมูลเป็น Boolean ออกมาใช้ต่อ\n
"""

from django.http import HttpRequest, JsonResponse, HttpResponse
import _request_utils.prepared_requests as RequestUtils
import os
# import base64

# Some special case for status code.

def check_status_code(response : HttpResponse):
    if response.status_code == "401":
        raise Exception("Unauthorized. Is the Token expired?")
    elif response.status_code == "403":
        raise Exception("Forbidden. Current IP Address perhaps not allowed?")

#############################################################################
# API REQUEST

# 1.
def get_health_check(version : str) -> bool:
    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "healthcheck"]

    response : JsonResponse = RequestUtils.get_request(
        base_url, 
        parameter_data=parameter
    )
    data : dict = response.json()

    return data
    
    # # Response OK.
    # if data.get("status") == "ok":
    #     return True
    
    # return False

##############################################################################
# 2. 
def post_login_authorize(version : str, request : HttpRequest, storage : str = "cookies") -> bool:
    """
    Token จะถูกใส่ลงไปใน Session/Cookie
    """

    # if not get_health_check("v1"):
    #     return False
    
    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "authorize"]

    # username = request.POST.get("username")
    # password = request.POST.get("password")

    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")

    post_data = {
        "username": username,
        "password": password,
    }
    response : HttpResponse = RequestUtils.post_request(
        base_url, 
        parameter_data=parameter, 
        post_data=post_data
    )
    data : dict = response.json()
    
    # Response OK.
    if not data.get("token"):
        return JsonResponse({
            "status": "fail"
        }, status=400)
    
    ##############################################################
    # Rewrap in real Django HTTP request/ json

    response : JsonResponse = JsonResponse({
        "status": 200,
        "token": data.get("token")
    }, status=200)    
    
    if storage == "session":
        request.session["bearer_token"] = data.get("token")
    else:
        response.set_cookie("bearer_token", data.get("token"), max_age=1800, httponly=True)
    
    return response

##############################################################################
# 3. 
def post_send_req_form(version : str, request : HttpRequest, post_data : dict) -> dict | bool:

    # if not get_health_check("v1"):
    #     return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "awis", "reqforms"]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : JsonResponse = RequestUtils.post_request_with_auth(
        base_url, 
        parameter_data=parameter, 
        post_data=post_data, 
        auth_token=auth_token
    )
    data : dict = response.json()

    print(data)

    return data

    # if data.get("status"):
    #     return data
    
    # return False

##############################################################################
# 4. 
def get_req_form_status(version : str, request : HttpRequest, req_no_plaintiff : str) -> list[dict]:
    """
    Return List ที่เป็น Dictionary ออกมา เป็นข้อมูลสถานะคำร้อง ReqForm
    """

    # if not get_health_check("v1"):
    #     return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "awis", "reqforms", req_no_plaintiff]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : JsonResponse = RequestUtils.get_request_with_auth(
        base_url, 
        parameter_data=parameter, 
        auth_token=auth_token
    )
    data : list[dict] = response.json()

    if data:
        return response
    
    return None

##############################################################################
# 5.
def get_search_warrants(version : str, request : HttpRequest, query_data : dict) -> list[dict] | str:
    """
    Return ข้อมูล Warrants ถ้าหาเจอ \n
    Return message ออกมา ถ้า False หาไม่เจอ
    """

    # if not get_health_check("v1"):
    #     return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "awis", "warrants", "search"]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : HttpResponse = RequestUtils.get_request_with_auth(
        base_url, 
        parameter_data=parameter, 
        query_data=query_data,
        auth_token=auth_token
    )
    data : dict = response.json()

    if data.get("success"):
        results = data.get("warrant_result")

        return results

    message = data.get("message")
    return message

##############################################################################
# 6.
def put_report_warrant_result(version : str, request : HttpRequest, put_data : dict) -> dict:
    # This one need PUT request
    # if not get_health_check("v1"):
    #     return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "awis", "arrests"]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : JsonResponse = RequestUtils.put_request_with_auth(
        base_url, 
        parameter_data=parameter, 
        put_data=put_data, 
        auth_token=auth_token
    )
    data : dict = response.json()

    if data:
        return data

    return False

##############################################################################
# 7.
def get_court_order_and_warrant(version : str, request : HttpRequest, plaintiff_code : str):
    """
    This one will return "file_path" value as Base64. Prepare to Convert.
    """
    # This one RETURN VALUE IN Base64
    # if not get_health_check("v1"):
    #     return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "awis", "warrants", "search_file", plaintiff_code]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : JsonResponse = RequestUtils.get_request_with_auth(
        base_url, 
        parameter_data=parameter,
        auth_token=auth_token
    )
    data : dict = response.json()

    if data:
        return data

    return False

##############################################################################
# 8.
def delete_req_form(version : str, request : HttpRequest, req_no_plaintiff : str):
    # This one need PUT request
    # if not get_health_check("v1"):
    #     return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "awis", "court", req_no_plaintiff]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : JsonResponse = RequestUtils.delete_request_with_auth(
        base_url, 
        parameter_data=parameter,
        auth_token=auth_token
    )
    data : dict = response.json()

    message = data.get("message")

    if message:
        return message

    return False

##############################################################################
# 9.
def get_court_list(version : str, request : HttpRequest) -> dict:

    # if not get_health_check("v1"):
    #     return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "awis", "court"]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : JsonResponse = RequestUtils.get_request_with_auth(
        base_url, 
        parameter_data=parameter,
        auth_token=auth_token
    )
    data : dict = response.json()

    if data:
        return data
    
    return False

#######################################################################
#
# Additional
#
#######################################################################\

##############################################################################
# 1.
def put_update_request_status(version : str, request : HttpRequest, put_data : dict) -> dict:
    # This one need PUT request
    # if not get_health_check("v1"):
    #     return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "updatestatusreqwarrant"]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : JsonResponse = RequestUtils.put_request_with_auth(
        base_url, 
        parameter_data=parameter, 
        put_data=put_data, 
        auth_token=auth_token
    )
    data : dict = response.json()

    if data:
        return data

    return False

##############################################################################
# 2.
def put_udate_warrant_status(version : str, request : HttpRequest, put_data : dict) -> dict:
    # This one need PUT request
    # if not get_health_check("v1"):
    #     return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "updatestatuswarrant"]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : JsonResponse = RequestUtils.put_request_with_auth(
        base_url, 
        parameter_data=parameter, 
        put_data=put_data, 
        auth_token=auth_token
    )
    data : dict = response.json()

    if data:
        return data

    return False