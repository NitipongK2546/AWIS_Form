from django.urls import path
from dashboard import views, views_reqform

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("success/", views.success_page, name="success_page"),

    ##########################################
    path("dashboard/approve_table/", views.approve_table_page, name="approve_table_page"),
    path("dashboard/approve/<str:req_no_plaintiff>/confirm_approve/", views.reqform_approve_page, name="confirm_approve"),

    path("dashboard/accept_table/", views.accept_table_page, name="accept_table_page"),
    path("dashboard/unsend/<str:req_no_plaintiff>/", views.unsend_reqform, name="delete_sent_reqform"),

    path("dashboard/accept_table/<str:req_no_plaintiff>/warrants/", views.warrant_status_page, name="view_reqform_warrants"),

    path("dashboard/report/<str:req_no_plaintiff>/warrant/<str:woa_refno>/", views.report_update_warrant_arrest_yet, name="report_warrant"),

    path("dashboard/download/<str:req_no_plaintiff>/warrant/<str:woa_refno>/", views.download_warrant, name="download_warrant"),

    ############################################################################

    path("dashboard/reqform/<str:req_no_plaintiff>/", views_reqform.reqform_info, name="reqform_info")

]   
