from django.urls import path
from api.webhook import endpoints

app_name = "webhook"

urlpatterns = [
    path("delete_user_access/", endpoints.delete_user_access_webhook, name="delete_user_access"),

    ########################
]
