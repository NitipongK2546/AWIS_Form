from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpRequest, JsonResponse, Http404
from .model_draftform import ReqformDraftDataModel, WarrantDraftDataModel, FormDraftContainer
from warrant_form.forms import ReqformDraftModelForm, FormDraftContainerModelForm, WarrantDraftDataModelForm

from dashboard.models import FormAwaitingApproval

from warrant_form.model_reqform import ReqformDataModel
from warrant_form.model_warrant import WarrantDataModel
from warrant_form.form_ownership import OwnershipForm

from django.forms.models import model_to_dict

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType
from users import PermissionList, PermissionType
from users.permissions.decorators import perm_req_log

@perm_req_log([PermissionType.CREATE], PermissionList.REQFORM_DRAFT, AccessType.CREATE)
def create_draft_main_local_page(request : HttpRequest):
    draft_container = FormDraftContainer.objects.create(
        form_owner=request.user,
        form_creator=request.user,
    )

    ReqformDraftDataModel.objects.create(
        draft_container=draft_container,
        create_uid=request.user.api_uid
    )

    return redirect("dashboard:dashboard")

@perm_req_log([PermissionType.VIEW], PermissionList.REQFORM_DRAFT, AccessType.VIEW)
def view_draft_main_local_page(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:
        if request.method == "POST":
            ownership_form = OwnershipForm(request.POST)
            if ownership_form.is_valid():
                cleaned_data = ownership_form.cleaned_data
                draft_container.form_owner = cleaned_data.get("form_owner")
                draft_container.save()

                return redirect("forms:view-draft-container", container_id=draft_container.pk)


        ownership_form = OwnershipForm()
        return render(request, "drafts/awis_draft_main_local.html", {
            "draft_container": draft_container,
            "ownership_form": ownership_form,
        })
    
    raise Http404()

@perm_req_log([PermissionType.DELETE], PermissionList.REQFORM_DRAFT, AccessType.DELETE)
def delete_draft_main_local_page(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:
        if request.method == "POST":
            draft_container.delete()

            return redirect("dashboard:dashboard")

        return render(request, "dashboard/confirmation_page.html", {
            "action": "Delete Draft",
        })
    
    raise Http404()


#####################################################################

@perm_req_log([PermissionType.EDIT], PermissionList.REQFORM_DRAFT, AccessType.EDIT)
def edit_reqform_draft(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:

        reqform_form = ReqformDraftModelForm(instance=draft_container.reqform_draft)

        if request.method == "POST":
            reqform_form = ReqformDraftModelForm(request.POST, instance=draft_container.reqform_draft)
            reqform_form.save()

            draft_container.save()

            return redirect("forms:view-draft-container", container_id=draft_container.pk)

        return render(request, "drafts/awis_draft_reqform.html", {
            "draft_form": reqform_form,
        })
    
    raise Http404()

###############################################################################

@perm_req_log([PermissionType.EDIT], PermissionList.REQFORM_DRAFT, AccessType.EDIT)
def create_warrant_draft(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:
        WarrantDraftDataModel.objects.create(
            draft_container=draft_container
        )
        draft_container.save()

        return redirect("forms:view-draft-container", container_id=draft_container.pk)
    
    raise Http404()

@perm_req_log([PermissionType.EDIT], PermissionList.REQFORM_DRAFT, AccessType.EDIT)
def edit_warrant_draft(request : HttpRequest, container_id : int, warrant_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:

        warrant_form = WarrantDraftDataModelForm(instance=draft_container.warrant_drafts.get(pk=warrant_id))

        if request.method == "POST":
            warrant_form = WarrantDraftDataModelForm(request.POST, instance=draft_container.warrant_drafts.get(pk=warrant_id))
            warrant_form.save()

            draft_container.save()

            return redirect("forms:view-draft-container", container_id=draft_container.pk)

        return render(request, "drafts/awis_draft_warrant.html", {
            "draft_form": warrant_form,
        })
    
    raise Http404()

@perm_req_log([PermissionType.DELETE, PermissionType.EDIT], PermissionList.REQFORM_DRAFT, AccessType.DELETE)
def delete_warrant_draft(request : HttpRequest, container_id : int, warrant_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:

        warrant_form = WarrantDraftDataModel.objects.get(pk=warrant_id)
        warrant_form.delete()

        draft_container.save()

        return redirect("forms:view-draft-container", container_id=draft_container.pk)

        # return render(request, "dashboard/confirmation_page.html", {
        #     "action": "Delete Warrant inside Draft",
        # })
    
    raise Http404()

###############################################################################

@perm_req_log([PermissionType.CREATE], PermissionList.REQFORM_AWAIT_APPROVAL, AccessType.CREATE)
def create_reqform_from_draft(request : HttpRequest, container_id : int):
    selected_draft = FormDraftContainer.objects.filter(pk=container_id).first()

    if selected_draft:
        if request.method == "POST":
            try:
                # reqform = AWISFormStep1(selected_draft.convertBacktoFormView())
                reqform_obj = ReqformDataModel.objects.create(
                    **selected_draft.reqform_draft.toRealReqform()
                )

                for draft in selected_draft.warrant_drafts.all():
                    warrant = WarrantDataModel.objects.create(
                        **model_to_dict(draft, exclude=["id", "draft_container"])
                    )
                    reqform_obj.warrants.add(warrant)

                FormAwaitingApproval.objects.create(
                    form=reqform_obj, 
                    form_owner=selected_draft.form_owner, 
                    form_creator=selected_draft.form_creator, 
                    approve_status=1
                )


                return redirect("dashboard:dashboard")
            except Exception as e:
                if reqform_obj:
                    reqform_obj.delete()

                return JsonResponse({"error": str(e)}, json_dumps_params={"ensure_ascii": False})

        return render(request, "dashboard/confirmation_page.html", {
            "action": "Create Reqform from Draft",
        })
    
    raise Http404()

################################################################################

