from django.urls import path
from warrant_form import views

app_name = "awis"

urlpatterns = [
    # path('', views.AWISFormWizard.as_view(ALL_FORMS), name="main_page"),
    path("", views.index, name="index"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path('logout/', views.custom_logout, name="logout"),
    path('plain-submit/', views.plain_form_submission, name="submit"),
    path('submit/', views.form_submission, name="submit"),
    path('success/', views.success_page, name="success"),
]
