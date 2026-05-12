from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from dashboard.models import FormAwaitingApproval 
from dashboard.models import VisualReqformData
from dashboard.warrant_wrapper import VisualWarrantData

from warrant_form.model_reqform import WarrantDataModel
from warrant_form.model_draftform import FormDraftContainer

from users.models import UserDataModel

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

import _request_utils.connect_api as AWISConnectAPI

from datetime import datetime
from django.utils import timezone

from users.permissions.perms import PermissionList, PermissionType, perm_str, perm_str_list
from users.permissions.decorators import perm_req_log

from . import _permissions as DashboardPerm

def getFormAwaitViaReqno(reqno : str):
    return FormAwaitingApproval.objects.filter(form__reqno=reqno).first()

def getFormAwaitViaPlaintiff(req_no_plaintiff : str):
    return FormAwaitingApproval.objects.filter(form__req_no_plaintiff=req_no_plaintiff).first()

def isNotUserAndNotHaveApprovePerm(form : FormAwaitingApproval, user_data : UserDataModel):

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

    written_draft = FormDraftContainer.objects.filter(form_creator=request.user)
    owned_draft = FormDraftContainer.objects.filter(form_owner=request.user)
    all_drafts = written_draft.union(owned_draft)

    context = {
        "user": request.user,
        "drafts": all_drafts,
    }

    if request.user.has_perms(
        perm_str_list([PermissionType.VIEW, PermissionType.CREATE], PermissionList.REQFORM_AWAIT_APPROVAL)
    ):
        context.update({
            "can_create_form": True,
        })
    
    if request.user.has_perms(
        perm_str_list([PermissionType.VIEW, PermissionType.APPROVE], PermissionList.REQFORM_AWAIT_APPROVAL)
    ):
        context.update({
            "can_approve_form": True,
        })


    return render(request, "dashboard/dashboard.html", context)

############################################################################

@perm_req_log(DashboardPerm.REQFORM_AWAIT_APPROVAL_PAGE)
def approve_table_page(request):
    written_form = FormAwaitingApproval.objects.filter(form_creator=request.user)
    owned_form = FormAwaitingApproval.objects.filter(form_owner=request.user)
    form_awaiting_approval = written_form.union(owned_form)

    return render(request, "dashboard/approve_table_page.html", {
        "forms": form_awaiting_approval,
    })

from warrant_form.views_reqform import view_form

@perm_req_log(DashboardPerm.APPROVE_REQFORM)
def confirm_approve(request : HttpRequest, req_no_plaintiff : str):

    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    if request.method == "POST":
        try:
            if settings.ENABLE_API:
                AWISConnectAPI.post_send_req_form("v1.1", request, selected_form.form.toAPICompatibleDict())

            selected_form.approve_status = FormAwaitingApproval.ApprovalStatus.APPROVED
            selected_form.date_approved = timezone.now()
            selected_form.save()

            for warrant in selected_form.form.warrants.all():
                VisualWarrantData.objects.create(
                    warrant=warrant,
                    judge_name=selected_form.form.judge_name,
                )
            
            VisualReqformData.objects.create(
                form=selected_form.form,
                accept=VisualReqformData.AcceptStatus.WAITING,
            )

            FileLogger.createNormalLog(request, AccessType.APPROVE, PermissionList.REQFORM_AWAIT_APPROVAL, selected_form.getLogInfoDict(),)

            return redirect("dashboard:accept_table_page")
        except Exception as e:
            return redirect("dashboard:dashboard")
        
    return view_form(request, req_no_plaintiff, selected_html="approve_form_view.html")

    # return render(request, "dashboard/confirmation_page.html", {
    #     "user": request.user,
    #     "action": "Approve",
    #     "form": selected_form,
    # })
    

@perm_req_log(DashboardPerm.REJECT_REQFORM)
def confirm_reject(request : HttpRequest, req_no_plaintiff : str):
    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)
    if request.method == "POST":
        selected_form.approve_status = FormAwaitingApproval.ApprovalStatus.REJECTED
        selected_form.save()

        FileLogger.createNormalLog(request, AccessType.REJECT, PermissionList.REQFORM_AWAIT_APPROVAL, selected_form.getLogInfoDict())
  
        return redirect(reverse("dashboard:success_page"))
    
    return render(request, "dashboard/confirmation_page.html", {
        "user": request.user,
        "action": "Reject",
        "form": selected_form,
    })


###########################################################################

@perm_req_log(DashboardPerm.REQFORM_SUBMITTED_PAGE)
def accept_table_page(request):
    form_sent = VisualReqformData.objects.all()

    output_list = []
    for obj in form_sent:
        data_dict = {
            "accept": obj.get_accept_display,
            "accept_date": convert_time(obj.accept_date),
            "req_no_plaintiff": obj.getReqNoPlaintiff(),
            "reqno": obj.getReqNo(),
        }

        output_list.append(data_dict)

    return render(request, "dashboard/accept_table_page.html", {
        "forms_sent": output_list,
    })

