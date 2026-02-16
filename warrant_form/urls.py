from django.urls import path
from warrant_form import views

from warrant_form.views import AWISFormWizard, ALL_FORMS

app_name = "awis"

urlpatterns = [
    # path('', views.AWISFormWizard.as_view(ALL_FORMS), name="main_page"),
    path('', views.index, name="main_page"),
    path('submit/', views.form_submission, name="submit"),
    path('success/', views.success_page, name="success"),
]
