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
from users.permissions.decorators import perm_req_log

from django.utils import timezone
import uuid

from . import _permissions as ReqformPerm 

@perm_req_log(*ReqformPerm.CREATE_DRAFT)
def view_draft_creation_page(request : HttpRequest):

    written_draft = FormDraftContainer.objects.filter(form_creator=request.user)
    owned_draft = FormDraftContainer.objects.filter(form_owner=request.user)
    all_drafts = written_draft.union(owned_draft)
    
    return render(request, "drafts/draft_creation_page.html", {
        "drafts": all_drafts
    })

@perm_req_log(*ReqformPerm.CREATE_DRAFT)
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

@perm_req_log(*ReqformPerm.VIEW_DRAFT)
def save_draft_main_local_page(request : HttpRequest, container_id : int):
    
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first().save()

    return redirect("dashboard:dashboard")

@perm_req_log(*ReqformPerm.VIEW_DRAFT)
def view_draft_main_local_page(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if not draft_container:
        raise Http404()
    
    is_owner = False
    not_owner_error = False
    if request.user == draft_container.form_owner:
        is_owner = True
    
    if request.method == "POST":
        if not is_owner:
            not_owner_error = True

        else:
            ownership_form = OwnershipForm(request.POST)
            if ownership_form.is_valid():
                cleaned_data = ownership_form.cleaned_data
                draft_container.form_owner = cleaned_data.get("form_owner")
                draft_container.form_creator = cleaned_data.get("form_creator")
                draft_container.save()

                return redirect("forms:view-draft-container", container_id=draft_container.pk)

    ownership_form = OwnershipForm()

    # ---- เช็ค field สำคัญที่ยังกรอกไม่ครบ ----
    # map: field name -> label ที่แสดงในหน้า
    REQUIRED_FIELDS = {
        "court_code":       "ศาล",
        "plaintiff":        "ชื่อผู้ร้อง",
        "accused":          "ชื่อผู้ต้องหา",
        "req_name":         "ผู้กรอกคำร้อง",
        "req_pos":          "ตำแหน่งผู้กรอกคำร้อง",
        "req_office":       "สถานที่ทำงาน",
        "req_age":          "อายุผู้กรอกคำร้อง",
        "req_province":     "จังหวัด (ผู้กรอก)",
        "req_district":     "อำเภอ/เขต (ผู้กรอก)",
        "req_sub_district": "ตำบล/แขวง (ผู้กรอก)",
        "req_tel":          "หมายเลขโทรศัพท์",
        "acc_full_name":    "ชื่อเต็มผู้ต้องหา",
        "acc_card_id":      "รหัสบัตรประจำตัวผู้ต้องหา",
    }

    reqform_missing_fields = []
    reqform_draft = getattr(draft_container, "reqform_draft", None)
    if reqform_draft:
        for field, label in REQUIRED_FIELDS.items():
            value = getattr(reqform_draft, field, None)
            # ถือว่าว่างถ้าเป็น None หรือ string ว่าง
            if value is None or value == "":
                reqform_missing_fields.append(label)

    # ---- เช็ค field สำคัญของหมายจับที่ยังกรอกไม่ครบ ----
    WARRANT_REQUIRED_FIELDS = {
        "acc_full_name": "ชื่อ-นามสกุล",
        "acc_card_id":   "เลขบัตร",
        "charge":        "ฐานความผิด",
        "cause_text":    "ด้วย (เหตุผลกล่าวหา)",
        "send_to_name":  "ส่งหมายถึง",
    }

    # list of (warrant, [missing_label, ...]) — missing list is empty if all good
    warrant_with_missing = []
    for warrant in draft_container.warrant_drafts.all():
        missing = [
            label for field, label in WARRANT_REQUIRED_FIELDS.items()
            if not getattr(warrant, field, None)
        ]
        warrant_with_missing.append((warrant, missing))

    warrants_unfinished_list = (sublist[1] for sublist in warrant_with_missing)

    all_filled = (
        (len(reqform_missing_fields) == 0) and
        (all(not warrant for warrant in warrants_unfinished_list)) and
        (draft_container.warrant_drafts.count() > 0)
    )

    return render(request, "drafts/awis_draft_main_local.html", {
        "draft_container": draft_container,
        "ownership_form": ownership_form,
        "is_owner": is_owner,
        "not_owner_error": not_owner_error,
        "missing_fields": reqform_missing_fields,
        "is_reqform_filled": (len(reqform_missing_fields) == 0),
        "warrant_with_missing": warrant_with_missing,
        "all_fields_filled": all_filled
    })
    
    

@perm_req_log(*ReqformPerm.DELETE_DRAFT)
def delete_draft_main_local_page(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:
        print("found")
        if request.method == "POST":

            print("success")
            
            draft_container.delete()

            print(draft_container)

            return redirect("dashboard:dashboard")
    
    print("lmao nah")
    raise Http404


#####################################################################

@perm_req_log(*ReqformPerm.EDIT_DRAFT)
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

@perm_req_log(*ReqformPerm.EDIT_DRAFT)
def create_warrant_draft(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:
        if draft_container.warrant_drafts.count() < 1:
            WarrantDraftDataModel.objects.create(
                draft_container=draft_container,
                **draft_container.reqform_draft.getAccusedInfo(),
                woa_type=2,
                fault_type_id=2,
            )
        else:
            WarrantDraftDataModel.objects.create(
                draft_container=draft_container,
                woa_type=2,
                fault_type_id=2,
            )

        draft_container.save()

        return redirect("forms:view-draft-container", container_id=draft_container.pk)
    
    raise Http404()

@perm_req_log(*ReqformPerm.EDIT_DRAFT)
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

@perm_req_log(*ReqformPerm.EDIT_DRAFT)
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
    last_request = ReqformDataModel.objects.last()
    if not last_request:
        num = 0
        return f"TCCT{today.year + 543}{f"{today.month}".zfill(2)}{f"{today.day}".zfill(2)}{f"{num + 1}".zfill(4)}"

    all_same_day_requests = ReqformDataModel.objects.filter(
        req_date__date=today.date()
    )

    num = all_same_day_requests.count()

    return f"TCCT{today.year + 543}{f"{today.month}".zfill(2)}{f"{today.day}".zfill(2)}{f"{num + 1}".zfill(4)}"

def woa_refno_generate(req_no_plaintiff : str, count : int):
    today = timezone.now()
    last_request = ReqformDataModel.objects.last()
    if not last_request:
        num = 0
        return f"{req_no_plaintiff}-W{f"{count + 1}".zfill(3)}"

    all_same_day_requests = ReqformDataModel.objects.filter(
        req_date__date=today.date()
    )

    num = all_same_day_requests.count()

    return f"{req_no_plaintiff}-W{f"{count + 1}".zfill(3)}"

@perm_req_log(*ReqformPerm.CREATE_REQFORM)
def create_reqform_from_draft(request : HttpRequest, container_id : int):
    def create_new_reqform():
        reqform_obj = ReqformDataModel(
            **selected_draft.reqform_draft.toRealReqform(),
        )

        if not selected_draft.warrant_drafts.all():
            return render(request, "errors/400.html", {
                "reason": "ยังไม่ได้ใส่หมายจับ"
            }, status=400)

        warrrant_wait_list : list[tuple] = []
        for draft in selected_draft.warrant_drafts.all():
            warrant = WarrantDataModel(
                **draft.toRealWarrant()
            )
            warrrant_wait_list.append(
                (warrant, draft)
            )

            if WarrantDataModel.objects.filter(woa_refno=warrant.woa_refno).first():
                return render(request, "errors/400.html", {
                    "reason": "เลขอ้างอิงของหมายซ้ำกับหมายที่เคยสร้างขึ้น"
                }, status=400)

        try:
            new_req_no_plaintiff = req_no_plaintiff_generate()
            reqform_obj.req_no_plaintiff = new_req_no_plaintiff
            reqform_obj.save()

            for count, warrant in enumerate(warrrant_wait_list):
                new_woa_refno = woa_refno_generate(new_req_no_plaintiff, count)
                warrant[0].woa_refno = new_woa_refno
                warrant[1].woa_refno = new_woa_refno

                warrant[0].save()
                warrant[1].save()
                reqform_obj.warrants.add(warrant[0])

            FormAwaitingApproval.objects.create(
                form=reqform_obj, 
                form_owner=selected_draft.form_owner, 
                form_creator=selected_draft.form_creator, 
                approve_status=1
            )

            selected_draft.reqform_draft.req_no_plaintiff = new_req_no_plaintiff
            selected_draft.reqform_draft.save()

            return redirect("dashboard:dashboard")
        except Exception as e:
            if reqform_obj.pk:
                reqform_obj.delete()
            for warrant in warrrant_wait_list:
                if warrant.pk:
                    warrant.delete()

            print(str(e))
            
            return render(request, "errors/400.html", {
                "reason": "ข้อมูลที่ใส่ลงไปในร่างไม่เพียงพอ"
            }, status=400)
        
    def update_old_reqform():
        try:
            old_unsent_form = FormAwaitingApproval.objects.filter(
                form=existing_reqform
            ).first()

            if not selected_draft.warrant_drafts.all():
                return render(request, "errors/400.html", {
                    "reason": "ยังไม่ได้ใส่หมายจับ"
                }, status=400)
            
            draft_warrants = selected_draft.warrant_drafts.all()
            existing_warrants = existing_reqform.warrants.all()

            warrrant_wait_list : list[dict] = []

            existing_reqform.warrants.all().delete()

            for draft in draft_warrants:
                warrant = WarrantDataModel(
                    **draft.toRealWarrant()
                )
                warrrant_wait_list.append(
                    (warrant, draft)
                )
            
            for count, warrant in enumerate(warrrant_wait_list):
                new_woa_refno = woa_refno_generate(
                    existing_reqform.req_no_plaintiff, count
                )
                warrant[0].woa_refno = new_woa_refno
                warrant[1].woa_refno = new_woa_refno

                warrant[0].save()
                warrant[1].save()
                existing_reqform.warrants.add(warrant[0])

            existing_reqform.save()

            old_unsent_form.approve_status = 1
            old_unsent_form.save()
        except Exception as e:
            print(str(e))

        return redirect("dashboard:dashboard")
    
    ##########################################################################3

    selected_draft = FormDraftContainer.objects.filter(pk=container_id).first()

    if not selected_draft:
        raise Http404()
    
    if request.method == "POST":          
        existing_reqform = ReqformDataModel.objects.filter(
            req_no_plaintiff=selected_draft.reqform_draft.req_no_plaintiff
        ).first()

        # print(selected_draft.reqform_draft.req_no_plaintiff)

        if existing_reqform:
            return update_old_reqform()
            # return HttpResponseBadRequest("OOOFFFF")
        else:
            return create_new_reqform()
        
        
    return render(request, "dashboard/confirmation_page.html", {
        "action": "Create Reqform from Draft",
    })

################################################################################