from django.urls import path
from api.v1 import endpoints

app_name = "v1"

urlpatterns = [
    path("authenticate/", endpoints.auth_api, name="auth"),

    #######################

    path("requests/<str:req_no_plaintiff>/", endpoints.update_status_req_warrant, name="update_reqwarrant"),
    path("warrants/<str:woa_refno>/", endpoints.update_status_warrant, name="update_warrant"),

    ########################
]
