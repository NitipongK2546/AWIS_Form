from django.urls import path
from api.v1 import endpoints

app_name = "v1"

urlpatterns = [
    path("update-status/reqwarrant/", endpoints.update_status_req_warrant, name="dashboard"),
    path("update-status/warrant/", endpoints.update_status_warrant, name="dashboard"),
]
