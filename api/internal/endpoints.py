from django.http import HttpRequest, JsonResponse
from warrant_form.forms_central import thai_codes

from users.models import UserDataModel
from api.models import HealthCheckStatus

from api.selector.court import checkCourtDifferent
import _request_utils.connect_api as AWISConnect

from django.conf import settings

# import os

from django.utils import timezone
from datetime import timedelta

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

def fetch_health_check(request : HttpRequest) -> JsonResponse:

    api_enabled : bool = settings.ENABLE_API
    
    try:
        result = False

        latest_check = HealthCheckStatus.objects.last()

        # If check has never been performed.
        # Or if check was 5 minutes old.
        if not latest_check:
            data = AWISConnect.get_health_check("v1")

            if data.get("status") == "ok":
                result = True
            else:
                result = False

            HealthCheckStatus.updateStatus(result)
        elif timezone.now() >= latest_check.last_date + timedelta(minutes=5):
            data = AWISConnect.get_health_check("v1")

            if data.get("status") == "ok":
                result = True
            else:
                result = False

            HealthCheckStatus.updateStatus(result)
        else:
            result = HealthCheckStatus.isHealthOK()
        
        if result:
            return JsonResponse({
                "status": 200,
                "api_enabled": api_enabled,
            })
        
        # Not true, API down.
        return JsonResponse({
            "status": 500,
        })
    
    except:
        return JsonResponse({
            "status": 500,
            "message": "เชื่อมต่อกับ API ไม่ได้"
        })


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
