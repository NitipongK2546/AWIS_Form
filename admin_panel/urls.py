from django.urls import path
from admin_panel import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.collections, name="collections"),
    path("signup/", views.signup, name="signup"),
    path("user_list/", views.check_all_users, name="user_list"),
    path("select_users/", views.admin_select_users, name="select_users"),
    path("add_specific-user/", views.add_specific_user, name="add_specific_user"),
    path("access_list/", views.access_list, name="access_list"),
]
