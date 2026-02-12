from django.urls import path
from warrant_form import views

urlpatterns = [
    path('', views.index, name="main_page"),
]