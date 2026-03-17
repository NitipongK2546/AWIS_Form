from django.urls import path
from api.test import endpoints

app_name = "test"

urlpatterns = [
    path("health/", endpoints.health_check, name="health"),
    path("token/", endpoints.fetch_token, name="login"),
    path("check_req/", endpoints.check_all_reqforms, name="check_reqform"),
]
