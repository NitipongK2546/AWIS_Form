from django.urls import path
from api.test import endpoints

app_name = "v1"

urlpatterns = [
    # path("authenticate/", endpoints.auth_api, name="auth"),

    #######################
    path("test1/", endpoints.test1, name="test1"),
    path("test2/", endpoints.test2, name="test2"),
]
