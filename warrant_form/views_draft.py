from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpRequest, JsonResponse, Http404, HttpResponseBadRequest
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

from django.utils import timezone

import uuid

@perm_req_log([PermissionType.CREATE], PermissionList.REQFORM_DRAFT, AccessType.CREATE)
def create_draft_main_local_page(request : HttpRequest):
    draft_container = FormDraftContainer.objects.create(
        form_owner=request.user,
        form_creator=request.user,
    )

    ReqformDraftDataModel.objects.create(
        draft_container=draft_container,
        create_uid=1000010,
        police_station_id="TCCT0001",
    )

    # return redirect("dashboard:dashboard")
    return redirect("forms:view-draft-container", container_id=draft_container.pk)

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
        try:
            if request.method == "POST":
                reqform_form = ReqformDraftModelForm(request.POST, instance=draft_container.reqform_draft)
                reqform_form.save()

                draft_container.save()

                return redirect("forms:view-draft-container", container_id=draft_container.pk)
            
        except Exception as e:
            print(reqform_form.errors)

        return render(request, "drafts/awis_draft_reqform.html", {
            "reqform_time": timezone.now(),
            "draft_form": reqform_form,
        })
    
    raise Http404()

###############################################################################

# def woa_refno_reduce():
#     woa_num = max(0, woa_num - 1)

@perm_req_log([PermissionType.EDIT], PermissionList.REQFORM_DRAFT, AccessType.EDIT)
def create_warrant_draft(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:
        WarrantDraftDataModel.objects.create(
            draft_container=draft_container,
            **draft_container.reqform_draft.getAccusedInfo(),
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

def req_no_plaintiff_generate():
    today = timezone.now()
    return f"TCCT{today.year + 543}{f"{today.month}".zfill(2)}{f"{today.day}".zfill(2)}{f"{ReqformDataModel.objects.last().pk + 1}".zfill(4)}"

def woa_refno_generate():
    return f"TCCT{timezone.now().year + 543}{f"{WarrantDataModel.objects.last().pk + 1}".zfill(4)}"

@perm_req_log([PermissionType.CREATE], PermissionList.REQFORM_AWAIT_APPROVAL, AccessType.CREATE)
def create_reqform_from_draft(request : HttpRequest, container_id : int):
    selected_draft = FormDraftContainer.objects.filter(pk=container_id).first()

    if selected_draft:
        if request.method == "POST":          
            existing_reqform = ReqformDataModel.objects.filter(
                req_no_plaintiff=selected_draft.reqform_draft.req_no_plaintiff
            ).union(
                ReqformDataModel.objects.filter(
                    req_no_plaintiff=selected_draft.reqform_draft.req_no_plaintiff
                )
            ).first()

            if existing_reqform:
                return render(request, "errors/400.html", {
                    "reason": "รหัสของฟอร์มคำร้องซ้ำกับคำร้องที่เคยมีอยู่"
                }, status=400)
            
            reqform_obj = ReqformDataModel(
                **selected_draft.reqform_draft.toRealReqform(),
            )

            warrrant_wait_list : list[WarrantDataModel] = []
            for draft in selected_draft.warrant_drafts.all():
                warrant = WarrantDataModel(
                    **model_to_dict(draft, exclude=["id", "draft_container"]),
                )
                warrrant_wait_list.append(warrant)

                if WarrantDataModel.objects.filter(woa_refno=warrant.woa_refno).first():
                    return render(request, "errors/400.html", {
                        "reason": "เลขอ้างอิงของหมายซ้ำกับหมายที่เคยสร้างขึ้น"
                    }, status=400)

            try:
                reqform_obj.req_no_plaintiff = req_no_plaintiff_generate()
                reqform_obj.save()

                for warrant in warrrant_wait_list:
                    warrant.woa_refno = woa_refno_generate()
                    warrant.save()
                    reqform_obj.warrants.add(warrant)

                FormAwaitingApproval.objects.create(
                    form=reqform_obj, 
                    form_owner=selected_draft.form_owner, 
                    form_creator=selected_draft.form_creator, 
                    approve_status=1
                )

                return redirect("dashboard:dashboard")
            except Exception as e:
                if reqform_obj.pk:
                    reqform_obj.delete()
                for warrant in warrrant_wait_list:
                    if warrant.pk:
                        warrant.delete()
                
                return render(request, "errors/400.html", {
                    "reason": "ข้อมูลที่ใส่ลงไปในร่างไม่เพียงพอ"
                }, status=400)

        return render(request, "dashboard/confirmation_page.html", {
            "action": "Create Reqform from Draft",
        })
    
    raise Http404()

################################################################################