@perm_req_log(DashboardPerm.WARRANT_SUBMITTED_PAGE)
def warrant_status_page(request, req_no_plaintiff : str):

    reqform = getFormAwaitViaPlaintiff(req_no_plaintiff)

    # warrants : list[VisualWarrantData] = VisualWarrantData.objects.filter(warrant_data.reqforms.first().reqno)

    warrants = reqform.form.warrants

    warrants_list = []
    for warrant_data in warrants.all():
        warrant_wrap = VisualWarrantData.objects.filter(warrant=warrant_data).first()

        data_dict = {
            "court_injunction": warrant_wrap.get_court_injunction_display(), 
            "woa_no_and_year": warrant_data.get_woa_no_and_year(),
            "woa_type": f"{warrant_data.get_woa_type_text()} | {warrant_data.get_fault_type_text()}",
            "woa_refno": warrant_data.woa_refno,
            "judge_name": warrant_wrap.judge_name,
            "injunction_date": convert_time(warrant_wrap.injunction_date),
            "file_path": warrant_wrap.file_path,
            "because": warrant_wrap.because,

            "court_injunction_int": warrant_wrap.court_injunction, 
            "req_no_plaintiff": req_no_plaintiff,

            "report_status": warrant_wrap.report_status
        }

        warrants_list.append(data_dict)

    return render(request, "dashboard/warrant_status_page.html", {
        "warrants": warrants_list
    })


#######################################################3
#
# FORM APPROVE SECTION
#

# @permission_required(perm_str(PermissionType.APPROVE, PermissionList.REQFORM_AWAIT_APPROVAL), raise_exception=True)
# def approve_form_page(request : HttpRequest):

#     written_form = FormAwaitingApproval.objects.filter(form_creator=request.user)
#     owned_form = FormAwaitingApproval.objects.filter(form_owner=request.user)
#     form_awaiting_approval = written_form.union(owned_form)

#     return render(request, "dashboard/approve_page.html", {
#         "user": request.user,
#         "forms": form_awaiting_approval,
#     })

@login_required
def success_page(request : HttpRequest):
    return render(request, "dashboard/success_page.html", {
        "user": request.user,
    })

################################################################################

from .forms_report_warrant import ReportWarrantForm
import warrant_form.forms_central as CentralForm

@perm_req_log(DashboardPerm.CREATE_REPORT_WARRANT_SUBMITTED)
def report_update_warrant_arrest_yet(request : HttpRequest, req_no_plaintiff : str, woa_refno : str):
    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    target_warrant : WarrantDataModel = selected_form.form.warrants.filter(woa_refno=woa_refno).first()

    current_user : UserDataModel = request.user

    report_form = ReportWarrantForm()

    if not target_warrant:
        raise Http404("ไม่พบข้อมูลดังกล่าว")
    
    context = {
        "court_code": CentralForm.court_codes.getValueOf(selected_form.form.court_code),
        "woa_no": target_warrant.get_woa_no_and_year(),
        "woa_type": target_warrant.get_woa_type_text(),
        "req_num_case_type_id": selected_form.form.get_req_case_type_id_display(),
        "arrest_report_uid": current_user.api_uid
    }

    api_data = {
        "court_code": selected_form.form.court_code,
        "woa_no": target_warrant.woa_no,
        "woa_type": target_warrant.woa_type,
        "woa_year": target_warrant.woa_year,
        "req_num_case_type_id": selected_form.form.req_case_type_id,
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

@perm_req_log(DashboardPerm.DELETE_REQFORM_SUBMITTED)
def unsend_reqform(request : HttpRequest, req_no_plaintiff : str):
    sent_form = VisualReqformData.objects.filter(form__req_no_plaintiff=req_no_plaintiff).first()

    unneeded_warrants = sent_form.form.warrants.all()

    warrant_results = VisualWarrantData.objects.filter(warrant__in=unneeded_warrants)

    print(warrant_results)

    if sent_form.accept == 1:
        return render(request, "errors/400.html", {
            "reason": "คำร้องดังกล่าวไม่สามารถยกเลิกการส่งได้แล้ว"
        }, status=403)

    if request.method == "POST":
        try:
            if settings.ENABLE_API:
                AWISConnectAPI.unsend_reqform_from_court("v1.1", request, req_no_plaintiff)

            for warrant in warrant_results.all():
                warrant.warrant.delete()
            sent_form.form.delete()
                
            return redirect("dashboard:success_page")

        except:
            return JsonResponse({
                "status": "Error",
            })
        
    return render(request, "dashboard/confirmation_page.html", {
        "action": "Unsend Reqform"
    })

###############################################################################

from warrant_form import doc_create

def download_warrant(request : HttpRequest, req_no_plaintiff : str, woa_refno : str):
    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    target_warrant : WarrantDataModel = selected_form.form.warrants.filter(woa_refno=woa_refno).first()

    doc_data = target_warrant.convertToDocumentData()

    response = doc_create.create_pdf(doc_data)

    return response


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