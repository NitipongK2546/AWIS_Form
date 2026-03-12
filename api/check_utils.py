from django.http import HttpRequest, JsonResponse
from django.utils import timezone

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

def check_token(data : dict) -> bool | JsonResponse:
    try:
        authorization : str = data.get("Authorization")
        
        if not authorization:
            return JsonResponse({
                "status": 400,
                "message": "No Authorization Token"
            }, status=400)
        
        token : str = authorization.split()[1]

        # Do the checking thing.

        return True

    except json.JSONDecodeError:
        return JsonResponse({
            "status": 400,
            "message": "Check Token Failed"
        }, status=400)