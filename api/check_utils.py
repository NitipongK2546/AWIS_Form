from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from api.models import APISecret

import json

def json_retrieval(request : HttpRequest) -> dict[str,] | JsonResponse:
    try:
        # Body is byte, so we need to decode to text.
        body_unicode = request.body.decode("utf-8")

        data : dict[str,] = json.loads(body_unicode)

        return data

    except json.JSONDecodeError:
        return JsonResponse({
            "status": 400,
            "message": "Cannot decode JSON"
        }, status=400)

def check_api_secret_permission(request : HttpRequest, required_permissions : list[str]):

    auth_header : str = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse({
            "status": 401,
            "message": "No Authorization Header?"
        }, status=401)
    
    splitted_header = auth_header.split()

    if len(splitted_header) != 2:
        return JsonResponse({
            "status": 400,
            "message": "Mistake in Authorization Header?"
        }, status=401)
    
    token : str = splitted_header[1]

    result = APISecret.checkAPIKey(token)

    if not result:
        return JsonResponse({
            "status": 400,
            "message": "No such API Key existed."
        }, status=401)
    
    gotten_permissions = result.get("permission")
    
    for perm in required_permissions:
        if perm not in gotten_permissions:
            return JsonResponse({
                "status": 403,
                "message": "Forbidden. This Key doesn't have such permission."
            }, status=401)
    
    return True