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
    path("edit/<path:form_id>/", views.edit_form, name="edit_form"),
    path("delete/<path:form_id>/", views.delete_form, name="delete_form"),
    path("approve_table/", views.approve_table_page, name="approve_table_page"),
    path("accept_table/", views.accept_table_page, name="accept_table_page"),
    path("warrant_status_table/", views.warrant_status_page, name="warrant_status_page"),
    
    path("unsend/<str:req_no_plaintiff>/", views.unsend_reqform, name="delete_sent_reqform"),

    path("report/<path:form_reqno_id>/warrant/<str:woa_refno>/<int:woa_year>/<int:woa_type>/<int:woa_no>/", views.report_update_warrant_arrest_yet, name="report_warrant"),
]   
