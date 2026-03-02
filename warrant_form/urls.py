from django.urls import path
from warrant_form import views

app_name = "forms"

urlpatterns = [
    # path('', views.AWISFormWizard.as_view(ALL_FORMS), name="main_page"),
    path("", views.index, name="first_page"),
    path('plain-submit/', views.plain_form_submission, name="plain-submit"),
    path('submit/', views.form_submission, name="submit"),
    path('success/', views.success_page, name="success"),
]
