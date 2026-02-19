from django.urls import path
from warrant_form import views

app_name = "awis"

urlpatterns = [
    # path('', views.AWISFormWizard.as_view(ALL_FORMS), name="main_page"),
    path('', views.index, name="main_page"),
    # path('submission/second_stage/', views.second_stage_prepared_view, name="second_stage"),
    path('plain-submit/', views.plain_form_submission, name="submit"),
    path('submit/', views.form_submission, name="submit"),
    path('success/', views.success_page, name="success"),
]
