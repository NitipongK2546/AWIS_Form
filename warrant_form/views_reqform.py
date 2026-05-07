import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse, Http404
from django.contrib.auth.decorators import permission_required

from warrant_form.forms import WarrantForm, AWISFormStep1, DisabledFormStep1, DisabledWarrantForm

from warrant_form.model_reqform import ReqformDataModel, WarrantDataModel

from dashboard.models import FormAwaitingApproval
from users.models import UserDataModel

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

from users.permissions.perms import PermissionList, PermissionType, perm_str, perm_str_list
from users.permissions.decorators import perm_req_log

from .doc_create import doc_create_with_context

def getFormAwaitViaReqno(reqno : str):
    return FormAwaitingApproval.objects.filter(form__reqno=reqno).first()

def getFormAwaitViaPlaintiff(req_no_plaintiff : str):
    return FormAwaitingApproval.objects.filter(form__req_no_plaintiff=req_no_plaintiff).first()

def isNotUserAndNotHaveApprovePerm(form : FormAwaitingApproval, user_data : UserDataModel):

    is_not_user = not (user_data in (form.form_creator, form.form_owner))

    not_has_approve_perm = not (user_data.has_perm(perm_str(PermissionType.VIEW, PermissionList.REQFORM_AWAIT_APPROVAL)))

    # print(is_not_user)

    return is_not_user and not_has_approve_perm

#######################################################
#
# Form Edit and View Section 
#

@perm_req_log([PermissionType.VIEW], PermissionList.REQFORM_AWAIT_APPROVAL)
def view_form(request : HttpRequest, req_no_plaintiff : int, ObjWarrantForm = DisabledWarrantForm, ObjStep1Form = DisabledFormStep1, selected_html : str = "view_all.html"):

    user_data = UserDataModel.objects.filter(id=request.user.id).first()

    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    if isNotUserAndNotHaveApprovePerm(selected_form, user_data):
        return render(request, "errors/403.html", {
            "reason": "ท่านไม่ใช่เจ้าของหรือผู้ร่างแบบฟอร์มดังกล่าว"
        }, status=403)

    reqform = selected_form.form

    print(json.dumps(reqform.toAPICompatibleDict(), ensure_ascii=False, indent=2))

    # print(selected_form.prepareTextToSpeech())

    warrants : list[WarrantDataModel] = reqform.warrants.all()

    warrant_list = []
    woa_date_list = []
    for item in warrants:
        dict_item = item.convertBacktoFormView()
        doc_create_with_context(dict_item)
        form = ObjWarrantForm(initial=dict_item)
        warrant_list.append(
            form
        )
        
        # woa_date_list.append({
        #     "start_date": dict_item.get("woa_start_date"),
        #     "end_date": dict_item.get("woa_end_date"),
        #     "judge_name": dict_item.get("judge_name")
        # })
        
    form_data = reqform.convertBacktoFormView()
    
    form = ObjStep1Form(initial=form_data, prefix="main_form")

    # print(
    #     json.dumps(
    #         selected_form.toAPICompatibleDictWithConvertedWarrants(), indent=2, ensure_ascii=False
    #     )
    # )

    FileLogger.createNormalLog(request, AccessType.VIEW, PermissionList.REQFORM_AWAIT_APPROVAL, selected_form.getLogInfoDict())

    return render(request, f"dashboard/{selected_html}", {
        "user": request.user,
        "form": form,
        "warrant_list": warrant_list,
        "woa_list": woa_date_list,
        "disabled": True,

        "req_province": form_data.get("req_province"),
        "req_district": form_data.get("req_district"),
        "req_sub_district": form_data.get("req_sub_district"),
        "acc_province": form_data.get("acc_province"),
        "acc_district": form_data.get("acc_district"),
        "acc_sub_district": form_data.get("acc_sub_district"),
    })

@permission_required(perm_str(PermissionType.EDIT, PermissionList.REQFORM_AWAIT_APPROVAL), raise_exception=True)
def edit_form(request : HttpRequest, req_no_plaintiff : int):

    user_data = UserDataModel.objects.filter(id=request.user.id).first()

    form_await = getFormAwaitViaPlaintiff(req_no_plaintiff)
    reqform = None

    if not form_await:
        return Http404()

    if isNotUserAndNotHaveApprovePerm(form_await, user_data):
        return HttpResponseForbidden("ท่านไม่ใช่เจ้าของหรือผู้ร่างแบบฟอร์มดังกล่าว")
    
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

            FileLogger.createNormalLog(request, AccessType.EDIT, PermissionList.REQFORM_AWAIT_APPROVAL, form_await.getLogInfoDict())

            return redirect(reverse("dashboard:dashboard"))

        except Exception as e:
            print(e)
            pass
        
    return view_form(request, req_no_plaintiff, WarrantForm, AWISFormStep1, "edit_form.html")

@permission_required(perm_str(PermissionType.DELETE, PermissionList.REQFORM_AWAIT_APPROVAL), raise_exception=True)
def delete_form(request : HttpRequest, req_no_plaintiff : str):

    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    if isNotUserAndNotHaveApprovePerm(selected_form, request.user):
        return HttpResponseForbidden()

    if request.method == "POST":
        FileLogger.createNormalLog(request, AccessType.DELETE, PermissionList.REQFORM_AWAIT_APPROVAL, selected_form.getLogInfoDict())

        selected_form.delete()
  
        return redirect(reverse("dashboard:success_page"))
    
    return render(request, "dashboard/confirmation_page.html", {
        "user": request.user,
        "action": "Delete",
        "form": selected_form,
    })