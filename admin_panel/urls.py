from django.urls import path
from admin_panel import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.collections, name="collections"),
    path("signup/", views.signup, name="signup"),

    path("user_list/", views.check_all_users, name="user_list"),
]
