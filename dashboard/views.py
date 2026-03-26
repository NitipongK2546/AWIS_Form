from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse, Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

from warrant_form.forms import WarrantForm, AWISFormStep1, DisabledFormStep1, DisabledWarrantForm

from dashboard.models import FormAwaitingApproval as FormData
from dashboard.models import VisualReqformData as FormSent
from dashboard.warrant_wrapper import VisualWarrantData

from warrant_form.model_reqform import ReqformDataModel, WarrantDataModel
from users.models import UserDataModel

import _request_utils.connect_api as AWISConnectAPI

import json
from datetime import datetime
from django.utils import timezone

from users.permissions.perms import PermissionList, PermissionType, perm_str

def getFormAwaitViaReqno(reqno : str):
    return FormData.objects.filter(form__reqno=reqno).first()

def isNotUserAndNotHaveApprovePerm(form : FormData, user_data : UserDataModel):

    is_not_user = not (user_data in (form.form_creator, form.form_owner))

    not_has_approve_perm = not (user_data.has_perm(perm_str(PermissionType.VIEW, PermissionList.REQFORM_AWAIT_APPROVAL)))

    # print(is_not_user)

    return is_not_user and not_has_approve_perm

# Create your views here.

# I will seperate dashboard + index, just in case.
def index(request : HttpRequest):
    return redirect("dashboard:dashboard")

@login_required
def dashboard(request : HttpRequest):

    waiting_approval_forms = FormData.objects.all()

    form_sent = FormSent.objects.all()

    warrants : list[VisualWarrantData] = VisualWarrantData.objects.all()

    # print(form_sent)

    output_list = []
    for obj in form_sent:
        data_dict = {
            "id": obj.form.req_form_number,
            "recive_date": convert_time(obj.recive_date),
            "accept": obj.get_accept_display,
            "accept_date": convert_time(obj.accept_date),
            "req_no_plaintiff": obj.getReqNoPlaintiff(),
            "reqno": obj.getReqNo(),
        }

        output_list.append(data_dict)

    warrants_list = []
    for warrant_wrap in warrants:
        warrant_data = warrant_wrap.warrant

        data_dict = {
            "court_injunction": warrant_wrap.get_court_injunction_display, 
            "reqno": warrant_data.reqforms.all().first().reqno,
            #"woa_no": f"{warrant_data.woa_no}/{warrant_data.woa_date.year + 543}",
            "woa_no": f"{warrant_data.woa_no}",
            "woa_year": warrant_data.woa_date.year + 543,
            "woa_type": f"หมายจับ {warrant_data.get_woa_type_text()}",
            "woa_refno": warrant_data.woa_refno,
            "judge_name": warrant_wrap.judge_name,
            "injunction_date": convert_time(warrant_wrap.injunction_date),
            "file_path": warrant_wrap.file_path,
            "because": warrant_wrap.because,
        }

        warrants_list.append(data_dict)

    return render(request, "dashboard/dashboard.html", {
        "user": request.user,
        "forms": waiting_approval_forms,
        "forms_sent": output_list,
        "warrants": warrants_list,
    })

#######################################################
#
# Form Edit and View Section 
#

@permission_required(perm_str(PermissionType.VIEW, PermissionList.REQFORM_AWAIT_APPROVAL))
def view_form(request : HttpRequest, form_id : int, ObjWarrantForm = DisabledWarrantForm, ObjStep1Form = DisabledFormStep1, selected_html : str = "view_all.html"):

    user_data = UserDataModel.objects.filter(id=request.user.id).first()

    selected_form = getFormAwaitViaReqno(form_id)

    if isNotUserAndNotHaveApprovePerm(selected_form, user_data):
        return HttpResponseForbidden()

    selected_form = selected_form.form
    print(selected_form.prepareTextToSpeech())

    warrants : list[WarrantDataModel] = selected_form.warrants.all()

    warrant_list = []
    for item in warrants:
        dict_item = item.convertBacktoFormView()
        form = ObjWarrantForm(initial=dict_item)
        warrant_list.append(
            form
        )

    form_data = selected_form.convertBacktoFormView()
    
    form = ObjStep1Form(initial=form_data, prefix="main_form")

    # print(
    #     json.dumps(
    #         selected_form.toAPICompatibleDictWithConvertedWarrants(), indent=2, ensure_ascii=False
    #     )
    # )

    return render(request, f"dashboard/{selected_html}", {
        "user": request.user,
        "form": form,
        "warrant_list": warrant_list,
        "disabled": True,

        "req_province": form_data.get("req_province"),
        "req_district": form_data.get("req_district"),
        "req_sub_district": form_data.get("req_sub_district"),
        "acc_province": form_data.get("acc_province"),
        "acc_district": form_data.get("acc_district"),
        "acc_sub_district": form_data.get("acc_sub_district"),
    })

