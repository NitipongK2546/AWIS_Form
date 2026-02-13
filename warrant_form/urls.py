from django.urls import path
from warrant_form import views

app_name = "awis"

urlpatterns = [
    path('', views.index, name="main_page"),
    path('submit/', views.form_submission, name="submit"),
    path('success/', views.success_page, name="success"),
]
