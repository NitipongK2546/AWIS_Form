from django.urls import path
from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("success/", views.success_page, name="success_page"),

    ##########################################
    
    path("approve/", views.approve_form_page, name="approve_form_page"),
    path("approve/<path:form_id>/confirm_approve/", views.confirm_approve, name="confirm_approve"),
    path("approve/<path:form_id>/confirm_reject/", views.confirm_reject, name="confirm_reject"),

    path("view/<path:form_id>/", views.view_form, name="get_form"),
    # path("view/<str:form_id>/", views.view_form, name="get_form"),
    path("edit/<path:form_id>/", views.edit_form, name="edit_form"),

]
