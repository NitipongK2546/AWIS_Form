from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("v1/", include("api.v1.urls")),
    path("internal/", include("api.internal.urls")),

    path("webhook/", include("api.webhook.urls")),

    path("test/", include("api.test.urls")),
]