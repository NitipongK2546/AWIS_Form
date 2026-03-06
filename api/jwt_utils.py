import jwt
from datetime import timedelta
from django.conf import settings

from django.utils import timezone 
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600

def create_jwt(user_id):
    payload = {
        "user_id": user_id,
        "expire": timezone.now() + timedelta(seconds=JWT_EXP_DELTA_SECONDS),
        "created": timezone.now(),
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token

def verify_jwt(token):
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