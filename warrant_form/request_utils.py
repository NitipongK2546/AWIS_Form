import requests
from requests import RequestException

from django.http import HttpRequest, JsonResponse, HttpResponse

import os
from dotenv import load_dotenv

load_dotenv()

# Extra utility function... in a util functions.

def check_auth_token(request : HttpRequest, token_type : str = "bearer_token") -> str | None:
    return request.session.get(token_type)

def get_base_url_from_env(var_name : str = "BASE_URL") -> str:
    return os.getenv(var_name)

def get_full_url_from_env(var_name : str = "FULL_API_URL") -> str:
    return os.getenv(var_name)

# Request function.

def prepare_request_data(target_url : str, data : dict, parameter_data : list, auth_token : str) -> tuple:
    """
    target_url: Base URL ของ Server ที่ต้องการเชื่อมต่อ \n
    data: ข้อมูลที่ส่ง ถ้าเป็น get จะเป็น query/ ถ้าเป็น post จะเป็น data\n
    parameter_data: Directory ใส่เพิ่มเติมหลังจาก URL หลัก อาจต้องแก้ตาม Version ของ API ทีหลัง เนื่องจากมี v1 และ v1.1\n 
    auth_token: Authentication Token ยืนยันตัวตน ตอนนี้มีแค่ Bearer Token (JSON Web Token) \n
    """
    if not target_url:
        raise Exception("The URL wasn't entered.")

    dict_header = {}
    if auth_token:
        dict_header.update({"Authorization": f"Bearer {auth_token}"})
    # PASS THE DATA AS DICT
    dict_data = data

    # Make sure the url ends with directory slash before we begin
    if not target_url.endswith("/"):
        target_url = target_url + "/"

    # http:localhost:8000/
    # incoming ["param1", "12345"]
    # http:localhost:8000/param1/12345/
    if not parameter_data:
        return (target_url, dict_data, dict_header)

    finalized_url = target_url
    for param in parameter_data:
        finalized_url = finalized_url + f"{param}/"

    return (finalized_url, dict_data, dict_header)

def send_request_receive_response(packed_data : tuple, request_type) -> HttpResponse:
    """
    packed_data: ข้อมูล url, dict_data, dict_header สำหรับส่ง request
    request_type: เพื่อแยก GET, POST และประเภท dict_data ออกจากกัน
    """
    final_url, dict_data, dict_header = packed_data
    try:
        if request_type == "GET":
            response : JsonResponse = requests.get(final_url, params=dict_data, headers=dict_header)
        elif request_type == "POST":
            response : JsonResponse = requests.post(final_url, data=dict_data, headers=dict_header)
        else: 
            raise RequestException("Unsupported. Has to add PUT and DELETE soon though.")

        # Get response data either way.
        # Return it as Dictionary.
        # data : dict = response.json()
        return response

    except Exception as e:
        raise RequestException("The API request has failed.")
    
def send_request(request_type : str, target_url : str, query_data : dict, parameter_data : list, auth_token : str):

    packed_data = prepare_request_data(target_url, query_data, parameter_data, auth_token)
    response_data = send_request_receive_response(packed_data, request_type)

    return response_data

def get_request(target_url : str, query_data : dict = None, parameter_data : list = None) -> HttpResponse:
    """
    target_url: Base URL ของ API Server ที่ต้องการเชื่อมต่อ \n
    query_data: ข้อมูลที่ส่ง เป็นแบบ ?id=5&name=test เป็นต้น \n
    parameter_data: Directory ใส่เพิ่มเติมหลังจาก Base URL เช่น example.com/param1 \n 
    """

    REQUEST_TYPE = "GET"
    AUTH_TOKEN = None

    return send_request(REQUEST_TYPE, target_url, query_data, parameter_data, AUTH_TOKEN)
    
    
def post_request(target_url : str, post_data : dict = None, parameter_data : list = None) -> HttpResponse:
    """
    target_url: Base URL ของ API Server ที่ต้องการเชื่อมต่อ \n
    post_data: ข้อมูลที่ส่ง เป็นแบบ Dictionary \n
    parameter_data: Directory ใส่เพิ่มเติมหลังจาก Base URL เช่น example.com/param1 \n 
    """

    REQUEST_TYPE = "POST"
    AUTH_TOKEN = None

    return send_request(REQUEST_TYPE, target_url, post_data, parameter_data, AUTH_TOKEN)


def get_request_with_auth(target_url : str, query_data : dict = None, parameter_data : list = None, auth_token : str = None) -> HttpResponse:
    """
    Request แบบที่มี Token ได้ ต้องเพิ่มเองโดยใช้ check_auth_token จา่ก session. \n\n
    target_url: Base URL ของ API Server ที่ต้องการเชื่อมต่อ \n
    query_data: ข้อมูลที่ส่ง เป็นแบบ ?id=5&name=test เป็นต้น \n
    parameter_data: Directory ใส่เพิ่มเติมหลังจาก Base URL เช่น example.com/param1 \n 
    auth_token: Authentication Token ยืนยันตัวตน ตอนนี้มีแค่ Bearer Token (JSON Web Token) \n
    """

    REQUEST_TYPE = "GET"

    return send_request(REQUEST_TYPE, target_url, query_data, parameter_data, auth_token)
    
    
def post_request_with_auth(target_url : str, post_data : dict = None, parameter_data : list = None, auth_token : str = None) -> HttpResponse:
    """
    Request แบบที่มี Token ได้ ต้องเพิ่มเองโดยใช้ check_auth_token จา่ก session. \n\n

    target_url: Base URL ของ API Server ที่ต้องการเชื่อมต่อ \n
    post_data: ข้อมูลที่ส่ง เป็นแบบ Dictionary \n
    parameter_data: Directory ใส่เพิ่มเติมหลังจาก Base URL เช่น example.com/param1 \n 
    auth_token: Authentication Token ยืนยันตัวตน ตอนนี้มีแค่ Bearer Token (JSON Web Token) \n
    """

    REQUEST_TYPE = "POST"

    return send_request(REQUEST_TYPE, target_url, post_data, parameter_data, auth_token)