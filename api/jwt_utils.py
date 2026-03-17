import jwt
from django.conf import settings

from dotenv import load_dotenv
import os
from django.http import HttpRequest, JsonResponse

from django.utils import timezone 
from datetime import timedelta

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

# CURRENT_TIMEZONE = timezone.get_current_timezone()

def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": (timezone.now() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)),
        "iat": (timezone.now()),
    }

    # print(timezone.now().isoformat())

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
        return "Token Expired"
    except jwt.InvalidTokenError:
        return "Invalid Token"
    
def _extract_jwt_from_header(headers : dict[str]):
    
    auth_header : str = headers.get("Authorization")

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

    payload = _verify_jwt(token)

    # FAILED BECAUSE ERROR
    if isinstance(payload, str):
        return JsonResponse({
            "status": 401,
            "message": payload
        }, status=401)
    
    # Finally extract the payload, which is USER_ID and others, maybe...
    return payload

def extract_jwt(request : HttpRequest):
    result = _extract_jwt_from_header(request.headers)
    
    return result