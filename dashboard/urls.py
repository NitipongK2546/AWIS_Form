from django.urls import path
from dashboard import views, views_reqform, views_main

app_name = "dashboard"

old_stuff = [
    path("", views.index, name="index"),
    path("dashboard/", views_main.dashboard, name="dashboard"),
    path("success/", views.success_page, name="success_page"),

    path("dashboard/approve_table/", views.approve_table_page, name="approve_table_page"),
    path("dashboard/approve/<str:req_no_plaintiff>/confirm_approve/", views.reqform_approve_page, name="confirm_approve"),

    path("dashboard/accept_table/", views.accept_table_page, name="accept_table_page"),
    path("dashboard/accept_table/<str:req_no_plaintiff>/warrants/", views.warrant_status_page, name="view_reqform_warrants"),

]

new_stuff = [

    path("dashboard/statistics/", views_main.statistic_page_view, name="statistics"),

    ####################################################################

    path("dashboard/report/<str:req_no_plaintiff>/warrant/<str:woa_refno>/", views_reqform.report_update_warrant_arrest_yet, name="report_warrant"),

    path("dashboard/unsend/<str:req_no_plaintiff>/", views_reqform.unsend_reqform, name="delete_sent_reqform"),
    
    path("dashboard/cancel/<str:req_no_plaintiff>/", views_reqform.cancel_reqform, name="cancel_reqform"),

    ############################################################################

    path("dashboard/download/<str:req_no_plaintiff>/", views.download_reqform, name="download_reqform"),

    path("dashboard/download/<str:req_no_plaintiff>/warrant/<str:woa_refno>/", views.download_warrant, name="download_warrant"),

    ############################################################################

    path("dashboard/reqform/<str:req_no_plaintiff>/", views_reqform.reqform_info, name="reqform_info")

]   

urlpatterns = old_stuff + new_stuff