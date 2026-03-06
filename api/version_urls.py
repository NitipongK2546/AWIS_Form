from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("test/", include("api.test.urls")),

    path("v1/", include("api.v1.urls")),
]