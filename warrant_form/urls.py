from django.urls import path
from warrant_form import views, views_draft

app_name = "forms"

urlpatterns = [
    path("", views.plain_form, name="to-new-form"),

    path("reqform-draft/create/", views_draft.create_draft_main_local_page, name="create-draft-container"),
    path("reqform-draft/view/<int:container_id>/", views_draft.view_draft_main_local_page, name="view-draft-container"),

    # path("reqform-draft/delete/<int:draft_id>/", views_draft.delete_reqform_draft, name="delete-draft-step1"),

    path("reqform-draft/create-reqform/<int:draft_id>/", views_draft.create_reqform_from_draft, name="create-reqform"),


    path("create-reqform/", views.step0_confirm_owner, name="step0"),

    path('create-reqform/step1/', views.step1_reqform, name="step1"),
    path('create-reqform/step2/', views.step2_warrantform, name="step2"),
    path('create-reqform/step3/', views.step3_confirm_form, name="step3"),

    path('success/', views.success_page, name="success"),
]
