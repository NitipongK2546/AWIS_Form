from django.urls import path
from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("approve/", views.approve_form_page, name="approve_form_page"),
    path("approve/<int:form_id>/", views.selected_form_to_see_page, name="get_form"),
    path("approve/<int:form_id>/confirm_approve/", views.confirm_approve, name="confirm_approve"),
    path("approve/<int:form_id>/confirm_reject/", views.confirm_reject, name="confirm_reject"),
    path("approve/success/", views.success_page, name="success_page"),
    ##########################################
    path("edit/<int:form_id>/", views.select_form_to_edit, name="edit_form"),
    ##########################################
    path("check/<int:form_id>/", views.select_form_to_edit, name="edit_form"),
]
