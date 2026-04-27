from django.urls import path
from warrant_form import views, views_draft

app_name = "forms"

urlpatterns = [
    path("", views.plain_form, name="to-new-form"),

    path("reqform-draft/create/", views_draft.create_draft_main_local_page, name="create-draft-container"),

    path("reqform-draft/view/<int:container_id>/", views_draft.view_draft_main_local_page, name="view-draft-container"),
    path("reqform-draft/delete/<int:container_id>/", views_draft.delete_draft_main_local_page, name="delete-draft-container"),


    path("reqform-draft/create/<int:container_id>/warrant/", views_draft.create_warrant_draft, name="create-draft-container-warrant"),
    path("reqform-draft/edit/<int:container_id>/warrant/<int:warrant_id>/", views_draft.edit_warrant_draft, name="edit-draft-container-warrant"),
    path("reqform-draft/delete/<int:container_id>/warrant/<int:warrant_id>/", views_draft.delete_warrant_draft, name="delete-draft-container-warrant"),


    path("reqform-draft/edit/<int:container_id>/reqform/", views_draft.edit_reqform_draft, name="edit-draft-container-reqform"),
    ######################################################################


    path("reqform-draft/create-reqform/<int:container_id>/", views_draft.create_reqform_from_draft, name="create-reqform"),

    path("create-reqform/", views.step0_confirm_owner, name="step0"),

    path('create-reqform/step1/', views.step1_reqform, name="step1"),
    path('create-reqform/step2/', views.step2_warrantform, name="step2"),
    path('create-reqform/step3/', views.step3_confirm_form, name="step3"),

    path('success/', views.success_page, name="success"),
]
