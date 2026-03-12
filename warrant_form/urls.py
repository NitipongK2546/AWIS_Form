from django.urls import path
from warrant_form import views

app_name = "forms"

urlpatterns = [
    path("", views.plain_form, name="plain-form"),
    path('plain-submit/', views.plain_form_submission, name="plain-submit"),
    path('success/', views.success_page, name="success"),

    ######################################################################

    # path('submit/<int:step>', views.form_submission, name="submit"),
    path('create-reqform/step1/', views.step1_reqform, name="step1"),
    path('create-reqform/step2/', views.step2_warrantform, name="step2"),
    path('create-reqform/step3/', views.step3_confirm_form, name="step3"),
]
