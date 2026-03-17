from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path('logout/', views.custom_logout, name="logout"),
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
]