@permission_required(perm_str(PermissionType.EDIT, PermissionList.REQFORM_AWAIT_APPROVAL))
def edit_form(request : HttpRequest, form_id : int):

    user_data = UserDataModel.objects.filter(id=request.user.id).first()

    form_await = getFormAwaitViaReqno(form_id)
    reqform = None

    if not form_await:
        return Http404()

    if isNotUserAndNotHaveApprovePerm(form_await, user_data):
        return HttpResponseForbidden()
    
    if form_await.approve_status == 2:
        return JsonResponse({
            "status": 400,
            "message": "Can't edit a reqform that has already been sent."
        }, status=400)

    if request.method == "POST":
        try:
            form = AWISFormStep1(request.POST, prefix="main_form")
            warrants = WarrantForm(request.POST,)

            temp_warrants_store = []

            if form.is_valid():
                pass
            else:
                print(form.errors.as_text())
                raise Exception("Failed")

            if warrants.is_valid():
                for item_dict in [warrants]:
                    warrant : WarrantDataModel = WarrantDataModel.objects.create(
                        **item_dict.cleaned_data
                    )
                    temp_warrants_store.append(warrant)

            old_form = form_await.form
            old_form.delete()

            reqform : ReqformDataModel = ReqformDataModel.objects.create(**form.cleaned_data)

            for item in temp_warrants_store:
                if reqform:
                    reqform.warrants.add(item)

            form_await.form = reqform
            form_await.approve_status = 1

            form_await.save()

            return redirect(reverse("dashboard:dashboard"))

        except Exception as e:
            print(e)
            pass
        
    return view_form(request, form_id, WarrantForm, AWISFormStep1, "edit_form.html")


#######################################################3
#
# FORM APPROVE SECTION
#

@permission_required(perm_str(PermissionType.APPROVE, PermissionList.REQFORM_AWAIT_APPROVAL))
def approve_form_page(request : HttpRequest):

    all_forms = FormData.objects.all()

    return render(request, "dashboard/approve_page.html", {
        "user": request.user,
        "forms": all_forms,
    })

@permission_required(perm_str(PermissionType.APPROVE, PermissionList.REQFORM_AWAIT_APPROVAL))
def confirm_approve(request : HttpRequest, form_id : int):

    selected_form = getFormAwaitViaReqno(form_id)
    # print(selected_form)
    if request.method == "POST":
        try:
            if settings.ENABLE_API:
                dict = AWISConnectAPI.post_send_req_form("v1.1", request, selected_form.form.toAPICompatibleDictWithConvertedWarrants())

            print(json.dumps(selected_form.form.toAPICompatibleDictWithConvertedWarrants(), indent=2, ensure_ascii=False))

            selected_form.approve_status = FormData.ApprovalStatus.APPROVED
            selected_form.date_approved = timezone.now()
            selected_form.save()

            warrant = selected_form.form.warrants.all().first()
            
            FormSent.objects.create(
                form=selected_form.form,
                accept=FormSent.AcceptStatus.WAITING,
            )

            VisualWarrantData.objects.create(
                warrant=warrant,
                judge_name=selected_form.form.judge_name,
            )
                  
            # print(f"Result: {json.dumps(dict)}")

            return redirect(reverse("dashboard:success_page"))
        except Exception as e:
            return redirect(reverse("dashboard:dashboard"))

    return render(request, "dashboard/confirmation_page.html", {
        "user": request.user,
        "action": "Approve",
        "form": selected_form,
    })
    

@permission_required(perm_str(PermissionType.APPROVE, PermissionList.REQFORM_AWAIT_APPROVAL))
def confirm_reject(request : HttpRequest, form_id : int):

    
    selected_form = getFormAwaitViaReqno(form_id)

    if request.method == "POST":
        selected_form.approve_status = FormData.ApprovalStatus.REJECTED
        selected_form.save()
  
        return redirect(reverse("dashboard:success_page"))
    
    return render(request, "dashboard/confirmation_page.html", {
        "user": request.user,
        "action": "Reject",
        "form": selected_form,
    })


@permission_required(perm_str(PermissionType.DELETE, PermissionList.REQFORM_AWAIT_APPROVAL))
def delete_form(request : HttpRequest, form_id : int):

    selected_form = getFormAwaitViaReqno(form_id)

    if isNotUserAndNotHaveApprovePerm(selected_form, request.user):
        return HttpResponseForbidden()

    if request.method == "POST":
        selected_form.delete()
  
        return redirect(reverse("dashboard:success_page"))
    
    return render(request, "dashboard/confirmation_page.html", {
        "user": request.user,
        "action": "Delete",
        "form": selected_form,
    })


@login_required
def success_page(request : HttpRequest):
    return render(request, "dashboard/success_page.html", {
        "user": request.user,
    })

def convert_time(datetime_obj : datetime):
    if datetime_obj:
        return datetime_obj
    else:
        return f"-"