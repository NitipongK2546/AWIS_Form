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
