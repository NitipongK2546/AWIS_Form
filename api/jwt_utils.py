import jwt
from datetime import timedelta
from django.conf import settings

from django.utils import timezone 
from dotenv import load_dotenv
import os
from django.http import HttpRequest, JsonResponse

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "expire": (timezone.now() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)).isoformat(),
        "created": (timezone.now()).isoformat(),
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token

def _verify_jwt(token : str):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def _extract_jwt_from_header(headers : dict[str]):
    
    auth_header : str = headers.get("Authorization")

    if not auth_header:
        return JsonResponse({
            "status": 401,
            "message": "No Authorization Header?"
        })
    
    splitted_header = auth_header.split()

    if len(splitted_header) != 2:
        return JsonResponse({
            "status": 400,
            "message": "Mistake in Authorization Header?"
        })
    
    token : str = splitted_header[1]

    payload = _verify_jwt(token)

    if not payload:
        return JsonResponse({
            "status": 401,
            "message": "Token Invalid."
        })

    return payload

def extract_jwt(request : HttpRequest):
    result = _extract_jwt_from_header(request.headers)
    
    return result