from django.urls import path
from admin_panel import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.collections, name="collections"),
    # path("signup/", views.signup, name="signup"),
    
    path("user_list/", views.check_all_users, name="user_list"),
    path("select_users/", views.admin_select_users, name="select_users"),
    path("add_specific-user/", views.add_specific_user, name="add_specific_user"),
    path("access_list/", views.access_list, name="access_list"),
    path("update-role/<int:user_id>/<int:role_value>/", views.update_role, name="update_role"),
    path("delete-access/<int:user_id>/", views.delete_access, name="delete_access"),


    # path("views_perms/", views.display_all_views_permissions, name="views_perms"),
    # path("views_perms/remove/<str:view_name>/<str:perm_name>/", views.delete_perm_from_view, name="delete_perms"),
]
