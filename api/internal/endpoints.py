from django.http import HttpRequest, JsonResponse
from warrant_form.forms_central import thai_codes

from users.models import UserDataModel
import json

from _request_utils.authenticate_user import post_login_authorize

# import requests
# import os

sub_district_select = thai_codes.getSubDistrictChoices()
district_select =thai_codes.getDistrictChoices()
province_select = thai_codes.getProvinceChoices()

def get_sub_district(request : HttpRequest) -> JsonResponse:
    return JsonResponse({
        "data": sub_district_select
    }, json_dumps_params={'ensure_ascii': False})

def get_district(request : HttpRequest) -> JsonResponse:
    return JsonResponse({
        "data": district_select
    }, json_dumps_params={'ensure_ascii': False})

def get_province(request : HttpRequest) -> JsonResponse:
    return JsonResponse({
        "data": province_select
    }, json_dumps_params={'ensure_ascii': False})

# ORG_API_FETCH_USERS = os.getenv("ORG_API_FETCH_USERS")
# def get_erp_users(request : HttpRequest):
#     response = requests.get(ORG_API_FETCH_USERS, timeout=5)
#     return response
    
