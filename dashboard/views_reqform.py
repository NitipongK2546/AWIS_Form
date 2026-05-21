from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, Http404

from dashboard.models import FormAwaitingApproval 
from dashboard.models import VisualReqformData
from dashboard.warrant_wrapper import VisualWarrantData

from warrant_form.model_reqform import WarrantDataModel, ReqformDataModel
from warrant_form.model_draftform import FormDraftContainer

from users.models import UserDataModel

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

from users.permissions.perms import PermissionList, PermissionType, perm_str, perm_str_list
from users.permissions.decorators import perm_req_log

from . import _permissions as DashboardPerm

from django.conf import settings
import _request_utils.connect_api as AWISConnectAPI

color_val_unsent = {
    1: 10,
    0: 11,
    2: 12,
    -1: 99,
}

color_val_sent = {
    99: 20,
    0: 22,
    1: 23,
}

def isNotUserAndNotHaveApprovePerm(form : FormAwaitingApproval, user_data : UserDataModel):

    is_not_user = not (user_data in (form.form_creator, form.form_owner))

    not_has_approve_perm = not (user_data.has_perm(perm_str(PermissionType.VIEW, PermissionList.REQFORM_AWAIT_APPROVAL)))

    # print(is_not_user)

    return is_not_user and not_has_approve_perm

@perm_req_log(*DashboardPerm.VIEW_REQFORM_DETAILS)
def reqform_info(request : HttpRequest, req_no_plaintiff : str):

    reqform = ReqformDataModel.objects.filter(
        req_no_plaintiff=req_no_plaintiff
    ).first()

    status = None
    status_int = None
    action = None
    warrants = None
    status_choice = None

    form_already_sent = VisualReqformData.objects.filter(
        form__req_no_plaintiff=req_no_plaintiff
    ).first()

    form_not_sent = FormAwaitingApproval.objects.filter(
        form__req_no_plaintiff=req_no_plaintiff
    ).first()

    if isNotUserAndNotHaveApprovePerm(form_not_sent, request.user):
        return render(request, "errors/403.html", {
            "reason": "ผู้ใช้ไม่มีสิทธิดูคำร้องดังกล่าว"
        }, status=403)

    if form_already_sent:
        status = form_already_sent.get_accept_display()
        status_int = form_already_sent.accept
        action = "report"

        warrants = VisualWarrantData.objects.filter(
            warrant__in=reqform.warrants.all()
        )
        status_choice = color_val_sent.get(status_int)

    elif form_not_sent:
        status = form_not_sent.get_approve_status_display()
        status_int = form_not_sent.approve_status
        action = "approve"

        warrants = reqform.warrants.all()
        status_choice = color_val_unsent.get(status_int)

    else:
        status = "ร่าง"

    return render(request, "dashboard/reqform_info_page.html", {
        "reqform": reqform,
        "warrants": warrants,
        "status": status,
        "status_int": status_int,
        "action": action,
        "status_choice": status_choice,
    })

####################################################################

def getFormAwaitViaReqno(reqno : str):
    return FormAwaitingApproval.objects.filter(form__reqno=reqno).first()

def getFormAwaitViaPlaintiff(req_no_plaintiff : str):
    return FormAwaitingApproval.objects.filter(form__req_no_plaintiff=req_no_plaintiff).first()

from .forms_report_warrant import ReportWarrantForm
import warrant_form.forms_central as CentralForm
from datetime import datetime
from django.utils import timezone

@perm_req_log(*DashboardPerm.CREATE_REPORT_WARRANT_SUBMITTED)
def report_update_warrant_arrest_yet(request : HttpRequest, req_no_plaintiff : str, woa_refno : str):
    unsent_form = getFormAwaitViaPlaintiff(req_no_plaintiff)
    if request.user not in [unsent_form.form_owner,]:
        return render(request, "errors/403.html", {
            "reason": "ผู้ใช้ไม่มีสิทธิรายงานหมายในคำร้องดังกล่าว"
        }, status=403)

    target_warrant : WarrantDataModel = unsent_form.form.warrants.filter(woa_refno=woa_refno).first()

    current_user : UserDataModel = request.user

    report_form = ReportWarrantForm()

    if not target_warrant:
        raise Http404("ไม่พบข้อมูลดังกล่าว")
    
    context = {
        "court_code": CentralForm.court_codes.getValueOf(unsent_form.form.court_code),
        "woa_no": target_warrant.get_woa_no_and_year(),
        "woa_type": target_warrant.get_woa_type_text(),
        "req_num_case_type_id": unsent_form.form.get_req_case_type_id_display(),
        "arrest_report_uid": current_user.api_uid
    }

    api_data = {
        "court_code": unsent_form.form.court_code,
        "woa_no": target_warrant.woa_no,
        "woa_type": target_warrant.woa_type,
        "woa_year": target_warrant.woa_year,
        "req_num_case_type_id": unsent_form.form.req_case_type_id,
        "arrest_report_date": timezone.now().astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S"),
        "arrest_report_uid": current_user.api_uid
    }
    
    if request.method == "POST":
        report_form = ReportWarrantForm(data=request.POST)

        if report_form.is_valid():
            put_data = report_form.cleaned_data
            
            put_data = combine_date(put_data)

            put_data.update(api_data)

            try:
                if settings.ENABLE_API:
                    AWISConnectAPI.put_report_warrant_result("v1.1", request, put_data)
                else:
                    print(put_data)

                warrant_wrapper = VisualWarrantData.objects.filter(warrant=target_warrant).first()

                # Change status to reported.
                warrant_wrapper.report_status = 1
                warrant_wrapper.save()

                return redirect("dashboard:view_reqform_warrants", req_no_plaintiff)

            except:
                return render(request, "errors/500.html", {

                })

    context.update({
        "report_form": report_form,
    })
    
    return render(request, "dashboard/report_warrant.html", context)

