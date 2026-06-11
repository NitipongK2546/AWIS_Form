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

#######################################################################

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

# I will seperate dashboard + index, just in case.
def index(request : HttpRequest):
    return redirect("dashboard:dashboard")

############################################################################

@perm_req_log(*DashboardPerm.REQFORM_AWAIT_APPROVAL_PAGE)
def approve_table_page(request):
    written_form = FormAwaitingApproval.objects.filter(form_creator=request.user)
    owned_form = FormAwaitingApproval.objects.filter(form_owner=request.user)
    form_awaiting_approval = written_form.union(owned_form)

    return render(request, "dashboard/approve_table_page.html", {
        "forms": form_awaiting_approval,
    })

##############################################################################

from warrant_form.views_reqform import view_form

@perm_req_log(*DashboardPerm.APPROVE_REQFORM)
def reqform_approve_page(request : HttpRequest, req_no_plaintiff : str):
    def handle_form_approved():
        try:
            if settings.ENABLE_API:
                AWISConnectAPI.post_send_req_form("v1.1", request, selected_form.form.toAPICompatibleDict())

            selected_form.approve_status = FormAwaitingApproval.ApprovalStatus.APPROVED
            selected_form.date_approved = timezone.now()
            selected_form.save()

            selected_form.form.save()

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

            return redirect("dashboard:dashboard")
        except Exception as e:
            print(str(e))
            return redirect("dashboard:dashboard")

    def handle_form_rejected():
        selected_form.approve_status = FormAwaitingApproval.ApprovalStatus.REJECTED
        selected_form.save()
        selected_form.form.save()

        FileLogger.createNormalLog(request, AccessType.REJECT, PermissionList.REQFORM_AWAIT_APPROVAL, selected_form.getLogInfoDict())

        return redirect("dashboard:dashboard")
        
    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    if request.user not in [selected_form.form_owner,]:
        return render(request, "errors/403.html", {
            "reason": "ผู้ใช้ไม่มีสิทธิรายงานหมายในคำร้องดังกล่าว"
        }, status=403)

    if request.method == "POST":
        confirm_approve = request.POST.get("confirm") == "true"

        if confirm_approve:
            return handle_form_approved()
        elif not confirm_approve:
            return handle_form_rejected()

        else:
            # ไม่ควรเกิดขึ้น หาก input ยังอยู่
            return render(request, "errors/400.html", {
                "reason": "ไม่ได้รับข้อมูลว่าอนุมัติหรือปฏิเสธ"
            }, status=400)
        
    return view_form(request, req_no_plaintiff, selected_html="approve_form_view.html")

@perm_req_log(*DashboardPerm.REJECT_REQFORM)
def confirm_reject(request : HttpRequest, req_no_plaintiff : str):
    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)
    if request.method == "POST":
        selected_form.approve_status = FormAwaitingApproval.ApprovalStatus.REJECTED
        selected_form.save()

        FileLogger.createNormalLog(request, AccessType.REJECT, PermissionList.REQFORM_AWAIT_APPROVAL, selected_form.getLogInfoDict())
  
        return redirect(reverse("dashboard:dashboard"))
    
    return render(request, "dashboard/confirmation_page.html", {
        "user": request.user,
        "action": "Reject",
        "form": selected_form,
    })


###########################################################################

@perm_req_log(*DashboardPerm.REQFORM_SUBMITTED_PAGE)
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

@perm_req_log(*DashboardPerm.WARRANT_SUBMITTED_PAGE)
def warrant_status_page(request, req_no_plaintiff : str):

    reqform = getFormAwaitViaPlaintiff(req_no_plaintiff)

    # warrants : list[VisualWarrantData] = VisualWarrantData.objects.filter(warrant_data.reqforms.first().reqno)

    warrants = reqform.form.warrants

    warrants_list = []
    for warrant_data in warrants.all():
        warrant_wrap = VisualWarrantData.objects.filter(warrant=warrant_data).first()

        data_dict = {
            "woa_no_and_year": warrant_data.get_woa_no_and_year(),
            "woa_type": f"{warrant_data.get_woa_type_text()} | {warrant_data.get_fault_type_text()}",
            "woa_refno": warrant_data.woa_refno,

            "court_injunction": warrant_wrap.get_court_injunction_display(), 
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


# @login_required
# def dashboard(request : HttpRequest):
#     return render(request, "dashboard/dashboard.html", {
#         "user": request.user,
#     })


###############################################################################

from warrant_form import doc_create

@perm_req_log(*DashboardPerm.DOWNLOAD_REQFORM)
def download_reqform(request : HttpRequest, req_no_plaintiff : str):
    unsent_form = getFormAwaitViaPlaintiff(req_no_plaintiff)
    if request.user not in [unsent_form.form_owner, unsent_form.form_creator]:
        return render(request, "errors/403.html", {
            "reason": "ผู้ใช้ไม่มีสิทธิดาวน์โหลดคำร้องดังกล่าว"
        }, status=403)

    doc_data = unsent_form.form.convertToDocumentData()

    response = doc_create.create_reqform_pdf(doc_data)
    print(doc_data)

    return response

@perm_req_log(*DashboardPerm.DOWNLOAD_WARRANT)
def download_warrant(request : HttpRequest, req_no_plaintiff : str, woa_refno : str):
    unsent_form = getFormAwaitViaPlaintiff(req_no_plaintiff)
    if request.user not in [unsent_form.form_owner, unsent_form.form_creator]:
        return render(request, "errors/403.html", {
            "reason": "ผู้ใช้ไม่มีสิทธิดาวน์โหลดหมายจับดังกล่าว"
        }, status=403)

    target_warrant : WarrantDataModel = unsent_form.form.warrants.filter(woa_refno=woa_refno).first()

    doc_data = target_warrant.convertToDocumentData()

    response = doc_create.create_warrant_pdf(doc_data)

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