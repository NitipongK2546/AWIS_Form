from django.urls import path
from api.internal import endpoints

app_name = "internal"

urlpatterns = [
    path("get-sub-district/", endpoints.get_sub_district, name="get_sub_district"),
    path("get-district/", endpoints.get_district, name="get_district"),
    path("get-province/", endpoints.get_province, name="get_province"),
]