@perm_req_log(*DashboardPerm.CANCEL_REQFORM)
def cancel_reqform(request : HttpRequest, req_no_plaintiff : str):

    sent_form = VisualReqformData.objects.filter(form__req_no_plaintiff=req_no_plaintiff).first()
    unsent_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    if request.user not in [unsent_form.form_owner,]:
        return render(request, "errors/403.html", {
            "reason": "ผู้ใช้ไม่มีสิทธิยกเลิกคำร้องดังกล่าว"
        }, status=403)

    if sent_form:
        return render(request, "errors/400.html", {
            "reason": "คำร้องดังกล่าวถูกส่งไปแล้ว กรุณายกเลิกการส่งคำร้องก่อน"
        }, status=400)

    if request.method == "POST":
        try:
            unsent_form.approve_status = FormAwaitingApproval.ApprovalStatus.CANCELED

            unsent_form.save()
            unsent_form.form.save()

            return redirect("dashboard:success_page")

        except:
            return JsonResponse({
                "status": "Error",
            })
        
    return render(request, "dashboard/confirmation_page.html", {
        "action": "Unsend Reqform"
    })

@perm_req_log(*DashboardPerm.DELETE_REQFORM_SUBMITTED)
def unsend_reqform(request : HttpRequest, req_no_plaintiff : str):
    sent_form = VisualReqformData.objects.filter(form__req_no_plaintiff=req_no_plaintiff).first()
    unsent_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    if request.user not in [unsent_form.form_owner,]:
        return render(request, "errors/403.html", {
            "reason": "ผู้ใช้ไม่มีสิทธิยกเลิกคำร้องดังกล่าว"
        }, status=403)
    
    if sent_form.accept == 1:
        return render(request, "errors/400.html", {
            "reason": "คำร้องดังกล่าวไม่สามารถยกเลิกการส่งได้แล้ว"
        }, status=400)

    unneeded_warrants = sent_form.form.warrants.all()

    warrant_results = VisualWarrantData.objects.filter(warrant__in=unneeded_warrants)

    if request.method == "POST":
        try:
            result = True
            if settings.ENABLE_API:
                result = AWISConnectAPI.unsend_reqform_from_court("v1.1", request, req_no_plaintiff)
                result = result.get("result")

            if not result:
                return render(request, "errors/400.html", {
                    "reason": "คำร้องดังกล่าวไม่สามารถยกเลิกการส่งได้แล้ว"
                }, status=400)

            form_await_approval = FormAwaitingApproval.objects.filter(
                form=sent_form.form
            ).first()
            
            form_await_approval.approve_status = FormAwaitingApproval.ApprovalStatus.PENDING

            form_await_approval.save()
            form_await_approval.form.save()
            sent_form.delete()
            warrant_results.delete()
                
            return redirect("dashboard:success_page")

        except:
            return render(request, "errors/400.html", {
                "reason": "เกิดข้อผิดพลาดขึ้นระหว่างยกเลิกการส่งคำร้อง"
            }, status=400)
        
    return render(request, "dashboard/confirmation_page.html", {
        "action": "Unsend Reqform"
    })

###############################################################################

def combine_date(put_data : dict):
    day = put_data.get("arrest_date_day")
    month = put_data.get("arrest_date_month")
    year = put_data.get("arrest_date_year")

    put_data.update({
        "arrest_date": f"{year}-{month}-{day}"
    })
    
    put_data.pop("arrest_date_day")
    put_data.pop("arrest_date_month")
    put_data.pop("arrest_date_year")

    return put_data

def convert_time(datetime_obj : datetime):
    if datetime_obj:
        return datetime_obj
    else:
        return f"-"