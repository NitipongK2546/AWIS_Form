from django.http import HttpRequest, JsonResponse
from warrant_form.forms_central import thai_codes

from users.models import UserDataModel
import json

from api.selector.court import checkCourtDifferent

# import requests
# import os

sub_district_select = thai_codes.getSubDistrictChoices()
district_select = thai_codes.getDistrictChoices()
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

def fetch_court_check(request : HttpRequest) ->JsonResponse:
    is_different = checkCourtDifferent()

    if is_different == "ERROR":
        return JsonResponse({
            "status": "error",
        })

    if is_different:
        return JsonResponse({
            "status": 200,
            "different": True
        })
    
    return JsonResponse({
        "status": 200,
        "different": False
    })
