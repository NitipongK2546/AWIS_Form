from django.urls import path
from warrant_form import views

app_name = "forms"

urlpatterns = [
    path("", views.plain_form, name="to-new-form"),
    # path("create-reqform/", views.plain_form, name="to-step1"),

    path("create-reqform/", views.step0_confirm_owner, name="step0"),

    path('create-reqform/step1/', views.step1_reqform, name="step1"),
    path('create-reqform/step2/', views.step2_warrantform, name="step2"),
    path('create-reqform/step3/', views.step3_confirm_form, name="step3"),

    path('success/', views.success_page, name="success"),


]
