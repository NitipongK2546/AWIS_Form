from django.urls import path
from api.test import endpoints

app_name = "test"

urlpatterns = [
    path("health/", endpoints.health_check, name="health"),
    path("token/", endpoints.fetch_token, name="login"),
    path("check_req/", endpoints.fetch_token, name="check_reqform"),
]
