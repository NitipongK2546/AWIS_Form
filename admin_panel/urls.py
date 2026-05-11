from django.urls import path
from admin_panel import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.collections, name="collections"),
    # path("signup/", views.signup, name="signup"),
    
    path("select_users/", views.admin_select_users, name="select_users"),
    path("access_list/", views.access_list, name="access_list"),

    path("select_court_users/", views.add_court_user, name="select_court_users"),

    path("update-role/<int:user_id>/<int:role_value>/", views.update_role, name="update_role"),
    path("update-role-admin/<int:user_id>/<int:role_value>/", views.update_role_admin, name="update_role_admin"),

    path("delete-access/<int:user_id>/", views.delete_access, name="delete_access"),
    path("delete-court-user/<str:user_id>/", views.delete_court_user, name="delete_court_user"),

    path("logs/", views.view_all_logs, name="view_logs"),

    path("logs/export/", views.export_logs, name="export_logs"),
    path("logs/delete/", views.delete_logs, name="delete_logs"),

    path("courts/", views.view_all_selected_courts, name="view_courts"),
    path("courts/edit/", views.edit_selected_courts, name="edit_courts")
]
